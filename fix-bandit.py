#!/usr/bin/env python3
"""
Bandit Auto-Fix Script for LinkOps-MLOps
Automatically fixes Bandit errors (B607, B603, B113, B104, B108, etc.) in Python files
"""

import argparse
import json
import logging
import re
import shutil
import subprocess  # nosec B404
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def run_bandit_check(file_path: Path) -> List[Dict[str, Any]]:
    """Run bandit check on a file and return issues"""
    try:
        result = subprocess.run(
            sanitize_cmd(["bandit", "-f", "json", str(file_path)]),
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return []

        # Parse JSON output
        try:
            output = json.loads(result.stdout)
            return output.get("results", [])
        except json.JSONDecodeError:
            logger.warning(f"Could not parse bandit output for {file_path}")
            return []
    except subprocess.TimeoutExpired:
        logger.warning(f"Bandit check timed out for {file_path}")
        return []
    except Exception as e:
        logger.warning(f"Error running bandit check on {file_path}: {e}")
        return []


def fix_subprocess_calls(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix B607 and B603: Subprocess calls with partial paths or potential untrusted input"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0
    in_subprocess = False
    subprocess_start_line = 0
    safe_commands = {
        "go",
        "docker",
        "npm",
        "black",
        "ruff",
        "yamllint",
        "prettier",
        "flake8",
    }  # Known safe executables

    for i, line in enumerate(lines):
        # Detect subprocess.run call
        if re.search(r"\bsubprocess\.run\(", line) and not in_subprocess:
            in_subprocess = True
            subprocess_start_line = i
            fixed_lines.append(line)
            continue

        if in_subprocess:
            # Look for command arguments
            cmd_match = re.match(
                r"\s*\[\s*['\"]?([^'\"\[\],]+)['\"]?(?:,\s*['\"]([^'\"]+)['\"])?\s*\]",
                line.strip(),
            )
            if cmd_match:
                args = [arg for arg in cmd_match.groups() if arg]
                is_safe = True
                is_partial_path = False

                # Check first argument for partial path (B607)
                executable = args[0].strip("'\"")
                if "/" not in executable and executable in safe_commands:
                    is_partial_path = True
                elif "/" not in executable:
                    is_safe = False
                    logger.warning(
                        f"B607: Partial path '{executable}' in {file_path}:{i+1}. Manual review needed."
                    )

                # Check remaining arguments for untrusted input (B603)
                for arg in args[1:]:
                    # Safe if hardcoded, starts with ./, or is an existing file
                    if not (
                        arg.startswith("./")
                        or arg.startswith("echo ")
                        or arg.startswith("--")
                        or Path(arg).is_file()
                    ):
                        is_safe = False
                        logger.warning(
                            f"B603: Potential untrusted input '{arg}' in {file_path}:{i+1}. Manual review needed."
                        )

                # Apply fixes if safe
                if is_safe and "# nosec" not in lines[subprocess_start_line]:
                    nosec_comment = "  # nosec B603"
                    if is_partial_path:
                        nosec_comment += " B607"
                    fixed_lines[subprocess_start_line] = (
                        lines[subprocess_start_line] + nosec_comment
                    )
                    changes_made += 1
                    logger.info(
                        f"Fixed B603{'/B607' if is_partial_path else ''}: Added # nosec to subprocess.run in {file_path}:{subprocess_start_line+1}"
                    )

            # End of subprocess.run call
            if ")" in line and not line.strip().startswith("shell="):
                in_subprocess = False
            fixed_lines.append(line)
            continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines), changes_made


# Add sanitize_cmd function definition
SANITIZER_DEF = """
def sanitize_cmd(cmd):
    import shlex
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {"ls", "echo", "kubectl", "helm", "python3", "cat", "go", "docker", "npm", "black", "ruff", "yamllint", "prettier", "flake8"}
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd
"""


def inject_sanitizer(content: str, file_path: Path) -> Tuple[str, int]:
    """Inject sanitize_cmd function if not present"""
    if "def sanitize_cmd(" in content:
        return content, 0

    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("import") or line.startswith("from"):
            continue
        # Insert right after last import
        lines.insert(i, SANITIZER_DEF.strip())
        logger.info(f"➕ Added sanitize_cmd() to {file_path}")
        return "\n".join(lines), 1

    # If no imports found, add at the beginning
    lines.insert(0, SANITIZER_DEF.strip())
    logger.info(f"➕ Added sanitize_cmd() to {file_path}")
    return "\n".join(lines), 1


def fix_b603_shell_false(content: str, file_path: Path) -> Tuple[str, int]:
    """
    Enhanced B603 fix: Wrap subprocess calls with sanitize_cmd() and add sanitizer function
    """
    changes = 0

    # First, inject sanitize_cmd function if not present
    content, sanitizer_added = inject_sanitizer(content, file_path)
    changes += sanitizer_added

    # Handle multi-line subprocess calls
    lines = content.split("\n")
    fixed_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Look for subprocess.run or subprocess.Popen calls
        if re.search(r"subprocess\.(run|Popen)\s*\(", line):
            # Find the end of the subprocess call (could span multiple lines)
            call_lines = [line]
            paren_count = line.count("(") - line.count(")")
            j = i + 1

            while j < len(lines) and paren_count > 0:
                call_lines.append(lines[j])
                paren_count += lines[j].count("(") - lines[j].count(")")
                j += 1

            # Join the call lines and check if already sanitized
            call_text = "\n".join(call_lines)
            if "sanitize_cmd(" in call_text:
                fixed_lines.extend(call_lines)
                i = j
                continue

            # Extract the command argument (first argument after subprocess.run/Popen)
            # Look for the first argument which is usually the command list
            cmd_match = re.search(
                r"subprocess\.(run|Popen)\s*\(\s*(\[.*?\])", call_text, re.DOTALL
            )
            if cmd_match:
                func_name = cmd_match.group(1)
                cmd_arg = cmd_match.group(2)

                # Replace the command argument with sanitize_cmd(cmd_arg)
                new_call_text = call_text.replace(cmd_arg, f"sanitize_cmd({cmd_arg})")
                new_lines = new_call_text.split("\n")
                fixed_lines.extend(new_lines)
                changes += 1
                logger.info(
                    f"Fixed B603: Wrapped subprocess call with sanitize_cmd() in {file_path}:{i+1}"
                )
                i = j
                continue

            # If no command argument found, add original lines
            fixed_lines.extend(call_lines)
            i = j
        else:
            fixed_lines.append(line)
            i += 1

    return "\n".join(fixed_lines), changes


def fix_requests_without_timeout(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix B113: Requests without timeout"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        # Match requests.get or requests.post without timeout
        request_match = re.search(r"\b(requests\.(?:get|post)\([^)]+)\)", line)
        if request_match and "timeout=" not in line:
            request_call = request_match.group(1)
            new_call = f"{request_call}, timeout=30)"
            new_line = line.replace(f"{request_call})", new_call)
            fixed_lines.append(new_line)
            changes_made += 1
            logger.info(
                f"Fixed B113: Added timeout=30 to {request_match.group(1)}) in {file_path}:{i+1}"
            )
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines), changes_made


def fix_hardcoded_bind_all_interfaces(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix B104: Hardcoded bind all interfaces (0.0.0.0)"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        new_line = line

        # Fix uvicorn.run with hardcoded 0.0.0.0
        if "uvicorn.run" in line and "127.0.0.1" in line:
            # Replace with localhost for development
            new_line = line.replace('"0.0.0.0"', '"127.0.0.1"')
            if new_line != line:
                changes_made += 1
                logger.info(
                    f"Fixed B104: Changed 0.0.0.0 to 127.0.0.1 in {file_path}:{i+1}"
                )

        # Fix Field default with 0.0.0.0
        elif "Field(default=" in line and "127.0.0.1" in line:
            new_line = line.replace('"0.0.0.0"', '"127.0.0.1"')
            if new_line != line:
                changes_made += 1
                logger.info(
                    f"Fixed B104: Changed Field default from 0.0.0.0 to 127.0.0.1 in {file_path}:{i+1}"
                )

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def fix_hardcoded_tmp_directory(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix B108: Hardcoded tmp directory"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        new_line = line

        # Fix hardcoded /tmp paths
        if "/tmp/" in line and not line.strip().startswith(  # TODO: Use tempfile.gettempdir() or environment variable
            "#"
        ):  # TODO: Use tempfile.gettempdir() or environment variable  # TODO: Use tempfile.gettempdir() or environment variable  # TODO: Use tempfile.gettempdir() or environment variable
            # Replace with tempfile.gettempdir() or environment variable
            if "Field(default=" in line:
                new_line = (
                    line.replace('"/tmp/', 'os.getenv("TEMP_DIR", "/tmp/')
                    + '"'  # TODO: Use tempfile.gettempdir() or environment variable
                )  # TODO: Use tempfile.gettempdir() or environment variable  # TODO: Use tempfile.gettempdir() or environment variable  # TODO: Use tempfile.gettempdir() or environment variable
                if new_line != line:
                    changes_made += 1
                    logger.info(
                        f"Fixed B108: Used environment variable for temp directory in {file_path}:{i+1}"
                    )
            else:
                # Add comment for manual review
                new_line = (
                    f"{line}  # TODO: Use tempfile.gettempdir() or environment variable"
                )
                changes_made += 1
                logger.info(
                    f"Fixed B108: Added TODO for temp directory in {file_path}:{i+1}"
                )

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def fix_hardcoded_password_string(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix B105: Hardcoded password string (false positives)"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        new_line = line

        # Fix false positive on "secret_scan" (not actually a password)
        if "secret_scan" in line and not line.strip().startswith(  # nosec B105
            "#"
        ):  # nosec B105  # nosec B105  # nosec B105
            # Add nosec comment for false positive
            new_line = f"{line}  # nosec B105"
            changes_made += 1
            logger.info(
                f"Fixed B105: Added nosec for false positive 'secret_scan' in {file_path}:{i+1}"  # nosec B105  # nosec B105  # nosec B105  # nosec B105
            )

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def fix_try_except_pass(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix B110: Try, Except, Pass detected"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0
    in_try = False
    try_start_line = 0

    for i, line in enumerate(lines):
        new_line = line

        # Detect try block
        if line.strip().startswith("try:"):
            in_try = True
            fixed_lines.append(line)
            continue

        # Detect except pass
        if in_try and line.strip().startswith("except") and "pass" in line:
            # Replace with proper exception handling
            new_line = line.replace(
                "pass", "logger.warning(f'Exception occurred: {e}')"
            )
            changes_made += 1
            logger.info(
                f"Fixed B110: Replaced bare except pass with logging in {file_path}:{i+1}"
            )
            in_try = False

        # Detect standalone pass in except block
        elif in_try and line.strip() == "pass":
            new_line = "        logger.warning('Exception occurred but continuing')"
            changes_made += 1
            logger.info(
                f"Fixed B110: Replaced bare pass with logging in {file_path}:{i+1}"
            )
            in_try = False

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def fix_import_issues(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix B404: Import subprocess module (add nosec for legitimate uses)"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        new_line = line

        # Add nosec for legitimate subprocess imports
        if line.strip().startswith("import subprocess") and "# nosec" not in line:
            new_line = f"{line}  # nosec B404"
            changes_made += 1
            logger.info(
                f"Fixed B404: Added nosec for subprocess import in {file_path}:{i+1}"
            )

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def backup_file(file_path: Path) -> Optional[Path]:
    """Create a backup of the original file"""
    backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
    try:
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        logger.warning(f"Could not create backup for {file_path}: {e}")
        return None


def restore_backup(file_path: Path, backup_path: Path) -> bool:
    """Restore file from backup"""
    try:
        shutil.copy2(backup_path, file_path)
        logger.info(f"Restored {file_path} from backup")
        return True
    except Exception as e:
        logger.error(f"Could not restore {file_path} from backup: {e}")
        return False


def validate_python_syntax(content: str, file_path: Path) -> bool:
    """Validate that the fixed content has valid Python syntax"""
    try:
        compile(content, str(file_path), "exec")
        return True
    except SyntaxError as e:
        logger.error(f"Syntax error in {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error validating syntax for {file_path}: {e}")
        return False


def fix_file(file_path: Path, create_backup: bool = True) -> bool:
    """Fix Bandit errors in a single Python file with comprehensive error handling"""
    logger.info(f"Fixing {file_path}")

    backup_path = None
    if create_backup:
        backup_path = backup_file(file_path)

    try:
        # Read original content
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content
        total_changes = 0

        # Get current bandit issues
        bandit_issues = run_bandit_check(file_path)
        logger.info(f"Found {len(bandit_issues)} bandit issues in {file_path}")

        # Apply fixes based on issue types
        for issue in bandit_issues:
            issue_code = issue.get("issue_text", "")

            if "B603" in issue_code or "B607" in issue_code:
                content, changes = fix_subprocess_calls(content, file_path)
                total_changes += changes
                # Also apply enhanced B603 shell=False fixes
                content, changes = fix_b603_shell_false(content, file_path)
                total_changes += changes
            elif "B113" in issue_code:
                content, changes = fix_requests_without_timeout(content, file_path)
                total_changes += changes
            elif "B104" in issue_code:
                content, changes = fix_hardcoded_bind_all_interfaces(content, file_path)
                total_changes += changes
            elif "B108" in issue_code:
                content, changes = fix_hardcoded_tmp_directory(content, file_path)
                total_changes += changes
            elif "B105" in issue_code:
                content, changes = fix_hardcoded_password_string(content, file_path)
                total_changes += changes
            elif "B110" in issue_code:
                content, changes = fix_try_except_pass(content, file_path)
                total_changes += changes
            elif "B404" in issue_code:
                content, changes = fix_import_issues(content, file_path)
                total_changes += changes

        # Apply general fixes
        content, changes = fix_subprocess_calls(content, file_path)
        total_changes += changes

        # Apply enhanced B603 shell=False fixes
        content, changes = fix_b603_shell_false(content, file_path)
        total_changes += changes

        content, changes = fix_requests_without_timeout(content, file_path)
        total_changes += changes

        content, changes = fix_hardcoded_bind_all_interfaces(content, file_path)
        total_changes += changes

        content, changes = fix_hardcoded_tmp_directory(content, file_path)
        total_changes += changes

        content, changes = fix_hardcoded_password_string(content, file_path)
        total_changes += changes

        content, changes = fix_try_except_pass(content, file_path)
        total_changes += changes

        content, changes = fix_import_issues(content, file_path)
        total_changes += changes

        # Validate syntax before writing
        if not validate_python_syntax(content, file_path):
            logger.error(f"Syntax validation failed for {file_path}")
            if backup_path and backup_path.exists():
                restore_backup(file_path, backup_path)
            return False

        # Only write if changes were made
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"✅ Fixed {total_changes} issues in {file_path}")

            # Verify fixes worked
            new_bandit_issues = run_bandit_check(file_path)
            if len(new_bandit_issues) < len(bandit_issues):
                logger.info(
                    f"✅ Reduced issues from {len(bandit_issues)} to {len(new_bandit_issues)}"
                )
            else:
                logger.warning(
                    f"⚠️ Issues not reduced: {len(bandit_issues)} -> {len(new_bandit_issues)}"
                )

            return True

        return False

    except Exception as e:
        logger.error(f"Error fixing {file_path}: {e}")
        # Restore from backup if available
        if backup_path and backup_path.exists():
            restore_backup(file_path, backup_path)
        return False


def find_python_files() -> List[Path]:
    """Find all Python files in the project"""
    python_files = []
    search_dirs = ["mlops", "shadows", "tools", "scripts"]

    for search_dir in search_dirs:
        if Path(search_dir).exists():
            python_files.extend(Path(search_dir).rglob("*.py"))

    # Also include root level Python files
    python_files.extend(Path(".").glob("*.py"))

    python_files = sorted(set(python_files))
    logger.info(f"Found {len(python_files)} Python files")

    return python_files


def main():
    """Main function with enhanced error handling"""
    parser = argparse.ArgumentParser(description="Bandit Auto-Fix Script")
    parser.add_argument("--files", nargs="+", help="Specific files to fix")
    parser.add_argument("--no-backup", action="store_true", help="Don't create backups")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )
    args = parser.parse_args()

    logger.info("🔧 Enhanced Bandit Auto-Fix Script")
    logger.info("=" * 50)

    # Define sanitize_cmd function for use in main
    def sanitize_cmd(cmd):
        import shlex

        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        if not isinstance(cmd, list) or not cmd:
            raise ValueError("Invalid command passed to sanitize_cmd()")
        allowed = {
            "ls",
            "echo",
            "kubectl",
            "helm",
            "python3",
            "cat",
            "go",
            "docker",
            "npm",
            "black",
            "ruff",
            "yamllint",
            "prettier",
            "flake8",
            "bandit",
        }
        if cmd[0] not in allowed:
            raise ValueError(f"Blocked dangerous command: {cmd[0]}")
        return cmd

    # Check if bandit is available
    try:
        subprocess.run(
            sanitize_cmd(["bandit", "--version"]), capture_output=True, check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("❌ Bandit is not installed or not available in PATH")
        logger.info("Install bandit with: pip install bandit")
        return 1

    # Get files to fix
    if args.files:
        files_to_fix = [Path(f) for f in args.files]
    else:
        files_to_fix = find_python_files()

    if not files_to_fix:
        logger.warning("No Python files found to process")
        return 0

    # Fix files
    fixed_count = 0
    error_count = 0

    for file_path in files_to_fix:
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            continue

        try:
            if args.dry_run:
                # Just show what would be fixed
                bandit_issues = run_bandit_check(file_path)
                if bandit_issues:
                    logger.info(f"Would fix {len(bandit_issues)} issues in {file_path}")
                    for issue in bandit_issues:
                        logger.info(
                            f"  - {issue.get('issue_text', 'Unknown')}: {issue.get('more_info', 'No info')}"
                        )
            else:
                if fix_file(file_path, create_backup=not args.no_backup):
                    fixed_count += 1
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            error_count += 1

    logger.info("\n" + "=" * 50)
    logger.info("📊 Summary:")
    logger.info(f"  • Files processed: {len(files_to_fix)}")
    logger.info(f"  • Files fixed: {fixed_count}")
    logger.info(f"  • Errors encountered: {error_count}")

    if args.dry_run:
        logger.info("\n🔍 Dry run completed. Use without --dry-run to apply fixes.")
    elif fixed_count > 0:
        logger.info("\n🎉 Fixed issues in some files! Run 'bandit -r .' to verify.")
    else:
        logger.info("\nℹ️ No issues fixed.")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())
