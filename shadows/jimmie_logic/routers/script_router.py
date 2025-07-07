"""
Script Router - Manages CLI workflows and infrastructure scripts
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

router = APIRouter()


class ScriptCreate(BaseModel):
    name: str
    description: str
    category: str  # cli, infrastructure, kubernetes, security, automation
    content: str
    language: str = "bash"  # bash, python, yaml, json, etc.
    tags: List[str] = []
    usage_examples: List[str] = []
    dependencies: List[str] = []


class ScriptUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[List[str]] = None
    usage_examples: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None


class ScriptResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    content: str
    language: str
    tags: List[str]
    usage_examples: List[str]
    dependencies: List[str]
    created_at: str
    updated_at: str
    usage_count: int = 0


def get_scripts_file():
    """Get the scripts data file path."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir / "scripts.json"


def load_scripts() -> List[Dict]:
    """Load scripts from JSON file."""
    scripts_file = get_scripts_file()
    if scripts_file.exists():
        try:
            with open(scripts_file, "r") as f:
                return json.load(f)
        except BaseException:
            return []
    return []


def save_scripts(scripts: List[Dict]):
    """Save scripts to JSON file."""
    scripts_file = get_scripts_file()
    with open(scripts_file, "w") as f:
        json.dump(scripts, f, indent=2)


@router.post("/", response_model=ScriptResponse)
async def create_script(script: ScriptCreate):
    """Create a new script."""
    scripts = load_scripts()

    script_id = f"script_{len(scripts) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    new_script = {
        "id": script_id,
        "name": script.name,
        "description": script.description,
        "category": script.category,
        "content": script.content,
        "language": script.language,
        "tags": script.tags,
        "usage_examples": script.usage_examples,
        "dependencies": script.dependencies,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "usage_count": 0,
    }

    scripts.append(new_script)
    save_scripts(scripts)

    return ScriptResponse(**new_script)


@router.get("/", response_model=List[ScriptResponse])
async def get_scripts(
    category: Optional[str] = None,
    language: Optional[str] = None,
    tag: Optional[str] = None,
):
    """Get all scripts with optional filtering."""
    scripts = load_scripts()

    # Apply filters
    if category:
        scripts = [s for s in scripts if s.get("category") == category]
    if language:
        scripts = [s for s in scripts if s.get("language") == language]
    if tag:
        scripts = [s for s in scripts if tag in s.get("tags", [])]

    return [ScriptResponse(**script) for script in scripts]


@router.get("/{script_id}", response_model=ScriptResponse)
async def get_script(script_id: str):
    """Get a specific script by ID."""
    scripts = load_scripts()

    for script in scripts:
        if script["id"] == script_id:
            return ScriptResponse(**script)

    raise HTTPException(status_code=404, detail="Script not found")


@router.put("/{script_id}", response_model=ScriptResponse)
async def update_script(script_id: str, script_update: ScriptUpdate):
    """Update a script."""
    scripts = load_scripts()

    for script in scripts:
        if script["id"] == script_id:
            # Update fields
            update_data = script_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                script[key] = value

            script["updated_at"] = datetime.now().isoformat()
            save_scripts(scripts)

            return ScriptResponse(**script)

    raise HTTPException(status_code=404, detail="Script not found")


@router.delete("/{script_id}")
async def delete_script(script_id: str):
    """Delete a script."""
    scripts = load_scripts()

    for i, script in enumerate(scripts):
        if script["id"] == script_id:
            scripts.pop(i)
            save_scripts(scripts)
            return {"message": "Script deleted successfully"}

    raise HTTPException(status_code=404, detail="Script not found")


@router.post("/{script_id}/execute")
async def execute_script(script_id: str, request: Request):
    """Execute a script (simulation for now)."""
    scripts = load_scripts()

    for script in scripts:
        if script["id"] == script_id:
            # Increment usage count
            script["usage_count"] += 1
            script["updated_at"] = datetime.now().isoformat()
            save_scripts(scripts)

            # For now, just return the script content
            # In a real implementation, you'd execute the script
            return {
                "message": "Script execution simulated",
                "script_id": script_id,
                "script_name": script["name"],
                "content": script["content"],
                "usage_count": script["usage_count"],
            }

    raise HTTPException(status_code=404, detail="Script not found")


@router.get("/templates/{category}")
async def get_script_templates(category: str):
    """Get script templates for a specific category."""
    templates = {
        "kubernetes": {
            "deploy": """#!/bin/bash
# Deploy application to Kubernetes
kubectl apply -f k8s/
kubectl rollout status deployment/app-name
echo "Deployment completed successfully"
""",
            "scale": """#!/bin/bash
# Scale deployment
kubectl scale deployment $DEPLOYMENT_NAME --replicas=$REPLICAS
kubectl rollout status deployment/$DEPLOYMENT_NAME
echo "Scaled to $REPLICAS replicas"
""",
            "logs": """#!/bin/bash
# Get logs from pods
kubectl logs -f deployment/$DEPLOYMENT_NAME --tail=100
""",
        },
        "infrastructure": {
            "terraform_init": """#!/bin/bash
# Initialize Terraform
terraform init
terraform plan
echo "Terraform initialized and planned"
""",
            "terraform_apply": """#!/bin/bash
# Apply Terraform changes
terraform apply -auto-approve
echo "Infrastructure deployed"
""",
        },
        "security": {
            "scan": """#!/bin/bash
# Security scan
trivy fs .
echo "Security scan completed"
""",
            "audit": """#!/bin/bash
# Audit compliance
kubectl get pods -o yaml | kubesec scan -
echo "Compliance audit completed"
""",
        },
    }

    return templates.get(category, {})


@router.get("/stats/popular")
async def get_popular_scripts():
    """Get most popular scripts by usage count."""
    scripts = load_scripts()

    # Sort by usage count
    popular_scripts = sorted(
        scripts, key=lambda x: x.get("usage_count", 0), reverse=True
    )

    return [ScriptResponse(**script) for script in popular_scripts[:10]]
