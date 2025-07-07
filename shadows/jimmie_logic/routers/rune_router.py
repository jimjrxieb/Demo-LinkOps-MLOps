"""
Rune Router - Manages reusable solutions and code templates
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

router = APIRouter()


class RuneCreate(BaseModel):
    name: str
    description: str
    category: str  # python, bash, yaml, terraform, kubernetes, docker
    content: str
    language: str
    tags: List[str] = []
    author: Optional[str] = None
    dependencies: List[str] = []
    usage_examples: List[str] = []
    test_cases: List[str] = []


class RuneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    dependencies: Optional[List[str]] = None
    usage_examples: Optional[List[str]] = None
    test_cases: Optional[List[str]] = None


class RuneResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    content: str
    language: str
    tags: List[str]
    author: Optional[str]
    dependencies: List[str]
    usage_examples: List[str]
    test_cases: List[str]
    created_at: str
    updated_at: str
    usage_count: int = 0
    success_rate: float = 0.0


def get_runes_file():
    """Get the runes data file path."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir / "runes.json"


def load_runes() -> List[Dict]:
    """Load runes from JSON file."""
    runes_file = get_runes_file()
    if runes_file.exists():
        try:
            with open(runes_file, "r") as f:
                return json.load(f)
        except BaseException:
            return []
    return []


def save_runes(runes: List[Dict]):
    """Save runes to JSON file."""
    runes_file = get_runes_file()
    with open(runes_file, "w") as f:
        json.dump(runes, f, indent=2)


@router.post("/", response_model=RuneResponse)
async def create_rune(rune: RuneCreate):
    """Create a new rune."""
    runes = load_runes()

    rune_id = f"rune_{len(runes) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    new_rune = {
        "id": rune_id,
        "name": rune.name,
        "description": rune.description,
        "category": rune.category,
        "content": rune.content,
        "language": rune.language,
        "tags": rune.tags,
        "author": rune.author,
        "dependencies": rune.dependencies,
        "usage_examples": rune.usage_examples,
        "test_cases": rune.test_cases,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "usage_count": 0,
        "success_rate": 0.0,
    }

    runes.append(new_rune)
    save_runes(runes)

    return RuneResponse(**new_rune)


@router.get("/", response_model=List[RuneResponse])
async def get_runes(
    category: Optional[str] = None,
    language: Optional[str] = None,
    tag: Optional[str] = None,
    author: Optional[str] = None,
):
    """Get all runes with optional filtering."""
    runes = load_runes()

    # Apply filters
    if category:
        runes = [r for r in runes if r.get("category") == category]
    if language:
        runes = [r for r in runes if r.get("language") == language]
    if tag:
        runes = [r for r in runes if tag in r.get("tags", [])]
    if author:
        runes = [r for r in runes if r.get("author") == author]

    return [RuneResponse(**rune) for rune in runes]


@router.get("/{rune_id}", response_model=RuneResponse)
async def get_rune(rune_id: str):
    """Get a specific rune by ID."""
    runes = load_runes()

    for rune in runes:
        if rune["id"] == rune_id:
            return RuneResponse(**rune)

    raise HTTPException(status_code=404, detail="Rune not found")


@router.put("/{rune_id}", response_model=RuneResponse)
async def update_rune(rune_id: str, rune_update: RuneUpdate):
    """Update a rune."""
    runes = load_runes()

    for rune in runes:
        if rune["id"] == rune_id:
            # Update fields
            update_data = rune_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                rune[key] = value

            rune["updated_at"] = datetime.now().isoformat()
            save_runes(runes)

            return RuneResponse(**rune)

    raise HTTPException(status_code=404, detail="Rune not found")


@router.delete("/{rune_id}")
async def delete_rune(rune_id: str):
    """Delete a rune."""
    runes = load_runes()

    for i, rune in enumerate(runes):
        if rune["id"] == rune_id:
            runes.pop(i)
            save_runes(runes)
            return {"message": "Rune deleted successfully"}

    raise HTTPException(status_code=404, detail="Rune not found")


@router.post("/{rune_id}/execute")
async def execute_rune(rune_id: str, request: Request):
    """Execute a rune (simulation for now)."""
    runes = load_runes()

    for rune in runes:
        if rune["id"] == rune_id:
            # Increment usage count
            rune["usage_count"] += 1
            rune["updated_at"] = datetime.now().isoformat()
            save_runes(runes)

            # For now, just return the rune content
            # In a real implementation, you'd execute the rune
            return {
                "message": "Rune execution simulated",
                "rune_id": rune_id,
                "rune_name": rune["name"],
                "content": rune["content"],
                "language": rune["language"],
                "usage_count": rune["usage_count"],
            }

    raise HTTPException(status_code=404, detail="Rune not found")


@router.post("/{rune_id}/feedback")
async def provide_feedback(rune_id: str, request: Request):
    """Provide feedback on rune success/failure."""
    data = await request.json()
    success = data.get("success", True)
    feedback = data.get("feedback", "")

    runes = load_runes()

    for rune in runes:
        if rune["id"] == rune_id:
            # Update success rate
            current_success = rune.get("success_count", 0)
            current_total = rune.get("total_attempts", 0)

            new_total = current_total + 1
            new_success = current_success + (1 if success else 0)
            new_rate = (new_success / new_total) * 100

            rune["success_count"] = new_success
            rune["total_attempts"] = new_total
            rune["success_rate"] = round(new_rate, 2)
            rune["updated_at"] = datetime.now().isoformat()

            # Store feedback
            if "feedback_history" not in rune:
                rune["feedback_history"] = []

            rune["feedback_history"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "success": success,
                    "feedback": feedback,
                }
            )

            save_runes(runes)

            return {
                "message": "Feedback recorded",
                "rune_id": rune_id,
                "rune_name": rune["name"],
                "new_success_rate": rune["success_rate"],
                "total_attempts": rune["total_attempts"],
            }

    raise HTTPException(status_code=404, detail="Rune not found")


@router.get("/templates/{category}")
async def get_rune_templates(category: str):
    """Get rune templates for a specific category."""
    templates = {
        "python": {
            "api_client": {
                "name": "API Client Rune",
                "description": "Reusable API client for microservices",
                "content": """import requests
import json
from typing import Dict, Any

class APIClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})

    def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()
""",
                "language": "python",
                "usage_examples": [
                    "client = APIClient('https://api.example.com', 'your-api-key')",
                    "data = client.get('/users')",
                    "new_user = client.post('/users', {'name': 'John', 'email': 'john@example.com'})",
                ],
            }},
        "kubernetes": {
            "deployment": {
                "name": "Kubernetes Deployment Rune",
                        "description": "Standard Kubernetes deployment template",
                        "content": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.name }}
  labels:
    app: {{ .Values.name }}
spec:
  replicas: {{ .Values.replicas | default 1 }}
  selector:
    matchLabels:
      app: {{ .Values.name }}
  template:
    metadata:
      labels:
        app: {{ .Values.name }}
    spec:
      containers:
      - name: {{ .Values.name }}
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        ports:
        - containerPort: {{ .Values.service.port }}
        env:
        {{- range .Values.env }}
        - name: {{ .name }}
          value: {{ .value | quote }}
        {{- end }}
        resources:
          requests:
            memory: {{ .Values.resources.requests.memory | default "64Mi" }}
            cpu: {{ .Values.resources.requests.cpu | default "250m" }}
          limits:
            memory: {{ .Values.resources.limits.memory | default "128Mi" }}
            cpu: {{ .Values.resources.limits.cpu | default "500m" }}
""",
                        "language": "yaml",
                        "usage_examples": [
                            "helm install myapp ./chart -f values.yaml",
                            "kubectl apply -f deployment.yaml",
                        ],
            }},
    }

    return templates.get(category, {})


@router.get("/stats/most_successful")
async def get_most_successful_runes():
    """Get most successful runes by success rate."""
    runes = load_runes()

    # Filter runes with at least 5 attempts
    qualified_runes = [r for r in runes if r.get("total_attempts", 0) >= 5]

    # Sort by success rate
    successful_runes = sorted(
        qualified_runes, key=lambda x: x.get("success_rate", 0), reverse=True
    )

    return [RuneResponse(**rune) for rune in successful_runes[:10]]


@router.get("/stats/most_used")
async def get_most_used_runes():
    """Get most used runes by usage count."""
    runes = load_runes()

    # Sort by usage count
    used_runes = sorted(runes, key=lambda x: x.get("usage_count", 0), reverse=True)

    return [RuneResponse(**rune) for rune in used_runes[:10]]
