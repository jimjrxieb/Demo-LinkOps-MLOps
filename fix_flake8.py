import os
import re
import subprocess

TARGET_DIR = "shadows"
ADDITIONAL_DIRS = ["mlops"]  # Add mlops directory to scanning


def find_python_files(paths):
    """Find Python files in multiple directories"""
    for path in paths:
        if os.path.exists(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        yield os.path.join(root, file)


def fix_f541_errors(filepath):
    """Fix F541 errors: f-strings missing placeholders"""
    print(f"🔧 Checking F541 errors in: {filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.splitlines()

        modified = False

        for i, line in enumerate(lines):
            # Look for f-strings without placeholders
            # Pattern: f"..." or f'...' where ... doesn't contain {
            f_string_pattern = r'f(["\'])((?:(?!\1)[^{])*)\1'

            def replace_f_string(match):
                quote = match.group(1)
                text = match.group(2)
                # Check if the text contains any { } placeholders
                if "{" not in text and "}" not in text:
                    # Convert f-string to regular string
                    return f"{quote}{text}{quote}"
                return match.group(0)  # Keep original if it has placeholders

            new_line = re.sub(f_string_pattern, replace_f_string, line)

            if new_line != line:
                lines[i] = new_line
                modified = True
                print(f"  🔧 Fixed F541 on line {i+1}: f-string → regular string")

        if modified:
            # Write back the modified content
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            print(f"  ✅ F541 fixes applied to {filepath}")
        else:
            print(f"  ℹ️  No F541 issues found in {filepath}")

    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")


def autoflake_cleanup(filepath):
    print(f"🧹 Running autoflake on: {filepath}")
    subprocess.run(
        [
            "autoflake",
            "--in-place",
            "--remove-unused-variables",
            "--remove-all-unused-imports",
            filepath,
        ],
        capture_output=True,
    )


def auto_fix_file(filepath):
    print(f"🛠️  Running autopep8 on: {filepath}")
    subprocess.run(
        ["autopep8", "--in-place", "--aggressive", "--aggressive", filepath],
        capture_output=True,
    )


def run_flake8(filepath):
    result = subprocess.run(["flake8", filepath], capture_output=True, text=True)
    if result.stdout:
        print(f"❌ Still issues in {filepath}:\n{result.stdout}")
        return False
    else:
        print(f"✅ Clean: {filepath}")
        return True


def run_flake8_check(filepath, error_code):
    """Check for specific flake8 error codes"""
    result = subprocess.run(["flake8", filepath], capture_output=True, text=True)
    if result.stdout:
        return error_code in result.stdout
    return False


def main():
    print("🔍 Scanning for Python files to auto-fix Flake8 issues...\n")

    # Combine all target directories
    all_dirs = [TARGET_DIR] + ADDITIONAL_DIRS
    total_files = 0
    clean_files = 0

    for py_file in find_python_files(all_dirs):
        total_files += 1
        print(f"\n📁 Processing: {py_file}")

        # Step 1: Fix F541 errors first (f-strings missing placeholders)
        if run_flake8_check(py_file, "F541"):
            fix_f541_errors(py_file)

        # Step 2: Run autoflake cleanup
        autoflake_cleanup(py_file)

        # Step 3: Run autopep8 for general formatting
        auto_fix_file(py_file)

        # Step 4: Final flake8 check
        if run_flake8(py_file):
            clean_files += 1

    print(f"\n{'='*50}")
    print(f"📊 Summary:")
    print(f"{'='*50}")
    print(f"Total files processed: {total_files}")
    print(f"Clean files: {clean_files}")
    print(f"Files with remaining issues: {total_files - clean_files}")

    if clean_files == total_files:
        print("🎉 All files are now flake8 compliant!")
    else:
        print("⚠️  Some files still have issues that need manual review.")


if __name__ == "__main__":
    main()
