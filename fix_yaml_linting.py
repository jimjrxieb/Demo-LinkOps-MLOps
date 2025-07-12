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
Script to fix YAML linting issues in the DEMO-LinkOps project.
"""

import os
import re


def fix_yaml_file(file_path):
    """Fix YAML linting issues in a single file."""
    print(f"Fixing: {file_path}")

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Fix indentation - convert 4 spaces to 2 spaces
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces > 0:
                # Convert to 2-space indentation
                indent_level = leading_spaces // 2
                fixed_line = "  " * indent_level + line.lstrip()
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)

        content = "\n".join(fixed_lines)

        # Ensure file ends with newline
        if not content.endswith("\n"):
            content += "\n"

        # Fix specific issues
        # Remove extra spaces in braces
        content = re.sub(r"\[ +", "[", content)
        content = re.sub(r" +\]", "]", content)
        content = re.sub(r"\{ +", "{", content)
        content = re.sub(r" +\}", "}", content)

        # Fix line length issues by breaking long lines
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            if len(line) > 140 and ":" in line and not line.strip().startswith("#"):
                # Try to break long lines at logical points
                if "tags:" in line and len(line) > 140:
                    # Break long tag lines
                    parts = line.split("tags:")
                    if len(parts) > 1:
                        indent = len(line) - len(line.lstrip())
                        fixed_lines.append("  " * (indent // 2) + "tags:")
                        tag_content = parts[1].strip()
                        if tag_content:
                            fixed_lines.append("  " * ((indent // 2) + 1) + tag_content)
                        continue
                elif "echo" in line and len(line) > 140:
                    # Break long echo lines
                    parts = line.split("echo")
                    if len(parts) > 1:
                        indent = len(line) - len(line.lstrip())
                        fixed_lines.append("  " * (indent // 2) + "echo")
                        echo_content = parts[1].strip()
                        if echo_content:
                            fixed_lines.append(
                                "  " * ((indent // 2) + 1) + echo_content
                            )
                        continue

            fixed_lines.append(line)

        content = "\n".join(fixed_lines)

        # Write back if content changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ Fixed: {file_path}")
        else:
            print(f"  - No changes needed: {file_path}")

    except Exception as e:
        print(f"  ✗ Error fixing {file_path}: {e}")


def main():
    """Main function to fix all YAML files."""
    # Get all YAML files
    yaml_files = []
    for root, dirs, files in os.walk("."):
        # Skip .git directory
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            if file.endswith((".yaml", ".yml")):
                yaml_files.append(os.path.join(root, file))

    print(f"Found {len(yaml_files)} YAML files to process")

    # Fix each file
    for yaml_file in sorted(yaml_files):
        fix_yaml_file(yaml_file)

    print("\nYAML linting fixes completed!")


if __name__ == "__main__":
    main()