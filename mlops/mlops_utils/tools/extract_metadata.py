#!/usr/bin/env python3
"""
Metadata extraction tool for Git, Dockerfile, and repository insights.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


def get_git_metadata(repo_path: str = ".") -> Dict[str, Any]:
    """
    Extract Git metadata from repository.

    Args:
        repo_path: Path to Git repository

    Returns:
        Dictionary containing Git metadata
    """
    metadata = {}
    repo_path = Path(repo_path)

    try:
        # Check if it's a Git repository
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {"error": "Not a Git repository"}

        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        metadata["branch"] = result.stdout.strip()

        # Get latest commit
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%H|%an|%ae|%ad|%s"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            commit_hash, author, email, date, message = result.stdout.split("|")
            metadata["latest_commit"] = {
                "hash": commit_hash,
                "author": author,
                "email": email,
                "date": date,
                "message": message,
            }

        # Get remote URL
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            metadata["remote_url"] = result.stdout.strip()

        # Get file count
        result = subprocess.run(
            ["git", "ls-files"], cwd=repo_path, capture_output=True, text=True
        )
        if result.returncode == 0:
            files = result.stdout.strip().split("\n")
            metadata["file_count"] = len([f for f in files if f])

        return metadata

    except Exception as e:
        return {"error": f"Failed to extract Git metadata: {e}"}


def extract_dockerfile_metadata(dockerfile_path: str) -> Dict[str, Any]:
    """
    Extract metadata from Dockerfile.

    Args:
        dockerfile_path: Path to Dockerfile

    Returns:
        Dictionary containing Dockerfile metadata
    """
    metadata = {}
    dockerfile_path = Path(dockerfile_path)

    if not dockerfile_path.exists():
        return {"error": f"Dockerfile {dockerfile_path} does not exist"}

    try:
        with open(dockerfile_path, "r") as f:
            content = f.read()

        # Extract base image
        base_match = re.search(r"FROM\s+([^\s]+)", content, re.IGNORECASE)
        if base_match:
            metadata["base_image"] = base_match.group(1)

        # Extract exposed ports
        ports = re.findall(r"EXPOSE\s+(\d+)", content, re.IGNORECASE)
        metadata["exposed_ports"] = [int(p) for p in ports]

        # Extract environment variables
        env_vars = re.findall(r"ENV\s+([^\s]+)\s+(.+)", content, re.IGNORECASE)
        metadata["environment_variables"] = {var: value for var, value in env_vars}

        # Extract labels
        labels = re.findall(r"LABEL\s+(.+)", content, re.IGNORECASE)
        metadata["labels"] = labels

        # Count lines
        metadata["line_count"] = len(content.splitlines())

        # Check for common patterns
        metadata["has_healthcheck"] = "HEALTHCHECK" in content.upper()
        metadata["has_volume"] = "VOLUME" in content.upper()
        metadata["has_user"] = "USER" in content.upper()

        return metadata

    except Exception as e:
        return {"error": f"Failed to extract Dockerfile metadata: {e}"}


def extract_repo_insights(repo_path: str = ".") -> Dict[str, Any]:
    """
    Extract general repository insights.

    Args:
        repo_path: Path to repository

    Returns:
        Dictionary containing repository insights
    """
    insights = {}
    repo_path = Path(repo_path)

    try:
        # Count files by extension
        extensions = {}
        for file_path in repo_path.rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                extensions[ext] = extensions.get(ext, 0) + 1

        insights["file_extensions"] = dict(
            sorted(extensions.items(), key=lambda x: x[1], reverse=True)
        )

        # Look for common config files
        config_files = [
            "docker-compose.yml",
            "docker-compose.yaml",
            "requirements.txt",
            "package.json",
            "Cargo.toml",
            "go.mod",
            "pom.xml",
            "build.gradle",
            "Makefile",
            "README.md",
            "LICENSE",
        ]

        found_configs = []
        for config in config_files:
            if (repo_path / config).exists():
                found_configs.append(config)

        insights["config_files"] = found_configs

        # Check for Docker files
        docker_files = list(repo_path.glob("Dockerfile*"))
        insights["docker_files"] = [str(f.name) for f in docker_files]

        # Check for Helm charts
        helm_charts = list(repo_path.rglob("Chart.yaml"))
        insights["helm_charts"] = [str(f.parent.name) for f in helm_charts]

        return insights

    except Exception as e:
        return {"error": f"Failed to extract repository insights: {e}"}


def main():
    """CLI entry point for metadata extraction tool."""
    parser = argparse.ArgumentParser(description="Extract metadata from repositories")
    parser.add_argument("path", nargs="?", default=".", help="Repository path")
    parser.add_argument("--git", action="store_true", help="Extract Git metadata")
    parser.add_argument("--dockerfile", help="Path to Dockerfile to analyze")
    parser.add_argument(
        "--insights", action="store_true", help="Extract repository insights"
    )
    parser.add_argument("--output", "-o", help="Output file for JSON results")
    parser.add_argument("--all", "-a", action="store_true", help="Extract all metadata")

    args = parser.parse_args()

    results = {}

    if args.all or args.git:
        results["git"] = get_git_metadata(args.path)

    if args.dockerfile:
        results["dockerfile"] = extract_dockerfile_metadata(args.dockerfile)

    if args.all or args.insights:
        results["insights"] = extract_repo_insights(args.path)

    # If no specific options, extract all
    if not any([args.git, args.dockerfile, args.insights]):
        results["git"] = get_git_metadata(args.path)
        results["insights"] = extract_repo_insights(args.path)

    # Output results
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"✅ Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2))

    # Check for errors
    has_errors = any(
        "error" in section for section in results.values() if isinstance(section, dict)
    )
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
