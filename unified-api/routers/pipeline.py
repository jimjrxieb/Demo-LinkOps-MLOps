#!/usr/bin/env python3
"""
Pipeline Router
==============

Router for training pipeline service endpoints.
Integrates with the actual pipeline service.
"""

import logging
import os
import sys
from datetime import datetime

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

# Add the pipeline service to the path
sys.path.append("/app/pipeline")

try:
    from main import TrainingPipeline, run_ml_pipeline, run_pipeline, run_rag_pipeline
except ImportError:
    # Fallback for when service is not available
    TrainingPipeline = None
    run_pipeline = None
    run_rag_pipeline = None
    run_ml_pipeline = None

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize pipeline
pipeline = TrainingPipeline() if TrainingPipeline else None


@router.get("/health")
async def health_check():
    """Health check for pipeline service."""
    try:
        if pipeline:
            status = pipeline.get_status()
            return {
                "status": "healthy",
                "service": "pipeline",
                "timestamp": datetime.now().isoformat(),
                "details": status,
            }
        else:
            return {
                "status": "degraded",
                "service": "pipeline",
                "timestamp": datetime.now().isoformat(),
                "error": "Pipeline service not available",
            }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "service": "pipeline",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@router.post("/run-pipeline")
async def run_pipeline_endpoint(
    file: UploadFile = File(...),
    task_type: str = Form(...),
    target_column: str = Form(""),
    chunk_size: int = Form(1000),
    test_size: int = Form(20),
    random_state: int = Form(42),
    security_level: str = Form("medium"),
):
    """Run the complete training pipeline."""
    try:
        if not run_pipeline:
            raise HTTPException(
                status_code=503, detail="Pipeline service not available"
            )

        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Prepare parameters
        model_params = {
            "test_size": test_size,
            "random_state": random_state,
            "security_level": security_level,
        }

        embedding_params = {"chunk_size": chunk_size, "security_level": security_level}

        # Run pipeline based on task type
        if task_type == "rag":
            result = run_rag_pipeline(temp_path, embedding_params)
        else:
            if not target_column:
                raise HTTPException(
                    status_code=400, detail="Target column required for ML tasks"
                )
            result = run_ml_pipeline(temp_path, task_type, target_column, model_params)

        # Clean up temp file
        os.remove(temp_path)

        return {
            "status": "success",
            "message": "Pipeline completed successfully",
            "task_type": task_type,
            "pipeline_id": result.get("pipeline_id"),
            "output_path": result.get("output_path"),
            "metrics": result.get("metrics"),
            "duration": result.get("duration"),
            "steps_completed": result.get("steps_completed"),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Pipeline execution failed: {str(e)}"
        )


@router.post("/intake")
async def run_intake(
    file: UploadFile = File(...), security_level: str = Form("medium")
):
    """Run data intake step only."""
    try:
        if not pipeline:
            raise HTTPException(
                status_code=503, detail="Pipeline service not available"
            )

        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Process intake using the actual service
        raw_data_path = pipeline.data_intake.save_upload(temp_path)

        # Clean up temp file
        os.remove(temp_path)

        return {
            "status": "success",
            "message": "Data intake completed",
            "raw_data_path": raw_data_path,
            "file_info": {
                "filename": file.filename,
                "size": file.size,
                "content_type": file.content_type,
            },
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Data intake failed: {e}")
        raise HTTPException(status_code=500, detail=f"Data intake failed: {str(e)}")


@router.post("/sanitize")
async def run_sanitize(
    file_path: str = Form(...), security_level: str = Form("medium")
):
    """Run data sanitization step only."""
    try:
        if not pipeline:
            raise HTTPException(
                status_code=503, detail="Pipeline service not available"
            )

        # Sanitize data using the actual service
        clean_data_path = pipeline.data_sanitizer.sanitize_file(
            file_path, security_level
        )

        return {
            "status": "success",
            "message": "Data sanitization completed",
            "clean_data_path": clean_data_path,
            "original_path": file_path,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Data sanitization failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Data sanitization failed: {str(e)}"
        )


@router.post("/embed")
async def run_embed(
    file_path: str = Form(...),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(200),
):
    """Run document embedding step only."""
    try:
        if not pipeline:
            raise HTTPException(
                status_code=503, detail="Pipeline service not available"
            )

        # Embed documents using the actual service
        embedding_path = pipeline.document_embedder.embed_file(
            file_path, chunk_size, chunk_overlap
        )

        return {
            "status": "success",
            "message": "Document embedding completed",
            "embedding_path": embedding_path,
            "original_path": file_path,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Document embedding failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Document embedding failed: {str(e)}"
        )


@router.post("/train")
async def run_training(
    file_path: str = Form(...),
    task_type: str = Form(...),
    target_column: str = Form(...),
    test_size: int = Form(20),
    random_state: int = Form(42),
):
    """Run model training step only."""
    try:
        if not pipeline:
            raise HTTPException(
                status_code=503, detail="Pipeline service not available"
            )

        # Train model using the actual service
        model_path = pipeline.model_trainer.train_model(
            file_path, task_type, target_column, test_size, random_state
        )

        return {
            "status": "success",
            "message": "Model training completed",
            "model_path": model_path,
            "original_path": file_path,
            "task_type": task_type,
            "target_column": target_column,
            "test_size": test_size,
            "random_state": random_state,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Model training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")


@router.get("/status/{job_id}")
async def get_pipeline_status(job_id: str):
    """Get status of a pipeline job."""
    try:
        if not pipeline:
            raise HTTPException(
                status_code=503, detail="Pipeline service not available"
            )

        status = pipeline.get_status()

        return {
            "job_id": job_id,
            "status": status.get("status"),
            "pipeline_id": status.get("pipeline_id"),
            "start_time": status.get("start_time"),
            "end_time": status.get("end_time"),
            "steps_completed": status.get("steps_completed"),
            "errors": status.get("errors"),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.get("/download/{output_path:path}")
async def download_output(output_path: str):
    """Download pipeline output files."""
    try:
        full_path = f"/app/pipeline/output/{output_path}"

        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="Output file not found")

        return FileResponse(
            path=full_path,
            filename=os.path.basename(full_path),
            media_type="application/octet-stream",
        )

    except Exception as e:
        logger.error(f"Output download failed: {e}")
        raise HTTPException(status_code=500, detail=f"Output download failed: {str(e)}")


@router.get("/outputs")
async def list_outputs():
    """List all pipeline outputs."""
    try:
        outputs_dir = "/app/pipeline/output"

        if not os.path.exists(outputs_dir):
            return {"outputs": [], "total": 0}

        outputs = []
        for filename in os.listdir(outputs_dir):
            file_path = os.path.join(outputs_dir, filename)
            stat = os.stat(file_path)
            outputs.append(
                {
                    "name": filename,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )

        return {
            "outputs": outputs,
            "total": len(outputs),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Output listing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Output listing failed: {str(e)}")


@router.get("/stats")
async def get_pipeline_stats():
    """Get pipeline statistics."""
    try:
        if not pipeline:
            raise HTTPException(
                status_code=503, detail="Pipeline service not available"
            )

        stats = pipeline.get_status()

        return {"stats": stats, "timestamp": datetime.now().isoformat()}

    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")


@router.get("/task-types")
async def get_task_types():
    """Get available task types."""
    task_types = [
        {
            "value": "rag",
            "label": "RAG Training",
            "description": "Document embedding for retrieval",
        },
        {
            "value": "classifier",
            "label": "Classification",
            "description": "Supervised classification model",
        },
        {
            "value": "regression",
            "label": "Regression",
            "description": "Supervised regression model",
        },
        {
            "value": "clustering",
            "label": "Clustering",
            "description": "Unsupervised clustering model",
        },
        {
            "value": "time_series",
            "label": "Time Series",
            "description": "Time series forecasting model",
        },
    ]

    return {"task_types": task_types, "timestamp": datetime.now().isoformat()}


@router.delete("/outputs/{output_name}")
async def delete_output(output_name: str):
    """Delete a pipeline output file."""
    try:
        output_path = f"/app/pipeline/output/{output_name}"

        if not os.path.exists(output_path):
            raise HTTPException(status_code=404, detail="Output not found")

        os.remove(output_path)

        return {
            "status": "success",
            "message": f"Output {output_name} deleted successfully",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Output deletion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Output deletion failed: {str(e)}")
