"""
ML Models Service - Main FastAPI Application

This service provides machine learning model management, creation, and inference
capabilities for the DEMO-LinkOps platform.
"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Application lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    logger.info("🚀 Starting ML Models Service...")

    # Create necessary directories
    directories = ["models", "data", "temp"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

    logger.info("✅ ML Models Service initialized")

    yield

    logger.info("🛑 Shutting down ML Models Service...")


# Initialize FastAPI app
app = FastAPI(
    title="DEMO-LinkOps ML Models Service",
    description="Machine Learning Model Management and Inference Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "DEMO-LinkOps ML Models Service",
        "version": "1.0.0",
        "description": "Machine Learning Model Management and Inference",
        "timestamp": datetime.now().isoformat(),
        "status": "running",
        "endpoints": {"health": "/health", "models": "/models", "docs": "/docs"},
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check if models directory is accessible
        models_dir = Path("models")
        models_accessible = models_dir.exists() and models_dir.is_dir()

        # Check if data directory is accessible
        data_dir = Path("data")
        data_accessible = data_dir.exists() and data_dir.is_dir()

        health_status = {
            "status": (
                "healthy" if models_accessible and data_accessible else "unhealthy"
            ),
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "models_directory": "accessible" if models_accessible else "error",
                "data_directory": "accessible" if data_accessible else "error",
            },
            "service": "ml-models",
            "version": "1.0.0",
        }

        if health_status["status"] == "unhealthy":
            return JSONResponse(status_code=503, content=health_status)

        return health_status

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "service": "ml-models",
            },
        )


@app.get("/models")
async def list_models():
    """List available models."""
    try:
        models_dir = Path("models")
        if not models_dir.exists():
            return {"models": [], "count": 0}

        models = []
        for model_path in models_dir.iterdir():
            if model_path.is_dir():
                models.append(
                    {
                        "name": model_path.name,
                        "path": str(model_path),
                        "created": datetime.fromtimestamp(
                            model_path.stat().st_ctime
                        ).isoformat(),
                    }
                )

        return {
            "models": models,
            "count": len(models),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/models/create")
async def create_model():
    """Create a new model (placeholder)."""
    return {
        "message": "Model creation endpoint - implementation needed",
        "status": "placeholder",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/models/{model_name}")
async def get_model(model_name: str):
    """Get model information."""
    try:
        model_path = Path("models") / model_name
        if not model_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Model '{model_name}' not found"
            )

        return {
            "name": model_name,
            "path": str(model_path),
            "exists": model_path.exists(),
            "is_directory": model_path.is_dir(),
            "timestamp": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/models/{model_name}/predict")
async def predict(model_name: str):
    """Make predictions with a model (placeholder)."""
    return {
        "model": model_name,
        "message": "Prediction endpoint - implementation needed",
        "status": "placeholder",
        "timestamp": datetime.now().isoformat(),
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "service": "ml-models",
            "timestamp": datetime.now().isoformat(),
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "service": "ml-models",
            "timestamp": datetime.now().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8002))
    logger.info(f"🔧 Starting ML Models Service on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
