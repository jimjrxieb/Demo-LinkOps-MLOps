#!/usr/bin/env python3
"""
YAML formatting and validation tool for MLOps utilities.
"""

import argparse
import sys
from pathlib import Path

import yaml


def format_yaml_file(file_path: str, validate_only: bool = False) -> bool:
    """
    Format and optionally validate a YAML file.

    Args:
        file_path: Path to the YAML file
        validate_only: If True, only validate without formatting

    Returns:
        True if successful, False otherwise
    """
    try:
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"Error: File {file_path} does not exist")
            return False

        # Read the file
        with open(file_path, "r") as f:
            content = f.read()

        # Parse YAML to validate
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML in {file_path}: {e}")
            return False

        if validate_only:
            print(f"✅ {file_path} is valid YAML")
            return True

        # Format the YAML
        formatted_content = yaml.dump(
            data, default_flow_style=False, sort_keys=False, indent=2
        )

        # Write back to file
        with open(file_path, "w") as f:
            f.write(formatted_content)

        print(f"✅ Formatted {file_path}")
        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """CLI entry point for YAML formatting tool."""
    parser = argparse.ArgumentParser(description="Format and validate YAML files")
    parser.add_argument("path", help="Path to YAML file or directory")
    parser.add_argument(
        "--validate-only", action="store_true", help="Only validate, don't format"
    )
    parser.add_argument(
        "--recursive", "-r", action="store_true", help="Process directories recursively"
    )

    args = parser.parse_args()

    path = Path(args.path)

    if path.is_file():
        success = format_yaml_file(str(path), args.validate_only)
        sys.exit(0 if success else 1)

    elif path.is_dir():
        yaml_files = []
        if args.recursive:
            yaml_files = list(path.rglob("*.yaml")) + list(path.rglob("*.yml"))
        else:
            yaml_files = list(path.glob("*.yaml")) + list(path.glob("*.yml"))

        if not yaml_files:
            print(f"No YAML files found in {path}")
            sys.exit(1)

        success_count = 0
        for yaml_file in yaml_files:
            if format_yaml_file(str(yaml_file), args.validate_only):
                success_count += 1

        print(f"\nProcessed {success_count}/{len(yaml_files)} files successfully")
        sys.exit(0 if success_count == len(yaml_files) else 1)

    else:
        print(f"Error: {path} does not exist")
        sys.exit(1)


if __name__ == "__main__":
    main()
