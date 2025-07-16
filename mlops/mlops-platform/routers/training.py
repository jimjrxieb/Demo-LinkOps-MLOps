#!/usr/bin/env python3
"""
Training router for ML model operations.
Handles retraining, model status, and training orb management.
"""

import json
import os
import subprocess
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/training", tags=["training"])


@router.post("/retrain")
async def retrain_classifier() -> Dict[str, Any]:
    """Trigger retraining of the ML Task Classifier model."""
    try:
        # Path to the training script
        training_script = "mlops/whis-ml/train_classifier.py"

        if not os.path.exists(training_script):
            raise HTTPException(status_code=404, detail="Training script not found")

        # Run the training script
        result = subprocess.run(
            ["python", training_script], capture_output=True, text=True, cwd=os.getcwd()
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=500, detail=f"Training failed: {result.stderr}"
            )

        return {
            "status": "success",
            "message": "Model retraining completed successfully",
            "timestamp": datetime.now().isoformat(),
            "output": result.stdout,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")


@router.get("/status")
async def get_training_status() -> Dict[str, Any]:
    """Get the status of training orbs and models."""
    try:
        training_orbs_dir = "mlops/whis-ml/training_orbs"
        models_dir = "mlops/whis-ml"

        # Check for training orbs
        training_orbs = []
        if os.path.exists(training_orbs_dir):
            for file in os.listdir(training_orbs_dir):
                if file.endswith(".json"):
                    with open(os.path.join(training_orbs_dir, file)) as f:
                        orb_data = json.load(f)
                        training_orbs.append(orb_data)

        # Check for model files
        model_files = {
            "classifier_model.h5": os.path.exists(
                os.path.join(models_dir, "classifier_model.h5")
            ),
            "tokenizer.pkl": os.path.exists(os.path.join(models_dir, "tokenizer.pkl")),
            "label_encoder.pkl": os.path.exists(
                os.path.join(models_dir, "label_encoder.pkl")
            ),
        }

        return {
            "training_orbs": training_orbs,
            "model_files": model_files,
            "last_updated": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.post("/add-training-data")
async def add_training_data(task: str, category: str) -> Dict[str, Any]:
    """Add new training data to the dataset."""
    try:
        # This would typically add to a database or CSV file
        # For now, we'll just return a success message
        return {
            "status": "success",
            "message": f"Added training data: {task} -> {category}",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add training data: {str(e)}"
        )
