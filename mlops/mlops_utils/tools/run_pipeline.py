#!/usr/bin/env python3
"""
Manual execution pipeline helper for MLOps utilities.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class PipelineRunner:
    """Pipeline execution helper."""

    def __init__(self, pipeline_config: Dict[str, Any]):
        self.config = pipeline_config
        self.results = {}
        self.start_time = None
        self.end_time = None

    def run_step(self, step_name: str, step_config: Dict[str, Any]) -> bool:
        """
        Execute a single pipeline step.

        Args:
            step_name: Name of the step
            step_config: Step configuration

        Returns:
            True if successful, False otherwise
        """
        print(f"🔄 Running step: {step_name}")

        step_type = step_config.get("type", "command")

        try:
            if step_type == "command":
                return self._run_command_step(step_name, step_config)
            elif step_type == "script":
                return self._run_script_step(step_name, step_config)
            elif step_type == "validation":
                return self._run_validation_step(step_name, step_config)
            else:
                print(f"❌ Unknown step type: {step_type}")
                return False

        except Exception as e:
            print(f"❌ Error in step {step_name}: {e}")
            return False

    def _run_command_step(self, step_name: str, step_config: Dict[str, Any]) -> bool:
        """Execute a command step."""
        command = step_config["command"]
        cwd = step_config.get("cwd", ".")
        timeout = step_config.get("timeout", 300)

        print(f"   Command: {command}")
        print(f"   Working directory: {cwd}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            self.results[step_name] = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }

            if result.returncode == 0:
                print(f"   ✅ Step {step_name} completed successfully")
                return True
            else:
                print(
                    f"   ❌ Step {step_name} failed with return code {result.returncode}"
                )
                if result.stderr:
                    print(f"   Error: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"   ❌ Step {step_name} timed out after {timeout} seconds")
            return False

    def _run_script_step(self, step_name: str, step_config: Dict[str, Any]) -> bool:
        """Execute a script step."""
        script_path = step_config["script"]
        args = step_config.get("args", [])

        print(f"   Script: {script_path}")
        print(f"   Args: {args}")

        try:
            result = subprocess.run(
                [sys.executable, script_path] + args, capture_output=True, text=True
            )

            self.results[step_name] = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }

            if result.returncode == 0:
                print(f"   ✅ Step {step_name} completed successfully")
                return True
            else:
                print(
                    f"   ❌ Step {step_name} failed with return code {result.returncode}"
                )
                if result.stderr:
                    print(f"   Error: {result.stderr}")
                return False

        except Exception as e:
            print(f"   ❌ Error running script {script_path}: {e}")
            return False

    def _run_validation_step(self, step_name: str, step_config: Dict[str, Any]) -> bool:
        """Execute a validation step."""
        validation_type = step_config["validation_type"]

        print(f"   Validation type: {validation_type}")

        try:
            if validation_type == "file_exists":
                file_path = step_config["file_path"]
                exists = Path(file_path).exists()
                self.results[step_name] = {"success": exists}

                if exists:
                    print(f"   ✅ File {file_path} exists")
                    return True
                else:
                    print(f"   ❌ File {file_path} does not exist")
                    return False

            elif validation_type == "json_valid":
                file_path = step_config["file_path"]
                with open(file_path, "r") as f:
                    json.load(f)  # This will raise an exception if invalid
                self.results[step_name] = {"success": True}
                print(f"   ✅ JSON file {file_path} is valid")
                return True

            else:
                print(f"   ❌ Unknown validation type: {validation_type}")
                return False

        except Exception as e:
            print(f"   ❌ Validation failed: {e}")
            return False

    def run_pipeline(self) -> bool:
        """
        Execute the entire pipeline.

        Returns:
            True if all steps succeeded, False otherwise
        """
        self.start_time = datetime.now()
        print(f"🚀 Starting pipeline: {self.config.get('name', 'Unnamed Pipeline')}")
        print(f"📅 Started at: {self.start_time}")

        steps = self.config.get("steps", [])
        if not steps:
            print("❌ No steps defined in pipeline")
            return False

        success_count = 0
        for step_config in steps:
            step_name = step_config["name"]

            # Check dependencies
            dependencies = step_config.get("depends_on", [])
            for dep in dependencies:
                if dep not in self.results or not self.results[dep].get(
                    "success", False
                ):
                    print(f"❌ Step {step_name} depends on {dep} which failed")
                    return False

            # Run the step
            if self.run_step(step_name, step_config):
                success_count += 1
            else:
                if step_config.get("required", True):
                    print(f"❌ Required step {step_name} failed, stopping pipeline")
                    break

        self.end_time = datetime.now()
        duration = self.end_time - self.start_time

        print(f"\n📊 Pipeline Summary:")
        print(f"   Steps completed: {success_count}/{len(steps)}")
        print(f"   Duration: {duration}")
        print(f"   Success: {success_count == len(steps)}")

        return success_count == len(steps)


def load_pipeline_config(config_path: str) -> Dict[str, Any]:
    """Load pipeline configuration from file."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading pipeline config: {e}")
        sys.exit(1)


def main():
    """CLI entry point for pipeline runner."""
    parser = argparse.ArgumentParser(description="Run MLOps pipelines")
    parser.add_argument("config", help="Pipeline configuration file (JSON)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show pipeline without executing"
    )
    parser.add_argument("--output", "-o", help="Output results to file")

    args = parser.parse_args()

    # Load configuration
    config = load_pipeline_config(args.config)

    if args.dry_run:
        print("🔍 Pipeline Configuration:")
        print(json.dumps(config, indent=2))
        return

    # Run pipeline
    runner = PipelineRunner(config)
    success = runner.run_pipeline()

    # Save results if requested
    if args.output:
        results = {
            "pipeline": config.get("name", "Unnamed Pipeline"),
            "start_time": runner.start_time.isoformat() if runner.start_time else None,
            "end_time": runner.end_time.isoformat() if runner.end_time else None,
            "success": success,
            "step_results": runner.results,
        }

        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"📄 Results saved to {args.output}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
