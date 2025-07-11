import base64
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional


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


from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter()


class ImageTextResult(BaseModel):
    image_id: str
    extracted_text: str
    confidence: float
    language: Optional[str] = None
    regions: List[Dict[str, Any]] = []
    metadata: Dict[str, Any]


class ImageTextRequest(BaseModel):
    image_data: str  # Base64 encoded image
    language_hint: Optional[str] = None
    tags: List[str] = []


@router.post("/extract-text")
async def extract_text_from_image(
    file: UploadFile = File(...),
    language_hint: Optional[str] = None,
    tags: Optional[str] = None,
):
    """
    Extract text from uploaded image using OCR.
    """
    try:
        # Validate file
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        image_id = str(uuid.uuid4())

        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]

        # Read image content
        image_content = await file.read()

        # TODO: Implement actual OCR processing
        # For now, return mock data
        extracted_text = f"Mock extracted text from {file.filename}"
        confidence = 0.85
        language = language_hint or "en"

        # Prepare result
        result = ImageTextResult(
            image_id=image_id,
            extracted_text=extracted_text,
            confidence=confidence,
            language=language,
            regions=[],  # TODO: Add bounding box regions
            metadata={
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": len(image_content),
                "language_hint": language_hint,
                "tags": tag_list,
            },
        )

        # Prepare data for downstream processing
        processing_data = {
            "id": image_id,
            "type": "image_text",
            "source": "ocr_extraction",
            "tags": tag_list + ["ocr", "image_text"],
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending_processing",
            "extracted_text": extracted_text,
            "confidence": confidence,
            "language": language,
            "metadata": result.metadata,
        }

        # TODO: Send to whis_sanitize service
        return {
            "message": "Text extracted successfully",
            "result": result,
            "processing_data": processing_data,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")


@router.post("/extract-text/base64")
async def extract_text_from_base64(request: ImageTextRequest):
    """
    Extract text from base64 encoded image.
    """
    try:
        image_id = str(uuid.uuid4())

        # Decode base64 image
        try:
            base64.b64decode(request.image_data)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")

        # TODO: Implement actual OCR processing
        extracted_text = "Mock extracted text from base64 image"
        confidence = 0.82
        language = request.language_hint or "en"

        result = ImageTextResult(
            image_id=image_id,
            extracted_text=extracted_text,
            confidence=confidence,
            language=language,
            regions=[],
            metadata={
                "source": "base64",
                "language_hint": request.language_hint,
                "tags": request.tags,
            },
        )

        # Prepare data for downstream processing
        processing_data = {
            "id": image_id,
            "type": "image_text",
            "source": "ocr_extraction",
            "tags": request.tags + ["ocr", "image_text"],
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending_processing",
            "extracted_text": extracted_text,
            "confidence": confidence,
            "language": language,
            "metadata": result.metadata,
        }

        return {
            "message": "Text extracted successfully",
            "result": result,
            "processing_data": processing_data,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")


@router.post("/extract-text/batch")
async def extract_text_batch(files: List[UploadFile] = File(...)):
    """
    Extract text from multiple images in batch.
    """
    try:
        batch_id = str(uuid.uuid4())
        results = []

        for file in files:
            if not file.content_type.startswith("image/"):
                continue

            image_id = str(uuid.uuid4())

            # TODO: Implement actual OCR processing
            extracted_text = f"Mock extracted text from {file.filename}"
            confidence = 0.85

            result = {
                "image_id": image_id,
                "filename": file.filename,
                "extracted_text": extracted_text,
                "confidence": confidence,
                "status": "processed",
            }

            results.append(result)

        return {
            "message": "Batch processing completed",
            "batch_id": batch_id,
            "total_images": len(files),
            "processed_images": len(results),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process batch: {str(e)}"
        )


@router.get("/extract-text/{image_id}")
async def get_extraction_result(image_id: str):
    """
    Get extraction result for a specific image.
    """
    # TODO: Implement retrieval from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/extract-text")
async def list_extractions(
    limit: int = 50, offset: int = 0, min_confidence: Optional[float] = None
):
    """
    List all text extractions with optional filtering.
    """
    # TODO: Implement listing from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")
