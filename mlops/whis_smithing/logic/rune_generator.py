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


"""
Whis Rune Generator - Creates fixed solution paths (scripts, CI flows) from structured data.
"""

import re
import uuid
from datetime import datetime
from typing import Any, Dict, List


class RuneGenerator:
    """Generates Runes (fixed solution paths) from sanitized data."""

    def __init__(self):
        self.rune_templates = {
            "kubernetes": {
                "deploy": self._generate_k8s_deploy_rune,
                "scale": self._generate_k8s_scale_rune,
                "debug": self._generate_k8s_debug_rune,
                "backup": self._generate_k8s_backup_rune,
            },
            "docker": {
                "build": self._generate_docker_build_rune,
                "push": self._generate_docker_push_rune,
                "cleanup": self._generate_docker_cleanup_rune,
            },
            "mlops": {
                "train": self._generate_mlops_train_rune,
                "deploy": self._generate_mlops_deploy_rune,
                "monitor": self._generate_mlops_monitor_rune,
            },
            "security": {
                "scan": self._generate_security_scan_rune,
                "audit": self._generate_security_audit_rune,
                "compliance": self._generate_security_compliance_rune,
            },
        }

    def generate_rune(self, sanitized_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a Rune from sanitized data.

        Args:
            sanitized_data: Sanitized data from whis_sanitize

        Returns:
            Generated Rune data
        """
        try:
            rune_id = str(uuid.uuid4())
            content = sanitized_data.get("sanitized_content", "")
            tags = sanitized_data.get("tags", [])

            # Determine rune type
            rune_type = self._determine_rune_type(content, tags)

            # Generate rune using appropriate template
            rune_content = self._generate_rune_content(content, rune_type)

            # Create rune metadata
            rune_metadata = self._create_rune_metadata(sanitized_data, rune_type)

            # Calculate rune effectiveness score
            effectiveness_score = self._calculate_rune_effectiveness(
                rune_content, sanitized_data
            )

            rune_data = {
                "id": rune_id,
                "type": "rune",
                "rune_type": rune_type,
                "title": rune_metadata.get("title", f"Generated Rune {rune_id[:8]}"),
                "content": rune_content,
                "tags": tags + [rune_type, "generated"],
                "source_data_id": sanitized_data.get("id"),
                "effectiveness_score": effectiveness_score,
                "metadata": rune_metadata,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "generated",
                "version": "1.0.0",
                "usage_count": 0,
                "success_rate": 0.0,
            }

            return rune_data

        except Exception as e:
            return {
                "id": str(uuid.uuid4()),
                "type": "rune",
                "status": "generation_failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _determine_rune_type(self, content: str, tags: List[str]) -> str:
        """Determine the type of rune to generate."""
        content_lower = content.lower()

        # Check tags first
        for tag in tags:
            if tag in self.rune_templates:
                # Determine specific type within domain
                if tag == "kubernetes":
                    if any(
                        word in content_lower for word in ["deploy", "apply", "create"]
                    ):
                        return "kubernetes_deploy"
                    elif any(word in content_lower for word in ["scale", "replicas"]):
                        return "kubernetes_scale"
                    elif any(
                        word in content_lower for word in ["debug", "logs", "describe"]
                    ):
                        return "kubernetes_debug"
                    elif any(
                        word in content_lower for word in ["backup", "export", "save"]
                    ):
                        return "kubernetes_backup"
                elif tag == "docker":
                    if any(word in content_lower for word in ["build", "image"]):
                        return "docker_build"
                    elif any(word in content_lower for word in ["push", "registry"]):
                        return "docker_push"
                    elif any(
                        word in content_lower for word in ["clean", "prune", "remove"]
                    ):
                        return "docker_cleanup"
                elif tag == "mlops":
                    if any(
                        word in content_lower for word in ["train", "training", "model"]
                    ):
                        return "mlops_train"
                    elif any(
                        word in content_lower
                        for word in ["deploy", "serve", "inference"]
                    ):
                        return "mlops_deploy"
                    elif any(
                        word in content_lower for word in ["monitor", "watch", "alert"]
                    ):
                        return "mlops_monitor"
                elif tag == "security":
                    if any(word in content_lower for word in ["scan", "vulnerability"]):
                        return "security_scan"
                    elif any(word in content_lower for word in ["audit", "check"]):
                        return "security_audit"
                    elif any(
                        word in content_lower for word in ["compliance", "policy"]
                    ):
                        return "security_compliance"

        # Default to general automation
        return "general_automation"

    def _generate_rune_content(self, content: str, rune_type: str) -> Dict[str, Any]:
        """Generate rune content based on type."""
        if rune_type.startswith("kubernetes_"):
            return self._generate_k8s_rune_content(content, rune_type)
        elif rune_type.startswith("docker_"):
            return self._generate_docker_rune_content(content, rune_type)
        elif rune_type.startswith("mlops_"):
            return self._generate_mlops_rune_content(content, rune_type)
        elif rune_type.startswith("security_"):
            return self._generate_security_rune_content(content, rune_type)
        else:
            return self._generate_general_rune_content(content)

    def _generate_k8s_rune_content(
        self, content: str, rune_type: str
    ) -> Dict[str, Any]:
        """Generate Kubernetes rune content."""
        if rune_type == "kubernetes_deploy":
            return {
                "script": self._extract_k8s_script(content, "deploy"),
                "steps": [
                    "Validate YAML configuration",
                    "Apply deployment to cluster",
                    "Wait for rollout completion",
                    "Verify deployment status",
                    "Check pod health",
                ],
                "rollback_script": self._generate_rollback_script(content),
                "validation_checks": [
                    "kubectl get pods",
                    "kubectl describe deployment",
                    "kubectl logs -line app=deployment-name",
                ],
            }
        elif rune_type == "kubernetes_scale":
            return {
                "script": self._extract_k8s_script(content, "scale"),
                "steps": [
                    "Check current replica count",
                    "Scale deployment",
                    "Monitor scaling progress",
                    "Verify new replica count",
                    "Check resource usage",
                ],
                "validation_checks": ["kubectl get deployment", "kubectl top pods"],
            }
        elif rune_type == "kubernetes_debug":
            return {
                "script": self._extract_k8s_script(content, "debug"),
                "steps": [
                    "Get pod status",
                    "Check pod logs",
                    "Describe pod details",
                    "Check events",
                    "Verify resource limits",
                ],
                "common_issues": [
                    "Image pull errors",
                    "Resource constraints",
                    "Configuration issues",
                    "Network connectivity",
                ],
            }

        return {"script": content, "steps": [], "validation_checks": []}

    def _generate_docker_rune_content(
        self, content: str, rune_type: str
    ) -> Dict[str, Any]:
        """Generate Docker rune content."""
        if rune_type == "docker_build":
            return {
                "script": self._extract_docker_script(content, "build"),
                "steps": [
                    "Build Docker image",
                    "Tag image appropriately",
                    "Scan for vulnerabilities",
                    "Test image functionality",
                    "Push to registry",
                ],
                "optimization_tips": [
                    "Use multi-stage builds",
                    "Leverage build cache",
                    "Minimize layer count",
                    "Use .dockerignore",
                ],
            }
        elif rune_type == "docker_push":
            return {
                "script": self._extract_docker_script(content, "push"),
                "steps": [
                    "Login to registry",
                    "Tag image for registry",
                    "Push image",
                    "Verify push success",
                    "Clean up local tags",
                ],
            }
        elif rune_type == "docker_cleanup":
            return {
                "script": self._extract_docker_script(content, "cleanup"),
                "steps": [
                    "Remove unused containers",
                    "Remove unused images",
                    "Remove unused networks",
                    "Remove unused volumes",
                    "Prune system",
                ],
            }

        return {"script": content, "steps": []}

    def _generate_mlops_rune_content(
        self, content: str, rune_type: str
    ) -> Dict[str, Any]:
        """Generate MLOps rune content."""
        if rune_type == "mlops_train":
            return {
                "script": self._extract_mlops_script(content, "train"),
                "steps": [
                    "Prepare training data",
                    "Set up training environment",
                    "Train model",
                    "Validate model performance",
                    "Save model artifacts",
                    "Update model registry",
                ],
                "monitoring": [
                    "Training metrics",
                    "Resource usage",
                    "Model performance",
                    "Data quality checks",
                ],
            }
        elif rune_type == "mlops_deploy":
            return {
                "script": self._extract_mlops_script(content, "deploy"),
                "steps": [
                    "Load trained model",
                    "Create deployment configuration",
                    "Deploy to staging",
                    "Run integration tests",
                    "Deploy to production",
                    "Monitor deployment",
                ],
                "rollback_procedure": [
                    "Revert to previous model version",
                    "Update deployment configuration",
                    "Verify rollback success",
                ],
            }
        elif rune_type == "mlops_monitor":
            return {
                "script": self._extract_mlops_script(content, "monitor"),
                "steps": [
                    "Collect model metrics",
                    "Monitor data drift",
                    "Check model performance",
                    "Generate alerts",
                    "Update dashboards",
                ],
                "alert_conditions": [
                    "Model accuracy below threshold",
                    "Data drift detected",
                    "High latency",
                    "Resource usage high",
                ],
            }

        return {"script": content, "steps": []}

    def _generate_security_rune_content(
        self, content: str, rune_type: str
    ) -> Dict[str, Any]:
        """Generate security rune content."""
        if rune_type == "security_scan":
            return {
                "script": self._extract_security_script(content, "scan"),
                "steps": [
                    "Run vulnerability scan",
                    "Analyze scan results",
                    "Generate security report",
                    "Check for critical issues",
                    "Update security baseline",
                ],
                "tools": ["trivy", "clair", "snyk"],
                "severity_levels": ["critical", "high", "medium", "low"],
            }
        elif rune_type == "security_audit":
            return {
                "script": self._extract_security_script(content, "audit"),
                "steps": [
                    "Review access controls",
                    "Check compliance status",
                    "Audit configuration",
                    "Generate audit report",
                    "Recommend improvements",
                ],
                "compliance_frameworks": ["SOC2", "ISO27001", "GDPR", "HIPAA"],
            }

        return {"script": content, "steps": []}

    def _generate_general_rune_content(self, content: str) -> Dict[str, Any]:
        """Generate general automation rune content."""
        return {
            "script": self._extract_general_script(content),
            "steps": self._extract_automation_steps(content),
            "error_handling": self._extract_error_handling(content),
            "validation": self._extract_validation_checks(content),
        }

    def _extract_k8s_script(self, content: str, action: str) -> str:
        """Extract Kubernetes script from content."""
        # Look for kubectl commands
        kubectl_pattern = r"kubectl\s+\w+.*"
        matches = re.findall(kubectl_pattern, content)

        if matches:
            return "\n".join(matches)

        # Look for shell scripts
        script_pattern = r"```bash\s*\n(.*?)\n```"
        matches = re.findall(script_pattern, content, re.DOTALL)

        if matches:
            return matches[0]

        return content

    def _extract_docker_script(self, content: str, action: str) -> str:
        """Extract Docker script from content."""
        # Look for docker commands
        docker_pattern = r"docker\s+\w+.*"
        matches = re.findall(docker_pattern, content)

        if matches:
            return "\n".join(matches)

        # Look for shell scripts
        script_pattern = r"```bash\s*\n(.*?)\n```"
        matches = re.findall(script_pattern, content, re.DOTALL)

        if matches:
            return matches[0]

        return content

    def _extract_mlops_script(self, content: str, action: str) -> str:
        """Extract MLOps script from content."""
        # Look for Python scripts
        python_pattern = r"```python\s*\n(.*?)\n```"
        matches = re.findall(python_pattern, content, re.DOTALL)

        if matches:
            return matches[0]

        # Look for shell scripts
        script_pattern = r"```bash\s*\n(.*?)\n```"
        matches = re.findall(script_pattern, content, re.DOTALL)

        if matches:
            return matches[0]

        return content

    def _extract_security_script(self, content: str, action: str) -> str:
        """Extract security script from content."""
        # Look for security tool commands
        security_patterns = [r"trivy\s+\w+.*", r"snyk\s+\w+.*", r"clair\s+\w+.*"]

        for pattern in security_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return "\n".join(matches)

        # Look for shell scripts
        script_pattern = r"```bash\s*\n(.*?)\n```"
        matches = re.findall(script_pattern, content, re.DOTALL)

        if matches:
            return matches[0]

        return content

    def _extract_general_script(self, content: str) -> str:
        """Extract general script from content."""
        # Look for code blocks
        code_patterns = [
            r"```bash\s*\n(.*?)\n```",
            r"```python\s*\n(.*?)\n```",
            r"```shell\s*\n(.*?)\n```",
        ]

        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                return matches[0]

        return content

    def _extract_automation_steps(self, content: str) -> List[str]:
        """Extract automation steps from content."""
        steps = []

        # Look for numbered or bulleted lists
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith(("- ", "* ", "• ", "1. ", "2. ", "3. ")):
                steps.append(line.lstrip("- *•123456789. "))

        return steps[:10]  # Limit to top 10

    def _extract_error_handling(self, content: str) -> List[str]:
        """Extract error handling from content."""
        error_handling = []

        # Look for error-related content
        error_patterns = [
            r"if.*error.*:",
            r"try.*except.*:",
            r"catch.*error",
            r"error.*handling",
        ]

        for pattern in error_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            error_handling.extend(matches)

        return list(set(error_handling))[:5]

    def _extract_validation_checks(self, content: str) -> List[str]:
        """Extract validation checks from content."""
        validations = []

        # Look for validation patterns
        validation_patterns = [r"check.*", r"verify.*", r"validate.*", r"assert.*"]

        for pattern in validation_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            validations.extend(matches)

        return list(set(validations))[:5]

    def _generate_rollback_script(self, content: str) -> str:
        """Generate rollback script for deployments."""
        return """#!/bin/bash
# Rollback script for Kubernetes deployment
echo "Rolling back deployment..."
kubectl rollout undo deployment/deployment-name
kubectl rollout status deployment/deployment-name
echo "Rollback completed."
"""

    def _create_rune_metadata(
        self, sanitized_data: Dict[str, Any], rune_type: str
    ) -> Dict[str, Any]:
        """Create metadata for the generated rune."""
        return {
            "title": f"{rune_type.replace('_', ' ').title()} Automation",
            "description": f"Automated solution for {rune_type}",
            "category": rune_type.split("_")[0],
            "subcategory": rune_type.split("_")[1] if "_" in rune_type else "general",
            "source_data_type": sanitized_data.get("type"),
            "generation_method": "ai_generated",
            "confidence_score": 0.80,
            "last_updated": datetime.utcnow().isoformat(),
            "estimated_execution_time": "5-10 minutes",
        }

    def _calculate_rune_effectiveness(
        self, rune_content: Dict[str, Any], sanitized_data: Dict[str, Any]
    ) -> float:
        """Calculate effectiveness score for the generated rune."""
        score = 0.0

        # Script completeness
        if rune_content.get("script"):
            score += 0.3
        if rune_content.get("steps"):
            score += 0.3
        if rune_content.get("validation_checks"):
            score += 0.2

        # Source data quality
        source_quality = sanitized_data.get("processing_stats", {}).get(
            "original_length", 0
        )
        if source_quality > 100:
            score += 0.1
        if source_quality > 500:
            score += 0.1

        return min(score, 1.0)


# Convenience functions for external use
def generate_rune(sanitized_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a rune from sanitized data."""
    generator = RuneGenerator()
    return generator.generate_rune(sanitized_data)


def batch_generate_runes(
    sanitized_data_list: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Generate runes from multiple sanitized data inputs."""
    generator = RuneGenerator()
    return [generator.generate_rune(data) for data in sanitized_data_list]
