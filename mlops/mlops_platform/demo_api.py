from datetime import datetime
from typing import Any, Optional, dict, list


def sanitize_cmd(cmd):
    import shlex
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {"ls", "echo", "kubectl", "helm", "python3", "cat", "go", "docker", "npm", "black", "ruff", "yamllint", "prettier", "flake8"}
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Demo data storage (in production, this would be in a database)
DEMO_ORBS = [
    {
        "id": 1,
        "title": "Kubernetes Deployment Best Practices",
        "description": "Standard practices for deploying applications to Kubernetes clusters.",
        "category": "DevOps",
        "steps": [
            "Use declarative manifests (YAML)",
            "Implement health checks (liveness/readiness probes)",
            "Set resource limits and requests",
            "Use ConfigMaps and Secrets for configuration",
            "Implement proper logging and monitoring",
            "Use rolling updates for zero-downtime deployments",
        ],
        "createdAt": "2024-01-15",
        "matchScore": 95,
    },
    {
        "id": 2,
        "title": "API Security Guidelines",
        "description": "Security best practices for RESTful API development.",
        "category": "Security",
        "steps": [
            "Use HTTPS/TLS encryption",
            "Implement proper authentication (JWT, OAuth)",
            "Validate and sanitize all inputs",
            "Use rate limiting to prevent abuse",
            "Implement proper error handling",
            "Log security events and monitor for anomalies",
        ],
        "createdAt": "2024-01-14",
        "matchScore": 88,
    },
    {
        "id": 3,
        "title": "Database Migration Best Practices",
        "description": "Safe practices for database schema changes and migrations.",
        "category": "Database",
        "steps": [
            "Always backup before migrations",
            "Use version control for migration scripts",
            "Test migrations on staging environment",
            "Make migrations reversible when possible",
            "Use transactions for atomicity",
            "Monitor migration performance and impact",
        ],
        "createdAt": "2024-01-13",
        "matchScore": 92,
    },
]


# Request/Response models
class TaskRequest(BaseModel):
    task: str


class TaskResponse(BaseModel):
    task_id: str
    task: str
    status: str
    timestamp: str


class OrbSearchRequest(BaseModel):
    query: str


class OrbSearchResponse(BaseModel):
    results: list[dict[str, Any]]
    total: int
    query: str


class OrbGenerationRequest(BaseModel):
    task: str


class OrbGenerationResponse(BaseModel):
    orb: dict[str, Any]
    generated_by: str
    timestamp: str


class OrbApprovalRequest(BaseModel):
    orb: dict[str, Any]


class OrbApprovalResponse(BaseModel):
    status: str
    orb_id: int
    message: str


class OrbRejectionRequest(BaseModel):
    orb_id: int
    reason: Optional[str] = None


class OrbRejectionResponse(BaseModel):
    status: str
    message: str


@router.post("/task/submit", response_model=TaskResponse)
async def submit_task(request: TaskRequest):
    """
    Submit a new task for processing.
    """
    try:
        task_id = f"task_{datetime.now().timestamp()}"

        return TaskResponse(
            task_id=task_id,
            task=request.task,
            status="submitted",
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error submitting task: {str(e)}"
        ) from e


@router.post("/orbs/search", response_model=OrbSearchResponse)
async def search_orbs(request: OrbSearchRequest):
    """
    Search existing Orbs for matches to the query.
    """
    try:
        query_lower = request.query.lower()
        results = []

        for orb in DEMO_ORBS:
            # Simple keyword matching for demo
            title_match = query_lower in orb["title"].lower()
            desc_match = query_lower in orb["description"].lower()
            category_match = query_lower in orb["category"].lower()

            if title_match or desc_match or category_match:
                # Calculate a simple match score
                score = 0
                if title_match:
                    score += 50
                if desc_match:
                    score += 30
                if category_match:
                    score += 20

                results.append({**orb, "matchScore": min(score, 100)})

        # Sort by match score
        results.sort(key=lambda x: x["matchScore"], reverse=True)

        return OrbSearchResponse(
            results=results, total=len(results), query=request.query
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error searching Orbs: {str(e)}"
        ) from e


@router.post("/orbs/generate", response_model=OrbGenerationResponse)
async def generate_orb(request: OrbGenerationRequest):
    """
    Generate a new Orb using Whis Logic and Grok API.
    """
    try:
        # Check for Grok API key - demo fallback if not available
        import os

        grok_api_key = os.getenv("GROK_API_KEY", "")

        # Demo fallback if no real API key is set
        if not grok_api_key or grok_api_key in [
            "your-grok-api-key-here",
            "demo",
            "test",
            "",
        ]:
            # Return demo message instead of real AI generation
            demo_orb = {
                "id": len(DEMO_ORBS) + 1,
                "title": f"Demo Response for: {request.task}",
                "description": "This is a Grok-simulated response from the demo version. No real model was used.",
                "category": "Demo",
                "steps": [
                    "This is a demo response - no real AI processing occurred",
                    "In the full version, this would use Grok API for actual generation",
                    "The demo version shows the interface without real AI capabilities",
                    "Contact the team for access to the full platform with real AI integration",
                ],
                "createdAt": datetime.now().strftime("%Y-%m-%d"),
                "matchScore": 0,
                "demo_warning": True,
            }

            return OrbGenerationResponse(
                orb=demo_orb,
                generated_by="Demo Mode - No Real AI",
                timestamp=datetime.now().isoformat(),
            )

        # TODO: In production, this would call Whis Logic and Grok API
        # For now, simulate AI generation for demo
        # Extract keywords from task
        task_words = request.task.lower().split()
        keywords = [word for word in task_words if len(word) > 3]

        # Generate a mock Orb
        new_orb = {
            "id": len(DEMO_ORBS) + 1,
            "title": f"Best Practice for: {request.task}",
            "description": f"AI-generated best practice for the submitted task: {request.task}",
            "category": "Generated",
            "steps": [
                "Analyze the task requirements and context",
                "Identify key components and dependencies",
                "Research industry best practices and standards",
                "Design a solution following established patterns",
                "Implement with proper error handling and validation",
                "Test thoroughly in a controlled environment",
                "Document the approach and lessons learned",
                "Monitor and iterate based on feedback",
            ],
            "createdAt": datetime.now().strftime("%Y-%m-%d"),
            "matchScore": 85,
        }

        return OrbGenerationResponse(
            orb=new_orb,
            generated_by="Whis Logic + Grok API",
            timestamp=datetime.now().isoformat(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating Orb: {str(e)}"
        ) from e


@router.post("/orbs/approve", response_model=OrbApprovalResponse)
async def approve_orb(request: OrbApprovalRequest):
    """
    Approve and save a generated Orb to the library.
    """
    try:
        orb = request.orb
        orb_id = len(DEMO_ORBS) + 1

        # Add to demo Orbs (in production, this would save to database)
        new_orb = {
            "id": orb_id,
            "title": orb.get("title", "Approved Orb"),
            "description": orb.get("description", "Approved best practice"),
            "category": orb.get("category", "Approved"),
            "steps": orb.get("steps", []),
            "createdAt": datetime.now().strftime("%Y-%m-%d"),
            "matchScore": 100,
        }

        DEMO_ORBS.append(new_orb)

        return OrbApprovalResponse(
            status="approved",
            orb_id=orb_id,
            message="Orb successfully approved and saved to library",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error approving Orb: {str(e)}"
        ) from e


@router.post("/orbs/reject", response_model=OrbRejectionResponse)
async def reject_orb(request: OrbRejectionRequest):
    """
    Handle Orb rejection (demo limitation).
    """
    try:
        return OrbRejectionResponse(
            status="rejected",
            message="The demo version doesn't support refinement. In the full version, the task would have been sent back through the learning loop with additional input and feedback.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error rejecting Orb: {str(e)}"
        ) from e


@router.get("/orbs/recent")
async def get_recent_orbs():
    """
    Get recent Orbs from the library.
    """
    try:
        # Return the most recent Orbs (last 5)
        recent = DEMO_ORBS[-5:] if len(DEMO_ORBS) > 5 else DEMO_ORBS

        return {"orbs": recent, "total": len(recent)}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching recent Orbs: {str(e)}"
        ) from e


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the demo API.
    """
    return {
        "status": "healthy",
        "service": "demo-api",
        "environment": "demo",
        "timestamp": datetime.now().isoformat(),
        "orbs_count": len(DEMO_ORBS),
    }