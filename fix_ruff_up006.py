#!/usr/bin/env python3
"""
Script to fix Ruff UP006 errors: "Use `dict` instead of `Dict` for type annotation"
"""

import re
from pathlib import Path
from typing import List


def fix_up006_errors(file_path: Path) -> bool:
    """Fix UP006 errors in a single file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Fix Dict -> dict in type annotations
        # Pattern: Dict[...] in type annotations
        dict_pattern = r"\bDict\b"
        dict_replacement = "dict"

        # Fix List -> list in type annotations
        # Pattern: List[...] in type annotations
        list_pattern = r"\bList\b"
        list_replacement = "list"

        # Apply fixes
        new_content = re.sub(dict_pattern, dict_replacement, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        new_content = re.sub(list_pattern, list_replacement, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed {changes_made} UP006 errors in {file_path}")
            return True

        return False

    except Exception as e:
        print(f"❌ Error fixing UP006 in {file_path}: {e}")
        return False


def find_python_files() -> List[Path]:
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
    """Main function to fix all UP006 errors"""
    print("🔧 Fixing Ruff UP006 Errors")
    print("=" * 50)

    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files to check")

    fixed_files = 0
    total_fixes = 0

    for file_path in python_files:
        if fix_up006_errors(file_path):
            fixed_files += 1
            total_fixes += 1

    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  • Files processed: {len(python_files)}")
    print(f"  • Files fixed: {fixed_files}")
    print(f"  • Total UP006 fixes applied: {total_fixes}")

    if fixed_files > 0:
        print("\n🎉 UP006 errors have been fixed!")
        print("⚠️  Please review the changes and ensure they meet your requirements.")
    else:
        print("\nℹ️  No UP006 errors found or fixed.")

    return 0


if __name__ == "__main__":
    exit(main())
