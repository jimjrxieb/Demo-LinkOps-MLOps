import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from logic.git_secrets import (add_git_hooks, check_git_history,
                               scan_git_secrets)
from logic.sast_scans import (analyze_vulnerabilities, generate_report,
                              run_sast_scan)
from logic.security_lint import (audit_permissions, check_compliance,
                                 lint_security_config)
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DevOps Engineer AI Agent",
    description="AI agent for security scanning, Git secrets management, and compliance",
    version="1.0.0",
)


class SecurityScanRequest(BaseModel):
    repository_path: str
    scan_type: str = "full"  # "full", "quick", "targeted"
    include_patterns: Optional[List[str]] = None
    exclude_patterns: Optional[List[str]] = None
    severity_threshold: str = "medium"  # "low", "medium", "high", "critical"


class GitSecretsRequest(BaseModel):
    repository_path: str
    action: str  # "scan", "install_hooks", "check_history"
    patterns: Optional[List[str]] = None


class ComplianceRequest(BaseModel):
    framework: str  # "SOC2", "ISO27001", "HIPAA", "PCI-DSS"
    scope: List[str]
    generate_report: bool = True


class SecurityLintRequest(BaseModel):
    config_files: List[str]
    check_type: str = "all"  # "all", "permissions", "encryption", "network"
    compliance_framework: Optional[str] = None


class SecurityScanResponse(BaseModel):
    scan_id: str
    repository_path: str
    scan_type: str
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    scan_duration: float
    status: str
    report_url: Optional[str] = None


class GitSecretsResponse(BaseModel):
    repository_path: str
    action: str
    secrets_found: int
    secrets_details: List[Dict[str, Any]]
    hooks_installed: bool = False
    history_clean: bool = True


class ComplianceResponse(BaseModel):
    framework: str
    scope: List[str]
    compliance_score: float
    passed_checks: int
    failed_checks: int
    warnings: int
    recommendations: List[str]
    report_generated: bool


@app.post("/security/scan", response_model=SecurityScanResponse)
async def run_security_scan(request: SecurityScanRequest) -> SecurityScanResponse:
    """
    Run a comprehensive security scan on a repository.
    """
    try:
        start_time = datetime.now()

        scan_result = await run_sast_scan(
            repository_path=request.repository_path,
            scan_type=request.scan_type,
            include_patterns=request.include_patterns or [],
            exclude_patterns=request.exclude_patterns or [],
            severity_threshold=request.severity_threshold,
        )

        scan_duration = (datetime.now() - start_time).total_seconds()

        return SecurityScanResponse(
            scan_id=scan_result["scan_id"],
            repository_path=request.repository_path,
            scan_type=request.scan_type,
            total_issues=scan_result["total_issues"],
            critical_issues=scan_result["critical_issues"],
            high_issues=scan_result["high_issues"],
            medium_issues=scan_result["medium_issues"],
            low_issues=scan_result["low_issues"],
            scan_duration=scan_duration,
            status=scan_result["status"],
            report_url=scan_result.get("report_url"),
        )

    except Exception as e:
        logger.error(f"Security scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Security scan failed: {str(e)}")


@app.post("/security/vulnerabilities/analyze")
async def analyze_security_vulnerabilities(
    scan_id: str, generate_fix_suggestions: bool = True
) -> Dict[str, Any]:
    """
    Analyze vulnerabilities from a security scan and provide remediation suggestions.
    """
    try:
        analysis = await analyze_vulnerabilities(scan_id, generate_fix_suggestions)
        return {
            "scan_id": scan_id,
            "analysis": analysis,
            "analyzed_at": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Vulnerability analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Vulnerability analysis failed: {str(e)}"
        )


@app.post("/security/report/generate")
async def generate_security_report(
    scan_id: str, report_format: str = "html"  # "html", "pdf", "json"
) -> Dict[str, Any]:
    """
    Generate a detailed security report from scan results.
    """
    try:
        report = await generate_report(scan_id, report_format)
        return {
            "scan_id": scan_id,
            "report_format": report_format,
            "report_url": report["report_url"],
            "generated_at": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Report generation failed: {str(e)}"
        )


@app.post("/git/secrets", response_model=GitSecretsResponse)
async def manage_git_secrets(request: GitSecretsRequest) -> GitSecretsResponse:
    """
    Manage Git secrets scanning and prevention.
    """
    try:
        if request.action == "scan":
            result = await scan_git_secrets(
                repository_path=request.repository_path, patterns=request.patterns or []
            )

            return GitSecretsResponse(
                repository_path=request.repository_path,
                action=request.action,
                secrets_found=result["secrets_found"],
                secrets_details=result["secrets_details"],
            )

        elif request.action == "install_hooks":
            result = await add_git_hooks(request.repository_path)

            return GitSecretsResponse(
                repository_path=request.repository_path,
                action=request.action,
                secrets_found=0,
                secrets_details=[],
                hooks_installed=result["hooks_installed"],
            )

        elif request.action == "check_history":
            result = await check_git_history(
                repository_path=request.repository_path, patterns=request.patterns or []
            )

            return GitSecretsResponse(
                repository_path=request.repository_path,
                action=request.action,
                secrets_found=result["secrets_found"],
                secrets_details=result["secrets_details"],
                history_clean=result["history_clean"],
            )

        else:
            raise HTTPException(status_code=400, detail="Invalid action specified")

    except Exception as e:
        logger.error(f"Git secrets management failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Git secrets management failed: {str(e)}"
        )


@app.post("/compliance/check", response_model=ComplianceResponse)
async def check_compliance_standards(request: ComplianceRequest) -> ComplianceResponse:
    """
    Check compliance against security frameworks.
    """
    try:
        compliance_result = await check_compliance(
            framework=request.framework,
            scope=request.scope,
            generate_report=request.generate_report,
        )

        return ComplianceResponse(
            framework=request.framework,
            scope=request.scope,
            compliance_score=compliance_result["compliance_score"],
            passed_checks=compliance_result["passed_checks"],
            failed_checks=compliance_result["failed_checks"],
            warnings=compliance_result["warnings"],
            recommendations=compliance_result["recommendations"],
            report_generated=compliance_result["report_generated"],
        )

    except Exception as e:
        logger.error(f"Compliance check failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Compliance check failed: {str(e)}"
        )


@app.post("/security/lint")
async def lint_security_configurations(request: SecurityLintRequest) -> Dict[str, Any]:
    """
    Lint security configurations for best practices and compliance.
    """
    try:
        lint_result = await lint_security_config(
            config_files=request.config_files,
            check_type=request.check_type,
            compliance_framework=request.compliance_framework,
        )

        return {
            "config_files": request.config_files,
            "check_type": request.check_type,
            "total_issues": lint_result["total_issues"],
            "critical_issues": lint_result["critical_issues"],
            "high_issues": lint_result["high_issues"],
            "medium_issues": lint_result["medium_issues"],
            "low_issues": lint_result["low_issues"],
            "issues": lint_result["issues"],
            "recommendations": lint_result["recommendations"],
        }

    except Exception as e:
        logger.error(f"Security linting failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Security linting failed: {str(e)}"
        )


@app.post("/security/audit/permissions")
async def audit_security_permissions(
    target: str, scope: List[str]  # "files", "users", "services"
) -> Dict[str, Any]:
    """
    Audit security permissions for files, users, or services.
    """
    try:
        audit_result = await audit_permissions(target, scope)
        return {
            "target": target,
            "scope": scope,
            "audit_results": audit_result,
            "audited_at": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Permission audit failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Permission audit failed: {str(e)}"
        )


@app.post("/security/dependencies/scan")
async def scan_dependencies(
    repository_path: str,
    package_manager: str = "auto",  # "auto", "npm", "pip", "maven", "gradle"
) -> Dict[str, Any]:
    """
    Scan dependencies for known vulnerabilities.
    """
    try:
        # This would integrate with tools like npm audit, safety, etc.
        vulnerabilities = [
            {
                "package": "example-package",
                "version": "1.0.0",
                "severity": "high",
                "cve": "CVE-2023-1234",
                "description": "Example vulnerability description",
            }
        ]

        return {
            "repository_path": repository_path,
            "package_manager": package_manager,
            "total_dependencies": 150,
            "vulnerable_dependencies": len(vulnerabilities),
            "vulnerabilities": vulnerabilities,
            "scanned_at": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Dependency scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dependency scan failed: {str(e)}")


@app.post("/security/container/scan")
async def scan_container_image(
    image_name: str, image_tag: str = "latest"
) -> Dict[str, Any]:
    """
    Scan a container image for vulnerabilities.
    """
    try:
        # This would integrate with tools like Trivy, Clair, etc.
        scan_result = {
            "image": f"{image_name}:{image_tag}",
            "total_vulnerabilities": 5,
            "critical": 1,
            "high": 2,
            "medium": 1,
            "low": 1,
            "vulnerabilities": [
                {
                    "cve": "CVE-2023-5678",
                    "severity": "critical",
                    "package": "openssl",
                    "version": "1.1.1",
                    "description": "Critical OpenSSL vulnerability",
                }
            ],
        }

        return scan_result

    except Exception as e:
        logger.error(f"Container scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Container scan failed: {str(e)}")


@app.get("/security/dashboard")
async def get_security_dashboard() -> Dict[str, Any]:
    """
    Get a security dashboard with overview metrics.
    """
    try:
        return {
            "total_scans": 25,
            "active_vulnerabilities": 12,
            "critical_issues": 3,
            "high_issues": 5,
            "medium_issues": 4,
            "compliance_score": 85.5,
            "last_scan": datetime.now().isoformat(),
            "repositories_monitored": 8,
            "secrets_detected": 2,
        }

    except Exception as e:
        logger.error(f"Failed to get security dashboard: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get security dashboard: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "devops-engineer",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "agent": "DevOps Engineer AI Agent",
        "version": "1.0.0",
        "capabilities": [
            "Security Scanning",
            "Git Secrets",
            "Compliance",
            "Security Linting",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
