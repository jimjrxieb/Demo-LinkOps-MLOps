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
    }
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd


#!/usr/bin/env python3
"""
Ruff Auto-Fix Script for LinkOps-MLOps
Automatically fixes Ruff errors (E741, F841, F821, etc.) in Python files
"""

import argparse
import logging
import re
import subprocess  # nosec B404
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def run_ruff_check(file_path: Path) -> List[Dict[str, Any]]:
    """Run ruff check on a file and return issues"""
    try:
        result = subprocess.run(
            sanitize_cmd(["ruff", "check", str(file_path), "--output-format=json"]),
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return []

        # Parse JSON output
        import json

        issues = json.loads(result.stdout)
        return issues
    except subprocess.TimeoutExpired:
        logger.warning(f"Ruff check timed out for {file_path}")
        return []
    except json.JSONDecodeError:
        logger.warning(f"Could not parse ruff output for {file_path}")
        return []
    except Exception as e:
        logger.warning(f"Error running ruff check on {file_path}: {e}")
        return []


def fix_ambiguous_names(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix E741: Ambiguous variable names (e.g., 'l' to 'line')"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for line in lines:
        # Look for 'l' as a variable name in common patterns (e.g., for loops, comprehensions)
        # Match 'l' in contexts like 'for i, l in ...' or 'l = ...'
        new_line = line
        # Replace 'l' in comprehension or for loop variables
        if re.search(r"\bfor\s+[a-zA-Z_]+,\s*l\s+in\b", line) or re.search(
            r"\b[a-zA-Z_]+,\s*l\s+in\b", line
        ):
            new_line = re.sub(r"\b(l)\b(?=\s+in\b)", "line", line)
            if new_line != line:
                changes_made += 1
                logger.info(f"Fixed E741: Renamed 'l' to 'line' in {file_path}")
        # Replace standalone 'l' assignments or usage
        elif re.search(r"\bl\s*=\b|\bl\b", line):
            new_line = re.sub(r"\b(l)\b", "line", line)
            if new_line != line:
                changes_made += 1
                logger.info(f"Fixed E741: Renamed 'l' to 'line' in {file_path}")

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def fix_unused_variables(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix F841: Remove unused variables"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0
    in_multiline = False

    for i, line in enumerate(lines):
        # Skip if in a multiline statement (e.g., dict, list)
        if in_multiline:
            if (
                line.strip().endswith("}")
                or line.strip().endswith("]")
                or line.strip().endswith(")")
            ):
                in_multiline = False
            fixed_lines.append(line)
            continue

        # Detect start of multiline statement
        if any(
            line.strip().endswith(start) for start in ["{", "[", "("]
        ) and not line.strip().endswith("}"):
            in_multiline = True
            fixed_lines.append(line)
            continue

        # Look for assignments like 'var = ...' that are unused
        assign_match = re.match(r"^\s*(\w+)\s*=\s*.+$", line.strip())
        if assign_match:
            var_name = assign_match.group(1)
            # Check if variable is used elsewhere
            content_without_line = "\n".join(lines[:i] + lines[i + 1 :])
            if not re.search(rf"\b{re.escape(var_name)}\b", content_without_line):
                # Skip this line (remove unused variable assignment)
                changes_made += 1
                logger.info(
                    f"Fixed F841: Removed unused variable '{var_name}' in {file_path}"
                )
                continue

        fixed_lines.append(line)

    return "\n".join(fixed_lines), changes_made


def fix_undefined_names(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix F821: Undefined name errors"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        new_line = line

        # Fix common undefined name patterns
        # Pattern: if content != original_content: (where original_content is undefined)
        if (
            re.search(r"\boriginal_content\b", line)
            and "original_content" not in content
        ):
            # Replace with a different comparison or remove the check
            if "!=" in line and "original_content" in line:
                new_line = re.sub(
                    r"if\s+content\s*!=\s*original_content:",
                    "if changes_made > 0:",
                    line,
                )
                if new_line != line:
                    changes_made += 1
                    logger.info(
                        f"Fixed F821: Replaced undefined 'original_content' check in {file_path}"
                    )

        # Pattern: undefined variable in function scope
        elif re.search(r"\bundefined_var\b", line):
            # Remove or comment out lines with undefined variables
            new_line = f"# {line}  # TODO: Fix undefined variable"
            changes_made += 1
            logger.info(f"Fixed F821: Commented out undefined variable in {file_path}")

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def fix_e402_imports(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix E402: Module level import not at top of file"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    # Collect all imports and non-import lines
    imports = []
    non_imports = []
    in_docstring = False
    in_multiline_string = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Handle docstrings
        if '"""' in line or "'''" in line:
            if not in_docstring:
                in_docstring = True
            else:
                in_docstring = False
            non_imports.append(line)
            continue

        # Handle multiline strings
        if in_multiline_string:
            non_imports.append(line)
            if '"""' in line or "'''" in line:
                in_multiline_string = False
            continue

        # Skip if in docstring or multiline string
        if in_docstring or in_multiline_string:
            non_imports.append(line)
            continue

        # Check for multiline string start
        if stripped.startswith('"""') or stripped.startswith("'''"):
            in_multiline_string = True
            non_imports.append(line)
            continue

        # Check if line is an import
        if (
            stripped.startswith("import ")
            or stripped.startswith("from ")
            and " import " in stripped
        ):
            imports.append(line)
        else:
            non_imports.append(line)

    # Reconstruct file with imports at the top
    if imports:
        # Add shebang and encoding if present
        if non_imports and non_imports[0].startswith("#!"):
            fixed_lines.append(non_imports.pop(0))

        # Add encoding declaration if present
        if non_imports and non_imports[0].startswith("# -*-"):
            fixed_lines.append(non_imports.pop(0))

        # Add all imports
        fixed_lines.extend(imports)
        changes_made += len(imports)

        # Add a blank line after imports if there are non-import lines
        if non_imports:
            fixed_lines.append("")

        # Add remaining non-import lines
        fixed_lines.extend(non_imports)

        if changes_made > 0:
            logger.info(
                f"Fixed E402: Moved {len(imports)} import(s) to top of file in {file_path}"
            )

    return "\n".join(fixed_lines), changes_made


def fix_import_issues(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix import-related issues"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for line in lines:
        new_line = line

        # Fix unused imports
        if line.strip().startswith("import ") or line.strip().startswith("from "):
            # Check if import is actually used
            import_name = re.search(r"import\s+(\w+)", line)
            if import_name:
                module_name = import_name.group(1)
                if module_name not in content.replace(line, ""):
                    # Comment out unused import
                    new_line = f"# {line}  # TODO: Remove if not needed"
                    changes_made += 1
                    logger.info(f"Fixed unused import '{module_name}' in {file_path}")

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def fix_syntax_errors(content: str, file_path: Path) -> Tuple[str, int]:
    """Fix basic syntax errors"""
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for line in lines:
        new_line = line

        # Fix common syntax issues
        # Remove trailing whitespace
        if line.rstrip() != line:
            new_line = line.rstrip()
            changes_made += 1

        # Fix missing colons after if/for/while/def/class
        if re.match(r"^\s*(if|for|while|def|class)\s+.*[^:]$", line):
            new_line = line + ":"
            changes_made += 1
            logger.info(f"Fixed syntax: Added missing colon in {file_path}")

        fixed_lines.append(new_line)

    return "\n".join(fixed_lines), changes_made


def backup_file(file_path: Path) -> Path:
    """Create a backup of the original file"""
    backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
    try:
        import shutil

        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        logger.warning(f"Could not create backup for {file_path}: {e}")
        return None


def restore_backup(file_path: Path, backup_path: Path) -> bool:
    """Restore file from backup"""
    try:
        import shutil

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
    """Fix Ruff errors in a single Python file with comprehensive error handling"""
    logger.info(f"Fixing {file_path}")

    backup_path = None
    if create_backup:
        backup_path = backup_file(file_path)

    try:
        # Read original content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        total_changes = 0

        # Get current ruff issues
        ruff_issues = run_ruff_check(file_path)
        logger.info(f"Found {len(ruff_issues)} ruff issues in {file_path}")

        # Apply fixes based on issue types
        for issue in ruff_issues:
            issue_code = issue.get("code", "")

            if "E741" in issue_code:
                content, changes = fix_ambiguous_names(content, file_path)
                total_changes += changes
            elif "F841" in issue_code:
                content, changes = fix_unused_variables(content, file_path)
                total_changes += changes
            elif "F821" in issue_code:
                content, changes = fix_undefined_names(content, file_path)
                total_changes += changes
            elif "E402" in issue_code:
                content, changes = fix_e402_imports(content, file_path)
                total_changes += changes

        # Apply general fixes
        content, changes = fix_e402_imports(content, file_path)
        total_changes += changes

        content, changes = fix_import_issues(content, file_path)
        total_changes += changes

        content, changes = fix_syntax_errors(content, file_path)
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
            new_ruff_issues = run_ruff_check(file_path)
            if len(new_ruff_issues) < len(ruff_issues):
                logger.info(
                    f"✅ Reduced issues from {len(ruff_issues)} to {len(new_ruff_issues)}"
                )
            else:
                logger.warning(
                    f"⚠️ Issues not reduced: {len(ruff_issues)} -> {len(new_ruff_issues)}"
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
    """Find all Python files in mlops/ and shadows/"""
    python_files = []
    search_dirs = ["mlops", "shadows"]

    for search_dir in search_dirs:
        if Path(search_dir).exists():
            python_files.extend(Path(search_dir).rglob("*.py"))

    python_files = sorted(set(python_files))
    logger.info(f"Found {len(python_files)} Python files")

    return python_files


def main():
    """Main function with enhanced error handling"""
    parser = argparse.ArgumentParser(description="Ruff Auto-Fix Script")
    parser.add_argument("--files", nargs="+", help="Specific files to fix")
    parser.add_argument("--no-backup", action="store_true", help="Don't create backups")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )
    args = parser.parse_args()

    logger.info("🔧 Enhanced Ruff Auto-Fix Script")
    logger.info("=" * 50)

    # Check if ruff is available
    try:
        subprocess.run(
            sanitize_cmd(["ruff", "--version"]), capture_output=True, check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("❌ Ruff is not installed or not available in PATH")
        logger.info("Install ruff with: pip install ruff")
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
                ruff_issues = run_ruff_check(file_path)
                if ruff_issues:
                    logger.info(f"Would fix {len(ruff_issues)} issues in {file_path}")
                    for issue in ruff_issues:
                        logger.info(
                            f"  - {issue.get('code', 'Unknown')}: {issue.get('message', 'No message')}"
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
        logger.info("\n🎉 Fixed issues in some files! Run 'ruff check .' to verify.")
    else:
        logger.info("\nℹ️ No issues fixed.")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())
