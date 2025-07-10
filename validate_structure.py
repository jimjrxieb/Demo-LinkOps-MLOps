def sanitize_cmd(cmd):
    import shlex

    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {
        "ls",
        "echo",
        "kubectl",
        "helm",
        "python3",
        "cat",
        "go",
        "docker",
        "npm",
        "black",
        "ruff",
        "yamllint",
        "prettier",
        "flake8",
    }
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd


#!/usr/bin/env python3
"""
Validate LinkOps Platform Structure
Checks that all required directories exist and reports any missing ones.
"""

import os


def validate_platform_structure():
    """Validate that all required directories exist."""

    # Required directories from the workflow
    required_dirs = [
        "mlops/audit_assess",
        "mlops/whis_enhance",
        "mlops/whis_data_input",
        "mlops/whis_webscraper",
        "mlops/whis_logic",
        "mlops/whis_smithing",
        "mlops/whis_sanitize",
        "mlops/mlops_utils",
        "mlops/mlops_platform",
        "mlops/audit_migrate",
        "shadows/kubernetes_specialist",
        "shadows/ml_data_scientist",
        "shadows/devops_engineer",
        "shadows/platform_engineer",
        "shadows/jimmie_logic",
        "shadows/ficknury_evaluator",
        "shadows/auditguard_logic",
        "shadows/audit_logic",
        "shadows/db",
        "frontend/src/pages",
        "frontend/src/components",
        "frontend/src/views",
        "frontend/src/stores",
        "frontend/src/router",
        "frontend/src/services",
        "frontend/src/assets",
        "scripts/audit",
        "scripts/devops",
        "scripts/sandbox",
        "scripts/ci",
        "helm/linkops",
        "helm/argocd",
        ".github/workflows",
    ]

    # Directories that should NOT exist
    deleted_dirs = [
        "shadows/whis_data_input",
        "shadows/whis_sanitize",
        "shadows/whis_smithing",
        "shadows/whis_enhance",
        "shadows/whis_logic",
        "shadows/whis_webscraper",
        "shadows/whis_kubeflow",
        "backend/routes",
        "mlops/old_service",
        "frontend/old_pages",
        "scripts/old_script",
        "helm/old_chart",
    ]

    print("🔍 Validating LinkOps platform structure...")
    print()

    # Check required directories
    missing_dirs = []
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ Found: {dir_path}")
        else:
            print(f"❌ Missing required directory: {dir_path}")
            missing_dirs.append(dir_path)

    print()

    # Check for deleted directories that shouldn't exist
    existing_deleted_dirs = []
    for dir_path in deleted_dirs:
        if os.path.isdir(dir_path):
            print(f"❌ Deleted directory still exists: {dir_path}")
            existing_deleted_dirs.append(dir_path)
        else:
            print(f"✅ Correctly deleted: {dir_path}")

    print()

    # Summary
    if not missing_dirs and not existing_deleted_dirs:
        print("🎉 Platform structure validation passed!")
        return True
    else:
        print("❌ Platform structure validation failed!")
        if missing_dirs:
            print(f"Missing directories: {len(missing_dirs)}")
        if existing_deleted_dirs:
            print(f"Unexpected directories: {len(existing_deleted_dirs)}")
        return False


if __name__ == "__main__":
    success = validate_platform_structure()
    exit(0 if success else 1)
