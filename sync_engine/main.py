"""
Sync Engine Service - Main FastAPI Application

This service provides data synchronization capabilities for the DEMO-LinkOps platform.
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
    logger.info("🚀 Starting Sync Engine Service...")

    # Create necessary directories
    directories = ["data", "sync", "temp"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

    logger.info("✅ Sync Engine Service initialized")

    yield

    logger.info("🛑 Shutting down Sync Engine Service...")


# Initialize FastAPI app
app = FastAPI(
    title="DEMO-LinkOps Sync Engine Service",
    description="Data Synchronization and Management Service",
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
        "service": "DEMO-LinkOps Sync Engine Service",
        "version": "1.0.0",
        "description": "Data Synchronization and Management",
        "timestamp": datetime.now().isoformat(),
        "status": "running",
        "endpoints": {"health": "/health", "sync": "/sync", "docs": "/docs"},
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check if data directory is accessible
        data_dir = Path("data")
        data_accessible = data_dir.exists() and data_dir.is_dir()

        # Check if sync directory is accessible
        sync_dir = Path("sync")
        sync_accessible = sync_dir.exists() and sync_dir.is_dir()

        health_status = {
            "status": "healthy" if data_accessible and sync_accessible else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "data_directory": "accessible" if data_accessible else "error",
                "sync_directory": "accessible" if sync_accessible else "error",
            },
            "service": "sync-engine",
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
                "service": "sync-engine",
            },
        )


@app.get("/sync/status")
async def sync_status():
    """Get synchronization status."""
    try:
        return {
            "sync_status": "idle",
            "last_sync": None,
            "pending_operations": 0,
            "timestamp": datetime.now().isoformat(),
            "service": "sync-engine",
        }

    except Exception as e:
        logger.error(f"Error getting sync status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sync/start")
async def start_sync():
    """Start synchronization process (placeholder)."""
    return {
        "message": "Sync start endpoint - implementation needed",
        "status": "placeholder",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/sync/stop")
async def stop_sync():
    """Stop synchronization process (placeholder)."""
    return {
        "message": "Sync stop endpoint - implementation needed",
        "status": "placeholder",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/data")
async def list_data():
    """List synchronized data."""
    try:
        data_dir = Path("data")
        if not data_dir.exists():
            return {"data": [], "count": 0}

        data_items = []
        for item_path in data_dir.iterdir():
            if item_path.is_file():
                data_items.append(
                    {
                        "name": item_path.name,
                        "path": str(item_path),
                        "size": item_path.stat().st_size,
                        "modified": datetime.fromtimestamp(
                            item_path.stat().st_mtime
                        ).isoformat(),
                    }
                )

        return {
            "data": data_items,
            "count": len(data_items),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error listing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "service": "sync-engine",
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
            "service": "sync-engine",
            "timestamp": datetime.now().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8004))
    logger.info(f"🔧 Starting Sync Engine Service on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
