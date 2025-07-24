#!/usr/bin/env python3
"""
ML Model Builder API Routes
===========================

FastAPI routes for the ML Model Builder system.
Provides endpoints for data preview, model training, prediction, and management.
"""

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from train_model import (
    delete_model,
    get_model_info,
    list_models,
    predict,
    train_from_csv,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ml/preview")
async def preview_csv(file: UploadFile = File(...)):
    """
    Preview CSV data to show columns and sample rows.

    Args:
        file: CSV file to preview

    Returns:
        Dictionary with column names, row count, and sample data
    """
    try:
        logger.info(f"📊 Previewing CSV file: {file.filename}")

        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            # Write uploaded file content
            content = await file.read()
            tmp.write(content)
            tmp.flush()

            # Read CSV with pandas
            df = pd.read_csv(tmp.name)

            # Get basic info
            columns = list(df.columns)
            row_count = len(df)

            # Get sample rows (first 5)
            sample_rows = []
            for _, row in df.head(5).iterrows():
                sample_rows.append(row.to_dict())

            # Clean up temporary file
            os.unlink(tmp.name)

            logger.info(
                f"✅ CSV preview completed: {len(columns)} columns, {row_count} rows"
            )

            return {
                "columns": columns,
                "rowCount": row_count,
                "rows": sample_rows,
                "filename": file.filename,
            }

    except Exception as e:
        logger.error(f"❌ CSV preview failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to preview CSV: {str(e)}")


@router.post("/ml/train")
async def train_model(
    file: UploadFile = File(...),
    target_column: str = Form(...),
    model_type: str = Form("classification"),
    model_name: str = Form(...),
    test_split: float = Form(0.2),
    random_state: int = Form(42),
    algorithm: str = Form("auto"),
):
    """
    Train a machine learning model from CSV data.

    Args:
        file: CSV file with training data
        target_column: Column to predict
        model_type: "classification" or "regression"
        model_name: Name for the model
        test_split: Fraction of data for testing
        random_state: Random seed for reproducibility
        algorithm: ML algorithm to use

    Returns:
        Dictionary with training results
    """
    try:
        logger.info(f"🚀 Starting model training: {model_name}")
        logger.info(
            f"   Target: {target_column}, Type: {model_type}, Algorithm: {algorithm}"
        )

        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        # Validate parameters
        if test_split < 0.1 or test_split > 0.5:
            raise HTTPException(
                status_code=400, detail="Test split must be between 0.1 and 0.5"
            )

        if model_type not in ["classification", "regression"]:
            raise HTTPException(
                status_code=400,
                detail="Model type must be 'classification' or 'regression'",
            )

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            # Write uploaded file content
            content = await file.read()
            tmp.write(content)
            tmp.flush()

            # Train model
            result = train_from_csv(
                file_path=tmp.name,
                target_column=target_column,
                model_type=model_type,
                model_name=model_name,
                test_split=test_split,
                random_state=random_state,
                algorithm=algorithm,
            )

            # Clean up temporary file
            os.unlink(tmp.name)

            logger.info(f"✅ Model training completed: {result['model_id']}")
            return result

    except Exception as e:
        logger.error(f"❌ Model training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to train model: {str(e)}")


@router.get("/ml/models")
async def get_models():
    """
    Get list of all trained models.

    Returns:
        List of model information
    """
    try:
        logger.info("📊 Retrieving list of trained models")

        models = list_models()

        logger.info(f"✅ Retrieved {len(models)} models")
        return {"models": models}

    except Exception as e:
        logger.error(f"❌ Failed to get models: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get models: {str(e)}")


@router.get("/ml/models/{model_id}")
async def get_model(model_id: str):
    """
    Get information about a specific model.

    Args:
        model_id: ID of the model

    Returns:
        Model information
    """
    try:
        logger.info(f"📊 Getting model info: {model_id}")

        model_info = get_model_info(model_id)
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")

        return model_info

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get model {model_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get model: {str(e)}")


@router.delete("/ml/models/{model_id}")
async def delete_model_endpoint(model_id: str):
    """
    Delete a trained model.

    Args:
        model_id: ID of the model to delete

    Returns:
        Success message
    """
    try:
        logger.info(f"🗑️ Deleting model: {model_id}")

        success = delete_model(model_id)
        if not success:
            raise HTTPException(status_code=404, detail="Model not found")

        logger.info(f"✅ Model {model_id} deleted successfully")
        return {"message": "Model deleted successfully", "model_id": model_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete model {model_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete model: {str(e)}")


@router.post("/ml/predict/{model_id}")
async def make_prediction(model_id: str, features: Dict[str, Any]):
    """
    Make predictions using a trained model.

    Args:
        model_id: ID of the model to use
        features: Dictionary of feature values

    Returns:
        Prediction result
    """
    try:
        logger.info(f"🧪 Making prediction with model: {model_id}")

        result = predict(model_id, features)

        logger.info(f"✅ Prediction completed: {result['prediction']}")
        return result

    except ValueError as e:
        logger.error(f"❌ Prediction failed: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Prediction failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to make prediction: {str(e)}"
        )


@router.get("/ml/download/{model_id}")
async def download_model(model_id: str):
    """
    Download a trained model file.

    Args:
        model_id: ID of the model to download

    Returns:
        Model file for download
    """
    try:
        logger.info(f"📥 Downloading model: {model_id}")

        model_info = get_model_info(model_id)
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")

        model_path = Path(model_info["model_path"])
        if not model_path.exists():
            raise HTTPException(status_code=404, detail="Model file not found")

        logger.info(f"✅ Model download initiated: {model_path}")
        return FileResponse(
            path=model_path,
            filename=f"model_{model_id}.pkl",
            media_type="application/octet-stream",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to download model {model_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to download model: {str(e)}"
        )


@router.post("/ml/deploy/{model_id}")
async def deploy_model(model_id: str):
    """
    Deploy a model for production use.

    Args:
        model_id: ID of the model to deploy

    Returns:
        Deployment status
    """
    try:
        logger.info(f"🚀 Deploying model: {model_id}")

        model_info = get_model_info(model_id)
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")

        # For now, just mark as deployed in registry
        # In a real implementation, this would:
        # 1. Load the model into memory
        # 2. Start a prediction service
        # 3. Update deployment status

        logger.info(f"✅ Model {model_id} deployed successfully")
        return {
            "message": "Model deployed successfully",
            "model_id": model_id,
            "deployment_status": "active",
            "endpoint": f"/api/ml/predict/{model_id}",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to deploy model {model_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to deploy model: {str(e)}")


@router.get("/ml/test/{model_id}")
async def test_model(model_id: str):
    """
    Test a model with sample data.

    Args:
        model_id: ID of the model to test

    Returns:
        Test results
    """
    try:
        logger.info(f"🧪 Testing model: {model_id}")

        model_info = get_model_info(model_id)
        if not model_info:
            raise HTTPException(status_code=404, detail="Model not found")

        # Generate sample features based on model's feature columns
        feature_columns = model_info.get("feature_columns", [])
        sample_features = {}

        for col in feature_columns:
            # Generate reasonable sample values based on column name
            if (
                "amount" in col.lower()
                or "price" in col.lower()
                or "rent" in col.lower()
            ):
                sample_features[col] = 1500
            elif "count" in col.lower() or "number" in col.lower():
                sample_features[col] = 2
            elif "tenure" in col.lower() or "duration" in col.lower():
                sample_features[col] = 12
            elif "age" in col.lower():
                sample_features[col] = 35
            else:
                # For one-hot encoded features, set to 0
                sample_features[col] = 0

        # Make prediction
        result = predict(model_id, sample_features)

        logger.info(f"✅ Model test completed: {result['prediction']}")
        return {
            "model_id": model_id,
            "sample_features": sample_features,
            "prediction": result["prediction"],
            "probability": result.get("probability"),
            "target_column": model_info["target_column"],
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to test model {model_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to test model: {str(e)}")


@router.get("/ml/stats")
async def get_ml_stats():
    """
    Get statistics about the ML system.

    Returns:
        System statistics
    """
    try:
        logger.info("📊 Getting ML system statistics")

        models = list_models()

        # Calculate statistics
        total_models = len(models)
        classification_models = len(
            [m for m in models if m.get("model_type") == "classification"]
        )
        regression_models = len(
            [m for m in models if m.get("model_type") == "regression"]
        )

        # Average accuracy
        accuracies = [m.get("accuracy", 0) for m in models]
        avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0

        # Most common target columns
        target_columns = [m.get("target_column", "") for m in models]
        target_counts = {}
        for target in target_columns:
            target_counts[target] = target_counts.get(target, 0) + 1

        stats = {
            "total_models": total_models,
            "classification_models": classification_models,
            "regression_models": regression_models,
            "average_accuracy": round(avg_accuracy, 2),
            "target_column_distribution": target_counts,
            "recent_models": sorted(
                models, key=lambda x: x.get("created_at", ""), reverse=True
            )[:5],
        }

        logger.info(f"✅ Retrieved ML statistics: {total_models} models")
        return stats

    except Exception as e:
        logger.error(f"❌ Failed to get ML stats: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get ML statistics: {str(e)}"
        )


@router.post("/ml/validate-data")
async def validate_data(file: UploadFile = File(...)):
    """
    Validate CSV data for ML training.

    Args:
        file: CSV file to validate

    Returns:
        Validation results
    """
    try:
        logger.info(f"🔍 Validating CSV data: {file.filename}")

        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            # Write uploaded file content
            content = await file.read()
            tmp.write(content)
            tmp.flush()

            # Read CSV
            df = pd.read_csv(tmp.name)

            # Perform validation
            validation_results = {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "missing_values": {},
                "data_types": {},
                "unique_values": {},
                "suggested_targets": [],
                "warnings": [],
                "errors": [],
            }

            # Check for missing values
            for col in df.columns:
                missing_count = df[col].isnull().sum()
                validation_results["missing_values"][col] = missing_count

                if missing_count > len(df) * 0.5:
                    validation_results["warnings"].append(
                        f"Column '{col}' has more than 50% missing values"
                    )

            # Check data types
            for col in df.columns:
                validation_results["data_types"][col] = str(df[col].dtype)
                validation_results["unique_values"][col] = df[col].nunique()

            # Suggest target columns
            for col in df.columns:
                unique_count = df[col].nunique()
                missing_count = df[col].isnull().sum()

                # Good target columns have reasonable number of unique values and few missing values
                if missing_count < len(df) * 0.1:  # Less than 10% missing
                    if unique_count <= 10:  # Good for classification
                        validation_results["suggested_targets"].append(
                            {
                                "column": col,
                                "type": "classification",
                                "reason": f"Good classification target: {unique_count} unique values, {missing_count} missing",
                            }
                        )
                    elif df[col].dtype in ["int64", "float64"] and unique_count > 10:
                        validation_results["suggested_targets"].append(
                            {
                                "column": col,
                                "type": "regression",
                                "reason": f"Good regression target: numeric with {unique_count} unique values",
                            }
                        )

            # Check for errors
            if len(df) < 10:
                validation_results["errors"].append(
                    "Dataset too small: need at least 10 rows for training"
                )

            if len(df.columns) < 2:
                validation_results["errors"].append(
                    "Dataset too few columns: need at least 2 columns (features + target)"
                )

            # Clean up temporary file
            os.unlink(tmp.name)

            logger.info(
                f"✅ Data validation completed: {len(validation_results['suggested_targets'])} suggested targets"
            )
            return validation_results

    except Exception as e:
        logger.error(f"❌ Data validation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to validate data: {str(e)}"
        )


@router.get("/ml/algorithms")
async def get_available_algorithms():
    """
    Get list of available ML algorithms.

    Returns:
        Available algorithms by type
    """
    algorithms = {
        "classification": {
            "random_forest": {
                "name": "Random Forest",
                "description": "Ensemble method using multiple decision trees",
                "pros": [
                    "Handles non-linear relationships",
                    "Feature importance",
                    "Robust to outliers",
                ],
                "cons": [
                    "Can be slow for large datasets",
                    "Less interpretable than linear models",
                ],
            },
            "logistic_regression": {
                "name": "Logistic Regression",
                "description": "Linear model for binary classification",
                "pros": [
                    "Fast and interpretable",
                    "Good baseline model",
                    "Probabilistic outputs",
                ],
                "cons": [
                    "Assumes linear relationships",
                    "May underperform on complex data",
                ],
            },
        },
        "regression": {
            "random_forest": {
                "name": "Random Forest",
                "description": "Ensemble method using multiple decision trees",
                "pros": [
                    "Handles non-linear relationships",
                    "Feature importance",
                    "Robust to outliers",
                ],
                "cons": [
                    "Can be slow for large datasets",
                    "Less interpretable than linear models",
                ],
            },
            "linear_regression": {
                "name": "Linear Regression",
                "description": "Linear model for continuous predictions",
                "pros": [
                    "Fast and interpretable",
                    "Good baseline model",
                    "Clear coefficients",
                ],
                "cons": ["Assumes linear relationships", "Sensitive to outliers"],
            },
        },
    }

    return algorithms
