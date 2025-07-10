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
Test the /manual API using a mock JSON payload.
"""
import json

import requests

with open("tools/mocks/sample_task.json") as f:
    payload = json.load(f)

r = requests.post("http://localhost:8000/api/input/manual", json=payload, timeout=30)
print("✅ Manual task upload test complete")
print("Status Code:", r.status_code)
print("Response:", r.json())
