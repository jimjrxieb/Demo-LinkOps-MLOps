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
Script to verify that UP006 errors have been fixed.
"""

import subprocess  # nosec B404
import sys
from pathlib import Path


def main():
    """Verify UP006 fixes"""
    print("🔍 Verifying UP006 fixes in DEMO-LinkOps...")

    try:
        # Run ruff check for UP006 errors
        result = subprocess.run(
            sanitize_cmd(["ruff", "check", ".", "--select", "UP006", "--output-format=text"]),
            capture_output=True,
            text=True,
            cwd=Path("."),
        )

        if result.returncode == 0:
            print("✅ No UP006 errors found!")
            return 0
        else:
            print("❌ UP006 errors found:")
            print(result.stdout)
            return 1

    except Exception as e:
        print(f"❌ Error running ruff: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
