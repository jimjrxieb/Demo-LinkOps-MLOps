#!/usr/bin/env python3
"""
Jimmie Logic - Unified Control Brain for LinkOps MLOps Platform
Centralizes all logic, orbs, runes, and models in one location.
"""

import csv
import json
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Import routers
from routers import (daily_router, model_router, orb_router, rune_router,
                     script_router, task_router)

app = FastAPI(
    title="Jimmie Logic - Unified Control Brain",
    description="Centralized logic, orbs, runes, and models for LinkOps MLOps Platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(task_router.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(script_router.router, prefix="/api/scripts", tags=["scripts"])
app.include_router(orb_router.router, prefix="/api/orbs", tags=["orbs"])
app.include_router(rune_router.router, prefix="/api/runes", tags=["runes"])
app.include_router(daily_router.router, prefix="/api/daily", tags=["daily"])
app.include_router(model_router.router, prefix="/api/models", tags=["models"])


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    data_files: Dict[str, int]


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "jimmie_logic",
        "description": "Unified Control Brain for LinkOps MLOps Platform",
        "version": "1.0.0",
        "endpoints": {
            "tasks": "/api/tasks",
            "scripts": "/api/scripts",
            "orbs": "/api/orbs",
            "runes": "/api/runes",
            "daily": "/api/daily",
            "models": "/api/models",
        },
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with data file statistics."""
    data_dir = Path("data")
    data_files = {}

    if data_dir.exists():
        for file_path in data_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        data_files[file_path.stem] = len(data)
                    elif isinstance(data, dict):
                        data_files[file_path.stem] = len(data.keys())
            except BaseException:
                data_files[file_path.stem] = 0

    return HealthResponse(
        status="healthy", service="jimmie_logic", version="1.0.0", data_files=data_files
    )


@app.get("/api/stats")
async def get_stats():
    """Get comprehensive statistics about stored data."""
    stats = {
        "total_tasks": 0,
        "total_runes": 0,
        "total_orbs": 0,
        "total_scripts": 0,
        "total_models": 0,
        "recent_activity": [],
        "top_categories": {},
    }

    # Count items in each data file
    data_dir = Path("data")
    if data_dir.exists():
        for file_path in data_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    if file_path.stem == "tasks":
                        stats["total_tasks"] = (
                            len(data) if isinstance(data, list) else 0
                        )
                    elif file_path.stem == "runes":
                        stats["total_runes"] = (
                            len(data) if isinstance(data, list) else 0
                        )
                    elif file_path.stem == "orbs":
                        stats["total_orbs"] = len(data) if isinstance(data, list) else 0
                    elif file_path.stem == "scripts":
                        stats["total_scripts"] = (
                            len(data) if isinstance(data, list) else 0
                        )
                    elif file_path.stem == "models":
                        stats["total_models"] = (
                            len(data) if isinstance(data, list) else 0
                        )
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Read recent activity from history
    history_file = data_dir / "history.csv"
    if history_file.exists():
        try:
            with open(history_file, "r") as f:
                reader = csv.DictReader(f)
                recent_entries = list(reader)[-10:]  # Last 10 entries
                stats["recent_activity"] = recent_entries
        except Exception as e:
            print(f"Error reading history: {e}")

    return stats


@app.post("/api/classify")
async def classify_input(request: Request):
    """Classify input as MLOps, K8s, Infra, Audit, or Other."""
    data = await request.json()
    content = data.get("content", "").lower()

    classification = {"type": "other", "confidence": 0.0, "tags": []}

    # Simple keyword-based classification
    mlops_keywords = [
        "mlops",
        "model",
        "training",
        "whis",
        "pipeline",
        "data",
        "ml",
        "ai",
    ]
    k8s_keywords = [
        "kubernetes",
        "k8s",
        "pod",
        "deployment",
        "service",
        "namespace",
        "helm",
    ]
    infra_keywords = [
        "terraform",
        "aws",
        "azure",
        "gcp",
        "infrastructure",
        "vpc",
        "subnet",
    ]
    audit_keywords = ["audit", "security", "compliance", "scan", "vulnerability", "cve"]

    mlops_score = sum(1 for keyword in mlops_keywords if keyword in content)
    k8s_score = sum(1 for keyword in k8s_keywords if keyword in content)
    infra_score = sum(1 for keyword in infra_keywords if keyword in content)
    audit_score = sum(1 for keyword in audit_keywords if keyword in content)

    scores = [
        ("mlops", mlops_score),
        ("kubernetes", k8s_score),
        ("infrastructure", infra_score),
        ("audit", audit_score),
    ]

    best_type, best_score = max(scores, key=lambda x: x[1])

    if best_score > 0:
        classification["type"] = best_type
        classification["confidence"] = min(best_score / len(content.split()), 1.0)
        classification["tags"] = [best_type]

    return classification


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
