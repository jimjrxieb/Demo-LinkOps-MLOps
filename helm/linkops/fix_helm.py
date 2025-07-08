import os
import re
import subprocess

HELM_DIR = "./helm/linkops"
EXCLUDE_FILES = [
    "values.yaml"
]  # Optional: don't modify Helm values directly unless confident


def is_yaml_file(filename):
    return filename.endswith((".yaml", ".yml"))


def clean_trailing_whitespace(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        # Preserve Helm templating braces
        line = re.sub(r"[ \t]+$", "", line)
        cleaned_lines.append(line)

    if not cleaned_lines[-1].endswith("\n"):
        cleaned_lines[-1] += "\n"

    with open(filepath, "w") as file:
        file.writelines(cleaned_lines)


def auto_indent_yaml(filepath):
    """Optional auto-indentation (experimental)"""
    try:
        subprocess.run(["yamlfmt", "-w", filepath], check=True)
    except FileNotFoundError:
        print(
            "❌ 'yamlfmt' not found. Install via: go install github.com/google/yamlfmt/cmd/yamlfmt@latest"
        )
    except subprocess.CalledProcessError:
        print(f"⚠️ Failed to auto-indent: {filepath}")


def lint_yaml(filepath):
    print(f"🔧 Cleaning YAML: {filepath}")
    clean_trailing_whitespace(filepath)

    print(f"🧪 Linting YAML: {filepath}")
    result = subprocess.run(["yamllint", filepath], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Issues found in {filepath}:\n{result.stdout}")
    else:
        print(f"✅ Clean: {filepath}")


def main():
    print("📂 Scanning Helm YAMLs...")

    for root, _, files in os.walk(HELM_DIR):
        for file in files:
            if is_yaml_file(file):
                path = os.path.join(root, file)
                if file in EXCLUDE_FILES:
                    print(f"⏭️ Skipping {path}")
                    continue
                lint_yaml(path)


if __name__ == "__main__":
    main()
