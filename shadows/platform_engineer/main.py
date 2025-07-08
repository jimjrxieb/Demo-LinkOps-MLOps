import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from logic.ci_cd import monitor_pipeline, rollback_deployment, trigger_pipeline
from logic.pipelines import (analyze_pipeline_health, create_pipeline,
                             update_pipeline)
from logic.terraform import apply_terraform, destroy_resources, plan_terraform
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Platform Engineer AI Agent",
    description="AI agent for CI/CD, Terraform, and pipeline management",
    version="1.0.0",
)


class PipelineRequest(BaseModel):
    pipeline_name: str
    repository_url: str
    branch: str = "main"
    environment: str = "production"
    variables: Optional[Dict[str, str]] = None


class TerraformRequest(BaseModel):
    workspace: str
    action: str  # "plan", "apply", "destroy"
    variables: Optional[Dict[str, str]] = None
    target_resources: Optional[List[str]] = None


class PipelineHealthRequest(BaseModel):
    pipeline_id: str
    time_range: str = "7d"  # "1d", "7d", "30d"


class PipelineResponse(BaseModel):
    pipeline_id: str
    status: str
    url: str
    triggered_at: str
    estimated_duration: Optional[int] = None


class TerraformResponse(BaseModel):
    workspace: str
    action: str
    status: str
    plan_output: Optional[str] = None
    applied_resources: Optional[List[str]] = None
    execution_time: float


class HealthResponse(BaseModel):
    pipeline_id: str
    success_rate: float
    avg_duration: float
    failure_points: List[str]
    recommendations: List[str]


@app.post("/pipeline/trigger", response_model=PipelineResponse)
async def trigger_ci_cd_pipeline(request: PipelineRequest) -> PipelineResponse:
    """
    Trigger a CI/CD pipeline for a specific repository and branch.
    """
    try:
        pipeline_id, status, url = await trigger_pipeline(
            name=request.pipeline_name,
            repo_url=request.repository_url,
            branch=request.branch,
            environment=request.environment,
            variables=request.variables or {},
        )

        return PipelineResponse(
            pipeline_id=pipeline_id,
            status=status,
            url=url,
            triggered_at=datetime.now().isoformat(),
            estimated_duration=300,  # 5 minutes default
        )

    except Exception as e:
        logger.error(f"Pipeline trigger failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Pipeline trigger failed: {str(e)}"
        )


@app.get("/pipeline/{pipeline_id}/status")
async def get_pipeline_status(pipeline_id: str) -> Dict[str, Any]:
    """
    Get the current status of a running pipeline.
    """
    try:
        status = await monitor_pipeline(pipeline_id)
        return {
            "pipeline_id": pipeline_id,
            "status": status,
            "checked_at": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@app.post("/pipeline/{pipeline_id}/rollback")
async def rollback_pipeline_deployment(pipeline_id: str) -> Dict[str, Any]:
    """
    Rollback a pipeline deployment to the previous version.
    """
    try:
        rollback_result = await rollback_deployment(pipeline_id)
        return {
            "pipeline_id": pipeline_id,
            "rollback_status": rollback_result,
            "rolled_back_at": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rollback failed: {str(e)}")


@app.post("/terraform/execute", response_model=TerraformResponse)
async def execute_terraform(request: TerraformRequest) -> TerraformResponse:
    """
    Execute Terraform operations (plan, apply, destroy).
    """
    try:
        start_time = datetime.now()

        if request.action == "plan":
            plan_output = await plan_terraform(
                workspace=request.workspace,
                variables=request.variables or {},
                targets=request.target_resources or [],
            )
            return TerraformResponse(
                workspace=request.workspace,
                action=request.action,
                status="planned",
                plan_output=plan_output,
                execution_time=(datetime.now() - start_time).total_seconds(),
            )

        elif request.action == "apply":
            applied_resources = await apply_terraform(
                workspace=request.workspace,
                variables=request.variables or {},
                targets=request.target_resources or [],
            )
            return TerraformResponse(
                workspace=request.workspace,
                action=request.action,
                status="applied",
                applied_resources=applied_resources,
                execution_time=(datetime.now() - start_time).total_seconds(),
            )

        elif request.action == "destroy":
            destroyed_resources = await destroy_resources(
                workspace=request.workspace, targets=request.target_resources or []
            )
            return TerraformResponse(
                workspace=request.workspace,
                action=request.action,
                status="destroyed",
                applied_resources=destroyed_resources,
                execution_time=(datetime.now() - start_time).total_seconds(),
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid Terraform action")

    except Exception as e:
        logger.error(f"Terraform execution failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Terraform execution failed: {str(e)}"
        )


@app.post("/pipeline/health", response_model=HealthResponse)
async def analyze_pipeline_health_endpoint(
    request: PipelineHealthRequest,
) -> HealthResponse:
    """
    Analyze pipeline health and provide recommendations.
    """
    try:
        health_data = await analyze_pipeline_health(
            pipeline_id=request.pipeline_id, time_range=request.time_range
        )

        return HealthResponse(
            pipeline_id=request.pipeline_id,
            success_rate=health_data["success_rate"],
            avg_duration=health_data["avg_duration"],
            failure_points=health_data["failure_points"],
            recommendations=health_data["recommendations"],
        )

    except Exception as e:
        logger.error(f"Pipeline health analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health analysis failed: {str(e)}")


@app.post("/pipeline/create")
async def create_new_pipeline(request: PipelineRequest) -> Dict[str, Any]:
    """
    Create a new CI/CD pipeline configuration.
    """
    try:
        pipeline_config = await create_pipeline(
            name=request.pipeline_name,
            repo_url=request.repository_url,
            branch=request.branch,
            environment=request.environment,
            variables=request.variables or {},
        )

        return {
            "pipeline_name": request.pipeline_name,
            "config": pipeline_config,
            "created_at": datetime.now().isoformat(),
            "status": "created",
        }

    except Exception as e:
        logger.error(f"Pipeline creation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Pipeline creation failed: {str(e)}"
        )


@app.put("/pipeline/{pipeline_name}/update")
async def update_existing_pipeline(
    pipeline_name: str, request: PipelineRequest
) -> Dict[str, Any]:
    """
    Update an existing pipeline configuration.
    """
    try:
        updated_config = await update_pipeline(
            name=pipeline_name,
            repo_url=request.repository_url,
            branch=request.branch,
            environment=request.environment,
            variables=request.variables or {},
        )

        return {
            "pipeline_name": pipeline_name,
            "updated_config": updated_config,
            "updated_at": datetime.now().isoformat(),
            "status": "updated",
        }

    except Exception as e:
        logger.error(f"Pipeline update failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline update failed: {str(e)}")


@app.get("/terraform/workspaces")
async def list_terraform_workspaces() -> Dict[str, List[str]]:
    """
    List available Terraform workspaces.
    """
    try:
        # Placeholder - would integrate with actual Terraform backend
        workspaces = ["dev", "staging", "production", "testing"]
        return {"workspaces": workspaces}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to list workspaces: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "platform-engineer",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "agent": "Platform Engineer AI Agent",
        "version": "1.0.0",
        "capabilities": ["CI/CD", "Terraform", "Pipeline Management"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
