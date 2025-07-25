#!/usr/bin/env python3
"""
ML Model Creator FastAPI Service
================================

FastAPI service for training and managing machine learning models from CSV data.
"""

import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from logic.model_generator import ModelGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ML Model Creator",
    description="Train and manage machine learning models from CSV data",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model generator
model_generator = ModelGenerator()

# Create temp directory for uploaded files
TEMP_DIR = Path("/tmp/ml_uploads")
TEMP_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "ML Model Creator",
        "status": "running",
        "version": "1.0.0",
        "endpoints": [
            "/analyze-dataset",
            "/train-model",
            "/list-models",
            "/predict",
            "/health",
        ],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ml-model-creator"}


@app.post("/analyze-dataset")
async def analyze_dataset(file: UploadFile):
    """
    Analyze uploaded CSV dataset and return column information.

    Args:
        file: CSV file to analyze

    Returns:
        Dataset analysis with column information and suggested targets
    """
    try:
        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="File must be a CSV")

        # Save uploaded file temporarily
        temp_file_path = TEMP_DIR / f"upload_{file.filename}"
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"📊 Analyzing dataset: {file.filename}")

        # Analyze dataset
        analysis = model_generator.analyze_dataset(str(temp_file_path))

        # Clean up temp file
        temp_file_path.unlink(missing_ok=True)

        if "error" in analysis:
            raise HTTPException(status_code=400, detail=analysis["error"])

        return analysis

    except Exception as e:
        logger.error(f"Dataset analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/train-model")
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
        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="File must be a CSV")

        # Validate model type
        if model_type not in ["classification", "regression"]:
            raise HTTPException(
                status_code=400,
                detail="Model type must be 'classification' or 'regression'",
            )

        # Validate test size
        if not 0.1 <= test_size <= 0.5:
            raise HTTPException(
                status_code=400, detail="Test size must be between 0.1 and 0.5"
            )

        # Save uploaded file temporarily
        temp_file_path = TEMP_DIR / f"train_{file.filename}"
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(
            f"🚀 Training model: {model_type} with {model_name} on {file.filename}"
        )

        # Train model
        result = model_generator.train_model(
            str(temp_file_path), target_column, model_type, model_name, test_size
        )

        # Clean up temp file
        temp_file_path.unlink(missing_ok=True)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except Exception as e:
        logger.error(f"Model training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@app.get("/list-models")
async def list_models():
    """
    List all trained models.

    Returns:
        List of model information
    """
    try:
        models = model_generator.list_models()
        return {"models": models, "count": len(models)}

    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")


@app.post("/predict")
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
        import json

        # Parse features JSON
        try:
            feature_dict = json.loads(features)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in features")

        logger.info(f"🔮 Making prediction with model {model_id}")

        # Make prediction
        result = model_generator.predict(model_id, feature_dict)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.delete("/model/{model_id}")
async def delete_model(model_id: str):
    """
    Delete a trained model.

    Args:
        model_id: ID of the model to delete

    Returns:
        Deletion confirmation
    """
    try:
        # Find model file
        model_files = list(model_generator.models_dir.glob(f"*{model_id}*.pkl"))
        if not model_files:
            raise HTTPException(
                status_code=404, detail=f"Model with ID {model_id} not found"
            )

        # Delete model file
        model_file = model_files[0]
        model_file.unlink()

        logger.info(f"🗑️ Deleted model: {model_id}")

        return {"message": f"Model {model_id} deleted successfully"}

    except Exception as e:
        logger.error(f"Failed to delete model: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete model: {str(e)}")


@app.get("/model/{model_id}/info")
async def get_model_info(model_id: str):
    """
    Get detailed information about a specific model.

    Args:
        model_id: ID of the model

    Returns:
        Model information
    """
    try:
        import joblib

        # Find model file
        model_files = list(model_generator.models_dir.glob(f"*{model_id}*.pkl"))
        if not model_files:
            raise HTTPException(
                status_code=404, detail=f"Model with ID {model_id} not found"
            )

        # Load model data
        model_file = model_files[0]
        model_data = joblib.load(model_file)

        # Extract relevant information
        info = {
            "model_id": model_data.get("model_id"),
            "model_type": model_data.get("model_type"),
            "model_name": model_data.get("model_name"),
            "target_column": model_data.get("target_column"),
            "training_timestamp": model_data.get("training_timestamp"),
            "feature_columns": model_data.get("feature_columns"),
            "feature_count": len(model_data.get("feature_columns", [])),
            "file_size": model_file.stat().st_size,
            "filename": model_file.name,
        }

        return info

    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get model info: {str(e)}"
        )


@app.get("/available-models")
async def get_available_models():
    """
    Get list of available model types and algorithms.

    Returns:
        Available model configurations
    """
    return {
        "classification": {
            "models": list(model_generator.classification_models.keys()),
            "description": "Predicts categorical outcomes",
        },
        "regression": {
            "models": list(model_generator.regression_models.keys()),
            "description": "Predicts continuous values",
        },
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8600, reload=True, log_level="info")
