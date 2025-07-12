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
Script to fix Ruff B904 errors: "Within an except clause, raise exceptions with raise ... from err"
"""

import re
from pathlib import Path
from typing import List


def fix_b904_errors(file_path: Path) -> bool:
    """Fix B904 errors in a single file"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Pattern 1: raise HTTPException(...) without from
        # Match: raise HTTPException(status_code=..., detail=f"... {str(e)}")
        pattern1 = r'raise HTTPException\s*\(\s*status_code\s*=\s*\d+\s*,\s*detail\s*=\s*f?"[^"]*\{str\(e\)\}[^"]*"\s*\)'
        replacement1 = r"raise HTTPException(\g<0>) from e"

        # Pattern 2: raise HTTPException(...) with str(e) but no from
        pattern2 = r'(raise HTTPException\s*\(\s*status_code\s*=\s*\d+\s*,\s*detail\s*=\s*f?"[^"]*\{str\(e\)\}[^"]*"\s*\)\s*)'
        replacement2 = r"\1from e"

        # Pattern 3: raise Exception(...) without from
        pattern3 = r"(raise \w+Exception\s*\(\s*[^)]*\{str\(e\)\}[^)]*\)\s*)"
        replacement3 = r"\1from e"

        # Pattern 4: raise ValueError(...) without from
        pattern4 = r"(raise ValueError\s*\(\s*[^)]*\{str\(e\)\}[^)]*\)\s*)"
        replacement4 = r"\1from e"

        # Apply patterns
        patterns = [
            (pattern1, replacement1),
            (pattern2, replacement2),
            (pattern3, replacement3),
            (pattern4, replacement4),
        ]

        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                changes_made += 1

        # More specific pattern for common cases
        # Match: except Exception as e: ... raise HTTPException(...)
        lines = content.split("\n")
        fixed_lines = []

        for i, line in enumerate(lines):
            # Check if this line has a raise statement after an except
            if (
                "raise HTTPException" in line
                and "str(e)" in line
                and "from e" not in line
            ):
                # Look for the except block
                for j in range(i - 1, max(0, i - 10), -1):
                    if "except" in lines[j] and "as e" in lines[j]:
                        # This is a B904 error - add 'from e'
                        if line.strip().endswith(")"):
                            new_line = line.rstrip() + " from e"
                            fixed_lines.append(new_line)
                            changes_made += 1
                            print(f"  Fixed B904 in {file_path}:{i+1}")
                        break
                    elif "except" in lines[j]:
                        break
                else:
                    fixed_lines.append(line)
            elif (
                "raise ValueError" in line and "str(e)" in line and "from e" not in line
            ):
                # Similar fix for ValueError
                if line.strip().endswith(")"):
                    new_line = line.rstrip() + " from e"
                    fixed_lines.append(new_line)
                    changes_made += 1
                    print(f"  Fixed B904 in {file_path}:{i+1}")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        content = "\n".join(fixed_lines)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed {changes_made} B904 errors in {file_path}")
            return True

        return False

    except Exception as e:
        print(f"❌ Error fixing B904 in {file_path}: {e}")
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
    """Main function to fix all B904 errors"""
    print("🔧 Fixing Ruff B904 Errors")
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
        print("\n🎉 B904 errors have been fixed!")
        print("⚠️  Please review the changes and ensure they meet your requirements.")
    else:
        print("\nℹ️  No B904 errors found or fixed.")

    return 0


if __name__ == "__main__":
    exit(main())