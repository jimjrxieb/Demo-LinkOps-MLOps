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
Orb Router - Manages best practices and workflow templates
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()


class OrbCreate(BaseModel):
    name: str
    description: str
    category: str  # ci_cd, security, monitoring, deployment, testing
    content: str  # YAML content
    version: str = "1.0.0"
    tags: List[str] = []
    author: Optional[str] = None
    dependencies: List[str] = []
    usage_instructions: str = ""


class OrbUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    version: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    dependencies: Optional[List[str]] = None
    usage_instructions: Optional[str] = None


class OrbResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    content: str
    version: str
    tags: List[str]
    author: Optional[str]
    dependencies: List[str]
    usage_instructions: str
    created_at: str
    updated_at: str
    usage_count: int = 0
    rating: float = 0.0


def get_orbs_file():
    """Get the orbs data file path."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir / "orbs.json"


def load_orbs() -> List[Dict]:
    """Load orbs from JSON file."""
    orbs_file = get_orbs_file()
    if orbs_file.exists():
        try:
            with open(orbs_file, "r") as f:
                return json.load(f)
        except BaseException:
            return []
    return []


def save_orbs(orbs: List[Dict]):
    """Save orbs to JSON file."""
    orbs_file = get_orbs_file()
    with open(orbs_file, "w") as f:
        json.dump(orbs, f, indent=2)


@router.post("/", response_model=OrbResponse)
async def create_orb(orb: OrbCreate):
    """Create a new orb."""
    orbs = load_orbs()

    orb_id = f"orb_{len(orbs) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    new_orb = {
        "id": orb_id,
        "name": orb.name,
        "description": orb.description,
        "category": orb.category,
        "content": orb.content,
        "version": orb.version,
        "tags": orb.tags,
        "author": orb.author,
        "dependencies": orb.dependencies,
        "usage_instructions": orb.usage_instructions,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "usage_count": 0,
        "rating": 0.0,
    }

    orbs.append(new_orb)
    save_orbs(orbs)

    return OrbResponse(**new_orb)


@router.get("/", response_model=List[OrbResponse])
async def get_orbs(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    author: Optional[str] = None,
):
    """Get all orbs with optional filtering."""
    orbs = load_orbs()

    # Apply filters
    if category:
        orbs = [o for o in orbs if o.get("category") == category]
    if tag:
        orbs = [o for o in orbs if tag in o.get("tags", [])]
    if author:
        orbs = [o for o in orbs if o.get("author") == author]

    return [OrbResponse(**orb) for orb in orbs]


@router.get("/{orb_id}", response_model=OrbResponse)
async def get_orb(orb_id: str):
    """Get a specific orb by ID."""
    orbs = load_orbs()

    for orb in orbs:
        if orb["id"] == orb_id:
            return OrbResponse(**orb)

    raise HTTPException(status_code=404, detail="Orb not found")


@router.put("/{orb_id}", response_model=OrbResponse)
async def update_orb(orb_id: str, orb_update: OrbUpdate):
    """Update an orb."""
    orbs = load_orbs()

    for orb in orbs:
        if orb["id"] == orb_id:
            # Update fields
            update_data = orb_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                orb[key] = value

            orb["updated_at"] = datetime.now().isoformat()
            save_orbs(orbs)

            return OrbResponse(**orb)

    raise HTTPException(status_code=404, detail="Orb not found")


@router.delete("/{orb_id}")
async def delete_orb(orb_id: str):
    """Delete an orb."""
    orbs = load_orbs()

    for i, orb in enumerate(orbs):
        if orb["id"] == orb_id:
            orbs.pop(i)
            save_orbs(orbs)
            return {"message": "Orb deleted successfully"}

    raise HTTPException(status_code=404, detail="Orb not found")


@router.post("/{orb_id}/use")
async def use_orb(orb_id: str):
    """Mark an orb as used (increment usage count)."""
    orbs = load_orbs()

    for orb in orbs:
        if orb["id"] == orb_id:
            orb["usage_count"] += 1
            orb["updated_at"] = datetime.now().isoformat()
            save_orbs(orbs)

            return {
                "message": "Orb usage recorded",
                "orb_id": orb_id,
                "orb_name": orb["name"],
                "usage_count": orb["usage_count"],
            }

    raise HTTPException(status_code=404, detail="Orb not found")


@router.post("/{orb_id}/rate")
async def rate_orb(orb_id: str, request: Request):
    """Rate an orb (1-5 stars)."""
    data = await request.json()
    rating = data.get("rating", 0)

    if not 1 <= rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    orbs = load_orbs()

    for orb in orbs:
        if orb["id"] == orb_id:
            # Simple average rating calculation
            current_rating = orb.get("rating", 0)
            current_count = orb.get("rating_count", 0)

            new_count = current_count + 1
            new_rating = ((current_rating * current_count) + rating) / new_count

            orb["rating"] = round(new_rating, 2)
            orb["rating_count"] = new_count
            orb["updated_at"] = datetime.now().isoformat()
            save_orbs(orbs)

            return {
                "message": "Rating recorded",
                "orb_id": orb_id,
                "orb_name": orb["name"],
                "new_rating": orb["rating"],
                "rating_count": orb["rating_count"],
            }

    raise HTTPException(status_code=404, detail="Orb not found")


@router.get("/templates/{category}")
async def get_orb_templates(category: str):
    """Get orb templates for a specific category."""
    templates = {
        "ci_cd": {
            "security_scan": {
                "name": "Security Scan Orb",
                "description": "Automated security scanning in CI/CD pipeline",
                "content": """name: "Security Scan"
version: "1.0.0"
description: "Automated security scanning for CI/CD pipelines"

workflows:
  security_scan:
    name: "Security Scan"
    description: "Run security scans on code and dependencies"
    steps:
      - name: "Trivy Vulnerability Scanner"
        action: "aquasecurity/trivy-action@v0.18.3"
        with:
          scan-type: "fs"
          scan-ref: "."
          format: "sarif"
          output: "trivy-results.sarif"

      - name: "Bandit Security Linter"
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-results.json

      - name: "Upload Security Results"
        uses: "github/codeql-action/upload-sarif@v3"
        with:
          sarif_file: "trivy-results.sarif"
""",
                "usage_instructions": "Add this orb to your CI/CD pipeline for automated security scanning.",
            }
        },
        "monitoring": {
            "health_check": {
                "name": "Health Check Orb",
                "description": "Application health monitoring",
                "content": """name: "Health Check"
version: "1.0.0"
description: "Application health monitoring and alerting"

workflows:
  health_check:
    name: "Health Check"
    description: "Monitor application health"
    steps:
      - name: "Check Application Health"
        run: |
          curl -f http://localhost:8000/health || exit 1

      - name: "Send Alert on Failure"
        if: failure()
        run: |
          echo "Application health check failed"
          # Add your alerting logic here
""",
                "usage_instructions": "Use this orb to monitor application health and send alerts on failures.",
            }
        },
    }

    return templates.get(category, {})


@router.get("/stats/popular")
async def get_popular_orbs():
    """Get most popular orbs by usage count."""
    orbs = load_orbs()

    # Sort by usage count
    popular_orbs = sorted(orbs, key=lambda x: x.get("usage_count", 0), reverse=True)

    return [OrbResponse(**orb) for orb in popular_orbs[:10]]


@router.get("/stats/highest_rated")
async def get_highest_rated_orbs():
    """Get highest rated orbs."""
    orbs = load_orbs()

    # Sort by rating
    rated_orbs = sorted(orbs, key=lambda x: x.get("rating", 0), reverse=True)

    return [OrbResponse(**orb) for orb in rated_orbs[:10]]
