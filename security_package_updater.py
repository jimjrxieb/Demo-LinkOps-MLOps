#!/usr/bin/env python3
"""
LinkOps-MLOps Security Package Updater
Systematically updates vulnerable packages across all microservices
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# High-priority security fixes
SECURITY_FIXES = {
    "protobuf": ">=4.25.8",
    "zipp": ">=3.19.1",
    "requests": ">=2.32.4",
    "urllib3": ">=2.5.0",
    # Additional security updates
    "fastapi": ">=0.109.1",
    "uvicorn": ">=0.29.0",
    "httpx": ">=0.27.0",
    "pydantic": ">=2.7.1",
    "anyio": ">=4.4.0",
    "pillow": ">=11.2.1",
    "python-multipart": ">=0.0.19",
    "pytesseract": ">=0.3.13",
    "bandit": ">=1.7.5",
    "safety": ">=2.3.5",
}

# JavaScript dependency updates
JS_SECURITY_FIXES = {
    "axios": "^1.7.4",
    "vite": "^5.4.8",
    "@vitejs/plugin-vue": "^5.1.4",
    "vue": "^3.5.10",
    "vue-router": "^4.4.5",
    "pinia": "^3.0.4",
    "tailwindcss": "^4.1.11",
    "postcss": "^8.4.47",
    "autoprefixer": "^10.4.20",
    "eslint": "^9.30.1",
    "typescript": "^5.6.2",
}


def find_all_dependency_files() -> Dict[str, List[str]]:
    """Find all dependency files in the project"""
    files = {"requirements": [], "package_json": [], "pyproject": []}

    # Known paths from exploration
    requirements_files = [
        "./mlops/whis_smithing/requirements.txt",
        "./mlops/mlops_utils/requirements.txt",
        "./mlops/whis_sanitize/requirements.txt",
        "./mlops/whis_logic/requirements.txt",
        "./mlops/whis_webscraper/requirements.txt",
        "./mlops/audit_assess/requirements.txt",
        "./mlops/whis_enhance/requirements.txt",
        "./mlops/whis_data_input/requirements.txt",
        "./mlops/mlops_platform/requirements.txt",
        "./mlops/audit_migrate/requirements.txt",
        "./shadows/jimmie_logic/requirements.txt",
        "./shadows/devops_engineer/requirements.txt",
        "./shadows/platform_engineer/requirements.txt",
        "./shadows/audit_logic/requirements.txt",
        "./shadows/ficknury_evaluator/requirements.txt",
        "./shadows/ml_data_scientist/requirements.txt",
        "./shadows/kubernetes_specialist/requirements.txt",
    ]

    # Verify files exist
    for file_path in requirements_files:
        if os.path.exists(file_path):
            files["requirements"].append(file_path)

    # Check for package.json and pyproject.toml
    if os.path.exists("./frontend/package.json"):
        files["package_json"].append("./frontend/package.json")
    if os.path.exists("./pyproject.toml"):
        files["pyproject"].append("./pyproject.toml")

    return files


def update_requirements_file(file_path: str) -> Tuple[bool, List[str]]:
    """Update a requirements.txt file with security fixes"""
    print(f"\n📝 Updating {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False, []

    changes = []

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        updated_lines = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                updated_lines.append(line)
                continue

            # Parse package name and version
            if "==" in line:
                package_name = line.split("==")[0].strip()
                if package_name in SECURITY_FIXES:
                    new_line = f"{package_name}{SECURITY_FIXES[package_name]}"
                    updated_lines.append(new_line)
                    changes.append(f"  ✅ {package_name}: {line} → {new_line}")
                else:
                    updated_lines.append(line)
            elif ">=" in line:
                package_name = line.split(">=")[0].strip()
                if package_name in SECURITY_FIXES:
                    # Check if current version is sufficient
                    current_version = line.split(">=")[1].strip()
                    required_version = SECURITY_FIXES[package_name].replace(">=", "")
                    if current_version < required_version:
                        new_line = f"{package_name}{SECURITY_FIXES[package_name]}"
                        updated_lines.append(new_line)
                        changes.append(f"  ✅ {package_name}: {line} → {new_line}")
                    else:
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
            else:
                # Handle packages without version specifier
                package_name = line.strip()
                if package_name in SECURITY_FIXES:
                    new_line = f"{package_name}{SECURITY_FIXES[package_name]}"
                    updated_lines.append(new_line)
                    changes.append(f"  ✅ {package_name}: {line} → {new_line}")
                else:
                    updated_lines.append(line)

        # Write updated file
        with open(file_path, "w") as f:
            for line in updated_lines:
                f.write(line + "\n")

        if changes:
            print(f"  📦 Updated {len(changes)} packages:")
            for change in changes:
                print(change)
        else:
            print("  ✅ No security updates needed")

        return True, changes

    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False, []


def update_package_json(file_path: str) -> Tuple[bool, List[str]]:
    """Update package.json with security fixes"""
    print(f"\n📝 Updating {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False, []

    changes = []

    try:
        with open(file_path, "r") as f:
            package_data = json.load(f)

        # Update dependencies
        for dep_type in ["dependencies", "devDependencies"]:
            if dep_type in package_data:
                for package_name, current_version in package_data[dep_type].items():
                    if package_name in JS_SECURITY_FIXES:
                        new_version = JS_SECURITY_FIXES[package_name]
                        if current_version != new_version:
                            package_data[dep_type][package_name] = new_version
                            changes.append(
                                f"  ✅ {package_name}: {current_version} → {new_version}"
                            )

        # Write updated file
        with open(file_path, "w") as f:
            json.dump(package_data, f, indent=2)

        if changes:
            print(f"  📦 Updated {len(changes)} packages:")
            for change in changes:
                print(change)
        else:
            print("  ✅ No security updates needed")

        return True, changes

    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False, []


def test_docker_build(service_path: str) -> bool:
    """Test Docker build for a service"""
    dockerfile_path = os.path.join(service_path, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        return True  # Skip if no Dockerfile

    print(f"🐳 Testing Docker build for {service_path}")

    try:
        result = subprocess.run(
            ["docker", "build", "-t", f"test-{os.path.basename(service_path)}", "."],
            cwd=service_path,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            print(f"  ✅ Docker build successful")
            return True
        else:
            print(f"  ❌ Docker build failed:")
            print(f"  {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"  ⏰ Docker build timed out")
        return False
    except Exception as e:
        print(f"  ❌ Error testing Docker build: {str(e)}")
        return False


def lint_and_format_files(file_paths: List[str]):
    """Lint and format updated files"""
    print(f"\n🎨 Linting and formatting updated files...")

    python_files = [f for f in file_paths if f.endswith(".py")]
    if python_files:
        # Run black
        try:
            subprocess.run(["black"] + python_files, check=True)
            print("  ✅ Python files formatted with black")
        except subprocess.CalledProcessError:
            print("  ⚠️ Black formatting had issues")
        except FileNotFoundError:
            print("  ⚠️ Black not installed, skipping Python formatting")

    # Check for JavaScript files
    js_files = [f for f in file_paths if f.endswith((".js", ".json", ".vue", ".ts"))]
    if js_files:
        frontend_dir = "./frontend"
        if os.path.exists(frontend_dir):
            try:
                subprocess.run(["npm", "run", "lint:fix"], cwd=frontend_dir, check=True)
                print("  ✅ JavaScript files linted")
            except subprocess.CalledProcessError:
                print("  ⚠️ JavaScript linting had issues")
            except FileNotFoundError:
                print("  ⚠️ npm not available, skipping JavaScript linting")


def main():
    """Main update function"""
    print("🔒 LinkOps-MLOps Security Package Updater")
    print("=" * 60)

    # Find all dependency files
    print("📁 Finding dependency files...")
    files = find_all_dependency_files()

    print(f"Found {len(files['requirements'])} requirements.txt files")
    print(f"Found {len(files['package_json'])} package.json files")
    print(f"Found {len(files['pyproject'])} pyproject.toml files")

    all_changes = []
    updated_files = []

    # Update requirements.txt files
    for req_file in files["requirements"]:
        success, changes = update_requirements_file(req_file)
        if success:
            updated_files.append(req_file)
            all_changes.extend(changes)

    # Update package.json files
    for pkg_file in files["package_json"]:
        success, changes = update_package_json(pkg_file)
        if success:
            updated_files.append(pkg_file)
            all_changes.extend(changes)

    # Test Docker builds for services with changes
    print(f"\n🧪 Testing Docker builds for updated services...")
    build_failures = []

    for req_file in files["requirements"]:
        if req_file in updated_files:
            service_path = os.path.dirname(req_file)
            if not test_docker_build(service_path):
                build_failures.append(service_path)

    # Lint and format
    lint_and_format_files(updated_files)

    # Summary
    print(f"\n📊 Update Summary")
    print("=" * 60)
    print(f"✅ Files updated: {len(updated_files)}")
    print(f"✅ Total package changes: {len(all_changes)}")

    if build_failures:
        print(f"❌ Docker build failures: {len(build_failures)}")
        for failure in build_failures:
            print(f"  - {failure}")
    else:
        print("✅ All Docker builds successful")

    print(f"\n🎉 Security updates completed!")

    # List changed files
    if updated_files:
        print(f"\n📝 Files changed:")
        for file_path in updated_files:
            print(f"  - {file_path}")


if __name__ == "__main__":
    main()
