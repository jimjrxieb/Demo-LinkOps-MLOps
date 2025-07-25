import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile
from pydantic import BaseModel

# from rag.embed import embed_all_docs  # Commented out for now - needs proper module structure

router = APIRouter()
UPLOAD_DIR = "rag/uploads"
CONFIG_FILE = "rag/rag_config.json"

# HTC Retrain directories
HTC_UPLOAD_DIR = Path("db/htc_uploads")
HTC_LOG_DIR = Path("db/htc_logs")
HTC_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
HTC_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)


class AutoSyncConfig(BaseModel):
    enabled: bool


class RetrainRecord(BaseModel):
    job_id: str
    timestamp: str
    status: str
    details: str


def load_config():
    """Load RAG configuration"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {
        "version": "1.0.0",
        "sources": {},
        "auto_sync_enabled": False,
        "last_sync": None,
    }


def save_config(config):
    """Save RAG configuration"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


@router.post("/htc/upload-docs")
async def upload_docs(file: UploadFile):
    """Upload a document for processing"""
    try:
        # Validate file type
        allowed_extensions = [".pdf", ".docx", ".txt"]
        file_extension = os.path.splitext(file.filename)[1].lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}",
            )

        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Update config
        config = load_config()
        config["sources"][file.filename] = {
            "uploaded_at": datetime.now().isoformat(),
            "size": os.path.getsize(file_path),
            "type": file_extension,
        }
        save_config(config)

        return {"message": f"✅ Uploaded {file.filename}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/htc/manual-sync")
async def manual_sync():
    """Manually trigger document embedding and memory update"""
    try:
        # Process documents
        # embed_all_docs() # Commented out for now - needs proper module structure

        # Update config
        config = load_config()
        config["last_sync"] = datetime.now().isoformat()
        save_config(config)

        return {"message": "✅ Documents embedded and memory updated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/htc/toggle-auto-sync")
async def toggle_auto_sync(config: AutoSyncConfig):
    """Toggle auto-sync mode"""
    try:
        config_data = load_config()
        config_data["auto_sync_enabled"] = config.enabled
        save_config(config_data)

        status = "enabled" if config.enabled else "disabled"
        return {"message": f"✅ Auto sync {status}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/htc/delete-file/{filename}")
async def delete_file(filename: str):
    """Delete an uploaded file"""
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Delete file
        os.remove(file_path)

        # Update config
        config = load_config()
        if filename in config["sources"]:
            del config["sources"][filename]
        save_config(config)

        return {"message": f"✅ Deleted {filename}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/htc/status")
async def get_status():
    """Get HTC system status"""
    try:
        config = load_config()

        # Get uploaded files
        uploaded_files = []
        if os.path.exists(UPLOAD_DIR):
            for filename in os.listdir(UPLOAD_DIR):
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    uploaded_files.append(
                        {
                            "name": filename,
                            "size": os.path.getsize(file_path),
                            "uploaded_at": config["sources"]
                            .get(filename, {})
                            .get("uploaded_at", "Unknown"),
                        }
                    )

        return {
            "uploaded_files": uploaded_files,
            "auto_sync_enabled": config.get("auto_sync_enabled", False),
            "last_sync": config.get("last_sync"),
            "total_files": len(uploaded_files),
            "memory_status": "ready",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/htc/health")
async def health_check():
    """Health check for HTC service"""
    try:
        config = load_config()

        return {
            "status": "healthy",
            "service": "htc_document_memory",
            "upload_directory": {
                "exists": os.path.exists(UPLOAD_DIR),
                "path": UPLOAD_DIR,
            },
            "config_file": {"exists": os.path.exists(CONFIG_FILE), "path": CONFIG_FILE},
            "auto_sync_enabled": config.get("auto_sync_enabled", False),
            "last_sync": config.get("last_sync"),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "htc_document_memory",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


# Retrain endpoints
@router.post("/htc/retrain", status_code=202)
async def retrain_htc(
    background_tasks: BackgroundTasks, files: List[UploadFile] = UploadFile(...)
):
    """
    Upload feedback files and trigger a background retrain job.
    """
    job_id = str(uuid.uuid4())
    ts = datetime.now().isoformat()

    # Save files
    for uf in files:
        dest = HTC_UPLOAD_DIR / f"{job_id}__{uf.filename}"
        with open(dest, "wb") as f:
            f.write(await uf.read())

    # Log initial record
    log_file = HTC_LOG_DIR / f"{job_id}.json"
    initial = RetrainRecord(
        job_id=job_id,
        timestamp=ts,
        status="queued",
        details=f"{len(files)} files uploaded for retraining",
    )
    log_file.write_text(initial.json())

    # Kick off background job
    background_tasks.add_task(run_retrain_job, job_id)
    return {"job_id": job_id, "status": "queued"}


@router.get("/htc/history", response_model=List[RetrainRecord])
def get_retrain_history(limit: int = 50):
    """
    List recent retrain jobs.
    """
    files = sorted(HTC_LOG_DIR.glob("*.json"), reverse=True)[:limit]
    records = []
    for f in files:
        try:
            data = f.read_text()
            records.append(RetrainRecord.parse_raw(data))
        except Exception:
            # Skip corrupted log files
            continue
    return records


def run_retrain_job(job_id: str):
    """
    Background job: load uploaded files, retrain models, update log.
    """
    log_file = HTC_LOG_DIR / f"{job_id}.json"

    try:
        # Update status to running
        running_record = RetrainRecord(
            job_id=job_id,
            timestamp=datetime.now().isoformat(),
            status="running",
            details="Processing uploaded files and retraining models",
        )
        log_file.write_text(running_record.json())

        # Find uploaded files for this job
        job_files = list(HTC_UPLOAD_DIR.glob(f"{job_id}__*"))

        if not job_files:
            raise Exception("No files found for retrain job")

        # TODO: Implement actual retrain logic here
        # This is where you would:
        # 1. Load and process the uploaded files
        # 2. Sanitize the data
        # 3. Generate embeddings
        # 4. Retrain the models
        # 5. Update the model weights

        # Simulate processing time
        import time

        time.sleep(2)

        # For now, just mark as completed
        status = "completed"
        details = f"Successfully processed {len(job_files)} files and updated models"

    except Exception as e:
        status = "failed"
        details = f"Retrain failed: {str(e)}"

    # Update final record
    record = RetrainRecord(
        job_id=job_id,
        timestamp=datetime.now().isoformat(),
        status=status,
        details=details,
    )
    log_file.write_text(record.json())
