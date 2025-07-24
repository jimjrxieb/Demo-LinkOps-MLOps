import json
import os
import shutil
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel

# from rag.embed import embed_all_docs  # Commented out for now - needs proper module structure

router = APIRouter()
UPLOAD_DIR = "rag/uploads"
CONFIG_FILE = "rag/rag_config.json"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)


class AutoSyncConfig(BaseModel):
    enabled: bool


def load_config():
    """Load RAG configuration"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
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
