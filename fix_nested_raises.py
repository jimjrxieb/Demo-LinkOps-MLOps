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
Script to fix nested raise HTTPException statements that were created by regex replacement.
"""

import re
from pathlib import Path


def fix_nested_raises(file_path: Path) -> bool:
    """Fix nested raise HTTPException statements in a single file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Pattern 1: Single line nested raise
        # From: raise HTTPException(raise HTTPException(...)from efrom e) from e
        # To:   raise HTTPException(...) from e
        pattern1 = (
            r"raise HTTPException\(raise HTTPException\(([^)]+)\)from efrom e\) from e"
        )
        replacement1 = r"raise HTTPException(\1) from e"

        new_content = re.sub(pattern1, replacement1, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        # Pattern 2: Multi-line nested raise
        # From: raise HTTPException(raise HTTPException(\n...\n)from efrom e) from e
        # To:   raise HTTPException(\n...\n) from e
        pattern2 = r"raise HTTPException\(raise HTTPException\(\s*\n\s*([^)]+)\s*\n\s*\)from efrom e\) from e"
        replacement2 = r"raise HTTPException(\n            \1\n        ) from e"

        new_content = re.sub(pattern2, replacement2, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        # Pattern 3: Any remaining nested patterns
        # Look for any remaining "raise HTTPException(raise HTTPException"
        pattern3 = r"raise HTTPException\(raise HTTPException"
        if pattern3 in content:
            print(f"⚠️  Found remaining nested raise in {file_path}")
            # This is a manual fix case - we'll handle it specifically

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed {changes_made} nested raise statements in {file_path}")
            return True

        return False

    except Exception as e:
        print(f"❌ Error fixing nested raises in {file_path}: {e}")
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
    """Main function to fix all nested raise statements"""
    print("🔧 Fixing Nested Raise HTTPException Statements")
    print("=" * 60)

    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files to check")

    fixed_files = 0
    total_fixes = 0

    for file_path in python_files:
        if fix_nested_raises(file_path):
            fixed_files += 1
            total_fixes += 1

    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  • Files processed: {len(python_files)}")
    print(f"  • Files fixed: {fixed_files}")
    print(f"  • Total nested raise fixes applied: {total_fixes}")

    if fixed_files > 0:
        print("\n🎉 Nested raise statements have been fixed!")
        print("⚠️  Please review the changes and ensure they meet your requirements.")
    else:
        print("\nℹ️  No nested raise statements found or fixed.")

    return 0


if __name__ == "__main__":
    exit(main())
