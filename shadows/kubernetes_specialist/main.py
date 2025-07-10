import logging
from datetime import datetime
from typing import Any, Dict, List, Optional


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


from fastapi import FastAPI, HTTPException
from logic.deployment_fix import diagnose_deployment, fix_deployment, scale_deployment
from logic.helm import install_chart, list_releases, uninstall_chart, upgrade_chart
from logic.rbac import check_permissions, create_role, create_role_binding
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kubernetes Specialist AI Agent",
    description="AI agent for Kubernetes operations, Helm management, and RBAC",
    version="1.0.0",
)


class HelmRequest(BaseModel):
    release_name: str
    chart_name: str
    namespace: str = "default"
    values: Optional[Dict[str, Any]] = None
    version: Optional[str] = None
    wait: bool = True
    timeout: Optional[int] = 300


class RBACRequest(BaseModel):
    name: str
    namespace: str = "default"
    role_type: str  # "Role", "ClusterRole"
    rules: List[Dict[str, Any]]
    subjects: Optional[List[Dict[str, str]]] = None


class DeploymentRequest(BaseModel):
    name: str
    namespace: str = "default"
    action: str  # "diagnose", "fix", "scale"
    replicas: Optional[int] = None
    image: Optional[str] = None


class HelmResponse(BaseModel):
    release_name: str
    status: str
    namespace: str
    chart_version: Optional[str] = None
    app_version: Optional[str] = None
    last_deployed: Optional[str] = None
    description: Optional[str] = None


class RBACResponse(BaseModel):
    name: str
    namespace: str
    role_type: str
    created: bool
    rules_count: int
    subjects_count: Optional[int] = None


class DeploymentResponse(BaseModel):
    name: str
    namespace: str
    status: str
    replicas: int
    available_replicas: int
    ready_replicas: int
    issues: List[str]
    fixes_applied: List[str]


@app.post("/helm/install", response_model=HelmResponse)
async def install_helm_chart(request: HelmRequest) -> HelmResponse:
    """
    Install a Helm chart in the specified namespace.
    """
    try:
        result = await install_chart(
            release_name=request.release_name,
            chart_name=request.chart_name,
            namespace=request.namespace,
            values=request.values or {},
            version=request.version,
            wait=request.wait,
            timeout=request.timeout,
        )

        return HelmResponse(
            release_name=request.release_name,
            status=result["status"],
            namespace=request.namespace,
            chart_version=result.get("chart_version"),
            app_version=result.get("app_version"),
            last_deployed=result.get("last_deployed"),
            description=result.get("description"),
        )

    except Exception as e:
        logger.error(f"Helm install failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Helm install failed: {str(e)}")


@app.post("/helm/upgrade", response_model=HelmResponse)
async def upgrade_helm_chart(request: HelmRequest) -> HelmResponse:
    """
    Upgrade an existing Helm chart.
    """
    try:
        result = await upgrade_chart(
            release_name=request.release_name,
            chart_name=request.chart_name,
            namespace=request.namespace,
            values=request.values or {},
            version=request.version,
            wait=request.wait,
            timeout=request.timeout,
        )

        return HelmResponse(
            release_name=request.release_name,
            status=result["status"],
            namespace=request.namespace,
            chart_version=result.get("chart_version"),
            app_version=result.get("app_version"),
            last_deployed=result.get("last_deployed"),
            description=result.get("description"),
        )

    except Exception as e:
        logger.error(f"Helm upgrade failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Helm upgrade failed: {str(e)}")


@app.delete("/helm/uninstall/{release_name}")
async def uninstall_helm_chart(
    release_name: str, namespace: str = "default"
) -> Dict[str, Any]:
    """
    Uninstall a Helm chart.
    """
    try:
        result = await uninstall_chart(release_name, namespace)
        return {
            "release_name": release_name,
            "namespace": namespace,
            "status": "uninstalled",
            "message": result.get("message", "Chart uninstalled successfully"),
        }

    except Exception as e:
        logger.error(f"Helm uninstall failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Helm uninstall failed: {str(e)}")


@app.get("/helm/releases")
async def list_helm_releases(
    namespace: Optional[str] = None,
) -> Dict[str, List[HelmResponse]]:
    """
    List all Helm releases in the cluster or namespace.
    """
    try:
        releases = await list_releases(namespace)
        return {
            "releases": [
                HelmResponse(
                    release_name=release["name"],
                    status=release["status"],
                    namespace=release["namespace"],
                    chart_version=release.get("chart_version"),
                    app_version=release.get("app_version"),
                    last_deployed=release.get("last_deployed"),
                    description=release.get("description"),
                )
                for release in releases
            ]
        }

    except Exception as e:
        logger.error(f"Failed to list Helm releases: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to list releases: {str(e)}"
        )


@app.post("/rbac/create", response_model=RBACResponse)
async def create_rbac_resources(request: RBACRequest) -> RBACResponse:
    """
    Create RBAC resources (Role/ClusterRole and RoleBinding/ClusterRoleBinding).
    """
    try:
        result = await create_role(
            name=request.name,
            namespace=request.namespace,
            role_type=request.role_type,
            rules=request.rules,
            subjects=request.subjects or [],
        )

        return RBACResponse(
            name=request.name,
            namespace=request.namespace,
            role_type=request.role_type,
            created=result["created"],
            rules_count=len(request.rules),
            subjects_count=len(request.subjects) if request.subjects else None,
        )

    except Exception as e:
        logger.error(f"RBAC creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"RBAC creation failed: {str(e)}")


@app.post("/rbac/binding")
async def create_role_binding_endpoint(request: RBACRequest) -> Dict[str, Any]:
    """
    Create a RoleBinding or ClusterRoleBinding.
    """
    try:
        result = await create_role_binding(
            name=request.name,
            namespace=request.namespace,
            role_type=request.role_type,
            subjects=request.subjects or [],
        )

        return {
            "name": request.name,
            "namespace": request.namespace,
            "role_type": request.role_type,
            "created": result["created"],
            "subjects_count": len(request.subjects) if request.subjects else 0,
        }

    except Exception as e:
        logger.error(f"Role binding creation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Role binding creation failed: {str(e)}"
        )


@app.post("/rbac/check")
async def check_user_permissions(
    user: str, namespace: str = "default", resource: str = "pods", verb: str = "get"
) -> Dict[str, Any]:
    """
    Check if a user has specific permissions.
    """
    try:
        result = await check_permissions(user, namespace, resource, verb)
        return {
            "user": user,
            "namespace": namespace,
            "resource": resource,
            "verb": verb,
            "allowed": result["allowed"],
            "reason": result.get("reason", ""),
        }

    except Exception as e:
        logger.error(f"Permission check failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Permission check failed: {str(e)}"
        )


@app.post("/deployment/diagnose", response_model=DeploymentResponse)
async def diagnose_deployment_issues(request: DeploymentRequest) -> DeploymentResponse:
    """
    Diagnose issues with a Kubernetes deployment.
    """
    try:
        result = await diagnose_deployment(
            name=request.name, namespace=request.namespace
        )

        return DeploymentResponse(
            name=request.name,
            namespace=request.namespace,
            status=result["status"],
            replicas=result["replicas"],
            available_replicas=result["available_replicas"],
            ready_replicas=result["ready_replicas"],
            issues=result["issues"],
            fixes_applied=[],
        )

    except Exception as e:
        logger.error(f"Deployment diagnosis failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Deployment diagnosis failed: {str(e)}"
        )


@app.post("/deployment/fix", response_model=DeploymentResponse)
async def fix_deployment_issues(request: DeploymentRequest) -> DeploymentResponse:
    """
    Automatically fix common deployment issues.
    """
    try:
        result = await fix_deployment(
            name=request.name, namespace=request.namespace, image=request.image
        )

        return DeploymentResponse(
            name=request.name,
            namespace=request.namespace,
            status=result["status"],
            replicas=result["replicas"],
            available_replicas=result["available_replicas"],
            ready_replicas=result["ready_replicas"],
            issues=result["issues"],
            fixes_applied=result["fixes_applied"],
        )

    except Exception as e:
        logger.error(f"Deployment fix failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deployment fix failed: {str(e)}")


@app.post("/deployment/scale")
async def scale_deployment_endpoint(
    name: str, namespace: str = "default", replicas: int = 1
) -> Dict[str, Any]:
    """
    Scale a deployment to the specified number of replicas.
    """
    try:
        result = await scale_deployment(name, namespace, replicas)
        return {
            "name": name,
            "namespace": namespace,
            "target_replicas": replicas,
            "current_replicas": result["current_replicas"],
            "status": result["status"],
        }

    except Exception as e:
        logger.error(f"Deployment scaling failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Deployment scaling failed: {str(e)}"
        )


@app.get("/cluster/nodes")
async def get_cluster_nodes() -> Dict[str, Any]:
    """
    Get information about cluster nodes.
    """
    try:
        # This would integrate with Kubernetes API
        nodes = [
            {
                "name": "node-1",
                "status": "Ready",
                "cpu_capacity": "4",
                "memory_capacity": "8Gi",
                "cpu_allocatable": "3.5",
                "memory_allocatable": "7Gi",
            },
            {
                "name": "node-2",
                "status": "Ready",
                "cpu_capacity": "4",
                "memory_capacity": "8Gi",
                "cpu_allocatable": "3.2",
                "memory_allocatable": "6.5Gi",
            },
        ]

        return {
            "nodes": nodes,
            "total_nodes": len(nodes),
            "ready_nodes": len([n for n in nodes if n["status"] == "Ready"]),
        }

    except Exception as e:
        logger.error(f"Failed to get cluster nodes: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get cluster nodes: {str(e)}"
        )


@app.get("/cluster/namespaces")
async def get_namespaces() -> Dict[str, List[str]]:
    """
    Get list of namespaces in the cluster.
    """
    try:
        # This would integrate with Kubernetes API
        namespaces = ["default", "kube-system", "kube-public", "kube-node-lease"]
        return {"namespaces": namespaces}

    except Exception as e:
        logger.error(f"Failed to get namespaces: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get namespaces: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "kubernetes-specialist",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "agent": "Kubernetes Specialist AI Agent",
        "version": "1.0.0",
        "capabilities": ["Helm", "RBAC", "Deployment Management"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
