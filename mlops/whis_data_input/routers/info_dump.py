import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

router = APIRouter()


class InfoDump(BaseModel):
    content: str
    title: Optional[str] = None
    source: Optional[str] = None
    tags: List[str] = []
    format_hint: Optional[str] = None  # json, yaml, text, code, etc.
    context: Optional[str] = None
    priority: Optional[str] = "medium"  # low, medium, high, critical


class InfoDumpBatch(BaseModel):
    dumps: List[InfoDump]
    batch_metadata: Optional[Dict[str, Any]] = None


@router.post("/dump")
async def submit_info_dump(dump: InfoDump):
    """
    Submit raw information dump for processing.
    """
    try:
        dump_id = str(uuid.uuid4())

        # Auto-detect format if not provided
        if not dump.format_hint:
            dump.format_hint = _detect_format(dump.content)

        # Auto-tag based on content
        auto_tags = _generate_auto_tags(dump.content, dump.format_hint)
        all_tags = list(set(dump.tags + auto_tags))

        # Prepare data for downstream processing
        dump_data = {
            "id": dump_id,
            "type": "info_dump",
            "title": dump.title or f"Info Dump {dump_id[:8]}",
            "content": dump.content,
            "source": dump.source or "manual_input",
            "tags": all_tags,
            "format_hint": dump.format_hint,
            "context": dump.context,
            "priority": dump.priority,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending_processing",
            "metadata": {
                "content_length": len(dump.content),
                "auto_detected_format": dump.format_hint,
                "auto_tags": auto_tags,
            },
        }

        # TODO: Send to whis_sanitize service
        return {
            "message": "Info dump submitted successfully",
            "dump_id": dump_id,
            "data": dump_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process info dump: {str(e)}"
        )


@router.post("/dump/batch")
async def submit_info_dump_batch(batch: InfoDumpBatch):
    """
    Submit multiple info dumps in a batch.
    """
    try:
        batch_id = str(uuid.uuid4())
        processed_dumps = []

        for dump in batch.dumps:
            dump_id = str(uuid.uuid4())

            # Auto-detect format if not provided
            if not dump.format_hint:
                dump.format_hint = _detect_format(dump.content)

            # Auto-tag based on content
            auto_tags = _generate_auto_tags(dump.content, dump.format_hint)
            all_tags = list(set(dump.tags + auto_tags))

            dump_data = {
                "id": dump_id,
                "type": "info_dump",
                "title": dump.title or f"Info Dump {dump_id[:8]}",
                "content": dump.content,
                "source": dump.source or "manual_input",
                "tags": all_tags,
                "format_hint": dump.format_hint,
                "context": dump.context,
                "priority": dump.priority,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pending_processing",
                "metadata": {
                    "content_length": len(dump.content),
                    "auto_detected_format": dump.format_hint,
                    "auto_tags": auto_tags,
                },
            }

            processed_dumps.append(dump_data)

        return {
            "message": "Batch submitted successfully",
            "batch_id": batch_id,
            "total_dumps": len(batch.dumps),
            "processed_dumps": len(processed_dumps),
            "batch_metadata": batch.batch_metadata,
            "dumps": processed_dumps,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process batch: {str(e)}"
        )


@router.post("/dump/structured")
async def submit_structured_dump(data: Dict[str, Any] = Body(...)):
    """
    Submit structured data dump (JSON, YAML, etc.).
    """
    try:
        dump_id = str(uuid.uuid4())

        # Convert structured data to string
        if isinstance(data, dict):
            content = json.dumps(data, indent=2)
            format_hint = "json"
        else:
            content = str(data)
            format_hint = "text"

        # Auto-tag based on content
        auto_tags = _generate_auto_tags(content, format_hint)

        dump_data = {
            "id": dump_id,
            "type": "structured_dump",
            "content": content,
            "source": "api_input",
            "tags": auto_tags + ["structured", "api"],
            "format_hint": format_hint,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending_processing",
            "metadata": {
                "content_length": len(content),
                "original_data_type": type(data).__name__,
            },
        }

        return {
            "message": "Structured dump submitted successfully",
            "dump_id": dump_id,
            "data": dump_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process structured dump: {str(e)}"
        )


def _detect_format(content: str) -> str:
    """
    Auto-detect the format of the content.
    """
    content = content.strip()

    # Check for JSON
    try:
        json.loads(content)
        return "json"
    except Exception:
        pass

    # Check for YAML indicators
    if content.startswith("---") or ":" in content and "\n" in content:
        return "yaml"

    # Check for code blocks
    if "```" in content or content.startswith("#"):
        return "code"

    # Check for markdown
    if any(marker in content for marker in ["# ", "## ", "### ", "**", "*", "["]):
        return "markdown"

    # Default to text
    return "text"


def _generate_auto_tags(content: str, format_hint: str) -> List[str]:
    """
    Generate automatic tags based on content and format.
    """
    tags = [format_hint]

    content_lower = content.lower()

    # Technology tags
    if any(
        tech in content_lower for tech in ["kubernetes", "k8s", "pod", "deployment"]
    ):
        tags.append("kubernetes")
    if any(tech in content_lower for tech in ["docker", "container", "image"]):
        tags.append("docker")
    if any(tech in content_lower for tech in ["helm", "chart", "values"]):
        tags.append("helm")
    if any(tech in content_lower for tech in ["terraform", "infrastructure"]):
        tags.append("terraform")
    if any(tech in content_lower for tech in ["python", "pip", "requirements"]):
        tags.append("python")
    if any(tech in content_lower for tech in ["javascript", "node", "npm"]):
        tags.append("javascript")

    # Domain tags
    if any(domain in content_lower for domain in ["mlops", "machine learning", "ai"]):
        tags.append("mlops")
    if any(domain in content_lower for domain in ["devops", "ci/cd", "pipeline"]):
        tags.append("devops")
    if any(domain in content_lower for domain in ["security", "vulnerability", "scan"]):
        tags.append("security")

    return list(set(tags))


@router.get("/dump/{dump_id}")
async def get_info_dump(dump_id: str):
    """
    Retrieve a specific info dump by ID.
    """
    # TODO: Implement retrieval from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/dump")
async def list_info_dumps(
    limit: int = 100,
    offset: int = 0,
    format_hint: Optional[str] = None,
    source: Optional[str] = None,
):
    """
    List info dumps with optional filtering.
    """
    # TODO: Implement listing from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")
