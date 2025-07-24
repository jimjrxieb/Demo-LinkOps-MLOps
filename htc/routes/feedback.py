#!/usr/bin/env python3
"""
HTC Feedback API Routes
======================

FastAPI routes for collecting and managing feedback for AI answer improvements.
"""

import logging

# Add parent directory to path for imports
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

sys.path.append(str(Path(__file__).parent.parent))

from feedback_collector import get_feedback_collector, log_feedback

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic models
class FeedbackRequest(BaseModel):
    query: str
    answer: str
    expected: str
    context: str = ""
    category: str = "incorrect_answer"
    user_notes: str = ""
    tenant_data: Optional[Dict[str, Any]] = None


class FeedbackResponse(BaseModel):
    feedback_id: str
    timestamp: str
    status: str
    message: str


class FeedbackStats(BaseModel):
    total_feedback: int
    pending_training: int
    trained: int
    recent_feedback: int
    categories: Dict[str, int]
    status: Dict[str, int]


class FeedbackEntry(BaseModel):
    feedback_id: str
    timestamp: str
    query: str
    generated_answer: str
    expected_answer: str
    context: str
    category: str
    user_notes: str
    status: str
    training_round: int


@router.post("/htc/feedback", response_model=FeedbackResponse)
async def collect_feedback(data: FeedbackRequest):
    """
    Collect feedback for AI answer correction.

    Args:
        data: Feedback data including query, AI answer, and expected answer

    Returns:
        Feedback response with ID and status
    """
    try:
        logger.info(f"📝 Collecting feedback for query: {data.query[:50]}...")

        # Log feedback using the collector
        feedback_entry = log_feedback(
            query=data.query,
            answer=data.answer,
            expected=data.expected,
            context=data.context,
            category=data.category,
            user_notes=data.user_notes,
            tenant_data=data.tenant_data,
        )

        return FeedbackResponse(
            feedback_id=feedback_entry["feedback_id"],
            timestamp=feedback_entry["timestamp"],
            status="logged",
            message="Feedback collected successfully",
        )

    except Exception as e:
        logger.error(f"❌ Failed to collect feedback: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to collect feedback: {str(e)}"
        )


@router.get("/htc/feedback", response_model=Dict[str, Any])
async def get_feedback_entries(
    limit: int = Query(default=50, ge=1, le=100),
    category: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
):
    """
    Get feedback entries with optional filtering.

    Args:
        limit: Maximum number of entries to return
        category: Filter by feedback category
        status: Filter by feedback status

    Returns:
        Dictionary with feedback entries and metadata
    """
    try:
        collector = get_feedback_collector()
        entries = collector.get_feedback_entries(limit=limit)

        # Apply filters
        if category:
            entries = [e for e in entries if e.get("category") == category]

        if status:
            entries = [e for e in entries if e.get("status") == status]

        # Convert to response format
        feedback_entries = []
        for entry in entries:
            feedback_entries.append(
                FeedbackEntry(
                    feedback_id=entry.get("feedback_id", ""),
                    timestamp=entry.get("timestamp", ""),
                    query=entry.get("query", ""),
                    generated_answer=entry.get("generated_answer", ""),
                    expected_answer=entry.get("expected_answer", ""),
                    context=entry.get("context", ""),
                    category=entry.get("category", ""),
                    user_notes=entry.get("user_notes", ""),
                    status=entry.get("status", ""),
                    training_round=entry.get("training_round", 0),
                )
            )

        return {
            "entries": [entry.dict() for entry in feedback_entries],
            "total": len(feedback_entries),
            "limit": limit,
            "filters": {"category": category, "status": status},
        }

    except Exception as e:
        logger.error(f"❌ Failed to get feedback entries: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get feedback entries: {str(e)}"
        )


@router.get("/htc/feedback/{feedback_id}", response_model=FeedbackEntry)
async def get_feedback_by_id(feedback_id: str):
    """
    Get specific feedback entry by ID.

    Args:
        feedback_id: Unique feedback identifier

    Returns:
        Feedback entry details
    """
    try:
        collector = get_feedback_collector()
        entry = collector.get_feedback_by_id(feedback_id)

        if not entry:
            raise HTTPException(status_code=404, detail="Feedback entry not found")

        return FeedbackEntry(
            feedback_id=entry.get("feedback_id", ""),
            timestamp=entry.get("timestamp", ""),
            query=entry.get("query", ""),
            generated_answer=entry.get("generated_answer", ""),
            expected_answer=entry.get("expected_answer", ""),
            context=entry.get("context", ""),
            category=entry.get("category", ""),
            user_notes=entry.get("user_notes", ""),
            status=entry.get("status", ""),
            training_round=entry.get("training_round", 0),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get feedback {feedback_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get feedback: {str(e)}")


@router.get("/htc/feedback/stats", response_model=FeedbackStats)
async def get_feedback_stats():
    """
    Get feedback statistics.

    Returns:
        Feedback statistics including counts by category and status
    """
    try:
        collector = get_feedback_collector()
        stats = collector.get_feedback_stats()

        return FeedbackStats(
            total_feedback=stats.get("total_feedback", 0),
            pending_training=stats.get("pending_training", 0),
            trained=stats.get("trained", 0),
            recent_feedback=stats.get("recent_feedback", 0),
            categories=stats.get("categories", {}),
            status=stats.get("status", {}),
        )

    except Exception as e:
        logger.error(f"❌ Failed to get feedback stats: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get feedback stats: {str(e)}"
        )


@router.put("/htc/feedback/{feedback_id}/status")
async def update_feedback_status(
    feedback_id: str,
    status: str = Query(..., regex="^(pending_training|trained|archived)$"),
    training_round: int = Query(default=0, ge=0),
):
    """
    Update feedback status.

    Args:
        feedback_id: Unique feedback identifier
        status: New status (pending_training, trained, archived)
        training_round: Training round number

    Returns:
        Success response
    """
    try:
        collector = get_feedback_collector()
        success = collector.update_feedback_status(feedback_id, status, training_round)

        if not success:
            raise HTTPException(status_code=404, detail="Feedback entry not found")

        return {
            "feedback_id": feedback_id,
            "status": status,
            "training_round": training_round,
            "message": "Status updated successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update feedback status: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to update status: {str(e)}"
        )


@router.delete("/htc/feedback/{feedback_id}")
async def delete_feedback(feedback_id: str):
    """
    Delete feedback entry.

    Args:
        feedback_id: Unique feedback identifier

    Returns:
        Success response
    """
    try:
        collector = get_feedback_collector()

        # Get the entry first to check if it exists
        entry = collector.get_feedback_by_id(feedback_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Feedback entry not found")

        # Delete the file
        import os

        file_path = collector.log_dir / f"{feedback_id}.json"
        if file_path.exists():
            file_path.unlink()
            logger.info(f"🗑️ Deleted feedback entry: {feedback_id}")

        return {
            "feedback_id": feedback_id,
            "message": "Feedback entry deleted successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete feedback {feedback_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to delete feedback: {str(e)}"
        )


@router.post("/htc/feedback/build-dataset")
async def build_training_dataset():
    """
    Build training dataset from feedback entries.

    Returns:
        Dataset information
    """
    try:
        collector = get_feedback_collector()
        dataset_path = collector.build_training_dataset()

        # Get stats about the dataset
        stats = collector.get_feedback_stats()

        return {
            "dataset_path": dataset_path,
            "total_examples": stats.get("total_feedback", 0),
            "pending_training": stats.get("pending_training", 0),
            "message": "Training dataset built successfully",
        }

    except Exception as e:
        logger.error(f"❌ Failed to build training dataset: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to build dataset: {str(e)}"
        )


@router.post("/htc/feedback/cleanup")
async def cleanup_old_feedback(days: int = Query(default=90, ge=1, le=365)):
    """
    Clean up old feedback entries.

    Args:
        days: Age threshold in days for cleanup

    Returns:
        Cleanup results
    """
    try:
        collector = get_feedback_collector()
        count = collector.cleanup_old_feedback(days=days)

        return {
            "deleted_count": count,
            "age_threshold_days": days,
            "message": f"Cleaned up {count} old feedback entries",
        }

    except Exception as e:
        logger.error(f"❌ Failed to cleanup old feedback: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup: {str(e)}")


@router.get("/htc/feedback/categories")
async def get_feedback_categories():
    """
    Get available feedback categories.

    Returns:
        List of feedback categories
    """
    from feedback_collector import FEEDBACK_CATEGORIES

    return {
        "categories": FEEDBACK_CATEGORIES,
        "description": "Available feedback categories for categorizing AI answer issues",
    }
