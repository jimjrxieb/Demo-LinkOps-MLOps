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
Auto-fix Helm chart structure issues:
- Ensures Chart.yaml has required fields (name, version, description)
- Adds missing fields: appVersion, type, maintainers
- Validates basic values.yaml structure
"""

from pathlib import Path

import yaml


def ensure_chart_yaml(chart_path: Path):
    default_chart = {
        "apiVersion": "v2",
        "name": "linkops",
        "description": "AI-driven DevSecOps platform",
        "version": "1.0.0",
        "appVersion": "1.0.0",
        "type": "application",
        "maintainers": [{"name": "jimjrxieb"}],
    }

    chart_file = chart_path / "Chart.yaml"
    if not chart_file.exists():
        print(f"🚨 Chart.yaml not found at {chart_file}, creating default.")
        chart_file.write_text(yaml.dump(default_chart, sort_keys=False))
        return

    with open(chart_file, encoding="utf-8") as f:
        content = yaml.safe_load(f)

    modified = False
    for key, value in default_chart.items():
        if key not in content:
            content[key] = value
            print(f"➕ Added missing key '{key}' to Chart.yaml")
            modified = True

    if modified:
        with open(chart_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(content, f, sort_keys=False)
        print("✅ Chart.yaml updated.")
    else:
        print("✔️ Chart.yaml already valid.")


def validate_values_yaml(chart_path: Path):
    values_file = chart_path / "values.yaml"
    if not values_file.exists():
        print(f"⚠️ values.yaml not found at {values_file}")
        return

    try:
        yaml.safe_load(values_file.read_text(encoding="utf-8"))
        print("✔️ values.yaml syntax valid.")
    except yaml.YAMLError as e:
        print("🚨 values.yaml has YAML syntax errors:", e)


def main():
    chart_path = Path("helm/linkops")
    if not chart_path.exists():
        print("❌ Chart path 'helm/linkops' not found.")
        return

    ensure_chart_yaml(chart_path)
    validate_values_yaml(chart_path)


if __name__ == "__main__":
    main()
