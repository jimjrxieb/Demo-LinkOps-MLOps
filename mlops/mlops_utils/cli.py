#!/usr/bin/env python3
"""
CLI wrapper for MLOps utilities using Google Fire.
"""

import fire

from tools import (convert_csv_to_json, extract_metadata, format_yaml,
                   run_pipeline)


def main():
    """Main CLI entry point."""
    fire.Fire(
        {
            "format_yaml": format_yaml.main,
            "convert_csv": convert_csv_to_json.main,
            "extract_metadata": extract_metadata.main,
            "run_pipeline": run_pipeline.main,
        }
    )


if __name__ == "__main__":
    main()
