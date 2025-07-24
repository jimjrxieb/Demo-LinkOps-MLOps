import logging
import os
import subprocess

from fastapi import APIRouter, HTTPException, Request
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


@router.post("/api/train-model")
async def train_model(config: TrainConfig):
    """
    Train a machine learning model using the specified configuration.

    Args:
        config: TrainConfig object containing model parameters

    Returns:
        dict: Status and message indicating training result
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
            "ml_models/trainer.py",  # <-- Add this next
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
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd(),  # Ensure we're in the right directory
        )

        logger.info(f"Training completed successfully for {config.model_name}")
        logger.info(f"Training output: {result.stdout}")

        return {
            "status": "success",
            "message": f"{config.model_name} trained successfully",
            "model_name": config.model_name,
            "target_column": config.target_column,
            "features_used": config.features,
            "training_output": result.stdout,
        }

    except subprocess.CalledProcessError as e:
        logger.error(f"Training failed with exit code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Training failed: {e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error during training: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


@router.get("/api/train-model/status")
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

        # Check for trained models (this would depend on your model storage structure)
        models_dir = "ml_models/trained_models"
        available_models = []

        if os.path.exists(models_dir):
            for model_file in os.listdir(models_dir):
                if model_file.endswith((".pkl", ".joblib", ".h5", ".pb")):
                    available_models.append(model_file)

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


@router.delete("/api/train-model/{model_name}")
async def delete_model(model_name: str):
    """
    Delete a trained model.

    Args:
        model_name: Name of the model to delete

    Returns:
        dict: Status message indicating deletion result
    """
    try:
        models_dir = "ml_models/trained_models"
        model_path = os.path.join(models_dir, model_name)

        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")

        os.remove(model_path)
        logger.info(f"Model {model_name} deleted successfully")

        return {
            "status": "success",
            "message": f"Model {model_name} deleted successfully",
        }

    except Exception as e:
        logger.error(f"Error deleting model {model_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting model: {str(e)}")
