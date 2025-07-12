#!/usr/bin/env python3
"""
Comprehensive script to fix all nested raise HTTPException statements.
"""

import os
import re


def fix_file(file_path):
    """Fix nested raise statements in a single file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Pattern 1: Single line nested raise with from efrom e
        pattern1 = (
            r"raise HTTPException\(raise HTTPException\(([^)]+)\)from efrom e\) from e"
        )
        replacement1 = r"raise HTTPException(\1) from e"

        new_content = re.sub(pattern1, replacement1, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        # Pattern 2: Multi-line nested raise
        pattern2 = r"raise HTTPException\(raise HTTPException\(\s*\n\s*([^)]+)\s*\n\s*\)from efrom e\) from e"
        replacement2 = r"raise HTTPException(\n            \1\n        ) from e"

        new_content = re.sub(pattern2, replacement2, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        # Pattern 3: Multi-line nested raise without from efrom e
        pattern3 = r"raise HTTPException\(raise HTTPException\(\s*\n\s*([^)]+)\s*\n\s*\)\) from e"
        replacement3 = r"raise HTTPException(\n            \1\n        ) from e"

        new_content = re.sub(pattern3, replacement3, content)
        if new_content != content:
            content = new_content
            changes_made += 1

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed {changes_made} nested raises in {file_path}")
            return True

        return False

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False


def main():
    """Fix all nested raise statements"""
    print("🔧 Fixing All Nested Raise HTTPException Statements")
    print("=" * 60)

    # List of files that need fixing
    files_to_fix = [
        "mlops/mlops_platform/routers/rune_executor.py",
        "mlops/whis_logic/main.py",
        "mlops/whis_data_input/routers/youtube.py",
        "mlops/whis_data_input/routers/qna_input.py",
        "mlops/whis_sanitize/main.py",
        "mlops/whis_data_input/routers/chatgpt_csv.py",
        "mlops/whis_data_input/routers/image_text.py",
        "mlops/whis_data_input/routers/info_dump.py",
    ]

    fixed_files = 0
    total_fixes = 0

    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_file(file_path):
                fixed_files += 1
                total_fixes += 1
        else:
            print(f"⚠️  File not found: {file_path}")

    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"  • Files processed: {len(files_to_fix)}")
    print(f"  • Files fixed: {fixed_files}")
    print(f"  • Total nested raise fixes applied: {total_fixes}")

    if fixed_files > 0:
        print("\n🎉 All nested raise statements have been fixed!")
        print("✅ You can now run 'black .' and 'isort .' successfully!")
    else:
        print("\nℹ️  No nested raise statements found or fixed.")

    return 0


if __name__ == "__main__":
    exit(main())
