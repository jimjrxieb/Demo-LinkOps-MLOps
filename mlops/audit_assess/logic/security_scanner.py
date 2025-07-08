"""
Security Scanner for Repository Auditing
Integrates GitGuardian, Trivy, and Semgrep for comprehensive security analysis.
"""

import json
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class SecurityScanner:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.results = {
            "secrets": [],
            "vulnerabilities": [],
            "code_quality": [],
            "compliance": [],
            "summary": {
                "total_issues": 0,
                "critical_issues": 0,
                "high_issues": 0,
                "medium_issues": 0,
                "low_issues": 0,
                "secrets_found": 0,
                "vulnerabilities_found": 0,
                "compliance_score": 0,
            },
        }

    async def run_full_security_scan(self) -> Dict[str, Any]:
        """
        Run comprehensive security scan using multiple tools.

        Returns:
            Complete security analysis results
        """
        try:
            logger.info(f"Starting security scan for {self.repo_path}")

            # Run all security scans
            await self._scan_secrets()
            await self._scan_vulnerabilities()
            await self._scan_code_quality()
            await self._scan_compliance()

            # Calculate summary statistics
            self._calculate_summary()

            logger.info(
                f"Security scan completed. Found {self.results['summary']['total_issues']} issues"
            )
            return self.results

        except Exception as e:
            logger.error(f"Security scan failed: {str(e)}")
            raise

    async def _scan_secrets(self) -> None:
        """Scan for secrets and sensitive information using GitGuardian patterns."""
        try:
            # GitGuardian-style secret patterns
            secret_patterns = [
                # API Keys
                r'["\']?[aA][pP][iI][-_]?[kK][eE][yY]["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{32,}["\']?',
                r'["\']?[sS][eE][cC][rR][eE][tT]["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{32,}["\']?',
                # AWS Keys
                r"AKIA[0-9A-Z]{16}",
                r'["\']?[aA][wW][sS][-_]?[aA][cC][cC][eE][sS][sS][-_]?[kK][eE][yY]["\']?\s*[:=]\s*["\']?[A-Z0-9]{20}["\']?',
                r'["\']?[aA][wW][sS][-_]?[sS][eE][cC][rR][eE][tT][-_]?[kK][eE][yY]["\']?\s*[:=]\s*["\']?[A-Za-z0-9/+=]{40}["\']?',
                # Database URLs
                r'["\']?[dD][aA][tT][aA][bB][aA][sS][eE][-_]?[uU][rR][lL]["\']?\s*[:=]\s*["\']?[a-zA-Z]+://[^\s"\']+["\']?',
                r'["\']?[dD][bB][-_]?[uU][rR][lL]["\']?\s*[:=]\s*["\']?[a-zA-Z]+://[^\s"\']+["\']?',
                # JWT Tokens
                r'["\']?[jJ][wW][tT]["\']?\s*[:=]\s*["\']?[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*["\']?',
                # Private Keys
                r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
                r"-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----",
                # Passwords
                r'["\']?[pP][aA][sS][sS][wW][oO][rR][dD]["\']?\s*[:=]\s*["\']?[^\s"\']{8,}["\']?',
                r'["\']?[pP][wW][dD]["\']?\s*[:=]\s*["\']?[^\s"\']{8,}["\']?',
                # OAuth Tokens
                r'["\']?[oO][aA][uU][tT][hH]["\']?\s*[:=]\s*["\']?[a-zA-Z0-9]{32,}["\']?',
                # Slack Tokens
                r"xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}",
                # GitHub Tokens
                r"gh[p|o|u|s|r]_[A-Za-z0-9_]{36}",
                # Docker Registry
                r'["\']?[dD][oO][cC][kK][eE][rR][-_]?[rR][eE][gG][iI][sS][tT][rR][yY]["\']?\s*[:=]\s*["\']?[^\s"\']+["\']?',
            ]

            secrets_found = []

            for root, dirs, files in os.walk(self.repo_path):
                # Skip common directories that shouldn't contain secrets
                dirs[:] = [
                    d
                    for d in dirs
                    if d not in [".git", "node_modules", "__pycache__", ".pytest_cache"]
                ]

                for file in files:
                    if file.startswith("."):
                        continue

                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.repo_path)

                    # Skip binary files
                    if self._is_binary_file(file_path):
                        continue

                    try:
                        with open(
                            file_path, "r", encoding="utf-8", errors="ignore"
                        ) as f:
                            content = f.read()
                            lines = content.split("\n")

                            for line_num, line in enumerate(lines, 1):
                                for pattern in secret_patterns:
                                    matches = re.finditer(pattern, line, re.IGNORECASE)
                                    for match in matches:
                                        secret_info = {
                                            "file": rel_path,
                                            "line": line_num,
                                            "pattern": pattern,
                                            "severity": self._classify_secret_severity(
                                                pattern
                                            ),
                                            "context": line.strip(),
                                            "recommendation": self._get_secret_recommendation(
                                                pattern
                                            ),
                                        }
                                        secrets_found.append(secret_info)
                    except Exception as e:
                        logger.warning(f"Could not read file {file_path}: {str(e)}")

            self.results["secrets"] = secrets_found
            self.results["summary"]["secrets_found"] = len(secrets_found)

        except Exception as e:
            logger.error(f"Secret scanning failed: {str(e)}")

    async def _scan_vulnerabilities(self) -> None:
        """Scan for vulnerabilities using Trivy."""
        try:
            vulnerabilities = []

            # Check if Trivy is available
            if not self._check_tool_available("trivy"):
                logger.warning("Trivy not available, skipping vulnerability scan")
                self.results["vulnerabilities"] = []
                return

            # Scan for Dockerfile vulnerabilities
            dockerfiles = self._find_dockerfiles()
            for dockerfile in dockerfiles:
                try:
                    result = subprocess.run(
                        ["trivy", "config", "--format", "json", dockerfile],
                        capture_output=True,
                        text=True,
                        cwd=self.repo_path,
                        timeout=300,
                    )

                    if result.returncode == 0:
                        vuln_data = json.loads(result.stdout)
                        for vuln in vuln_data.get("Results", []):
                            for finding in vuln.get("Misconfigurations", []):
                                vulnerability = {
                                    "file": os.path.relpath(dockerfile, self.repo_path),
                                    "type": "dockerfile",
                                    "severity": finding.get("Severity", "UNKNOWN"),
                                    "title": finding.get("Title", ""),
                                    "description": finding.get("Description", ""),
                                    "remediation": finding.get("Resolution", ""),
                                    "line": finding.get("CauseMetadata", {}).get(
                                        "StartLine", 0
                                    ),
                                }
                                vulnerabilities.append(vulnerability)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Trivy scan timeout for {dockerfile}")
                except Exception as e:
                    logger.error(f"Trivy scan failed for {dockerfile}: {str(e)}")

            # Scan for dependency vulnerabilities
            lock_files = self._find_lock_files()
            for lock_file in lock_files:
                try:
                    result = subprocess.run(
                        ["trivy", "fs", "--format", "json", lock_file],
                        capture_output=True,
                        text=True,
                        cwd=self.repo_path,
                        timeout=300,
                    )

                    if result.returncode == 0:
                        vuln_data = json.loads(result.stdout)
                        for vuln in vuln_data.get("Results", []):
                            for finding in vuln.get("Vulnerabilities", []):
                                vulnerability = {
                                    "file": os.path.relpath(lock_file, self.repo_path),
                                    "type": "dependency",
                                    "severity": finding.get("Severity", "UNKNOWN"),
                                    "title": finding.get("Title", ""),
                                    "description": finding.get("Description", ""),
                                    "package": finding.get("PkgName", ""),
                                    "version": finding.get("InstalledVersion", ""),
                                    "fixed_version": finding.get("FixedVersion", ""),
                                }
                                vulnerabilities.append(vulnerability)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Trivy dependency scan timeout for {lock_file}")
                except Exception as e:
                    logger.error(
                        f"Trivy dependency scan failed for {lock_file}: {str(e)}"
                    )

            self.results["vulnerabilities"] = vulnerabilities
            self.results["summary"]["vulnerabilities_found"] = len(vulnerabilities)

        except Exception as e:
            logger.error(f"Vulnerability scanning failed: {str(e)}")

    async def _scan_code_quality(self) -> None:
        """Scan for code quality issues using Semgrep."""
        try:
            code_issues = []

            # Check if Semgrep is available
            if not self._check_tool_available("semgrep"):
                logger.warning("Semgrep not available, skipping code quality scan")
                self.results["code_quality"] = []
                return

            # Run Semgrep scan
            try:
                result = subprocess.run(
                    ["semgrep", "scan", "--config=auto", "--json", "--no-git-ignore"],
                    capture_output=True,
                    text=True,
                    cwd=self.repo_path,
                    timeout=600,
                )

                if result.returncode in [
                    0,
                    1,
                ]:  # Semgrep returns 1 when issues are found
                    findings = json.loads(result.stdout)
                    for finding in findings.get("results", []):
                        issue = {
                            "file": finding.get("path", ""),
                            "line": finding.get("start", {}).get("line", 0),
                            "severity": finding.get("extra", {}).get(
                                "severity", "UNKNOWN"
                            ),
                            "title": finding.get("extra", {}).get("message", ""),
                            "description": finding.get("extra", {}).get(
                                "description", ""
                            ),
                            "rule_id": finding.get("check_id", ""),
                            "category": finding.get("extra", {})
                            .get("metadata", {})
                            .get("category", "security"),
                        }
                        code_issues.append(issue)

            except subprocess.TimeoutExpired:
                logger.warning("Semgrep scan timeout")
            except Exception as e:
                logger.error(f"Semgrep scan failed: {str(e)}")

            self.results["code_quality"] = code_issues

        except Exception as e:
            logger.error(f"Code quality scanning failed: {str(e)}")

    async def _scan_compliance(self) -> None:
        """Scan for compliance and best practices."""
        try:
            compliance_issues = []

            # Check for common compliance issues
            compliance_checks = [
                self._check_env_files(),
                self._check_hardcoded_paths(),
                self._check_missing_documentation(),
                self._check_security_headers(),
                self._check_docker_best_practices(),
                self._check_kubernetes_best_practices(),
            ]

            for check_result in compliance_checks:
                compliance_issues.extend(check_result)

            self.results["compliance"] = compliance_issues

        except Exception as e:
            logger.error(f"Compliance scanning failed: {str(e)}")

    def _check_env_files(self) -> List[Dict[str, Any]]:
        """Check for environment file issues."""
        issues = []

        # Check for .env files in repository
        env_files = list(Path(self.repo_path).rglob(".env*"))
        for env_file in env_files:
            rel_path = env_file.relative_to(self.repo_path)
            issues.append(
                {
                    "type": "environment_file",
                    "severity": "high",
                    "title": "Environment file found in repository",
                    "description": f"Environment file {rel_path} should not be committed to version control",
                    "file": str(rel_path),
                    "recommendation": "Add .env* to .gitignore and use environment variables or secrets management",
                }
            )

        return issues

    def _check_hardcoded_paths(self) -> List[Dict[str, Any]]:
        """Check for hardcoded paths and URLs."""
        issues = []

        hardcoded_patterns = [
            r"/home/[a-zA-Z0-9_-]+",
            r"/usr/local/",
            r"/opt/",
            r"C:\\",
            r"D:\\",
            r"http://localhost",
            r"https://localhost",
        ]

        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in [".git", "node_modules"]]

            for file in files:
                if file.startswith("."):
                    continue

                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.repo_path)

                if self._is_binary_file(file_path):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        lines = content.split("\n")

                        for line_num, line in enumerate(lines, 1):
                            for pattern in hardcoded_patterns:
                                if re.search(pattern, line, re.IGNORECASE):
                                    issues.append(
                                        {
                                            "type": "hardcoded_path",
                                            "severity": "medium",
                                            "title": "Hardcoded path found",
                                            "description": f"Hardcoded path detected in {rel_path}",
                                            "file": rel_path,
                                            "line": line_num,
                                            "context": line.strip(),
                                            "recommendation": "Use environment variables or configuration files",
                                        }
                                    )
                except Exception:
                    continue

        return issues

    def _check_missing_documentation(self) -> List[Dict[str, Any]]:
        """Check for missing documentation."""
        issues = []

        # Check for README files
        readme_files = list(Path(self.repo_path).glob("README*"))
        if not readme_files:
            issues.append(
                {
                    "type": "missing_documentation",
                    "severity": "medium",
                    "title": "Missing README file",
                    "description": "No README file found in repository root",
                    "recommendation": "Create a comprehensive README.md file",
                }
            )

        # Check for API documentation
        api_docs = list(Path(self.repo_path).rglob("*api*"))
        if not api_docs:
            issues.append(
                {
                    "type": "missing_documentation",
                    "severity": "low",
                    "title": "Missing API documentation",
                    "description": "No API documentation found",
                    "recommendation": "Add API documentation using OpenAPI/Swagger",
                }
            )

        return issues

    def _check_security_headers(self) -> List[Dict[str, Any]]:
        """Check for security headers in web applications."""
        issues = []

        # This would be implemented based on the type of application
        # For now, return empty list
        return issues

    def _check_docker_best_practices(self) -> List[Dict[str, Any]]:
        """Check Docker best practices."""
        issues = []

        dockerfiles = self._find_dockerfiles()
        for dockerfile in dockerfiles:
            rel_path = os.path.relpath(dockerfile, self.repo_path)

            try:
                with open(dockerfile, "r") as f:
                    content = f.read()

                    # Check for root user
                    if "USER root" in content or "RUN useradd" not in content:
                        issues.append(
                            {
                                "type": "docker_best_practice",
                                "severity": "medium",
                                "title": "Docker container running as root",
                                "description": f"Container in {rel_path} should not run as root",
                                "file": rel_path,
                                "recommendation": "Add non-root user and use USER directive",
                            }
                        )

                    # Check for latest tag
                    if "FROM" in content and ":latest" in content:
                        issues.append(
                            {
                                "type": "docker_best_practice",
                                "severity": "medium",
                                "title": "Using latest tag in Dockerfile",
                                "description": f"Dockerfile {rel_path} uses latest tag",
                                "file": rel_path,
                                "recommendation": "Use specific version tags for reproducibility",
                            }
                        )

            except Exception:
                continue

        return issues

    def _check_kubernetes_best_practices(self) -> List[Dict[str, Any]]:
        """Check Kubernetes best practices."""
        issues = []

        k8s_files = list(Path(self.repo_path).rglob("*.yaml")) + list(
            Path(self.repo_path).rglob("*.yml")
        )

        for k8s_file in k8s_files:
            rel_path = k8s_file.relative_to(self.repo_path)

            try:
                with open(k8s_file, "r") as f:
                    content = f.read()

                    # Check for resource limits
                    if "resources:" in content and "limits:" not in content:
                        issues.append(
                            {
                                "type": "kubernetes_best_practice",
                                "severity": "medium",
                                "title": "Missing resource limits",
                                "description": f"Kubernetes manifest {rel_path} missing resource limits",
                                "file": str(rel_path),
                                "recommendation": "Add CPU and memory limits to prevent resource exhaustion",
                            }
                        )

            except Exception:
                continue

        return issues

    def _calculate_summary(self) -> None:
        """Calculate summary statistics."""
        summary = self.results["summary"]

        # Count issues by severity
        for issue_type in ["secrets", "vulnerabilities", "code_quality", "compliance"]:
            for issue in self.results[issue_type]:
                severity = issue.get("severity", "UNKNOWN").lower()
                if severity == "critical":
                    summary["critical_issues"] += 1
                elif severity == "high":
                    summary["high_issues"] += 1
                elif severity == "medium":
                    summary["medium_issues"] += 1
                elif severity == "low":
                    summary["low_issues"] += 1

        summary["total_issues"] = (
            summary["critical_issues"]
            + summary["high_issues"]
            + summary["medium_issues"]
            + summary["low_issues"]
        )

        # Calculate compliance score (0-100)
        total_checks = 10  # Number of compliance checks
        passed_checks = total_checks - len(self.results["compliance"])
        summary["compliance_score"] = max(
            0, min(100, (passed_checks / total_checks) * 100)
        )

    def _classify_secret_severity(self, pattern: str) -> str:
        """Classify secret severity based on pattern."""
        high_severity_patterns = [
            r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
            r"AKIA[0-9A-Z]{16}",
            r"gh[p|o|u|s|r]_[A-Za-z0-9_]{36}",
        ]

        medium_severity_patterns = [
            r'["\']?[aA][pP][iI][-_]?[kK][eE][yY]["\']?',
            r'["\']?[sS][eE][cC][rR][eE][tT]["\']?',
            r"xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}",
        ]

        for high_pattern in high_severity_patterns:
            if re.search(high_pattern, pattern, re.IGNORECASE):
                return "critical"

        for medium_pattern in medium_severity_patterns:
            if re.search(medium_pattern, pattern, re.IGNORECASE):
                return "high"

        return "medium"

    def _get_secret_recommendation(self, pattern: str) -> str:
        """Get recommendation for secret type."""
        if "private key" in pattern.lower():
            return "Remove private key and use proper key management"
        elif "api" in pattern.lower():
            return "Use environment variables or secrets management for API keys"
        elif "password" in pattern.lower():
            return "Use secure password management and avoid hardcoding"
        else:
            return (
                "Remove sensitive information and use secure configuration management"
            )

    def _check_tool_available(self, tool: str) -> bool:
        """Check if a tool is available in the system."""
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _is_binary_file(self, file_path: str) -> bool:
        """Check if a file is binary."""
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                return b"\x00" in chunk
        except Exception:
            return False

    def _find_dockerfiles(self) -> List[str]:
        """Find all Dockerfiles in the repository."""
        dockerfiles = []
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.lower() in ["dockerfile", "dockerfile.dev", "dockerfile.prod"]:
                    dockerfiles.append(os.path.join(root, file))
        return dockerfiles

    def _find_lock_files(self) -> List[str]:
        """Find lock files for dependency scanning."""
        lock_files = []
        lock_patterns = [
            "package-lock.json",
            "yarn.lock",
            "poetry.lock",
            "Pipfile.lock",
            "Gemfile.lock",
        ]

        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file in lock_patterns:
                    lock_files.append(os.path.join(root, file))

        return lock_files
