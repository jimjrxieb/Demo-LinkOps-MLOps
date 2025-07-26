#!/usr/bin/env python3
"""
Demo Sync Router
===============

Router for demo data synchronization functionality.
Handles loading demo CSV data into the RAG index for ZRS Property Management demo.
"""

import logging
import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

# Add the RAG service to the path
sys.path.append("/app/rag")

try:
    from loaders.csv_embedder import CSVTEmbedder
    from loaders.delinquency_embedder import DelinquencyEmbedder
    from logic.embed import DocumentEmbedder
    from logic.search import RAGSearchEngine
except ImportError:
    # Fallback for when service is not available
    RAGSearchEngine = None
    DocumentEmbedder = None
    CSVTEmbedder = None
    DelinquencyEmbedder = None

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/demo")

# Initialize RAG components
search_engine = RAGSearchEngine() if RAGSearchEngine else None
document_embedder = DocumentEmbedder() if DocumentEmbedder else None
csv_embedder = CSVTEmbedder() if CSVTEmbedder else None
delinquency_embedder = DelinquencyEmbedder() if DelinquencyEmbedder else None

# Demo data path
DEMO_CSV = Path("db/demo_data/delinquency.csv")


@router.post("/sync")
async def demo_sync() -> dict[str, Any]:
    """
    Sync demo data into the RAG index.

    Loads the delinquency.csv file into the vector store for demo queries.
    """
    try:
        if not DEMO_CSV.exists():
            raise HTTPException(
                status_code=500,
                detail="Demo data not found. Please ensure db/demo_data/delinquency.csv exists.",
            )

        if not delinquency_embedder:
            raise HTTPException(
                status_code=503, detail="RAG delinquency embedder not available"
            )

        # Embed the CSV file using the delinquency embedder
        logger.info(f"🔄 Starting demo sync for {DEMO_CSV}")

        # Use the delinquency embedder to process the file
        success = delinquency_embedder.embed_csv_file(DEMO_CSV)

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to embed delinquency CSV file"
            )

        result = {
            "status": "success",
            "file_processed": str(DEMO_CSV),
            "embedder": "Delinquency Embedder",
        }

        logger.info(f"✅ Demo sync completed: {result}")

        return {
            "status": "Sync complete",
            "message": "Demo delinquency data loaded successfully",
            "details": result,
        }

    except Exception as e:
        logger.error(f"❌ Demo sync failed: {e}")
        raise HTTPException(status_code=500, detail=f"Demo sync failed: {str(e)}")


@router.get("/status")
async def demo_status() -> dict[str, Any]:
    """
    Get the status of demo data in the RAG index.
    """
    try:
        if not search_engine:
            return {
                "status": "unavailable",
                "message": "RAG search engine not available",
            }

        # Check if demo data exists in the index
        # This is a simplified check - in a real implementation you'd query the index
        demo_data_exists = DEMO_CSV.exists()

        return {
            "status": "available" if demo_data_exists else "not_loaded",
            "demo_data_file": str(DEMO_CSV),
            "file_exists": demo_data_exists,
            "message": (
                "Demo data ready for sync"
                if demo_data_exists
                else "Demo data file not found"
            ),
        }

    except Exception as e:
        logger.error(f"❌ Demo status check failed: {e}")
        return {"status": "error", "message": f"Status check failed: {str(e)}"}


@router.delete("/clear")
async def clear_demo_data() -> dict[str, Any]:
    """
    Clear demo data from the RAG index.
    """
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        # Clear the index using the search engine's clear_index method
        search_engine.clear_index()
        logger.info("🗑️ Demo data cleared from RAG index")

        return {"status": "cleared", "message": "Demo data cleared from index"}

    except Exception as e:
        logger.error(f"❌ Demo data clear failed: {e}")
        raise HTTPException(status_code=500, detail=f"Demo data clear failed: {str(e)}")
