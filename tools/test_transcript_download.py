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
Test direct transcript download from YouTube (no API call).
"""
from services.whis_data_input.utils.youtube_transcript import download_transcript

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
transcript = download_transcript(url)

if transcript:
    print("✅ Transcript Downloaded:\n")
    print(transcript[:300] + "...")
else:
    print("❌ No transcript found.")
