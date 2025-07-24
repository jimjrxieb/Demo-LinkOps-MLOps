import json
import logging
import os
import shutil
import subprocess
from datetime import datetime

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class TrainConfig(BaseModel):
    model_name: str
    target_column: str
    features: list
    csv_path: str


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file for model training.

    Args:
        file: CSV file to upload

    Returns:
        dict: Upload result with file path
    """
    try:
        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        # Create uploads directory if it doesn't exist
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(uploads_dir, filename)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"CSV file uploaded: {file_path}")

        return {
            "status": "success",
            "message": "File uploaded successfully",
            "path": file_path,
            "filename": filename,
            "size": os.path.getsize(file_path),
        }

    except Exception as e:
        logger.error(f"Error uploading CSV file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/train-model")
async def train_model(config: TrainConfig):
    """
    Train a machine learning model using the specified configuration.

    Args:
        config: TrainConfig object containing model parameters

    Returns:
        dict: Training result with model metrics
    """
    try:
        logger.info(f"Starting model training for {config.model_name}")

        # Validate that the CSV file exists
        if not os.path.exists(config.csv_path):
            raise HTTPException(
                status_code=400, detail=f"CSV file not found: {config.csv_path}"
            )

        # Build the command to run the trainer
        command = [
            "python3",
            "ml_models/trainer.py",
            "--model",
            config.model_name,
            "--target",
            config.target_column,
            "--features",
            ",".join(config.features),
            "--data",
            config.csv_path,
        ]

        logger.info(f"Executing command: {' '.join(command)}")

        # Run the training process
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, cwd=os.getcwd()
        )

        logger.info(f"Training completed successfully for {config.model_name}")
        logger.info(f"Training output: {result.stdout}")

        # Try to read the model summary
        summary_path = f"ml_models/models/{config.model_name}_summary.json"
        model_summary = {}

        if os.path.exists(summary_path):
            try:
                with open(summary_path, "r") as f:
                    model_summary = json.load(f)
            except Exception as e:
                logger.warning(f"Could not read model summary: {e}")

        return {
            "status": "success",
            "message": f"{config.model_name} trained successfully",
            "model_name": config.model_name,
            "target_column": config.target_column,
            "features_used": config.features,
            "training_output": result.stdout,
            "mae": model_summary.get("mae", 0.0),
            "r2": model_summary.get("r2", 0.0),
            "contractor_recommendations": model_summary.get(
                "contractor_recommendations", []
            ),
        }

    except subprocess.CalledProcessError as e:
        logger.error(f"Training failed with exit code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Training failed: {e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error during training: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


@router.get("/train-model/models")
async def list_models():
    """
    List all trained models.

    Returns:
        list: List of trained models with metadata
    """
    try:
        models_dir = "ml_models/models"
        models = []

        if os.path.exists(models_dir):
            for filename in os.listdir(models_dir):
                if filename.endswith("_summary.json"):
                    model_name = filename.replace("_summary.json", "")
                    summary_path = os.path.join(models_dir, filename)

                    try:
                        with open(summary_path, "r") as f:
                            summary = json.load(f)

                        # Get file modification time
                        mtime = os.path.getmtime(summary_path)
                        date = datetime.fromtimestamp(mtime).isoformat()

                        models.append(
                            {
                                "name": model_name,
                                "target": summary.get("target_column", ""),
                                "features": summary.get("features", []),
                                "mae": summary.get("mae", 0.0),
                                "r2": summary.get("r2", 0.0),
                                "date": date,
                            }
                        )
                    except Exception as e:
                        logger.warning(f"Could not read summary for {model_name}: {e}")

        return models

    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing models: {str(e)}")


@router.get("/train-model/models/{model_name}/summary")
async def get_model_summary(model_name: str):
    """
    Get summary for a specific model.

    Args:
        model_name: Name of the model

    Returns:
        dict: Model summary
    """
    try:
        summary_path = f"ml_models/models/{model_name}_summary.json"

        if not os.path.exists(summary_path):
            raise HTTPException(
                status_code=404, detail=f"Model summary not found: {model_name}"
            )

        with open(summary_path, "r") as f:
            summary = json.load(f)

        return summary

    except Exception as e:
        logger.error(f"Error getting model summary: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error getting model summary: {str(e)}"
        )


@router.get("/train-model/status")
async def get_training_status():
    """
    Get the current status of model training processes.

    Returns:
        dict: Current training status and available models
    """
    try:
        # Check if trainer.py exists
        trainer_path = "ml_models/trainer.py"
        if not os.path.exists(trainer_path):
            return {
                "status": "error",
                "message": "Trainer script not found",
                "available_models": [],
            }

        # Check for trained models
        models_dir = "ml_models/models"
        available_models = []

        if os.path.exists(models_dir):
            for model_file in os.listdir(models_dir):
                if model_file.endswith("_summary.json"):
                    model_name = model_file.replace("_summary.json", "")
                    available_models.append(model_name)

        return {
            "status": "ready",
            "message": "Training service is available",
            "available_models": available_models,
            "trainer_script": trainer_path,
        }

    except Exception as e:
        logger.error(f"Error checking training status: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error checking training status: {str(e)}"
        )


@router.delete("/train-model/{model_name}")
async def delete_model(model_name: str):
    """
    Delete a trained model.

    Args:
        model_name: Name of the model to delete

    Returns:
        dict: Status message indicating deletion result
    """
    try:
        models_dir = "ml_models/models"
        model_path = os.path.join(models_dir, f"{model_name}.pkl")
        summary_path = os.path.join(models_dir, f"{model_name}_summary.json")

        deleted_files = []

        # Delete model file
        if os.path.exists(model_path):
            os.remove(model_path)
            deleted_files.append("model")

        # Delete summary file
        if os.path.exists(summary_path):
            os.remove(summary_path)
            deleted_files.append("summary")

        if not deleted_files:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")

        logger.info(f"Model {model_name} deleted successfully")

        return {
            "status": "success",
            "message": f"Model {model_name} deleted successfully",
            "deleted_files": deleted_files,
        }

    except Exception as e:
        logger.error(f"Error deleting model {model_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting model: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check for the training service.

    Returns:
        dict: Health status of the training service
    """
    try:
        # Check if trainer.py exists
        trainer_path = "ml_models/trainer.py"
        trainer_exists = os.path.exists(trainer_path)

        # Check if models directory exists
        models_dir = "ml_models/models"
        models_dir_exists = os.path.exists(models_dir)

        # Check if uploads directory exists
        uploads_dir = "uploads"
        uploads_dir_exists = os.path.exists(uploads_dir)

        return {
            "status": "healthy" if trainer_exists else "degraded",
            "service": "model_training",
            "trainer_script": {"exists": trainer_exists, "path": trainer_path},
            "models_directory": {"exists": models_dir_exists, "path": models_dir},
            "uploads_directory": {"exists": uploads_dir_exists, "path": uploads_dir},
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "model_training",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
