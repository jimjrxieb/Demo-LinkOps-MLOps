from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import os

router = APIRouter()


class WorkflowStep(BaseModel):
    name: str
    description: str
    action: str  # script, api_call, manual, decision
    parameters: Dict[str, Any] = {}
    dependencies: List[str] = []
    timeout: Optional[int] = None


class Workflow(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    category: str  # ci_cd, deployment, testing, monitoring, security
    steps: List[WorkflowStep]
    triggers: List[str] = []  # manual, webhook, schedule, event
    tags: List[str] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    execution_count: int = 0
    last_execution: Optional[str] = None


def get_workflows_file():
    """Get the workflows data file path."""
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "workflows.json")


def load_workflows():
    """Load workflows from JSON file."""
    workflows_file = get_workflows_file()
    if os.path.exists(workflows_file):
        try:
            with open(workflows_file, "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_workflows(workflows):
    """Save workflows to JSON file."""
    workflows_file = get_workflows_file()
    with open(workflows_file, "w") as f:
        json.dump(workflows, f, indent=2)


@router.post("/", response_model=Workflow)
async def create_workflow(workflow: Workflow):
    """Create a new workflow."""
    workflows = load_workflows()

    workflow.id = (
        f"workflow_{len(workflows) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    workflow.created_at = datetime.now().isoformat()
    workflow.updated_at = datetime.now().isoformat()

    workflows.append(workflow.dict())
    save_workflows(workflows)

    return workflow


@router.get("/", response_model=List[Workflow])
async def get_workflows(category: Optional[str] = None, tag: Optional[str] = None):
    """Get all workflows with optional filtering."""
    workflows = load_workflows()

    # Apply filters
    if category:
        workflows = [w for w in workflows if w.get("category") == category]
    if tag:
        workflows = [w for w in workflows if tag in w.get("tags", [])]

    return [Workflow(**workflow) for workflow in workflows]


@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str):
    """Get a specific workflow by ID."""
    workflows = load_workflows()

    for workflow in workflows:
        if workflow["id"] == workflow_id:
            return Workflow(**workflow)

    raise HTTPException(status_code=404, detail="Workflow not found")


@router.put("/{workflow_id}", response_model=Workflow)
async def update_workflow(workflow_id: str, workflow_update: Workflow):
    """Update a workflow."""
    workflows = load_workflows()

    for i, workflow in enumerate(workflows):
        if workflow["id"] == workflow_id:
            update_data = workflow_update.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.now().isoformat()
            workflows[i].update(update_data)
            save_workflows(workflows)
            return Workflow(**workflows[i])

    raise HTTPException(status_code=404, detail="Workflow not found")


@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete a workflow."""
    workflows = load_workflows()

    for i, workflow in enumerate(workflows):
        if workflow["id"] == workflow_id:
            workflows.pop(i)
            save_workflows(workflows)
            return {"message": "Workflow deleted successfully"}

    raise HTTPException(status_code=404, detail="Workflow not found")


@router.post("/{workflow_id}/execute")
async def execute_workflow(workflow_id: str):
    """Execute a workflow (simulation for now)."""
    workflows = load_workflows()

    for workflow in workflows:
        if workflow["id"] == workflow_id:
            # Increment execution count
            workflow["execution_count"] += 1
            workflow["last_execution"] = datetime.now().isoformat()
            workflow["updated_at"] = datetime.now().isoformat()
            save_workflows(workflows)

            # For now, just return workflow info
            # In a real implementation, you'd execute the workflow steps
            return {
                "message": "Workflow execution started",
                "workflow_id": workflow_id,
                "workflow_name": workflow["name"],
                "steps_count": len(workflow.get("steps", [])),
                "execution_count": workflow["execution_count"],
                "last_execution": workflow["last_execution"],
            }

    raise HTTPException(status_code=404, detail="Workflow not found")


@router.get("/templates/{category}")
async def get_workflow_templates(category: str):
    """Get workflow templates for a specific category."""
    templates = {
        "ci_cd": {
            "standard_pipeline": {
                "name": "Standard CI/CD Pipeline",
                "description": "Standard CI/CD pipeline with build, test, and deploy",
                "category": "ci_cd",
                "steps": [
                    {
                        "name": "Build",
                        "description": "Build the application",
                        "action": "script",
                        "parameters": {"script": "npm run build"},
                    },
                    {
                        "name": "Test",
                        "description": "Run tests",
                        "action": "script",
                        "parameters": {"script": "npm test"},
                    },
                    {
                        "name": "Deploy",
                        "description": "Deploy to staging",
                        "action": "script",
                        "parameters": {"script": "kubectl apply -f k8s/"},
                    },
                ],
                "triggers": ["webhook"],
                "tags": ["ci_cd", "automation"],
            }
        },
        "deployment": {
            "blue_green": {
                "name": "Blue-Green Deployment",
                "description": "Blue-green deployment workflow",
                "category": "deployment",
                "steps": [
                    {
                        "name": "Deploy Blue",
                        "description": "Deploy to blue environment",
                        "action": "script",
                        "parameters": {"script": "kubectl apply -f blue/"},
                    },
                    {
                        "name": "Health Check",
                        "description": "Verify blue deployment health",
                        "action": "api_call",
                        "parameters": {"url": "/health", "timeout": 30},
                    },
                    {
                        "name": "Switch Traffic",
                        "description": "Switch traffic to blue",
                        "action": "script",
                        "parameters": {
                            "script": 'kubectl patch svc app -p \'{"spec":{"selector":{"version":"blue"}}}\''
                        },
                    },
                ],
                "triggers": ["manual"],
                "tags": ["deployment", "zero_downtime"],
            }
        },
        "security": {
            "security_scan": {
                "name": "Security Scan Workflow",
                "description": "Comprehensive security scanning workflow",
                "category": "security",
                "steps": [
                    {
                        "name": "Vulnerability Scan",
                        "description": "Run vulnerability scanner",
                        "action": "script",
                        "parameters": {"script": "trivy fs ."},
                    },
                    {
                        "name": "SAST Analysis",
                        "description": "Static application security testing",
                        "action": "script",
                        "parameters": {"script": "bandit -r ."},
                    },
                    {
                        "name": "Dependency Check",
                        "description": "Check for vulnerable dependencies",
                        "action": "script",
                        "parameters": {"script": "safety check"},
                    },
                ],
                "triggers": ["schedule", "manual"],
                "tags": ["security", "compliance"],
            }
        },
    }

    return templates.get(category, {})


@router.get("/stats/execution")
async def get_workflow_execution_stats():
    """Get workflow execution statistics."""
    workflows = load_workflows()

    if not workflows:
        return {"total_workflows": 0, "message": "No workflows found"}

    total_executions = sum(w.get("execution_count", 0) for w in workflows)
    avg_executions = total_executions / len(workflows) if workflows else 0

    # Most executed workflows
    most_executed = sorted(
        workflows, key=lambda x: x.get("execution_count", 0), reverse=True
    )[:5]

    # Executions by category
    category_executions = {}
    for workflow in workflows:
        category = workflow.get("category", "unknown")
        executions = workflow.get("execution_count", 0)
        category_executions[category] = (
            category_executions.get(category, 0) + executions
        )

    return {
        "total_workflows": len(workflows),
        "total_executions": total_executions,
        "average_executions_per_workflow": round(avg_executions, 2),
        "most_executed_workflows": most_executed,
        "executions_by_category": category_executions,
    }


@router.get("/")
def list_workflows():
    return {"message": "All workflows (to be implemented)."}


@router.post("/")
def add_workflow(workflow: dict = Body(...)):
    return {"message": "Workflow recorded.", "workflow": workflow}
