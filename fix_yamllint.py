import os
import re
import subprocess
import argparse

YAML_EXTENSIONS = (".yaml", ".yml")


def find_yaml_files(exclude_github_actions=False):
    """Find all YAML files, optionally excluding GitHub Actions workflows"""
    github_actions_files = []
    regular_files = []
    
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(YAML_EXTENSIONS):
                filepath = os.path.join(root, file)
                
                # Check if it's a GitHub Actions workflow
                if "/.github/workflows/" in filepath or "\\.github\\workflows\\" in filepath:
                    if not exclude_github_actions:
                        github_actions_files.append(filepath)
                else:
                    regular_files.append(filepath)
    
    # Return regular files first, then GitHub Actions files (if not excluded)
    return regular_files + github_actions_files


def is_github_actions_file(filepath):
    """Check if file is a GitHub Actions workflow"""
    return "/.github/workflows/" in filepath or "\\.github\\workflows\\" in filepath


def fix_github_actions_formatting(lines):
    """Fix GitHub Actions workflow specific formatting issues - CONSERVATIVE VERSION"""
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

        # CONSERVATIVE: Only fix obvious 'with:' block indentation issues
        if content.startswith("with:") and i > 0:
            prev_line = lines[i - 1].strip()
            if prev_line.startswith("- uses:") or "uses:" in prev_line:
                # 'with:' should be indented 2 more spaces than the 'uses:' line
                prev_leading = len(lines[i - 1]) - len(lines[i - 1].lstrip())
                correct_indent = prev_leading + 2
                # Only fix if severely wrong (off by more than 1 space)
                if abs(leading_spaces - correct_indent) > 1:
                    fixed_line = " " * correct_indent + content
                    fixed_lines.append(fixed_line)
                    print(f"  🔧 Fixed 'with:' indentation: {leading_spaces} → {correct_indent} spaces")
                    i += 1
                    continue

        # CONSERVATIVE: Only fix properties under 'with:' if severely wrong
        elif (":" in content and not content.startswith("#") and i > 0 
              and lines[i - 1].strip() == "with:"):
            # Properties under 'with:' should be indented 2 more spaces than 'with:'
            with_line_indent = len(lines[i - 1]) - len(lines[i - 1].lstrip())
            correct_indent = with_line_indent + 2
            # Only fix if severely wrong (off by more than 1 space)
            if abs(leading_spaces - correct_indent) > 1:
                fixed_line = " " * correct_indent + content
                fixed_lines.append(fixed_line)
                print(f"  🔧 Fixed 'with:' property indentation: {leading_spaces} → {correct_indent} spaces")
                i += 1
                continue

        # Keep original line if no fixes applied
        fixed_lines.append(original_line)
        i += 1

    return fixed_lines


def fix_bash_syntax(line):
    """Fix common bash syntax issues in YAML run blocks - CONSERVATIVE VERSION"""
    original = line
    
    # ONLY fix obvious double bracket spacing issues
    # Fix: [[-z to [[ -z (missing space after [[)
    line = re.sub(r'\[\[([^\s])', r'[[ \1', line)
    
    # Fix: -z"]] to -z "]] (missing space before ]])
    line = re.sub(r'([^\s])\]\]', r'\1 ]]', line)
    
    # Fix: [[ -z"var" ]] to [[ -z "$var" ]] (missing space around quotes)
    line = re.sub(r'\[\[\s*([^"]*)"([^"]*)"([^]]*)\]\]', r'[[ \1 "\2" \3]]', line)
    
    if line != original:
        print(f"  🔧 Fixed bash syntax: '{original.strip()}' → '{line.strip()}'")
    
    return line


def fix_indentation_errors(lines):
    """Fix common YAML indentation errors - CONSERVATIVE VERSION"""
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

        # CONSERVATIVE: Only fix severely wrong indentation (multiples of 2)
        if content.startswith("- "):  # List items
            # Only fix if indentation is odd number (clearly wrong)
            if leading_spaces % 2 == 1:
                fixed_indent = leading_spaces + 1 if leading_spaces % 2 == 1 else leading_spaces
                fixed_line = " " * fixed_indent + content
                fixed_lines.append(fixed_line)
                if fixed_line != original_line:
                    print(f"  🔧 Fixed list indentation: {leading_spaces} → {fixed_indent} spaces")
                continue

        # Keep original line if no fixes applied
        fixed_lines.append(original_line)

    return fixed_lines


def fix_github_actions_structure(lines):
    """Fix GitHub Actions structure issues - CONSERVATIVE VERSION"""
    fixed_lines = []

    for i, line in enumerate(lines):
        content = line.lstrip()
        leading_spaces = len(line) - len(line.lstrip())

        # CONSERVATIVE: Only fix obvious missing dashes in steps
        if (content.startswith("uses:") and not content.startswith("- uses:") and 
            i > 0 and "steps:" in "".join(lines[max(0, i - 5):i])):
            
            # Check if we're clearly in a steps section and missing dash
            in_steps = False
            for j in range(i - 1, max(0, i - 10), -1):
                if lines[j].strip() == "steps:":
                    in_steps = True
                    break
                elif lines[j].lstrip().startswith(("jobs:", "name:", "on:")):
                    break
            
            if in_steps:
                fixed_line = " " * (leading_spaces - 2) + "- " + content
                fixed_lines.append(fixed_line)
                print(f"  🔧 Added missing dash before uses statement")
                continue

        # Keep original line if no fixes applied
        fixed_lines.append(line)

    return fixed_lines


def clean_yaml_file(filepath, conservative_mode=False):
    """Clean YAML file with optional conservative mode for critical files"""
    print(f"\n🔧 Cleaning YAML: {filepath}")
    is_github_actions = is_github_actions_file(filepath)
    helm_safe = filepath.startswith("./helm")

    with open(filepath, "r") as f:
        lines = f.readlines()

    # For GitHub Actions workflows, use conservative mode by default
    if is_github_actions:
        conservative_mode = True
        print("  ⚠️  Using conservative mode for GitHub Actions workflow")

    # Apply general indentation fixes
    if not conservative_mode:
    lines = fix_indentation_errors(lines)

    # Apply GitHub Actions specific fixes
    if is_github_actions:
        if not conservative_mode:
            lines = fix_github_actions_structure(lines)
        lines = fix_github_actions_formatting(lines)

    # Handle bash syntax in run blocks
    if is_github_actions:
        for i, line in enumerate(lines):
            if "run:" in line and i + 1 < len(lines):
                # Look for bash syntax issues in subsequent lines
                j = i + 1
                while j < len(lines) and (lines[j].startswith(" ") or not lines[j].strip()):
                    if lines[j].strip() and "[" in lines[j]:
                        fixed_bash = fix_bash_syntax(lines[j])
                        lines[j] = fixed_bash
                    j += 1

    cleaned = []
    for i, line in enumerate(lines):
        # Skip templating fixes for Helm charts
        if helm_safe and ("{{" in line or "{%" in line):
            cleaned.append(line)
            continue

        # Remove leading dash from first line if present (but not for GitHub Actions)
        if i == 0 and line.strip().startswith("-") and not is_github_actions:
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

    if fixed:
        with open(filepath, "w") as f:
            f.writelines(lines)
        return True

    return False


def main():
    parser = argparse.ArgumentParser(description="Fix YAML linting issues")
    parser.add_argument("--exclude-github-actions", action="store_true", 
                       help="Exclude GitHub Actions workflow files")
    parser.add_argument("--github-actions-last", action="store_true",
                       help="Process GitHub Actions workflow files last")
    args = parser.parse_args()

    print(f"📂 Scanning YAML files for indentation and formatting issues...\n")
    
    if args.exclude_github_actions:
        print("⚠️  Excluding GitHub Actions workflow files from processing")
    elif args.github_actions_last:
        print("🔄 Processing GitHub Actions workflow files last with conservative fixes")

    all_clean = True
    processed_files = []

    # Get files in appropriate order
    if args.github_actions_last:
        # Process regular files first, then GitHub Actions files
        regular_files = []
        github_actions_files = []
        
        for filepath in find_yaml_files(exclude_github_actions=False):
            if is_github_actions_file(filepath):
                github_actions_files.append(filepath)
            else:
                regular_files.append(filepath)
        
        files_to_process = regular_files + github_actions_files
        
        if github_actions_files:
            print(f"📋 Processing order:")
            print(f"  1. Regular YAML files: {len(regular_files)} files")
            print(f"  2. GitHub Actions workflows: {len(github_actions_files)} files (conservative mode)")
            print()
    else:
        files_to_process = find_yaml_files(exclude_github_actions=args.exclude_github_actions)

    for filepath in files_to_process:
        print(f"{'='*60}")
        
        # Mark when we switch to GitHub Actions files
        if (args.github_actions_last and is_github_actions_file(filepath) and 
            processed_files and not is_github_actions_file(processed_files[-1][0])):
            print("🔄 Switching to GitHub Actions workflows (conservative mode)")
            print(f"{'='*60}")
        
        # First pass: clean and fix known issues
        clean_yaml_file(filepath, conservative_mode=is_github_actions_file(filepath))

        # Second pass: lint and check for remaining issues
        is_clean = lint_yaml_file(filepath)

        # Third pass: attempt auto-fix for remaining issues (conservative for GitHub Actions)
        if not is_clean and not is_github_actions_file(filepath):
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
    
    # Separate counts for different file types
    github_actions_count = sum(1 for filepath, _ in processed_files if is_github_actions_file(filepath))
    regular_count = total_count - github_actions_count

    for filepath, is_clean in processed_files:
        status = "✅" if is_clean else "❌"
        file_type = "🚀" if is_github_actions_file(filepath) else "📄"
        print(f"{status} {file_type} {filepath}")

    print(f"\n📈 Results: {clean_count}/{total_count} files clean")
    if github_actions_count > 0:
        print(f"   📄 Regular files: {total_count - github_actions_count}")
        print(f"   🚀 GitHub Actions: {github_actions_count}")

    if all_clean:
        print("🎉 All YAML files are now lint-free!")
    else:
        print("⚠️  Some files still have issues that need manual attention.")
        print("\nRecommended next steps:")
        print("  1. For GitHub Actions workflows: Review changes carefully before committing")
        print("  2. Test workflow syntax using 'gh workflow view' if available")
        print("  3. For complex issues, consider using '--exclude-github-actions' flag")
        print("  4. Manual fixes may be needed for complex nested structures")

    print(f"\n💡 Usage tips:")
    print(f"  • To exclude GitHub Actions: python3 fix_yamllint.py --exclude-github-actions")
    print(f"  • To process GitHub Actions last: python3 fix_yamllint.py --github-actions-last")


if __name__ == "__main__":
    main()
