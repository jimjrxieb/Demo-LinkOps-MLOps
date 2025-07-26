import random  # For demo data generation
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# In-memory storage for demo purposes
sync_status = {
    "watch_folder": "/data/input",
    "last_sync": None,
    "active": True,
    "logs": [],
}

# Store sync history
SYNC_LOG_HISTORY = []


class SyncStatus(BaseModel):
    watch_folder: str
    last_sync: Optional[datetime]
    active: bool
    logs: List[str]


class SyncResponse(BaseModel):
    status: Dict
    logs: List[str]


class SyncHistoryEntry(BaseModel):
    timestamp: datetime
    redacted_count: int


@router.get("/sync-engine/status", response_model=SyncResponse)
async def get_status():
    """Get current sync engine status and logs"""
    return {
        "status": sync_status,
        "logs": sync_status["logs"][-50:],  # Return last 50 logs
    }


@router.get("/sync-engine/history", response_model=List[SyncHistoryEntry])
async def get_redaction_history():
    """Get historical sync data for charting"""
    # For demo, if no history, generate some sample data
    if not SYNC_LOG_HISTORY:
        # Generate last 24 hours of sample data
        for i in range(24):
            SYNC_LOG_HISTORY.append(
                {
                    "timestamp": datetime.utcnow().replace(hour=i),
                    "redacted_count": random.randint(5, 50),
                }
            )
    return SYNC_LOG_HISTORY


@router.post("/sync-engine/manual-sync")
async def manual_sync():
    """Trigger a manual sync operation"""
    try:
        # In production, this would trigger actual sync logic
        sync_status["last_sync"] = datetime.utcnow()
        sync_status["logs"].append(f"Manual sync triggered at {datetime.utcnow()}")

        # Simulate sync process
        sync_status["logs"].append("Scanning watch folder for new files...")
        sync_status["logs"].append("Processing 3 new files...")
        sync_status["logs"].append("Applying PII redaction...")
        sync_status["logs"].append("Updating vector embeddings...")
        sync_status["logs"].append("Sync completed successfully")

        # Add to history with random count for demo
        redacted_count = random.randint(5, 50)
        SYNC_LOG_HISTORY.append(
            {"timestamp": datetime.utcnow(), "redacted_count": redacted_count}
        )

        # Keep history capped at 100 entries
        if len(SYNC_LOG_HISTORY) > 100:
            SYNC_LOG_HISTORY.pop(0)

        # Trim logs if too long
        if len(sync_status["logs"]) > 1000:
            sync_status["logs"] = sync_status["logs"][-1000:]

        return {"message": "Manual sync completed successfully"}
    except Exception as e:
        sync_status["logs"].append(f"Error during manual sync: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
