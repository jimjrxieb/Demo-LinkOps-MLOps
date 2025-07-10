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
Enhanced YAML Lint Auto-Fix Script for LinkOps-MLOps
Automatically fixes YAML linting errors (indentation, syntax, braces, etc.)
"""

import argparse
import logging
import os
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

YAML_EXTENSIONS = (".yaml", ".yml")


def run_yamllint_check(file_path: Path) -> List[Dict[str, Any]]:
    try:
        result = subprocess.run(
            sanitize_cmd(["yamllint", str(file_path), "--format", "parsable"]),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return []

        issues = []
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                parts = line.split(":")
                if len(parts) >= 5:
                    issues.append(
                        {
                            "file": parts[0],
                            "line": int(parts[1]),
                            "column": int(parts[2]),
                            "level": parts[3],
                            "message": ":".join(parts[4:]).strip(),
                        }
                    )
        return issues
    except subprocess.TimeoutExpired:
        logger.warning(f"Yamllint check timed out for {file_path}")
        return []
    except Exception as e:
        logger.warning(f"Error running yamllint check on {file_path}: {e}")
        return []


def normalize_indentation(
    content: str, file_path: Path, expected_levels: List[int] = [0, 2, 4, 6, 8]
) -> Tuple[str, int]:
    """
    Normalize YAML indentation to nearest *lower* allowed level (e.g., from 10 to 8).
    """
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        if not line.strip():
            fixed_lines.append(line)
            continue

        original_indent = len(line) - len(line.lstrip())
        content_stripped = line.lstrip()

        # Find closest valid indent (round down to nearest in expected_levels)
        valid_indent = max(
            [lvl for lvl in expected_levels if lvl <= original_indent], default=0
        )

        if original_indent != valid_indent:
            fixed_line = " " * valid_indent + content_stripped
            fixed_lines.append(fixed_line)
            changes_made += 1
            logger.info(
                f"Fixed indent from {original_indent} → {valid_indent} in {file_path}:{i+1}"
            )
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines), changes_made


def fix_braces_spacing(line: str) -> str:
    """Fix spacing around braces in YAML content"""
    if "{" in line and "}" in line:
        fixed = re.sub(r"\{\s+", "{ ", line)
        fixed = re.sub(r"\s+\}", " }", fixed)
        return fixed
    return line


def fix_yaml_formatting(content: str, file_path: Path) -> Tuple[str, int]:
    """
    Comprehensive YAML formatting fixes:
    - Wrong indentation (2 vs 0, 6 vs 4, etc.)
    - Extra/missing newlines
    - Too many spaces in braces
    - Simple syntax errors (safe auto-adjust)
    """
    logger.info(f"Applying comprehensive YAML formatting fixes to {file_path}")
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        original_line = line

        # Skip comments
        if line.strip().startswith("#"):
            fixed_lines.append(line)
            continue

        # Fix braces spacing
        line = fix_braces_spacing(line)

        # Fix specific indentation patterns
        leading = len(line) - len(line.lstrip())
        if leading in [6, 2, 12, 8]:
            # Common yamllint indentation fixes
            if leading == 6:
                line = " " * 4 + line.lstrip()
                changes_made += 1
            elif leading == 2:
                line = line.lstrip()  # Remove leading spaces
                changes_made += 1
            elif leading == 12:
                line = " " * 10 + line.lstrip()
                changes_made += 1
            elif leading == 8:
                line = " " * 6 + line.lstrip()
                changes_made += 1

        if line != original_line:
            logger.info(f"Fixed formatting in {file_path}:{i+1}")

        fixed_lines.append(line)

    # Ensure proper newline at end of file
    if fixed_lines and not fixed_lines[-1].endswith("\n"):
        fixed_lines[-1] += "\n"
        changes_made += 1

    return "\n".join(fixed_lines), changes_made


def backup_file(file_path: Path) -> Optional[Path]:
    backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
    try:
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        logger.warning(f"Could not create backup for {file_path}: {e}")
        return None


def validate_yaml_syntax(content: str, file_path: Path) -> bool:
    try:
        import yaml

        yaml.safe_load(content)
        return True
    except Exception as e:
        logger.error(f"YAML syntax error in {file_path}: {e}")
        return False


def fix_file(file_path: Path, create_backup: bool = True) -> bool:
    logger.info(f"Fixing {file_path}")
    backup_path = backup_file(file_path) if create_backup else None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        total_changes = 0

        # Apply comprehensive YAML formatting fixes
        content, changes = fix_yaml_formatting(content, file_path)
        total_changes += changes

        # Apply specific yamllint rule fixes
        content, changes = fix_specific_yamllint_rules(content, file_path)
        total_changes += changes

        # Normalize indentation (backup method)
        content, changes = normalize_indentation(
            content, file_path, expected_levels=[0, 2, 4, 6, 8]
        )
        total_changes += changes

        if not validate_yaml_syntax(content, file_path):
            logger.error(f"YAML syntax validation failed for {file_path}")
            if backup_path and backup_path.exists():
                shutil.copy2(backup_path, file_path)
            return False

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(
                f"✅ Fixed {total_changes} YAML formatting issues in {file_path}"
            )

        return True
    except Exception as e:
        logger.error(f"Error fixing {file_path}: {e}")
        if backup_path and backup_path.exists():
            shutil.copy2(backup_path, file_path)
        return False


def find_yaml_files():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(YAML_EXTENSIONS):
                yield Path(os.path.join(root, file))


def fix_specific_yamllint_rules(content: str, file_path: Path) -> Tuple[str, int]:
    """
    Fix specific yamllint rule violations:
    - indentation: Wrong indentation (2 vs 0, 6 vs 4, etc.)
    - braces: Too many spaces in braces
    - new-line: Extra/missing newlines
    """
    logger.info(f"Applying specific yamllint rule fixes to {file_path}")
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    yamllint_rules = {
        "indentation": [(6, 4), (2, 0), (12, 10), (8, 6)],
        "braces": True,
        "new-line": True,
    }

    for i, line in enumerate(lines):
        original_line = line

        # Skip comments
        if line.strip().startswith("#"):
            fixed_lines.append(line)
            continue

        # Fix indentation based on yamllint rules
        leading = len(line) - len(line.lstrip())
        for bad, good in yamllint_rules["indentation"]:
            if leading == bad:
                line = " " * good + line.lstrip()
                changes_made += 1
                logger.info(f"Fixed indentation rule {bad}→{good} in {file_path}:{i+1}")
                break

        # Fix braces spacing
        if yamllint_rules["braces"]:
            line = fix_braces_spacing(line)

        if line != original_line:
            changes_made += 1

        fixed_lines.append(line)

    # Fix newline at end of file
    if yamllint_rules["new-line"] and fixed_lines:
        if not fixed_lines[-1].endswith("\n"):
            fixed_lines[-1] += "\n"
            changes_made += 1

    return "\n".join(fixed_lines), changes_made


def main():
    parser = argparse.ArgumentParser(description="Enhanced YAML Auto-Fix Script")
    parser.add_argument("--files", nargs="+", help="Specific files to fix")
    parser.add_argument("--no-backup", action="store_true", help="Don't create backups")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )
    args = parser.parse_args()

    targets = [Path(f) for f in args.files] if args.files else list(find_yaml_files())

    logger.info("🔧 Enhanced YAML Auto-Fix Script")
    logger.info("=" * 50)
    logger.info("Fixing yamllint issues:")
    logger.info("  - Wrong indentation (2 vs 0, 6 vs 4, etc.)")
    logger.info("  - Extra/missing newlines")
    logger.info("  - Too many spaces in braces")
    logger.info("  - Simple syntax errors (safe auto-adjust)")

    fixed = 0
    for file in targets:
        if args.dry_run:
            logger.info(f"Would fix: {file}")
            fixed += 1
        else:
            if fix_file(file, create_backup=not args.no_backup):
                fixed += 1

    logger.info(f"🔹 Fixed {fixed} YAML file(s)")
    if args.dry_run:
        logger.info("Dry run completed - no files were modified")


if __name__ == "__main__":
    exit(main())
