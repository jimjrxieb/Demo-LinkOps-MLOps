#!/usr/bin/env python3
"""
CSV to JSON conversion tool for MLOps utilities.
"""

import csv
import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any


def csv_to_json(
    csv_path: str, json_path: Optional[str] = None, format_type: str = "list"
) -> bool:
    """
    Convert CSV file to JSON format.

    Args:
        csv_path: Path to input CSV file
        json_path: Path to output JSON file (optional)
        format_type: Output format - "list" or "dict"

    Returns:
        True if successful, False otherwise
    """
    try:
        csv_path = Path(csv_path)

        if not csv_path.exists():
            print(f"Error: CSV file {csv_path} does not exist")
            return False

        # Determine output path
        if json_path is None:
            json_path = csv_path.with_suffix(".json")
        else:
            json_path = Path(json_path)

        # Read CSV
        with open(csv_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        # Convert to desired format
        if format_type == "list":
            output_data = rows
        elif format_type == "dict":
            # Use first column as key
            if not rows:
                output_data = {}
            else:
                first_col = list(rows[0].keys())[0]
                output_data = {row[first_col]: row for row in rows}
        else:
            print(f"Error: Unknown format type '{format_type}'")
            return False

        # Write JSON
        with open(json_path, "w", encoding="utf-8") as jsonfile:
            json.dump(output_data, jsonfile, indent=2, ensure_ascii=False)

        print(f"✅ Converted {csv_path} to {json_path}")
        print(f"   Format: {format_type}")
        print(f"   Records: {len(rows)}")
        return True

    except Exception as e:
        print(f"Error converting {csv_path}: {e}")
        return False


def json_to_csv(json_path: str, csv_path: Optional[str] = None) -> bool:
    """
    Convert JSON file to CSV format.

    Args:
        json_path: Path to input JSON file
        csv_path: Path to output CSV file (optional)

    Returns:
        True if successful, False otherwise
    """
    try:
        json_path = Path(json_path)

        if not json_path.exists():
            print(f"Error: JSON file {json_path} does not exist")
            return False

        # Determine output path
        if csv_path is None:
            csv_path = json_path.with_suffix(".csv")
        else:
            csv_path = Path(csv_path)

        # Read JSON
        with open(json_path, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)

        # Handle different JSON structures
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            # Convert dict to list of dicts
            rows = list(data.values())
        else:
            print(f"Error: Unsupported JSON structure")
            return False

        if not rows:
            print(f"Error: No data found in {json_path}")
            return False

        # Write CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = rows[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"✅ Converted {json_path} to {csv_path}")
        print(f"   Records: {len(rows)}")
        return True

    except Exception as e:
        print(f"Error converting {json_path}: {e}")
        return False


def main():
    """CLI entry point for CSV/JSON conversion tool."""
    parser = argparse.ArgumentParser(description="Convert between CSV and JSON formats")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    parser.add_argument(
        "--format",
        "-f",
        choices=["list", "dict"],
        default="list",
        help="JSON output format (for CSV->JSON)",
    )
    parser.add_argument(
        "--reverse", "-r", action="store_true", help="Convert JSON to CSV instead"
    )

    args = parser.parse_args()

    input_path = Path(args.input_file)

    if not input_path.exists():
        print(f"Error: Input file {input_path} does not exist")
        sys.exit(1)

    if args.reverse:
        success = json_to_csv(str(input_path), args.output)
    else:
        success = csv_to_json(str(input_path), args.output, args.format)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
