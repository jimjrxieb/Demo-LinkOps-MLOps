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
Script to fix E402 errors by moving imports to the top of files.
"""

import ast
import re
from pathlib import Path
from typing import List, Tuple


def extract_imports_from_code(content: str) -> Tuple[List[str], List[str]]:
    """Extract all import statements from code content"""
    try:
        tree = ast.parse(content)
        imports = []
        other_code = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Get the original import line
                import_line = ast.unparse(node)
                if import_line not in imports:
                    imports.append(import_line)

        return imports, other_code
    except SyntaxError:
        # If AST parsing fails, use regex fallback
        return extract_imports_regex(content)


def extract_imports_regex(content: str) -> Tuple[List[str], List[str]]:
    """Extract imports using regex as fallback"""
    import_pattern = r"^(?:from\s+\S+\s+import\s+.*|import\s+.*)$"
    imports = []

    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if re.match(import_pattern, line) and line not in imports:
            imports.append(line)

    return imports, []


def fix_e402_errors(file_path: Path) -> bool:
    """Fix E402 errors in a single file by moving imports to top"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Skip files that are already properly formatted
        if content.startswith("import ") or content.startswith("from "):
            return False

        # Find all import statements in the file
        lines = content.split("\n")
        import_lines = []
        non_import_lines = []
        in_docstring = False
        in_multiline_string = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Skip empty lines and comments at the top
            if not stripped or stripped.startswith("#"):
                if not non_import_lines:  # Only at the very top
                    continue
                else:
                    non_import_lines.append(line)
                    continue

            # Check for docstrings
            if '"""' in line or "'''" in line:
                if not in_docstring:
                    in_docstring = True
                    non_import_lines.append(line)
                    continue
                else:
                    in_docstring = False
                    non_import_lines.append(line)
                    continue

            if in_docstring:
                non_import_lines.append(line)
                continue

            # Check for multiline strings
            if '"""' in line or "'''" in line:
                in_multiline_string = not in_multiline_string
                non_import_lines.append(line)
                continue

            if in_multiline_string:
                non_import_lines.append(line)
                continue

            # Check if this is an import statement
            if (
                stripped.startswith("import ")
                or stripped.startswith("from ")
                and " import " in stripped
            ):
                import_lines.append(line)
            else:
                non_import_lines.append(line)

        # If we found imports that aren't at the top, reorganize the file
        if import_lines and non_import_lines:
            # Find the first non-import, non-empty, non-comment line
            first_code_line = None
            for i, line in enumerate(non_import_lines):
                stripped = line.strip()
                if (
                    stripped
                    and not stripped.startswith("#")
                    and not stripped.startswith('"""')
                    and not stripped.startswith("'''")
                ):
                    first_code_line = i
                    break

            if first_code_line is not None:
                # Reorganize: imports first, then other code
                new_lines = []

                # Add imports at the top
                new_lines.extend(import_lines)
                new_lines.append("")  # Empty line after imports

                # Add the rest of the code
                new_lines.extend(non_import_lines)

                new_content = "\n".join(new_lines)

                if new_content != original_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Fixed E402 errors in {file_path}")
                    return True

        return False

    except Exception as e:
        print(f"❌ Error fixing E402 in {file_path}: {e}")
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
    """Main function to fix all E402 errors"""
    print("🔧 Fixing E402 Import Errors")
    print("=" * 50)

    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files to check")

    fixed_files = 0
    total_fixes = 0

    for file_path in python_files:
        if fix_e402_errors(file_path):
            fixed_files += 1
            total_fixes += 1

    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  • Files processed: {len(python_files)}")
    print(f"  • Files fixed: {fixed_files}")
    print(f"  • Total E402 fixes applied: {total_fixes}")

    if fixed_files > 0:
        print("\n🎉 E402 errors have been fixed!")
        print("⚠️  Please review the changes and ensure they meet your requirements.")
    else:
        print("\nℹ️  No E402 errors found or fixed.")

    return 0


if __name__ == "__main__":
    exit(main())