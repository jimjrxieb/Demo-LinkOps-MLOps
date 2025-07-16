#!/usr/bin/env python3
"""
FastAPI server for the ML Task Classifier orb.
Provides inference endpoints for task classification.
"""

import json
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from infer import predict_category
from pydantic import BaseModel

app = FastAPI(
    title="Whis ML Service",
    description="ML Task Classifier for Whis Smithing",
    version="1.0.0",
)


class TaskRequest(BaseModel):
    task: str


class TaskResponse(BaseModel):
    task: str
    category: str
    confidence: float
    model_version: str = "v1"


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "whis-ml"}


@app.post("/predict", response_model=TaskResponse)
async def predict_task(request: TaskRequest):
    """Predict the category of a given task."""
    try:
        category, confidence = predict_category(request.task)
        return TaskResponse(
            task=request.task, category=category, confidence=float(confidence)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/model-info")
async def get_model_info():
    """Get information about the current model."""
    try:
        with open("training_orbs/orb.ml.task_classifier.v1.json") as f:
            orb_info = json.load(f)

        # Check if model files exist
        model_exists = os.path.exists("classifier_model.h5")
        tokenizer_exists = os.path.exists("tokenizer.pkl")
        encoder_exists = os.path.exists("label_encoder.pkl")

        return {
            "orb_info": orb_info,
            "model_status": {
                "model_file": model_exists,
                "tokenizer_file": tokenizer_exists,
                "encoder_file": encoder_exists,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get model info: {str(e)}"
        )


@app.post("/retrain")
async def trigger_retrain():
    """Trigger model retraining."""
    try:
        # This would typically be done asynchronously
        # For now, we'll just return a success message
        return {"message": "Retraining triggered", "status": "scheduled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
