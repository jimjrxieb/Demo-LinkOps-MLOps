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
Whis Orb Generator - Creates best practices knowledge assets from structured data.
"""

import re
import uuid
from datetime import datetime
from typing import Any, Dict, List


class OrbGenerator:
    """Generates Orbs (best practices) from sanitized data."""

    def __init__(self):
        self.orb_templates = {
            "kubernetes": {
                "deployment": self._generate_k8s_deployment_orb,
                "service": self._generate_k8s_service_orb,
                "configmap": self._generate_k8s_configmap_orb,
                "secret": self._generate_k8s_secret_orb,
            },
            "docker": {
                "dockerfile": self._generate_dockerfile_orb,
                "compose": self._generate_compose_orb,
            },
            "mlops": {
                "pipeline": self._generate_mlops_pipeline_orb,
                "model": self._generate_model_orb,
                "monitoring": self._generate_monitoring_orb,
            },
            "security": {
                "scan": self._generate_security_scan_orb,
                "audit": self._generate_security_audit_orb,
            },
        }

    def generate_orb(self, sanitized_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an Orb from sanitized data.

        Args:
            sanitized_data: Sanitized data from whis_sanitize

        Returns:
            Generated Orb data
        """
        try:
            orb_id = str(uuid.uuid4())
            content = sanitized_data.get("sanitized_content", "")
            tags = sanitized_data.get("tags", [])

            # Determine orb type
            orb_type = self._determine_orb_type(content, tags)

            # Generate orb using appropriate template
            orb_content = self._generate_orb_content(content, orb_type)

            # Create orb metadata
            orb_metadata = self._create_orb_metadata(sanitized_data, orb_type)

            # Calculate orb quality score
            quality_score = self._calculate_orb_quality(orb_content, sanitized_data)

            orb_data = {
                "id": orb_id,
                "type": "orb",
                "orb_type": orb_type,
                "title": orb_metadata.get("title", f"Generated Orb {orb_id[:8]}"),
                "content": orb_content,
                "tags": tags + [orb_type, "generated"],
                "source_data_id": sanitized_data.get("id"),
                "quality_score": quality_score,
                "metadata": orb_metadata,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "generated",
                "version": "1.0.0",
            }

            return orb_data

        except Exception as e:
            return {
                "id": str(uuid.uuid4()),
                "type": "orb",
                "status": "generation_failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _determine_orb_type(self, content: str, tags: List[str]) -> str:
        """Determine the type of orb to generate."""
        content_lower = content.lower()

        # Check tags first
        for tag in tags:
            if tag in self.orb_templates:
                # Determine specific type within domain
                if tag == "kubernetes":
                    if "deployment" in content_lower or "pod" in content_lower:
                        return "kubernetes_deployment"
                    elif "service" in content_lower:
                        return "kubernetes_service"
                    elif "config" in content_lower:
                        return "kubernetes_configmap"
                elif tag == "docker":
                    if "dockerfile" in content_lower:
                        return "docker_dockerfile"
                    elif "compose" in content_lower:
                        return "docker_compose"
                elif tag == "mlops":
                    if "pipeline" in content_lower:
                        return "mlops_pipeline"
                    elif "model" in content_lower:
                        return "mlops_model"
                    elif "monitor" in content_lower:
                        return "mlops_monitoring"
                elif tag == "security":
                    if "scan" in content_lower:
                        return "security_scan"
                    elif "audit" in content_lower:
                        return "security_audit"

        # Default to general best practice
        return "general_best_practice"

    def _generate_orb_content(self, content: str, orb_type: str) -> Dict[str, Any]:
        """Generate orb content based on type."""
        if orb_type.startswith("kubernetes_"):
            return self._generate_k8s_orb_content(content, orb_type)
        elif orb_type.startswith("docker_"):
            return self._generate_docker_orb_content(content, orb_type)
        elif orb_type.startswith("mlops_"):
            return self._generate_mlops_orb_content(content, orb_type)
        elif orb_type.startswith("security_"):
            return self._generate_security_orb_content(content, orb_type)
        else:
            return self._generate_general_orb_content(content)

    def _generate_k8s_orb_content(self, content: str, orb_type: str) -> Dict[str, Any]:
        """Generate Kubernetes orb content."""
        if orb_type == "kubernetes_deployment":
            return {
                "template": self._extract_k8s_template(content, "deployment"),
                "best_practices": [
                    "Always specify resource limits and requests",
                    "Use rolling update strategy for zero-downtime deployments",
                    "Set appropriate replica count for high availability",
                    "Use health checks (liveness and readiness probes)",
                    "Implement proper security contexts",
                ],
                "common_pitfalls": [
                    "Not setting resource limits",
                    "Using latest tag for images",
                    "Missing health checks",
                    "Insufficient replica count",
                ],
                "examples": self._extract_k8s_examples(content),
            }
        elif orb_type == "kubernetes_service":
            return {
                "template": self._extract_k8s_template(content, "service"),
                "best_practices": [
                    "Use appropriate service type (ClusterIP, NodePort, LoadBalancer)",
                    "Implement proper selector labels",
                    "Consider using headless services for stateful applications",
                    "Use service accounts for authentication",
                ],
                "examples": self._extract_k8s_examples(content),
            }

        return {"template": content, "best_practices": [], "examples": []}

    def _generate_docker_orb_content(
        self, content: str, orb_type: str
    ) -> Dict[str, Any]:
        """Generate Docker orb content."""
        if orb_type == "docker_dockerfile":
            return {
                "template": self._extract_dockerfile_template(content),
                "best_practices": [
                    "Use multi-stage builds to reduce image size",
                    "Copy requirements first for better layer caching",
                    "Use specific base image tags, not 'latest'",
                    "Run as non-root user for security",
                    "Minimize the number of layers",
                ],
                "security_considerations": [
                    "Scan images for vulnerabilities",
                    "Use minimal base images",
                    "Remove unnecessary packages",
                    "Set proper file permissions",
                ],
            }

        return {"template": content, "best_practices": []}

    def _generate_mlops_orb_content(
        self, content: str, orb_type: str
    ) -> Dict[str, Any]:
        """Generate MLOps orb content."""
        if orb_type == "mlops_pipeline":
            return {
                "template": self._extract_pipeline_template(content),
                "best_practices": [
                    "Implement data versioning",
                    "Use reproducible environments",
                    "Automate model testing and validation",
                    "Monitor model performance in production",
                    "Implement A/B testing capabilities",
                ],
                "stages": [
                    "data_prep",
                    "training",
                    "validation",
                    "deployment",
                    "monitoring",
                ],
            }
        elif orb_type == "mlops_model":
            return {
                "template": self._extract_model_template(content),
                "best_practices": [
                    "Version your models",
                    "Implement model validation",
                    "Use feature stores for consistency",
                    "Monitor model drift",
                    "Implement rollback mechanisms",
                ],
            }

        return {"template": content, "best_practices": []}

    def _generate_security_orb_content(
        self, content: str, orb_type: str
    ) -> Dict[str, Any]:
        """Generate security orb content."""
        if orb_type == "security_scan":
            return {
                "template": self._extract_security_template(content),
                "best_practices": [
                    "Scan images before deployment",
                    "Use multiple scanning tools",
                    "Automate security scanning in CI/CD",
                    "Regular vulnerability assessments",
                    "Keep security tools updated",
                ],
                "tools": ["trivy", "clair", "snyk", "anchore"],
            }

        return {"template": content, "best_practices": []}

    def _generate_general_orb_content(self, content: str) -> Dict[str, Any]:
        """Generate general best practice orb content."""
        return {
            "template": content,
            "best_practices": self._extract_best_practices(content),
            "key_points": self._extract_key_points(content),
            "examples": self._extract_examples(content),
        }

    def _extract_k8s_template(self, content: str, resource_type: str) -> str:
        """Extract Kubernetes template from content."""
        # Look for YAML blocks
        yaml_pattern = r"```yaml\s*\n(.*?)\n```"
        matches = re.findall(yaml_pattern, content, re.DOTALL)

        if matches:
            return matches[0]

        # Look for YAML content
        if "apiVersion:" in content and "kind:" in content:
            lines = content.split("\n")
            yaml_lines = []
            in_yaml = False

            for line in lines:
                if "apiVersion:" in line or "kind:" in line:
                    in_yaml = True
                if in_yaml:
                    yaml_lines.append(line)
                if in_yaml and line.strip() == "":
                    break

            return "\n".join(yaml_lines)

        return content

    def _extract_dockerfile_template(self, content: str) -> str:
        """Extract Dockerfile template from content."""
        # Look for Dockerfile blocks
        docker_pattern = r"```dockerfile\s*\n(.*?)\n```"
        matches = re.findall(docker_pattern, content, re.DOTALL)

        if matches:
            return matches[0]

        # Look for FROM statements
        if "FROM " in content:
            lines = content.split("\n")
            docker_lines = []

            for line in lines:
                if line.strip().startswith(
                    ("FROM ", "RUN ", "COPY ", "WORKDIR ", "EXPOSE ", "CMD ")
                ):
                    docker_lines.append(line)

            return "\n".join(docker_lines)

        return content

    def _extract_pipeline_template(self, content: str) -> str:
        """Extract pipeline template from content."""
        # Look for pipeline definitions
        pipeline_patterns = [
            r"```yaml\s*\n(.*?)\n```",
            r"pipeline:\s*\n(.*?)(?=\n\w|$)",
            r"stages:\s*\n(.*?)(?=\n\w|$)",
        ]

        for pattern in pipeline_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                return matches[0]

        return content

    def _extract_model_template(self, content: str) -> str:
        """Extract model template from content."""
        # Look for model definitions
        model_patterns = [
            r"```python\s*\n(.*?)\n```",
            r"class.*Model.*:\s*\n(.*?)(?=\n\w|$)",
            r"def.*train.*:\s*\n(.*?)(?=\n\w|$)",
        ]

        for pattern in model_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                return matches[0]

        return content

    def _extract_security_template(self, content: str) -> str:
        """Extract security template from content."""
        # Look for security configurations
        security_patterns = [
            r"```yaml\s*\n(.*?)\n```",
            r"security:\s*\n(.*?)(?=\n\w|$)",
            r"scan:\s*\n(.*?)(?=\n\w|$)",
        ]

        for pattern in security_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                return matches[0]

        return content

    def _extract_best_practices(self, content: str) -> List[str]:
        """Extract best practices from content."""
        practices = []

        # Look for numbered or bulleted lists
        lines = content.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith(("- ", "* ", "• ", "1. ", "2. ", "3. ")):
                if any(
                    word in line.lower()
                    for word in [
                        "best",
                        "practice",
                        "should",
                        "recommend",
                        "always",
                        "never",
                    ]
                ):
                    practices.append(line.lstrip("- *•123456789. "))

        return practices[:10]  # Limit to top 10

    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from content."""
        points = []

        # Look for emphasized text
        emphasis_patterns = [r"\*\*(.*?)\*\*", r"__(.*?)__", r"`(.*?)`"]

        for pattern in emphasis_patterns:
            matches = re.findall(pattern, content)
            points.extend(matches)

        return list(set(points))[:5]  # Limit to top 5

    def _extract_examples(self, content: str) -> List[str]:
        """Extract examples from content."""
        examples = []

        # Look for code blocks
        code_pattern = r"```\w*\s*\n(.*?)\n```"
        matches = re.findall(code_pattern, content, re.DOTALL)

        examples.extend(matches)

        return examples[:3]  # Limit to top 3

    def _extract_k8s_examples(self, content: str) -> List[str]:
        """Extract Kubernetes examples from content."""
        return self._extract_examples(content)

    def _create_orb_metadata(
        self, sanitized_data: Dict[str, Any], orb_type: str
    ) -> Dict[str, Any]:
        """Create metadata for the generated orb."""
        return {
            "title": f"{orb_type.replace('_', ' ').title()} Best Practices",
            "description": f"Generated best practices for {orb_type}",
            "category": orb_type.split("_")[0],
            "subcategory": orb_type.split("_")[1] if "_" in orb_type else "general",
            "source_data_type": sanitized_data.get("type"),
            "generation_method": "ai_generated",
            "confidence_score": 0.85,
            "last_updated": datetime.utcnow().isoformat(),
        }

    def _calculate_orb_quality(
        self, orb_content: Dict[str, Any], sanitized_data: Dict[str, Any]
    ) -> float:
        """Calculate quality score for the generated orb."""
        score = 0.0

        # Content completeness
        if orb_content.get("template"):
            score += 0.3
        if orb_content.get("best_practices"):
            score += 0.3
        if orb_content.get("examples"):
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
def generate_orb(sanitized_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate an orb from sanitized data."""
    generator = OrbGenerator()
    return generator.generate_orb(sanitized_data)


def batch_generate_orbs(
    sanitized_data_list: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Generate orbs from multiple sanitized data inputs."""
    generator = OrbGenerator()
    return [generator.generate_orb(data) for data in sanitized_data_list]
