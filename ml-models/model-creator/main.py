import os
import shutil
import tempfile

from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from logic.model_generator import generate_agent_code, generate_model_code

app = FastAPI(title="ML Model Creator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ml-model-creator"}


@app.post("/generate-model/")
async def generate_model(
    model_type: str = Form(
        ..., description="Type of model: classification, regression, clustering"
    ),
    target_column: str = Form(..., description="Target column name"),
    algorithm: str = Form("auto", description="ML algorithm to use"),
    file: UploadFile = None,
):
    """
    Generate ML model code based on uploaded data and parameters.

    Args:
        model_type: Type of ML model (classification, regression, clustering)
        target_column: Name of the target column
        algorithm: ML algorithm to use (auto, random_forest, svm, neural_network, etc.)
        file: CSV file containing the dataset

    Returns:
        Generated model code and metadata
    """
    try:
        # Handle file upload
        if file:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
                shutil.copyfileobj(file.file, tmp_file)
                data_path = tmp_file.name
        else:
            # Use sample data for demo
            data_path = "/tmp/sample_data.csv"
            # Create sample data if it doesn't exist
            if not os.path.exists(data_path):
                import numpy as np
                import pandas as pd

                sample_data = pd.DataFrame(
                    {
                        "feature1": np.random.randn(100),
                        "feature2": np.random.randn(100),
                        "feature3": np.random.randn(100),
                        "target": np.random.randint(0, 2, 100),
                    }
                )
                sample_data.to_csv(data_path, index=False)

        # Generate model code
        output_path = generate_model_code(
            model_type=model_type,
            target_column=target_column,
            algorithm=algorithm,
            data_path=data_path,
        )

        # Read generated code
        with open(output_path, "r") as f:
            generated_code = f.read()

        return {
            "message": "Model script created successfully",
            "model_type": model_type,
            "algorithm": algorithm,
            "target_column": target_column,
            "output_path": output_path,
            "model_code": generated_code,
            "status": "success",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Model generation failed: {str(e)}"
        )


@app.post("/generate-agent/")
async def generate_agent(
    agent_type: str = Form(
        ..., description="Type of agent: task_evaluator, data_analyzer, model_trainer"
    ),
    capabilities: str = Form(
        "classification,scoring", description="Comma-separated list of capabilities"
    ),
    model_type: str = Form(
        "classification", description="Type of model the agent will work with"
    ),
):
    """
    Generate AI agent code for ML tasks.

    Args:
        agent_type: Type of agent (task_evaluator, data_analyzer, model_trainer)
        capabilities: Comma-separated list of capabilities
        model_type: Type of model the agent will work with

    Returns:
        Generated agent code and metadata
    """
    try:
        # Parse capabilities
        capability_list = [cap.strip() for cap in capabilities.split(",")]

        # Generate agent code
        output_path = generate_agent_code(
            agent_type=agent_type, capabilities=capability_list, model_type=model_type
        )

        # Read generated code
        with open(output_path, "r") as f:
            generated_code = f.read()

        return {
            "message": "Agent script created successfully",
            "agent_type": agent_type,
            "capabilities": capability_list,
            "model_type": model_type,
            "output_path": output_path,
            "agent_code": generated_code,
            "status": "success",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Agent generation failed: {str(e)}"
        )


@app.get("/supported-models")
async def get_supported_models():
    """Get list of supported model types and algorithms."""
    return {
        "model_types": ["classification", "regression", "clustering", "time_series"],
        "algorithms": {
            "classification": [
                "random_forest",
                "svm",
                "neural_network",
                "logistic_regression",
            ],
            "regression": [
                "linear_regression",
                "random_forest",
                "neural_network",
                "xgboost",
            ],
            "clustering": ["kmeans", "dbscan", "hierarchical"],
            "time_series": ["arima", "lstm", "prophet"],
        },
    }


@app.get("/supported-agents")
async def get_supported_agents():
    """Get list of supported agent types and capabilities."""
    return {
        "agent_types": [
            "task_evaluator",
            "data_analyzer",
            "model_trainer",
            "pipeline_orchestrator",
        ],
        "capabilities": [
            "classification",
            "regression",
            "clustering",
            "scoring",
            "recommendation",
            "optimization",
            "monitoring",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
