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
GitOps Compliance Scanner
Evaluates repositories for GitOps readiness and provides comprehensive scoring.
"""

import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class GitOpsScanner:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.score = 0
        self.max_score = 100
        self.categories = {
            "containerization": {"score": 0, "max": 20, "items": []},
            "orchestration": {"score": 0, "max": 25, "items": []},
            "ci_cd": {"score": 0, "max": 20, "items": []},
            "gitops_tools": {"score": 0, "max": 20, "items": []},
            "security": {"score": 0, "max": 15, "items": []},
        }

    async def scan_gitops_compliance(self) -> Dict[str, Any]:
        """
        Perform comprehensive GitOps compliance scan.

        Returns:
            GitOps compliance report with scoring and recommendations
        """
        try:
            logger.info(f"Starting GitOps compliance scan for {self.repo_path}")

            # Scan each category
            await self._scan_containerization()
            await self._scan_orchestration()
            await self._scan_ci_cd()
            await self._scan_gitops_tools()
            await self._scan_security()

            # Calculate overall score
            self._calculate_overall_score()

            # Generate recommendations
            recommendations = self._generate_recommendations()

            report = {
                "overall_score": self.score,
                "max_score": self.max_score,
                "grade": self._get_grade(),
                "categories": self.categories,
                "recommendations": recommendations,
                "summary": self._generate_summary(),
            }

            logger.info(
                f"GitOps compliance scan completed. Score: {self.score}/{self.max_score}"
            )
            return report

        except Exception as e:
            logger.error(f"GitOps compliance scan failed: {str(e)}")
            raise

    async def _scan_containerization(self) -> None:
        """Scan for containerization readiness."""
        category = self.categories["containerization"]

        # Check for Dockerfile
        dockerfiles = self._find_files(
            ["Dockerfile", "Dockerfile.dev", "Dockerfile.prod"]
        )
        if dockerfiles:
            category["score"] += 10
            category["items"].append(
                {
                    "item": "Dockerfile present",
                    "score": 10,
                    "status": "✅",
                    "details": f"Found {len(dockerfiles)} Dockerfile(s)",
                }
            )

        # Check for docker-compose
        compose_files = self._find_files(
            ["docker-compose.yml", "docker-compose.yaml", "compose.yml"]
        )
        if compose_files:
            category["score"] += 5
            category["items"].append(
                {
                    "item": "Docker Compose present",
                    "score": 5,
                    "status": "✅",
                    "details": f"Found {len(compose_files)} compose file(s)",
                }
            )

        # Check for multi-stage builds
        for dockerfile in dockerfiles:
            if self._has_multi_stage_build(dockerfile):
                category["score"] += 5
                category["items"].append(
                    {
                        "item": "Multi-stage Dockerfile",
                        "score": 5,
                        "status": "✅",
                        "details": "Optimized container builds",
                    }
                )
                break

        # Check for .dockerignore
        dockerignore_files = self._find_files([".dockerignore"])
        if dockerignore_files:
            category["items"].append(
                {
                    "item": ".dockerignore present",
                    "score": 0,
                    "status": "ℹ️",
                    "details": "Good practice for optimized builds",
                }
            )

    async def _scan_orchestration(self) -> None:
        """Scan for Kubernetes orchestration readiness."""
        category = self.categories["orchestration"]

        # Check for Kubernetes manifests
        k8s_files = self._find_files(["*.yaml", "*.yml"], recursive=True)
        k8s_manifests = [f for f in k8s_files if self._is_k8s_manifest(f)]

        if k8s_manifests:
            category["score"] += 10
            category["items"].append(
                {
                    "item": "Kubernetes manifests present",
                    "score": 10,
                    "status": "✅",
                    "details": f"Found {len(k8s_manifests)} K8s manifest(s)",
                }
            )

        # Check for Helm charts
        helm_charts = self._find_helm_charts()
        if helm_charts:
            category["score"] += 10
            category["items"].append(
                {
                    "item": "Helm charts present",
                    "score": 10,
                    "status": "✅",
                    "details": f"Found {len(helm_charts)} Helm chart(s)",
                }
            )

        # Check for Kustomize
        kustomize_files = self._find_files(["kustomization.yaml", "kustomization.yml"])
        if kustomize_files:
            category["score"] += 5
            category["items"].append(
                {
                    "item": "Kustomize configuration present",
                    "score": 5,
                    "status": "✅",
                    "details": "Kustomize-based configuration management",
                }
            )

    async def _scan_ci_cd(self) -> None:
        """Scan for CI/CD pipeline readiness."""
        category = self.categories["ci_cd"]

        # Check for GitHub Actions
        github_actions = self._find_files(
            [".github/workflows/*.yml", ".github/workflows/*.yaml"]
        )
        if github_actions:
            category["score"] += 8
            category["items"].append(
                {
                    "item": "GitHub Actions workflows",
                    "score": 8,
                    "status": "✅",
                    "details": f"Found {len(github_actions)} workflow(s)",
                }
            )

        # Check for other CI/CD tools
        ci_files = self._find_files(
            [
                ".gitlab-ci.yml",
                "Jenkinsfile",
                "azure-pipelines.yml",
                ".circleci/config.yml",
                ".travis.yml",
            ]
        )
        if ci_files:
            category["score"] += 6
            category["items"].append(
                {
                    "item": "CI/CD pipeline configured",
                    "score": 6,
                    "status": "✅",
                    "details": f"Found {len(ci_files)} CI/CD configuration(s)",
                }
            )

        # Check for automated testing
        test_files = self._find_test_files()
        if test_files:
            category["score"] += 3
            category["items"].append(
                {
                    "item": "Test files present",
                    "score": 3,
                    "status": "✅",
                    "details": f"Found {len(test_files)} test file(s)",
                }
            )

        # Check for security scanning in CI
        if self._has_security_scanning():
            category["score"] += 3
            category["items"].append(
                {
                    "item": "Security scanning in CI",
                    "score": 3,
                    "status": "✅",
                    "details": "Security scanning integrated in pipeline",
                }
            )

    async def _scan_gitops_tools(self) -> None:
        """Scan for GitOps tool integration."""
        category = self.categories["gitops_tools"]

        # Check for ArgoCD
        argocd_files = self._find_files(["*.yaml", "*.yml"], recursive=True)
        argocd_manifests = [f for f in argocd_files if self._is_argocd_manifest(f)]

        if argocd_manifests:
            category["score"] += 10
            category["items"].append(
                {
                    "item": "ArgoCD manifests present",
                    "score": 10,
                    "status": "✅",
                    "details": "ArgoCD-ready configuration",
                }
            )

        # Check for Flux
        flux_files = self._find_files(["*.yaml", "*.yml"], recursive=True)
        flux_manifests = [f for f in flux_files if self._is_flux_manifest(f)]

        if flux_manifests:
            category["score"] += 10
            category["items"].append(
                {
                    "item": "Flux manifests present",
                    "score": 10,
                    "status": "✅",
                    "details": "Flux-ready configuration",
                }
            )

        # Check for Kustomize
        kustomize_files = self._find_files(["kustomization.yaml", "kustomization.yml"])
        if kustomize_files:
            category["items"].append(
                {
                    "item": "Kustomize configuration",
                    "score": 0,
                    "status": "ℹ️",
                    "details": "Kustomize-based GitOps",
                }
            )

    async def _scan_security(self) -> None:
        """Scan for security best practices."""
        category = self.categories["security"]

        # Check for secrets management
        if self._has_secrets_management():
            category["score"] += 5
            category["items"].append(
                {
                    "item": "Secrets management",
                    "score": 5,
                    "status": "✅",
                    "details": "Proper secrets handling configured",
                }
            )

        # Check for RBAC
        rbac_files = self._find_rbac_files()
        if rbac_files:
            category["score"] += 5
            category["items"].append(
                {
                    "item": "RBAC configuration",
                    "score": 5,
                    "status": "✅",
                    "details": f"Found {len(rbac_files)} RBAC file(s)",
                }
            )

        # Check for network policies
        network_policies = self._find_network_policies()
        if network_policies:
            category["score"] += 3
            category["items"].append(
                {
                    "item": "Network policies",
                    "score": 3,
                    "status": "✅",
                    "details": "Network security policies configured",
                }
            )

        # Check for security contexts
        if self._has_security_contexts():
            category["score"] += 2
            category["items"].append(
                {
                    "item": "Security contexts",
                    "score": 2,
                    "status": "✅",
                    "details": "Pod security contexts configured",
                }
            )

    def _calculate_overall_score(self) -> None:
        """Calculate overall GitOps compliance score."""
        total_score = 0
        total_max = 0

        for category_name, category_data in self.categories.items():
            total_score += category_data["score"]
            total_max += category_data["max"]

        self.score = total_score
        self.max_score = total_max

    def _get_grade(self) -> str:
        """Get letter grade based on score."""
        percentage = (self.score / self.max_score) * 100

        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"

    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate recommendations for improvement."""
        recommendations = []

        # Containerization recommendations
        if self.categories["containerization"]["score"] < 15:
            recommendations.append(
                {
                    "category": "Containerization",
                    "priority": "high",
                    "title": "Improve Containerization",
                    "description": "Add Dockerfile and optimize container builds",
                    "steps": [
                        "Create a multi-stage Dockerfile",
                        "Add .dockerignore file",
                        "Optimize container size and security",
                    ],
                }
            )

        # Orchestration recommendations
        if self.categories["orchestration"]["score"] < 15:
            recommendations.append(
                {
                    "category": "Orchestration",
                    "priority": "high",
                    "title": "Add Kubernetes Configuration",
                    "description": "Create Kubernetes manifests and Helm charts",
                    "steps": [
                        "Create basic Kubernetes manifests (deployment, service)",
                        "Add Helm chart for package management",
                        "Configure resource limits and health checks",
                    ],
                }
            )

        # CI/CD recommendations
        if self.categories["ci_cd"]["score"] < 10:
            recommendations.append(
                {
                    "category": "CI/CD",
                    "priority": "high",
                    "title": "Implement CI/CD Pipeline",
                    "description": "Set up automated build and deployment pipeline",
                    "steps": [
                        "Create GitHub Actions workflow",
                        "Add automated testing",
                        "Integrate security scanning",
                    ],
                }
            )

        # GitOps recommendations
        if self.categories["gitops_tools"]["score"] < 10:
            recommendations.append(
                {
                    "category": "GitOps",
                    "priority": "medium",
                    "title": "Implement GitOps",
                    "description": "Set up ArgoCD or Flux for GitOps workflows",
                    "steps": [
                        "Install ArgoCD in your cluster",
                        "Create Application manifests",
                        "Configure automated sync policies",
                    ],
                }
            )

        # Security recommendations
        if self.categories["security"]["score"] < 10:
            recommendations.append(
                {
                    "category": "Security",
                    "priority": "medium",
                    "title": "Enhance Security",
                    "description": "Implement security best practices",
                    "steps": [
                        "Add RBAC configuration",
                        "Implement network policies",
                        "Configure pod security contexts",
                    ],
                }
            )

        return recommendations

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary of GitOps compliance."""
        return {
            "total_score": self.score,
            "max_possible_score": self.max_score,
            "percentage": round((self.score / self.max_score) * 100, 1),
            "grade": self._get_grade(),
            "strengths": self._identify_strengths(),
            "weaknesses": self._identify_weaknesses(),
            "next_steps": self._get_next_steps(),
        }

    def _identify_strengths(self) -> List[str]:
        """Identify areas of strength."""
        strengths = []

        for category_name, category_data in self.categories.items():
            if category_data["score"] >= category_data["max"] * 0.8:
                strengths.append(
                    f"Strong {category_name.replace('_', ' ')} implementation"
                )

        return strengths

    def _identify_weaknesses(self) -> List[str]:
        """Identify areas of weakness."""
        weaknesses = []

        for category_name, category_data in self.categories.items():
            if category_data["score"] < category_data["max"] * 0.5:
                weaknesses.append(
                    f"Needs improvement in {category_name.replace('_', ' ')}"
                )

        return weaknesses

    def _get_next_steps(self) -> List[str]:
        """Get immediate next steps."""
        steps = []

        if self.categories["containerization"]["score"] == 0:
            steps.append("Create a Dockerfile for your application")

        if self.categories["orchestration"]["score"] == 0:
            steps.append("Add basic Kubernetes manifests")

        if self.categories["ci_cd"]["score"] == 0:
            steps.append("Set up a CI/CD pipeline")

        return steps[:3]  # Return top 3 priorities

    def _find_files(self, patterns: List[str], recursive: bool = True) -> List[str]:
        """Find files matching patterns."""
        files = []

        if recursive:
            for pattern in patterns:
                if "*" in pattern:
                    # Handle glob patterns
                    import glob

                    matches = glob.glob(os.path.join(self.repo_path, pattern))
                    files.extend(matches)
                else:
                    # Handle specific files
                    file_path = os.path.join(self.repo_path, pattern)
                    if os.path.exists(file_path):
                        files.append(file_path)
        else:
            for pattern in patterns:
                file_path = os.path.join(self.repo_path, pattern)
                if os.path.exists(file_path):
                    files.append(file_path)

        return files

    def _has_multi_stage_build(self, dockerfile_path: str) -> bool:
        """Check if Dockerfile has multi-stage build."""
        try:
            with open(dockerfile_path, "r") as f:
                content = f.read()
                return "FROM" in content and content.count("FROM") > 1
        except Exception:
            return False

    def _is_k8s_manifest(self, file_path: str) -> bool:
        """Check if file is a Kubernetes manifest."""
        try:
            with open(file_path, "r") as f:
                content = f.read()
                # Check for common K8s resource types
                k8s_resources = [
                    "apiVersion:",
                    "kind:",
                    "metadata:",
                    "spec:",
                    "Deployment",
                    "Service",
                    "ConfigMap",
                    "Secret",
                    "Ingress",
                    "PersistentVolumeClaim",
                ]
                return any(resource in content for resource in k8s_resources)
        except Exception:
            return False

    def _find_helm_charts(self) -> List[str]:
        """Find Helm charts in the repository."""
        charts = []

        for root, dirs, files in os.walk(self.repo_path):
            if "Chart.yaml" in files:
                charts.append(root)

        return charts

    def _find_test_files(self) -> List[str]:
        """Find test files in the repository."""
        test_files = []
        test_patterns = [
            "*test*.py",
            "*test*.js",
            "*test*.ts",
            "*test*.go",
            "*spec*.py",
            "*spec*.js",
            "*spec*.ts",
            "test_*.py",
            "test_*.js",
            "test_*.ts",
        ]

        for pattern in test_patterns:
            test_files.extend(self._find_files([pattern], recursive=True))

        return test_files

    def _has_security_scanning(self) -> bool:
        """Check if security scanning is configured in CI/CD."""
        ci_files = self._find_files(
            [
                ".github/workflows/*.yml",
                ".github/workflows/*.yaml",
                ".gitlab-ci.yml",
                "Jenkinsfile",
            ]
        )

        security_tools = ["trivy", "snyk", "semgrep", "bandit", "sonarqube"]

        for ci_file in ci_files:
            try:
                with open(ci_file, "r") as f:
                    content = f.read().lower()
                    if any(tool in content for tool in security_tools):
                        return True
            except Exception:
                continue

        return False

    def _is_argocd_manifest(self, file_path: str) -> bool:
        """Check if file is an ArgoCD Application manifest."""
        try:
            with open(file_path, "r") as f:
                content = f.read()
                return "kind: Application" in content and "argoproj.io" in content
        except Exception:
            return False

    def _is_flux_manifest(self, file_path: str) -> bool:
        """Check if file is a Flux manifest."""
        try:
            with open(file_path, "r") as f:
                content = f.read()
                return "fluxcd.io" in content or "kind: GitRepository" in content
        except Exception:
            return False

    def _has_secrets_management(self) -> bool:
        """Check if secrets management is configured."""
        # Check for external secrets operator, vault, etc.
        k8s_files = self._find_files(["*.yaml", "*.yml"], recursive=True)

        for k8s_file in k8s_files:
            try:
                with open(k8s_file, "r") as f:
                    content = f.read()
                    if any(
                        keyword in content
                        for keyword in [
                            "ExternalSecret",
                            "SecretStore",
                            "vault",
                            "secrets-manager",
                        ]
                    ):
                        return True
            except Exception:
                continue

        return False

    def _find_rbac_files(self) -> List[str]:
        """Find RBAC configuration files."""
        rbac_files = []
        k8s_files = self._find_files(["*.yaml", "*.yml"], recursive=True)

        for k8s_file in k8s_files:
            try:
                with open(k8s_file, "r") as f:
                    content = f.read()
                    if any(
                        rbac_type in content
                        for rbac_type in [
                            "kind: Role",
                            "kind: ClusterRole",
                            "kind: RoleBinding",
                            "kind: ClusterRoleBinding",
                        ]
                    ):
                        rbac_files.append(k8s_file)
            except Exception:
                continue

        return rbac_files

    def _find_network_policies(self) -> List[str]:
        """Find network policy files."""
        network_policies = []
        k8s_files = self._find_files(["*.yaml", "*.yml"], recursive=True)

        for k8s_file in k8s_files:
            try:
                with open(k8s_file, "r") as f:
                    content = f.read()
                    if "kind: NetworkPolicy" in content:
                        network_policies.append(k8s_file)
            except Exception:
                continue

        return network_policies

    def _has_security_contexts(self) -> bool:
        """Check if security contexts are configured."""
        k8s_files = self._find_files(["*.yaml", "*.yml"], recursive=True)

        for k8s_file in k8s_files:
            try:
                with open(k8s_file, "r") as f:
                    content = f.read()
                    if "securityContext:" in content:
                        return True
            except Exception:
                continue

        return False
