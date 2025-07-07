import os
import subprocess

YAML_EXTENSIONS = (".yaml", ".yml")


def find_yaml_files():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(YAML_EXTENSIONS):
                yield os.path.join(root, file)


def clean_yaml_file(filepath):
    print(f"\n🔧 Cleaning YAML: {filepath}")
    helm_safe = filepath.startswith("./helm")

    with open(filepath, "r") as f:
        lines = f.readlines()

    cleaned = []
    for i, line in enumerate(lines):
        if helm_safe and ("{{" in line or "{%" in line):
            cleaned.append(line)
            continue

        if i == 0 and line.strip().startswith("-"):
            cleaned.append(line.lstrip("-").lstrip())
        else:
            cleaned.append(line.rstrip() + "\n")

    if not cleaned[-1].endswith("\n"):
        cleaned[-1] += "\n"

    with open(filepath, "w") as f:
        f.writelines(cleaned)


def lint_yaml_file(filepath):
    print(f"🧪 Linting YAML: {filepath}")
    result = subprocess.run(["yamllint", filepath], capture_output=True, text=True)
    if result.stdout:
        print(f"❌ Issues found in {filepath}:\n{result.stdout}")
    else:
        print(f"✅ Clean: {filepath}")


def main():
    print(f"📂 Scanning all YAML files...\n")
    for filepath in find_yaml_files():
        clean_yaml_file(filepath)
        lint_yaml_file(filepath)


if __name__ == "__main__":
    main()
