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
#!/usr/bin/env python3
"""
Script to properly fix Ruff B904 errors by correcting malformed syntax.
"""

import re
from pathlib import Path


def fix_b904_errors(file_path: Path) -> bool:
    """Fix B904 errors in a single file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Fix malformed raise statements that were created by the previous script
        # Pattern: raise HTTPException(raise HTTPException(...)from efrom e) from e
        malformed_pattern = (
            r"raise HTTPException\(raise HTTPException\(([^)]+)\)from efrom e\) from e"
        )
        malformed_replacement = r"raise HTTPException(\1) from e"

        # Apply the fix
        new_content = re.sub(malformed_pattern, malformed_replacement, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        # Also fix multi-line malformed patterns
        # Pattern: raise HTTPException(raise HTTPException(\n...\n)from efrom e) from e
        malformed_multiline_pattern = r"raise HTTPException\(raise HTTPException\(\s*\n\s*([^)]+)\s*\n\s*\)from efrom e\) from e"
        malformed_multiline_replacement = (
            r"raise HTTPException(\n            \1\n        ) from e"
        )

        new_content = re.sub(
            malformed_multiline_pattern, malformed_multiline_replacement, content
        )
        if new_content != content:
            content = new_content
            changes_made += 1

        # Fix any remaining simple cases
        # Pattern: raise HTTPException(...) without from e
        simple_pattern = r'(raise HTTPException\s*\(\s*status_code\s*=\s*\d+\s*,\s*detail\s*=\s*f?"[^"]*\{str\(e\)\}[^"]*"\s*\)\s*)(?!from e)'
        simple_replacement = r"\1from e"

        new_content = re.sub(simple_pattern, simple_replacement, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        # Fix ValueError cases
        value_error_pattern = (
            r"(raise ValueError\s*\(\s*[^)]*\{str\(e\)\}[^)]*\)\s*)(?!from e)"
        )
        value_error_replacement = r"\1from e"

        new_content = re.sub(value_error_pattern, value_error_replacement, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed {changes_made} B904 errors in {file_path}")
            return True

        return False

    except Exception as e:
        print(f"❌ Error fixing B904 in {file_path}: {e}")
        return False


def find_python_files() -> list[Path]:
    """Find all Python files in the project"""
    python_files = []
    search_dirs = ["mlops", "shadows"]

    for search_dir in search_dirs:
        if Path(search_dir).exists():
            for py_file in Path(search_dir).rglob("*.py"):
                if "node_modules" not in str(py_file) and "__pycache__" not in str(
                    py_file
                ):
                    python_files.append(py_file)

    return sorted(set(python_files))


def main():
    """Main function to fix all B904 errors"""
    print("🔧 Properly Fixing Ruff B904 Errors")
    print("=" * 50)

    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files to check")

    fixed_files = 0
    total_fixes = 0

    for file_path in python_files:
        if fix_b904_errors(file_path):
            fixed_files += 1
            total_fixes += 1

    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  • Files processed: {len(python_files)}")
    print(f"  • Files fixed: {fixed_files}")
    print(f"  • Total B904 fixes applied: {total_fixes}")

    if fixed_files > 0:
        print("\n🎉 B904 errors have been properly fixed!")
        print("⚠️  Please review the changes and ensure they meet your requirements.")
    else:
        print("\nℹ️  No B904 errors found or fixed.")

    return 0


if __name__ == "__main__":
    exit(main())