#!/usr/bin/env python3
"""
Model Creator Router
===================

Router for ML model creation service endpoints.
Integrates with the actual model-creator service.
"""

import logging
import os
import sys
from datetime import datetime

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

# Add the model creator service to the path
sys.path.append("/app/ml-models/model-creator")

try:
    from logic.model_generator import generate_agent_code, generate_model_code
except ImportError:
    # Fallback for when service is not available
    generate_model_code = None
    generate_agent_code = None

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check for model creator service."""
    try:
        if generate_model_code:
            return {
                "status": "healthy",
                "service": "model_creator",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "model_generator": "available",
                    "agent_generator": "available",
                },
            }
        else:
            return {
                "status": "degraded",
                "service": "model_creator",
                "timestamp": datetime.now().isoformat(),
                "error": "Model generator not available",
            }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "service": "model_creator",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@router.post("/generate-model")
async def generate_model(
    file: UploadFile = File(...),
    model_type: str = Form(...),
    target_column: str = Form(...),
    algorithm: str = Form("auto"),
    test_size: int = Form(20),
    random_state: int = Form(42),
    feature_selection: str = Form("auto"),
):
    """Generate a machine learning model from uploaded data."""
    try:
        if not generate_model_code:
            raise HTTPException(
                status_code=503, detail="Model generator service not available"
            )

        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Generate model using the actual service
        output_path = generate_model_code(
            model_type=model_type,
            target_column=target_column,
            algorithm=algorithm,
            data_path=temp_path,
        )

        # Read generated code
        with open(output_path) as f:
            generated_code = f.read()

        # Clean up temp file
        os.remove(temp_path)

        return {
            "status": "success",
            "message": "Model generated successfully",
            "model_type": model_type,
            "algorithm": algorithm,
            "target_column": target_column,
            "output_path": output_path,
            "model_code": generated_code,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Model generation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Model generation failed: {str(e)}"
        )


@router.post("/generate-agent")
async def generate_agent(
    agent_type: str = Form(...),
    capabilities: str = Form("classification,scoring"),
    model_type: str = Form("classification"),
):
    """Generate an AI agent for ML tasks."""
    try:
        if not generate_agent_code:
            raise HTTPException(
                status_code=503, detail="Agent generator service not available"
            )

        # Generate agent using the actual service
        output_path = generate_agent_code(
            agent_type=agent_type, capabilities=capabilities, model_type=model_type
        )

        # Read generated code
        with open(output_path) as f:
            generated_code = f.read()

        return {
            "status": "success",
            "message": "Agent generated successfully",
            "agent_type": agent_type,
            "capabilities": capabilities,
            "model_type": model_type,
            "output_path": output_path,
            "agent_code": generated_code,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Agent generation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Agent generation failed: {str(e)}"
        )


@router.post("/preview")
async def preview_data(file: UploadFile = File(...)):
    """Preview uploaded data file."""
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Read and preview data
        import pandas as pd

        df = pd.read_csv(temp_path)

        # Get preview data
        preview_data = df.head(10).to_dict("records")
        columns = df.columns.tolist()
        shape = df.shape

        # Clean up temp file
        os.remove(temp_path)

        return {
            "status": "success",
            "preview": preview_data,
            "columns": columns,
            "shape": shape,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Data preview failed: {e}")
        raise HTTPException(status_code=500, detail=f"Data preview failed: {str(e)}")


@router.get("/download/{model_path:path}")
async def download_model(model_path: str):
    """Download a generated model file."""
    try:
        full_path = f"/app/ml-models/model-creator/output/{model_path}"

        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="Model file not found")

        return FileResponse(
            path=full_path,
            filename=os.path.basename(full_path),
            media_type="text/plain",
        )

    except Exception as e:
        logger.error(f"Model download failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model download failed: {str(e)}")


@router.get("/models")
async def list_models():
    """List all available models."""
    try:
        models_dir = "/app/ml-models/model-creator/output"

        if not os.path.exists(models_dir):
            return {"models": [], "total": 0}

        models = []
        for filename in os.listdir(models_dir):
            if filename.endswith(".py") or filename.endswith(".pkl"):
                file_path = os.path.join(models_dir, filename)
                stat = os.stat(file_path)
                models.append(
                    {
                        "name": filename,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    }
                )

        return {
            "models": models,
            "total": len(models),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Model listing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model listing failed: {str(e)}")


@router.get("/algorithms")
async def get_algorithms():
    """Get available algorithms for each model type."""
    algorithms = {
        "classifier": [
            {"value": "random_forest", "label": "Random Forest"},
            {"value": "svm", "label": "Support Vector Machine"},
            {"value": "neural_network", "label": "Neural Network"},
            {"value": "logistic_regression", "label": "Logistic Regression"},
        ],
        "regression": [
            {"value": "linear_regression", "label": "Linear Regression"},
            {"value": "random_forest", "label": "Random Forest"},
            {"value": "neural_network", "label": "Neural Network"},
            {"value": "ridge", "label": "Ridge Regression"},
        ],
        "clustering": [
            {"value": "kmeans", "label": "K-Means"},
            {"value": "dbscan", "label": "DBSCAN"},
            {"value": "hierarchical", "label": "Hierarchical Clustering"},
        ],
    }

    return {"algorithms": algorithms, "timestamp": datetime.now().isoformat()}


@router.get("/supported-models")
async def get_supported_models():
    """Get supported model types."""
    models = [
        {"value": "classifier", "label": "Classification"},
        {"value": "regression", "label": "Regression"},
        {"value": "clustering", "label": "Clustering"},
        {"value": "time_series", "label": "Time Series"},
    ]

    return {"supported_models": models, "timestamp": datetime.now().isoformat()}


@router.get("/supported-agents")
async def get_supported_agents():
    """Get supported agent types."""
    agents = [
        {"value": "task_evaluator", "label": "Task Evaluator"},
        {"value": "data_analyzer", "label": "Data Analyzer"},
        {"value": "model_trainer", "label": "Model Trainer"},
    ]

    return {"supported_agents": agents, "timestamp": datetime.now().isoformat()}


@router.delete("/models/{model_name}")
async def delete_model(model_name: str):
    """Delete a model file."""
    try:
        model_path = f"/app/ml-models/model-creator/output/{model_name}"

        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model not found")

        os.remove(model_path)

        return {
            "status": "success",
            "message": f"Model {model_name} deleted successfully",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Model deletion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model deletion failed: {str(e)}")
