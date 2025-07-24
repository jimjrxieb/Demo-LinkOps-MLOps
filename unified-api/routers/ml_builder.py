#!/usr/bin/env python3
"""
ML Builder Router
================

Router for ML Model Builder service endpoints.
Proxies requests to the model-builder service.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter()

# ML Builder service configuration
ML_BUILDER_BASE_URL = "http://model-builder:8600"
ML_BUILDER_TIMEOUT = 300  # 5 minutes for model training


@router.get("/health")
async def health_check():
    """Health check for ML Builder service."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{ML_BUILDER_BASE_URL}/health")
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "service": "ml-builder",
                    "timestamp": datetime.now().isoformat(),
                    "details": response.json(),
                }
            else:
                return {
                    "status": "degraded",
                    "service": "ml-builder",
                    "timestamp": datetime.now().isoformat(),
                    "error": f"Service returned status {response.status_code}",
                }
    except Exception as e:
        logger.error(f"ML Builder health check failed: {e}")
        return {
            "status": "error",
            "service": "ml-builder",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@router.post("/analyze-dataset")
async def analyze_dataset(file: UploadFile):
    """
    Analyze uploaded CSV dataset and return column information.

    Args:
        file: CSV file to analyze

    Returns:
        Dataset analysis with column information and suggested targets
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            files = {"file": (file.filename, file.file, file.content_type)}
            response = await client.post(
                f"{ML_BUILDER_BASE_URL}/analyze-dataset", files=files
            )

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Request timeout")
    except Exception as e:
        logger.error(f"Dataset analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/train-model")
async def train_model(
    file: UploadFile,
    target_column: str = Form(...),
    model_type: str = Form("classification"),
    model_name: str = Form("random_forest"),
    test_size: float = Form(0.2),
):
    """
    Train a machine learning model from uploaded CSV data.

    Args:
        file: CSV file with training data
        target_column: Name of the target column
        model_type: 'classification' or 'regression'
        model_name: Name of the model algorithm
        test_size: Fraction of data for testing

    Returns:
        Training results with metrics and model information
    """
    try:
        async with httpx.AsyncClient(timeout=ML_BUILDER_TIMEOUT) as client:
            files = {"file": (file.filename, file.file, file.content_type)}
            data = {
                "target_column": target_column,
                "model_type": model_type,
                "model_name": model_name,
                "test_size": str(test_size),
            }

            response = await client.post(
                f"{ML_BUILDER_BASE_URL}/train-model", files=files, data=data
            )

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408, detail="Training timeout - model may still be training"
        )
    except Exception as e:
        logger.error(f"Model training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("/list-models")
async def list_models():
    """
    List all trained models.

    Returns:
        List of model information
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{ML_BUILDER_BASE_URL}/list-models")

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")


@router.post("/predict")
async def predict(
    model_id: str = Form(...), features: str = Form(...)  # JSON string of features
):
    """
    Make predictions using a trained model.

    Args:
        model_id: ID of the model to use
        features: JSON string of feature values

    Returns:
        Prediction result
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            data = {"model_id": model_id, "features": features}

            response = await client.post(f"{ML_BUILDER_BASE_URL}/predict", data=data)

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.delete("/model/{model_id}")
async def delete_model(model_id: str):
    """
    Delete a trained model.

    Args:
        model_id: ID of the model to delete

    Returns:
        Deletion confirmation
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(f"{ML_BUILDER_BASE_URL}/model/{model_id}")

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Failed to delete model: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete model: {str(e)}")


@router.get("/model/{model_id}/info")
async def get_model_info(model_id: str):
    """
    Get detailed information about a specific model.

    Args:
        model_id: ID of the model

    Returns:
        Model information
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{ML_BUILDER_BASE_URL}/model/{model_id}/info")

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get model info: {str(e)}"
        )


@router.get("/available-models")
async def get_available_models():
    """
    Get list of available model types and algorithms.

    Returns:
        Available model configurations
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{ML_BUILDER_BASE_URL}/available-models")

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Failed to get available models: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get available models: {str(e)}"
        )


@router.get("/stats")
async def get_ml_builder_stats():
    """
    Get ML Builder service statistics.

    Returns:
        Service statistics and status
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get models list for stats
            models_response = await client.get(f"{ML_BUILDER_BASE_URL}/list-models")
            models_data = (
                models_response.json()
                if models_response.status_code == 200
                else {"models": [], "count": 0}
            )

            # Get available models
            available_response = await client.get(
                f"{ML_BUILDER_BASE_URL}/available-models"
            )
            available_data = (
                available_response.json()
                if available_response.status_code == 200
                else {}
            )

            return {
                "service": "ml-builder",
                "timestamp": datetime.now().isoformat(),
                "models": {
                    "total_count": models_data.get("count", 0),
                    "by_type": {
                        "classification": len(
                            [
                                m
                                for m in models_data.get("models", [])
                                if m.get("model_type") == "classification"
                            ]
                        ),
                        "regression": len(
                            [
                                m
                                for m in models_data.get("models", [])
                                if m.get("model_type") == "regression"
                            ]
                        ),
                    },
                },
                "available_algorithms": available_data,
                "status": "operational",
            }

    except Exception as e:
        logger.error(f"Failed to get ML Builder stats: {e}")
        return {
            "service": "ml-builder",
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "error": str(e),
        }
