#!/usr/bin/env python3
"""
GitHub Actions Pipeline Rune
Generates CI/CD workflows for Python microservices
"""

import yaml
import os
from typing import Dict


class GHAPipelineRune:
    """Generates GitHub Actions workflows for microservices."""

    def __init__(self, service_name: str, python_version: str = "3.11"):
        self.service_name = service_name
        self.python_version = python_version

    def generate_workflow(self) -> Dict:
        """Generate a complete GitHub Actions workflow."""
        return {
            "name": f"{self.service_name.title()} CI/CD",
            "on": {
                "push": {
                    "branches": ["main", "develop"],
                    "paths": [f"mlops/{self.service_name}/**"],
                },
                "pull_request": {
                    "branches": ["main"],
                    "paths": [f"mlops/{self.service_name}/**"],
                },
            },
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"name": "Checkout code", "uses": "actions/checkout@v4"},
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v4",
                            "with": {"python-version": self.python_version},
                        },
                        {
                            "name": "Install dependencies",
                            "run": f"cd mlops/{self.service_name} && pip install -r requirements.txt",
                        },
                        {
                            "name": "Run tests",
                            "run": f"cd mlops/{self.service_name} && python -m pytest tests/",
                        },
                        {
                            "name": "Lint code",
                            "run": f"cd mlops/{self.service_name} && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics",
                        },
                    ],
                },
                "build": {
                    "runs-on": "ubuntu-latest",
                    "needs": "test",
                    "if": "github.ref == 'refs/heads/main'",
                    "steps": [
                        {
                            "name": "Build Docker image",
                            "run": f"docker build -t linkops/{self.service_name}:latest mlops/{self.service_name}/",
                        },
                        {
                            "name": "Push to registry",
                            "run": f"docker push linkops/{self.service_name}:latest",
                        },
                    ],
                },
            },
        }

    def save_workflow(self, output_path: str = None):
        """Save the generated workflow to a file."""
        if output_path is None:
            output_path = f".github/workflows/{self.service_name}.yml"

        workflow = self.generate_workflow()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            yaml.dump(workflow, f, default_flow_style=False, sort_keys=False)

        print(f"✅ Generated workflow: {output_path}")


# Example usage
if __name__ == "__main__":
    rune = GHAPipelineRune("whis_data_input")
    rune.save_workflow()
