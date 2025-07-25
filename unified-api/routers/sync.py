# unified-api/routers/sync.py
import logging
import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Add sync_engine to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / "sync_engine"))

try:
    from sync_engine.auto_embed import get_processing_stats
    from sync_engine.config import (
        get_sync_config,
        is_auto_sync_enabled,
        toggle_auto_sync,
        update_sync_config,
    )
    from sync_engine.watcher import start_watcher, stop_watcher
except ImportError as e:
    logging.warning(f"Sync engine modules not available: {e}")

    # Mock functions for development
    def get_sync_config():
        return {"auto_sync_enabled": False}

    def update_sync_config(updates):
        return True

    def toggle_auto_sync(enabled):
        return True

    def is_auto_sync_enabled():
        return False

    def get_processing_stats():
        return {"error": "Sync engine not available"}


router = APIRouter(prefix="/api")

# Global watcher instance
watcher_observer = None


class SyncSettingRequest(BaseModel):
    enabled: bool


class SyncSettingResponse(BaseModel):
    enabled: bool
    config: dict[str, Any]


class SyncStatsResponse(BaseModel):
    processing: int
    processed: int
    failed: int
    today_processed: int
    today_failed: int
    logs: int


class SyncStatusResponse(BaseModel):
    enabled: bool
    watcher_running: bool
    config: dict[str, Any]
    stats: dict[str, Any]


@router.get("/sync/setting", response_model=SyncSettingResponse)
def get_sync_setting():
    """
    Get current auto-sync setting and configuration
    """
    try:
        config = get_sync_config()
        return SyncSettingResponse(
            enabled=config.get("auto_sync_enabled", False), config=config
        )
    except Exception as e:
        logging.error(f"Failed to get sync setting: {e}")
        raise HTTPException(status_code=500, detail="Failed to get sync setting")


@router.post("/sync/setting", response_model=SyncSettingResponse)
def update_sync_setting(request: SyncSettingRequest):
    """
    Update auto-sync setting
    """
    try:
        # Update the configuration
        success = update_sync_config({"auto_sync_enabled": request.enabled})

        if not success:
            raise HTTPException(status_code=500, detail="Failed to update sync setting")

        # Start/stop watcher based on setting
        global watcher_observer

        if request.enabled:
            if watcher_observer is None:
                try:
                    watcher_observer = start_watcher()
                    logging.info("Auto-sync watcher started")
                except Exception as e:
                    logging.error(f"Failed to start watcher: {e}")
                    # Revert the setting
                    update_sync_config({"auto_sync_enabled": False})
                    raise HTTPException(
                        status_code=500, detail="Failed to start file watcher"
                    )
        else:
            if watcher_observer is not None:
                try:
                    stop_watcher(watcher_observer)
                    watcher_observer = None
                    logging.info("Auto-sync watcher stopped")
                except Exception as e:
                    logging.error(f"Failed to stop watcher: {e}")

        # Return updated setting
        config = get_sync_config()
        return SyncSettingResponse(
            enabled=config.get("auto_sync_enabled", False), config=config
        )

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to update sync setting: {e}")
        raise HTTPException(status_code=500, detail="Failed to update sync setting")


@router.get("/sync/stats", response_model=SyncStatsResponse)
def get_sync_stats():
    """
    Get sync processing statistics
    """
    try:
        stats = get_processing_stats()

        if "error" in stats:
            # Return empty stats if sync engine not available
            return SyncStatsResponse(
                processing=0,
                processed=0,
                failed=0,
                today_processed=0,
                today_failed=0,
                logs=0,
            )

        return SyncStatsResponse(
            processing=stats.get("processing", 0),
            processed=stats.get("processed", 0),
            failed=stats.get("failed", 0),
            today_processed=stats.get("today_processed", 0),
            today_failed=stats.get("today_failed", 0),
            logs=stats.get("logs", 0),
        )

    except Exception as e:
        logging.error(f"Failed to get sync stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get sync stats")


@router.get("/sync/status", response_model=SyncStatusResponse)
def get_sync_status():
    """
    Get comprehensive sync status including settings, watcher status, and stats
    """
    try:
        config = get_sync_config()
        stats = get_processing_stats()

        return SyncStatusResponse(
            enabled=config.get("auto_sync_enabled", False),
            watcher_running=watcher_observer is not None,
            config=config,
            stats=stats if "error" not in stats else {},
        )

    except Exception as e:
        logging.error(f"Failed to get sync status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get sync status")


@router.post("/sync/process-file")
def process_single_file(file_path: str):
    """
    Manually process a single file through the sync pipeline
    """
    try:
        from pathlib import Path

        from sync_engine.auto_embed import process_file

        path = Path(file_path)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        result = process_file(path)

        return {"success": result["status"] == "completed", "result": result}

    except ImportError:
        raise HTTPException(status_code=503, detail="Sync engine not available")
    except Exception as e:
        logging.error(f"Failed to process file {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


@router.post("/sync/process-batch")
def process_batch_files(file_paths: list):
    """
    Process multiple files through the sync pipeline
    """
    try:
        from sync_engine.auto_embed import process_batch

        results = process_batch(file_paths)

        return {
            "total_files": len(file_paths),
            "processed": len([r for r in results if r["status"] == "completed"]),
            "failed": len([r for r in results if r["status"] == "failed"]),
            "results": results,
        }

    except ImportError:
        raise HTTPException(status_code=503, detail="Sync engine not available")
    except Exception as e:
        logging.error(f"Failed to process batch files: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process batch files: {str(e)}"
        )


@router.post("/sync/cleanup")
def cleanup_old_files(days_to_keep: int = 7):
    """
    Clean up old processed and failed files
    """
    try:
        from sync_engine.auto_embed import cleanup_old_files

        cleanup_old_files(days_to_keep)

        return {
            "message": f"Cleanup completed for files older than {days_to_keep} days"
        }

    except ImportError:
        raise HTTPException(status_code=503, detail="Sync engine not available")
    except Exception as e:
        logging.error(f"Failed to cleanup old files: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to cleanup old files: {str(e)}"
        )


@router.get("/sync/watch-directory")
def get_watch_directory():
    """
    Get the current watch directory path
    """
    try:
        from sync_engine.config import get_watch_directory

        watch_dir = get_watch_directory()
        return {
            "watch_directory": str(watch_dir),
            "exists": watch_dir.exists(),
            "files": (
                [f.name for f in watch_dir.iterdir() if f.is_file()]
                if watch_dir.exists()
                else []
            ),
        }

    except ImportError:
        raise HTTPException(status_code=503, detail="Sync engine not available")
    except Exception as e:
        logging.error(f"Failed to get watch directory: {e}")
        raise HTTPException(status_code=500, detail="Failed to get watch directory")


@router.post("/sync/restart-watcher")
def restart_watcher():
    """
    Restart the file watcher service
    """
    try:
        global watcher_observer

        # Stop existing watcher
        if watcher_observer is not None:
            stop_watcher(watcher_observer)
            watcher_observer = None

        # Start new watcher if auto-sync is enabled
        if is_auto_sync_enabled():
            watcher_observer = start_watcher()
            logging.info("File watcher restarted")

        return {
            "message": "Watcher restarted successfully",
            "watcher_running": watcher_observer is not None,
        }

    except Exception as e:
        logging.error(f"Failed to restart watcher: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to restart watcher: {str(e)}"
        )


# Startup event to initialize watcher if auto-sync is enabled
@router.on_event("startup")
async def startup_event():
    """Initialize watcher on startup if auto-sync is enabled"""
    global watcher_observer

    try:
        if is_auto_sync_enabled():
            watcher_observer = start_watcher()
            logging.info("Auto-sync watcher started on startup")
    except Exception as e:
        logging.error(f"Failed to start watcher on startup: {e}")


# Shutdown event to clean up watcher
@router.on_event("shutdown")
async def shutdown_event():
    """Clean up watcher on shutdown"""
    global watcher_observer

    try:
        if watcher_observer is not None:
            stop_watcher(watcher_observer)
            watcher_observer = None
            logging.info("Auto-sync watcher stopped on shutdown")
    except Exception as e:
        logging.error(f"Failed to stop watcher on shutdown: {e}")
