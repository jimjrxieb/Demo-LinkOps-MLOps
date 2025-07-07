#!/usr/bin/env python3
"""
Validate Refactor Script
Checks for any remaining references to deleted folders and ensures the refactor is complete.
"""

import re
import sys
from pathlib import Path


def check_for_deleted_references():
    """Check for references to deleted shadow/whis folders."""
    project_root = Path(__file__).parent.parent
    deleted_patterns = [
        r"shadows/whis_",
        r"\./shadows/whis_",
        r"\.\./shadows/whis_",
        r"LinkOps-MLOps/shadows/whis_",
    ]

    issues = []

    # Check Python files
    for py_file in project_root.rglob("*.py"):
        if "node_modules" in str(py_file) or ".git" in str(py_file):
            continue

        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                for pattern in deleted_patterns:
                    if re.search(pattern, content):
                        issues.append(
                            f"Python file {py_file} contains reference to deleted path: {pattern}"
                        )
        except Exception as e:
            print(f"Warning: Could not read {py_file}: {e}")

    # Check YAML files
    for yaml_file in project_root.rglob("*.yml"):
        if "node_modules" in str(yaml_file) or ".git" in str(yaml_file):
            continue

        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                content = f.read()
                for pattern in deleted_patterns:
                    if re.search(pattern, content):
                        issues.append(
                            f"YAML file {yaml_file} contains reference to deleted path: {pattern}"
                        )
        except Exception as e:
            print(f"Warning: Could not read {yaml_file}: {e}")

    # Check YAML files
    for yaml_file in project_root.rglob("*.yaml"):
        if "node_modules" in str(yaml_file) or ".git" in str(yaml_file):
            continue

        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                content = f.read()
                for pattern in deleted_patterns:
                    if re.search(pattern, content):
                        issues.append(
                            f"YAML file {yaml_file} contains reference to deleted path: {pattern}"
                        )
        except Exception as e:
            print(f"Warning: Could not read {yaml_file}: {e}")

    return issues


def check_folder_structure():
    """Check that the folder structure is correct."""
    project_root = Path(__file__).parent.parent

    expected_folders = [
        "mlops/whis_data_input",
        "mlops/whis_sanitize",
        "mlops/whis_smithing",
        "mlops/whis_enhance",
        "mlops/whis_logic",
        "mlops/whis_webscraper",
        "mlops/mlops_utils",
        "shadows/igris_logic",
        "shadows/katie_logic",
        "shadows/auditguard_logic",
        "shadows/ficknury_evaluator",
        "frontend/src/pages",
        "frontend/src/components",
        "backend/core/api",
        "backend/core",
        "scripts/audit",
        "scripts/devops",
        "scripts/sandbox",
        "reports/audit",
        "helm",
        "infrastructure/k8s",
        "infrastructure/terraform",
        ".github/workflows",
    ]

    missing_folders = []
    for folder in expected_folders:
        if not (project_root / folder).exists():
            missing_folders.append(folder)

    return missing_folders


def check_deleted_folders():
    """Check that deleted folders are actually gone."""
    project_root = Path(__file__).parent.parent

    deleted_folders = [
        "shadows/whis_data_input",
        "shadows/whis_sanitize",
        "shadows/whis_smithing",
        "shadows/whis_enhance",
        "shadows/whis_logic",
        "shadows/whis_webscraper",
        "shadows/whis_kubeflow",
    ]

    still_exist = []
    for folder in deleted_folders:
        if (project_root / folder).exists():
            still_exist.append(folder)

    return still_exist


def main():
    print("🔍 Validating LinkOps-MLOps refactor...")
    print("=" * 50)

    # Check for references to deleted folders
    print("\n1. Checking for references to deleted folders...")
    issues = check_for_deleted_references()
    if issues:
        print("❌ Found issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ No references to deleted folders found")

    # Check folder structure
    print("\n2. Checking folder structure...")
    missing_folders = check_folder_structure()
    if missing_folders:
        print("❌ Missing expected folders:")
        for folder in missing_folders:
            print(f"   - {folder}")
    else:
        print("✅ All expected folders exist")

    # Check that deleted folders are gone
    print("\n3. Checking that deleted folders are gone...")
    still_exist = check_deleted_folders()
    if still_exist:
        print("❌ Deleted folders still exist:")
        for folder in still_exist:
            print(f"   - {folder}")
    else:
        print("✅ All deleted folders have been removed")

    # Summary
    print("\n" + "=" * 50)
    if not issues and not missing_folders and not still_exist:
        print("🎉 Refactor validation PASSED! Your LinkOps-MLOps structure is clean.")
        return 0
    else:
        print("⚠️  Refactor validation found issues. Please review and fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
