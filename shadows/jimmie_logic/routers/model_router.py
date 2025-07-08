"""
Model Router - Manages AI models and ML artifacts
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()


class ModelCreate(BaseModel):
    name: str
    description: str
    category: str  # ml_model, ai_agent, data_pipeline, evaluation
    version: str = "1.0.0"
    framework: str  # tensorflow, pytorch, scikit-learn, custom
    model_type: str  # classification, regression, nlp, vision, reinforcement
    tags: List[str] = []
    author: Optional[str] = None
    dependencies: List[str] = []
    performance_metrics: Dict[str, float] = {}
    model_path: Optional[str] = None
    config: Dict[str, Any] = {}


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    version: Optional[str] = None
    framework: Optional[str] = None
    model_type: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    dependencies: Optional[List[str]] = None
    performance_metrics: Optional[Dict[str, float]] = None
    model_path: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class ModelResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    version: str
    framework: str
    model_type: str
    tags: List[str]
    author: Optional[str]
    dependencies: List[str]
    performance_metrics: Dict[str, float]
    model_path: Optional[str]
    config: Dict[str, Any]
    created_at: str
    updated_at: str
    usage_count: int = 0
    accuracy: float = 0.0


def get_models_file():
    """Get the models data file path."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir / "models.json"


def load_models() -> List[Dict]:
    """Load models from JSON file."""
    models_file = get_models_file()
    if models_file.exists():
        try:
            with open(models_file, "r") as f:
                return json.load(f)
        except BaseException:
            return []
    return []


def save_models(models: List[Dict]):
    """Save models to JSON file."""
    models_file = get_models_file()
    with open(models_file, "w") as f:
        json.dump(models, f, indent=2)


@router.post("/", response_model=ModelResponse)
async def create_model(model: ModelCreate):
    """Create a new model."""
    models = load_models()

    model_id = f"model_{len(models) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    new_model = {
        "id": model_id,
        "name": model.name,
        "description": model.description,
        "category": model.category,
        "version": model.version,
        "framework": model.framework,
        "model_type": model.model_type,
        "tags": model.tags,
        "author": model.author,
        "dependencies": model.dependencies,
        "performance_metrics": model.performance_metrics,
        "model_path": model.model_path,
        "config": model.config,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "usage_count": 0,
        "accuracy": model.performance_metrics.get("accuracy", 0.0),
    }

    models.append(new_model)
    save_models(models)

    return ModelResponse(**new_model)


@router.get("/", response_model=List[ModelResponse])
async def get_models(
    category: Optional[str] = None,
    framework: Optional[str] = None,
    model_type: Optional[str] = None,
    tag: Optional[str] = None,
    author: Optional[str] = None,
):
    """Get all models with optional filtering."""
    models = load_models()

    # Apply filters
    if category:
        models = [m for m in models if m.get("category") == category]
    if framework:
        models = [m for m in models if m.get("framework") == framework]
    if model_type:
        models = [m for m in models if m.get("model_type") == model_type]
    if tag:
        models = [m for m in models if tag in m.get("tags", [])]
    if author:
        models = [m for m in models if m.get("author") == author]

    return [ModelResponse(**model) for model in models]


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: str):
    """Get a specific model by ID."""
    models = load_models()

    for model in models:
        if model["id"] == model_id:
            return ModelResponse(**model)

    raise HTTPException(status_code=404, detail="Model not found")


@router.put("/{model_id}", response_model=ModelResponse)
async def update_model(model_id: str, model_update: ModelUpdate):
    """Update a model."""
    models = load_models()

    for model in models:
        if model["id"] == model_id:
            # Update fields
            update_data = model_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                model[key] = value

            model["updated_at"] = datetime.now().isoformat()

            # Update accuracy if performance metrics changed
            if "performance_metrics" in update_data:
                model["accuracy"] = update_data["performance_metrics"].get(
                    "accuracy", 0.0
                )

            save_models(models)

            return ModelResponse(**model)

    raise HTTPException(status_code=404, detail="Model not found")


@router.delete("/{model_id}")
async def delete_model(model_id: str):
    """Delete a model."""
    models = load_models()

    for i, model in enumerate(models):
        if model["id"] == model_id:
            models.pop(i)
            save_models(models)
            return {"message": "Model deleted successfully"}

    raise HTTPException(status_code=404, detail="Model not found")


@router.post("/{model_id}/predict")
async def predict_with_model(model_id: str, request: Request):
    """Make a prediction with a model (simulation for now)."""
    models = load_models()

    for model in models:
        if model["id"] == model_id:
            # Increment usage count
            model["usage_count"] += 1
            model["updated_at"] = datetime.now().isoformat()
            save_models(models)

            # For now, just return a simulated prediction
            # In a real implementation, you'd load and run the model
            return {
                "message": "Prediction simulated",
                "model_id": model_id,
                "model_name": model["name"],
                "model_type": model["model_type"],
                "prediction": "simulated_result",
                "confidence": 0.85,
                "usage_count": model["usage_count"],
            }

    raise HTTPException(status_code=404, detail="Model not found")


@router.post("/{model_id}/evaluate")
async def evaluate_model(model_id: str, request: Request):
    """Evaluate a model with new data."""
    data = await request.json()
    data.get("test_data", [])
    data.get("metrics", ["accuracy", "precision", "recall"])

    models = load_models()

    for model in models:
        if model["id"] == model_id:
            # Simulate evaluation
            # In a real implementation, you'd run the model on test data
            evaluation_results = {
                "accuracy": 0.92,
                "precision": 0.89,
                "recall": 0.94,
                "f1_score": 0.91,
            }

            # Update model performance metrics
            model["performance_metrics"].update(evaluation_results)
            model["accuracy"] = evaluation_results["accuracy"]
            model["updated_at"] = datetime.now().isoformat()
            save_models(models)

            return {
                "message": "Model evaluation completed",
                "model_id": model_id,
                "model_name": model["name"],
                "evaluation_results": evaluation_results,
                "updated_metrics": model["performance_metrics"],
            }

    raise HTTPException(status_code=404, detail="Model not found")


@router.get("/templates/{category}")
async def get_model_templates(category: str):
    """Get model templates for a specific category."""
    templates = {
        "ml_model": {
            "classification": {
                "name": "Classification Model Template",
                "description": "Standard classification model with scikit-learn",
                "framework": "scikit-learn",
                "model_type": "classification",
                "config": {
                    "algorithm": "RandomForest",
                    "n_estimators": 100,
                    "max_depth": 10,
                    "random_state": 42,
                },
                "dependencies": ["scikit-learn", "pandas", "numpy"],
                "performance_metrics": {
                    "accuracy": 0.0,
                    "precision": 0.0,
                    "recall": 0.0,
                    "f1_score": 0.0,
                },
            },
            "regression": {
                "name": "Regression Model Template",
                "description": "Standard regression model with scikit-learn",
                "framework": "scikit-learn",
                "model_type": "regression",
                "config": {"algorithm": "LinearRegression", "fit_intercept": True},
                "dependencies": ["scikit-learn", "pandas", "numpy"],
                "performance_metrics": {
                    "r2_score": 0.0,
                    "mean_squared_error": 0.0,
                    "mean_absolute_error": 0.0,
                },
            },
        },
        "ai_agent": {
            "task_classifier": {
                "name": "Task Classification Agent",
                "description": "AI agent for classifying MLOps tasks",
                "framework": "custom",
                "model_type": "nlp",
                "config": {
                    "model": "bert-base-uncased",
                    "max_length": 512,
                    "batch_size": 16,
                },
                "dependencies": ["transformers", "torch", "numpy"],
                "performance_metrics": {"accuracy": 0.0, "classification_report": {}},
            }
        },
    }

    return templates.get(category, {})


@router.get("/stats/performance")
async def get_model_performance_stats():
    """Get performance statistics for all models."""
    models = load_models()

    if not models:
        return {"total_models": 0, "message": "No models found"}

    # Calculate average accuracy by category
    category_accuracies = {}
    framework_accuracies = {}

    for model in models:
        category = model.get("category", "unknown")
        framework = model.get("framework", "unknown")
        accuracy = model.get("accuracy", 0.0)

        if category not in category_accuracies:
            category_accuracies[category] = []
        category_accuracies[category].append(accuracy)

        if framework not in framework_accuracies:
            framework_accuracies[framework] = []
        framework_accuracies[framework].append(accuracy)

    # Calculate averages
    avg_category_accuracies = {
        category: round(sum(accuracies) / len(accuracies), 3)
        for category, accuracies in category_accuracies.items()
    }

    avg_framework_accuracies = {
        framework: round(sum(accuracies) / len(accuracies), 3)
        for framework, accuracies in framework_accuracies.items()
    }

    return {
        "total_models": len(models),
        "average_accuracy_by_category": avg_category_accuracies,
        "average_accuracy_by_framework": avg_framework_accuracies,
        "top_performing_models": sorted(
            models, key=lambda x: x.get("accuracy", 0.0), reverse=True
        )[:5],
    }


@router.get("/stats/usage")
async def get_model_usage_stats():
    """Get usage statistics for all models."""
    models = load_models()

    if not models:
        return {"total_models": 0, "message": "No models found"}

    # Most used models
    most_used = sorted(models, key=lambda x: x.get("usage_count", 0), reverse=True)[:10]

    # Usage by category
    category_usage = {}
    for model in models:
        category = model.get("category", "unknown")
        usage = model.get("usage_count", 0)
        category_usage[category] = category_usage.get(category, 0) + usage

    return {
        "total_models": len(models),
        "total_usage": sum(model.get("usage_count", 0) for model in models),
        "most_used_models": most_used,
        "usage_by_category": category_usage,
    }
