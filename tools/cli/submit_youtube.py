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
Submit a YouTube URL and topic to the whis_data_input API for transcript processing.
"""
import argparse

import requests


def main():
    parser = argparse.ArgumentParser(
        description="Submit YouTube URL for transcript processing."
    )
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--topic", required=True, help="Topic for the transcript")
    parser.add_argument(
        "--api",
        default="http://localhost:8001/api/input/youtube-transcript",
        help="Data input API endpoint",
    )
    args = parser.parse_args()

    payload = {"url": args.url, "topic": args.topic}
    try:
        resp = requests.post(args.api, json=payload, timeout=30)
        print(f"Status: {resp.status_code}")
        print(resp.json())
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
