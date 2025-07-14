import uuid
from datetime import datetime
from typing import Optional, list


def sanitize_cmd(cmd):
    import shlex

    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {
        "ls",
        "echo",
        "kubectl",
        "helm",
        "python3",
        "cat",
        "go",
        "docker",
        "npm",
        "black",
        "ruff",
        "yamllint",
        "prettier",
        "flake8",
    }
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class QnAInput(BaseModel):
    question: str
    answer: str
    context: Optional[str] = None
    tags: list[str] = []
    source: str = "manual_input"
    confidence: Optional[float] = None
    domain: Optional[str] = None


class QnABatch(BaseModel):
    qna_pairs: list[QnAInput]
    batch_metadata: Optional[dict] = None


@router.post("/qna")
async def submit_qna(qna: QnAInput):
    """
    Submit a single Q&A pair for processing.
    """
    try:
        # Generate unique ID
        qna_id = str(uuid.uuid4())

        # Prepare data for downstream processing
        qna_data = {
            "id": qna_id,
            "type": "qna",
            "question": qna.question,
            "answer": qna.answer,
            "context": qna.context,
            "tags": qna.tags,
            "source": qna.source,
            "confidence": qna.confidence,
            "domain": qna.domain,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending_processing",
        }

        # TODO: Send to whis-sanitize service
        # For now, just return the structured data
        print("QnA input processed.")
        return {
            "message": "Q&A submitted successfully",
            "qna_id": qna_id,
            "data": qna_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process Q&A: {str(e)}"
        ) from e


@router.post("/qna/batch")
async def submit_qna_batch(batch: QnABatch):
    """
    Submit multiple Q&A pairs in a batch.
    """
    try:
        batch_id = str(uuid.uuid4())
        processed_count = 0

        batch_data = {
            "batch_id": batch_id,
            "total_pairs": len(batch.qna_pairs),
            "batch_metadata": batch.batch_metadata,
            "timestamp": datetime.utcnow().isoformat(),
            "qna_pairs": [],
        }

        for qna in batch.qna_pairs:
            qna_id = str(uuid.uuid4())
            qna_data = {
                "id": qna_id,
                "type": "qna",
                "question": qna.question,
                "answer": qna.answer,
                "context": qna.context,
                "tags": qna.tags,
                "source": qna.source,
                "confidence": qna.confidence,
                "domain": qna.domain,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pending_processing",
            }
            batch_data["qna_pairs"].append(qna_data)
            processed_count += 1

        # TODO: Send batch to whis-sanitize service
        return {
            "message": "Batch submitted successfully",
            "batch_id": batch_id,
            "processed_count": processed_count,
            "batch_data": batch_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process Q&A: {str(e)}"
        ) from e


@router.get("/qna/{qna_id}")
async def get_qna(qna_id: str):
    """
    Retrieve a specific Q&A pair by ID.
    """
    # TODO: Implement retrieval from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/qna")
async def list_qna(
    limit: int = 100,
    offset: int = 0,
    domain: Optional[str] = None,
    source: Optional[str] = None,
):
    """
    list Q&A pairs with optional filtering.
    """
    # TODO: Implement listing from storage with filters
    raise HTTPException(status_code=501, detail="Not implemented yet")
