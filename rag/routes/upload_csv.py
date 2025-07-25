#!/usr/bin/env python3
"""
CSV Upload API Routes
====================

API endpoints for uploading and embedding CSV files into the RAG system.
"""

import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

# Import CSV embedder
from loaders.csv_embedder import embed_csv_content, get_csv_embedder

logger = logging.getLogger(__name__)

router = APIRouter()

# Configuration
UPLOAD_DIR = Path("uploads/csv")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {".csv"}


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and embed a CSV file into the RAG system."""
    try:
        # Validate file type
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        # Validate file size (max 10MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        if file.size and file.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB",
            )

        logger.info(f"📤 Processing CSV upload: {file.filename}")

        # Save file to upload directory
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read file content for embedding
        with open(file_path, encoding="utf-8") as f:
            csv_content = f.read()

        # Embed CSV content
        success = embed_csv_content(csv_content, file.filename)

        if success:
            logger.info(f"✅ Successfully embedded CSV: {file.filename}")
            return {
                "status": "success",
                "message": f"Successfully embedded {file.filename}",
                "filename": file.filename,
                "file_path": str(file_path),
                "embedded": True,
            }
        else:
            # Clean up file if embedding failed
            if file_path.exists():
                file_path.unlink()

            raise HTTPException(
                status_code=500, detail=f"Failed to embed CSV file: {file.filename}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ CSV upload failed for {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-csv-batch")
async def upload_csv_batch(files: list[UploadFile] = File(...)):
    """Upload multiple CSV files in batch."""
    try:
        results = []

        for file in files:
            try:
                # Validate file type
                file_extension = Path(file.filename).suffix.lower()
                if file_extension not in ALLOWED_EXTENSIONS:
                    results.append(
                        {
                            "filename": file.filename,
                            "status": "error",
                            "message": f"File type not supported: {file_extension}",
                        }
                    )
                    continue

                # Save and embed file
                file_path = UPLOAD_DIR / file.filename
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                # Read and embed content
                with open(file_path, encoding="utf-8") as f:
                    csv_content = f.read()

                success = embed_csv_content(csv_content, file.filename)

                if success:
                    results.append(
                        {
                            "filename": file.filename,
                            "status": "success",
                            "message": "Successfully embedded",
                        }
                    )
                else:
                    # Clean up on failure
                    if file_path.exists():
                        file_path.unlink()
                    results.append(
                        {
                            "filename": file.filename,
                            "status": "error",
                            "message": "Failed to embed",
                        }
                    )

            except Exception as e:
                logger.error(f"❌ Batch upload failed for {file.filename}: {e}")
                results.append(
                    {"filename": file.filename, "status": "error", "message": str(e)}
                )

        # Count successes and failures
        success_count = sum(1 for r in results if r["status"] == "success")
        error_count = len(results) - success_count

        return {
            "status": "completed",
            "total_files": len(files),
            "successful": success_count,
            "failed": error_count,
            "results": results,
        }

    except Exception as e:
        logger.error(f"❌ Batch upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/csv-status")
async def get_csv_status():
    """Get status of uploaded CSV files."""
    try:
        csv_embedder = get_csv_embedder()

        # Get list of uploaded files
        uploaded_files = []
        if UPLOAD_DIR.exists():
            for file_path in UPLOAD_DIR.glob("*.csv"):
                uploaded_files.append(
                    {
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime,
                    }
                )

        return {
            "upload_directory": str(UPLOAD_DIR),
            "uploaded_files": uploaded_files,
            "total_files": len(uploaded_files),
            "processed_files": len(csv_embedder.processed_files),
        }

    except Exception as e:
        logger.error(f"❌ Failed to get CSV status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/csv/{filename}")
async def delete_csv(filename: str):
    """Delete an uploaded CSV file."""
    try:
        file_path = UPLOAD_DIR / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        # Delete file
        file_path.unlink()

        logger.info(f"🗑️ Deleted CSV file: {filename}")

        return {"status": "success", "message": f"Successfully deleted {filename}"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete CSV {filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/csv-template")
async def get_csv_template():
    """Get a sample CSV template for tenant data."""
    template_content = """tenant_name,unit,status,lease_start,lease_end,rent_amount,email,phone
John Smith,101,active,2024-01-01,2024-12-31,1500,john.smith@email.com,555-0101
Jane Doe,102,active,2024-02-01,2024-11-30,1600,jane.doe@email.com,555-0102
Bob Johnson,103,active,2024-03-01,2024-10-31,1400,bob.johnson@email.com,555-0103"""

    return {
        "template": template_content,
        "description": "Sample CSV template for tenant data",
        "required_columns": ["tenant_name"],
        "optional_columns": [
            "unit",
            "status",
            "lease_start",
            "lease_end",
            "rent_amount",
            "email",
            "phone",
        ],
        "date_format": "YYYY-MM-DD",
        "rent_format": "Numeric (e.g., 1500 or 1500.00)",
    }
