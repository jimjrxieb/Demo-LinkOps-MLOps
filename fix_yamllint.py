import os
import re
import subprocess

YAML_EXTENSIONS = (".yaml", ".yml")


def find_yaml_files():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(YAML_EXTENSIONS):
                yield os.path.join(root, file)


def fix_github_actions_formatting(lines):
    """Fix GitHub Actions workflow specific formatting issues"""
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        original_line = line
        
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            i += 1
            continue
            
        leading_spaces = len(line) - len(line.lstrip())
        content = line.lstrip()
        
        # Fix 'with:' block indentation after 'uses:' statements
        if content.startswith("with:") and i > 0:
            prev_line = lines[i - 1].strip()
            if prev_line.startswith("- uses:") or "uses:" in prev_line:
                # 'with:' should be indented 2 more spaces than the 'uses:' line
                prev_leading = len(lines[i - 1]) - len(lines[i - 1].lstrip())
                correct_indent = prev_leading + 2
                if leading_spaces != correct_indent:
                    fixed_line = " " * correct_indent + content
                    fixed_lines.append(fixed_line)
                    print(f"  🔧 Fixed 'with:' indentation: {leading_spaces} → {correct_indent} spaces")
                    i += 1
                    continue
        
        # Fix properties under 'with:' blocks
        elif (":" in content and not content.startswith("#") and 
              i > 0 and "with:" in lines[i - 1]):
            # Properties under 'with:' should be indented 2 more spaces than 'with:'
            with_line_indent = len(lines[i - 1]) - len(lines[i - 1].lstrip())
            correct_indent = with_line_indent + 2
            if leading_spaces != correct_indent:
                fixed_line = " " * correct_indent + content
                fixed_lines.append(fixed_line)
                print(f"  🔧 Fixed 'with:' property indentation: {leading_spaces} → {correct_indent} spaces")
                i += 1
                continue
        
        # Fix 'continue-on-error:' alignment
        elif content.startswith("continue-on-error:"):
            # Find the corresponding step to align with
            step_indent = None
            for j in range(i - 1, -1, -1):
                prev_content = lines[j].lstrip()
                if (prev_content.startswith("- name:") or 
                    prev_content.startswith("- uses:") or 
                    prev_content.startswith("- run:")):
                    step_indent = len(lines[j]) - len(lines[j].lstrip()) + 2
                    break
            
            if step_indent and leading_spaces != step_indent:
                fixed_line = " " * step_indent + content
                fixed_lines.append(fixed_line)
                print(f"  🔧 Fixed 'continue-on-error:' alignment: {leading_spaces} → {step_indent} spaces")
                i += 1
                continue
        
        # Fix step properties (run:, env:, etc.) alignment
        elif (content.startswith(("run:", "env:", "name:", "uses:")) and 
              not content.startswith("- ") and i > 0):
            # Check if previous line is a step
            prev_content = lines[i - 1].lstrip()
            if (prev_content.startswith("- name:") or 
                prev_content.startswith("- uses:") or 
                prev_content.startswith("- run:")):
                prev_indent = len(lines[i - 1]) - len(lines[i - 1].lstrip())
                correct_indent = prev_indent + 2
                if leading_spaces != correct_indent:
                    fixed_line = " " * correct_indent + content
                    fixed_lines.append(fixed_line)
                    print(f"  🔧 Fixed step property indentation: {leading_spaces} → {correct_indent} spaces")
                    i += 1
                    continue
        
        # Fix bash syntax in run blocks
        if content.startswith("run:") and i + 1 < len(lines):
            # Look for bash syntax issues in subsequent lines
            j = i + 1
            while j < len(lines) and (lines[j].startswith(" ") or not lines[j].strip()):
                if lines[j].strip():
                    bash_line = lines[j]
                    fixed_bash = fix_bash_syntax(bash_line)
                    if fixed_bash != bash_line:
                        lines[j] = fixed_bash
                        print(f"  🔧 Fixed bash syntax in run block")
                j += 1
        
        # Keep original line if no fixes applied
        fixed_lines.append(original_line)
        i += 1
    
    return fixed_lines


def fix_bash_syntax(line):
    """Fix common bash syntax issues in YAML run blocks"""
    # Fix single bracket usage to double brackets
    line = re.sub(r'\[\s+([^]]+)\s+\]', r'[[\1]]', line)  # [ -f ] -> [[ -f ]]
    line = re.sub(r'\[\s*([^]]+?)\s*\](?!\])', r'[[\1]]', line)  # [ condition ] -> [[ condition ]]
    
    # Don't double-fix already correct patterns
    line = re.sub(r'\[\[\[\[', r'[[', line)
    line = re.sub(r'\]\]\]\]', r']]', line)
    
    return line


def fix_indentation_errors(lines):
    """Fix common YAML indentation errors"""
    fixed_lines = []

    for i, line in enumerate(lines):
        original_line = line

        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            continue

        # Count leading spaces
        leading_spaces = len(line) - len(line.lstrip())
        content = line.lstrip()

        # Fix common indentation issues
        if content.startswith("- "):  # List items
            # List items should be at proper YAML levels (0, 2, 4, 6, etc.)
            # If we find 6 spaces for a list item, it should likely be 4
            if leading_spaces == 6:
                fixed_line = "    " + content  # 4 spaces
                fixed_lines.append(fixed_line)
                if fixed_line != original_line:
                    print(f"  🔧 Fixed list indentation: {leading_spaces} → 4 spaces")
                continue
            # If we find 8 spaces for a list item, it should likely be 6
            elif leading_spaces == 8:
                fixed_line = "      " + content  # 6 spaces
                fixed_lines.append(fixed_line)
                if fixed_line != original_line:
                    print(f"  🔧 Fixed list indentation: {leading_spaces} → 6 spaces")
                continue

        # Fix step indentation in GitHub Actions workflows
        elif (
            content.startswith("- uses:")
            or content.startswith("- name:")
            or content.startswith("- run:")
        ):
            # GitHub Actions steps should be at 4 spaces under 'steps:'
            if leading_spaces == 6:
                fixed_line = "    " + content  # 4 spaces
                fixed_lines.append(fixed_line)
                if fixed_line != original_line:
                    print(f"  🔧 Fixed step indentation: {leading_spaces} → 4 spaces")
                continue

        # Fix property indentation
        elif ":" in content and not content.startswith("#"):
            # Properties at wrong indentation levels
            if leading_spaces == 6 and i > 0:
                # Check if previous line suggests this should be at 4 spaces
                prev_line = lines[i - 1].strip() if i > 0 else ""
                if prev_line.endswith(":") or prev_line.startswith("- "):
                    fixed_line = "    " + content  # 4 spaces
                    fixed_lines.append(fixed_line)
                    if fixed_line != original_line:
                        print(
                            f"  🔧 Fixed property indentation: {leading_spaces} → 4 spaces"
                        )
                    continue

        # Fix bracket spacing issues - remove extra spaces inside brackets
        if "[" in content and "]" in content:
            # Fix "[ main ]" to "[main]"
            fixed_content = re.sub(r"\[\s+([^]]+)\s+\]", r"[\1]", content)
            if fixed_content != content:
                fixed_line = " " * leading_spaces + fixed_content
                fixed_lines.append(fixed_line)
                print(f"  🔧 Fixed bracket spacing")
                continue

        # Keep original line if no fixes applied
        fixed_lines.append(original_line)

    return fixed_lines


def fix_github_actions_structure(lines):
    """Fix GitHub Actions workflow structure issues"""
    fixed_lines = []
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            continue
            
        # Fix action step structure issues
        content = line.lstrip()
        leading_spaces = len(line) - len(line.lstrip())
        
        # Fix missing dash before action names
        if (content.startswith("name:") and i > 0 and 
            "steps:" in lines[i-1] and 
            not any("- name:" in lines[j] for j in range(max(0, i-5), i))):
            # Add dash for first step
            fixed_line = " " * (leading_spaces - 2) + "- " + content
            fixed_lines.append(fixed_line)
            print(f"  🔧 Added missing dash before step name")
            continue
            
        # Fix action uses without proper structure
        if (content.startswith("uses:") and 
            not content.startswith("- uses:") and
            i > 0 and "steps:" in "".join(lines[max(0, i-10):i])):
            # Check if this should be a step
            needs_dash = True
            for j in range(i-1, max(0, i-5), -1):
                if lines[j].lstrip().startswith("- "):
                    needs_dash = False
                    break
                elif lines[j].lstrip().startswith(("name:", "run:", "with:", "env:")):
                    break
                    
            if needs_dash:
                fixed_line = " " * (leading_spaces - 2) + "- " + content
                fixed_lines.append(fixed_line)
                print(f"  🔧 Added missing dash before uses statement")
                continue
        
        # Keep original line if no fixes applied
        fixed_lines.append(original_line)
    
    return fixed_lines


def clean_yaml_file(filepath):
    print(f"\n🔧 Cleaning YAML: {filepath}")
    is_github_actions = "/.github/workflows/" in filepath or "\\.github\\workflows\\" in filepath
    helm_safe = filepath.startswith("./helm")

    with open(filepath, "r") as f:
        lines = f.readlines()

    # Apply general indentation fixes
    lines = fix_indentation_errors(lines)
    
    # Apply GitHub Actions specific fixes
    if is_github_actions:
        lines = fix_github_actions_structure(lines)
        lines = fix_github_actions_formatting(lines)

    cleaned = []
    for i, line in enumerate(lines):
        # Skip templating fixes for Helm charts
        if helm_safe and ("{{" in line or "{%" in line):
            cleaned.append(line)
            continue

        # Remove leading dash from first line if present
        if i == 0 and line.strip().startswith("-"):
            cleaned.append(line.lstrip("-").lstrip())
        else:
            # Ensure proper line endings
            cleaned.append(line.rstrip() + "\n")

    # Ensure file ends with newline
    if cleaned and not cleaned[-1].endswith("\n"):
        cleaned[-1] += "\n"

    # Write the cleaned content back
    with open(filepath, "w") as f:
        f.writelines(cleaned)


def lint_yaml_file(filepath):
    print(f"🧪 Linting YAML: {filepath}")
    result = subprocess.run(
        ["yamllint", filepath, "--format", "parsable"], capture_output=True, text=True
    )

    if result.returncode != 0 and result.stdout:
        print(f"❌ Issues found in {filepath}:")
        # Parse and display specific issues
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                # Extract issue type from yamllint output
                if "wrong indentation" in line:
                    print(f"  📏 {line}")
                elif "too many spaces inside brackets" in line:
                    print(f"  🔲 {line}")
                elif "no new line character at the end" in line:
                    print(f"  📄 {line}")
                elif "syntax error" in line:
                    print(f"  ⚠️  {line}")
                else:
                    print(f"  ⚠️  {line}")
        return False
    else:
        print(f"✅ Clean: {filepath}")
        return True


def auto_fix_remaining_issues(filepath):
    """Attempt to automatically fix remaining yamllint issues"""
    print(f"🔄 Auto-fixing remaining issues in: {filepath}")

    result = subprocess.run(
        ["yamllint", filepath, "--format", "parsable"], capture_output=True, text=True
    )

    if result.returncode == 0:
        return True

    with open(filepath, "r") as f:
        lines = f.readlines()

    fixed = False

    # Parse yamllint output for specific line issues
    for issue_line in result.stdout.strip().split("\n"):
        if "no new line character at the end" in issue_line:
            # Add newline at end
            if lines and not lines[-1].endswith("\n"):
                lines[-1] += "\n"
                fixed = True
                print(f"  🔧 Added newline at end of file")
                
        # Fix syntax errors related to mapping structure
        elif "syntax error" in issue_line and "mapping" in issue_line:
            # Extract line number from yamllint output
            try:
                line_num = int(issue_line.split(":")[1]) - 1
                if 0 <= line_num < len(lines):
                    line = lines[line_num]
                    # Fix common mapping structure issues
                    if "with:" in line and not line.lstrip().startswith("with:"):
                        # Fix indentation for with block
                        fixed_line = "      with:\n"
                        lines[line_num] = fixed_line
                        fixed = True
                        print(f"  🔧 Fixed 'with:' block structure at line {line_num + 1}")
            except (ValueError, IndexError):
                pass

    if fixed:
        with open(filepath, "w") as f:
            f.writelines(lines)
        return True

    return False


def main():
    print(f"📂 Scanning all YAML files for indentation and formatting issues...\n")

    all_clean = True
    processed_files = []

    for filepath in find_yaml_files():
        # First pass: clean and fix known issues
        clean_yaml_file(filepath)

        # Second pass: lint and check for remaining issues
        is_clean = lint_yaml_file(filepath)

        # Third pass: attempt auto-fix for remaining issues
        if not is_clean:
            if auto_fix_remaining_issues(filepath):
                # Re-lint after fixes
                is_clean = lint_yaml_file(filepath)

        processed_files.append((filepath, is_clean))
        all_clean = all_clean and is_clean

    # Summary
    print(f"\n{'='*50}")
    print(f"📊 YAML Linting Summary:")
    print(f"{'='*50}")

    clean_count = sum(1 for _, is_clean in processed_files if is_clean)
    total_count = len(processed_files)

    for filepath, is_clean in processed_files:
        status = "✅" if is_clean else "❌"
        print(f"{status} {filepath}")

    print(f"\n📈 Results: {clean_count}/{total_count} files clean")

    if all_clean:
        print("🎉 All YAML files are now lint-free!")
    else:
        print("⚠️  Some files still have issues that need manual attention.")
        print("\nCommon fixes you might need to apply manually:")
        print("  • Check for complex indentation in nested structures")
        print("  • Verify Helm template syntax is preserved")
        print("  • Review any custom YAML constructs")
        print("  • For GitHub Actions: ensure proper step structure and indentation")


if __name__ == "__main__":
    main()
