import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logic.sanitizer import WhisSanitizer, batch_sanitize, sanitize_input
from pydantic import BaseModel

app = FastAPI(
    title="Whis Sanitizer Service",
    description="Cleans, structures, and tags data like a pro data scientist",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize sanitizer
sanitizer = WhisSanitizer()


class SanitizeRequest(BaseModel):
    data: Dict[str, Any]


class BatchSanitizeRequest(BaseModel):
    data_list: List[Dict[str, Any]]


class SanitizeResponse(BaseModel):
    message: str
    processing_id: str
    sanitized_data: Dict[str, Any]


@app.get("/")
async def root():
    return {
        "service": "whis_sanitize",
        "status": "healthy",
        "version": "1.0.0",
        "description": "Cleans, structures, and tags data like a pro data scientist",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "whis_sanitize",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/sanitize", response_model=SanitizeResponse)
async def sanitize_data(request: SanitizeRequest):
    """
    Sanitize a single data input.
    """
    try:
        sanitized_data = sanitize_input(request.data)

        return SanitizeResponse(
            message="Data sanitized successfully",
            processing_id=sanitized_data.get("id", str(uuid.uuid4())),
            sanitized_data=sanitized_data,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sanitization failed: {str(e)}")


@app.post("/sanitize/batch")
async def sanitize_batch(request: BatchSanitizeRequest):
    """
    Sanitize multiple data inputs in batch.
    """
    try:
        batch_id = str(uuid.uuid4())
        sanitized_results = batch_sanitize(request.data_list)

        # Calculate batch statistics
        successful = len(
            [r for r in sanitized_results if r.get("status") == "sanitized"]
        )
        failed = len(
            [r for r in sanitized_results if r.get("status") == "sanitization_failed"]
        )

        return {
            "message": "Batch sanitization completed",
            "batch_id": batch_id,
            "total_inputs": len(request.data_list),
            "successful": successful,
            "failed": failed,
            "results": sanitized_results,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Batch sanitization failed: {str(e)}"
        )


@app.post("/sanitize/stream")
async def sanitize_stream(data: Dict[str, Any]):
    """
    Stream sanitization for real-time processing.
    """
    try:
        # Process with minimal overhead for streaming
        sanitized_data = sanitizer.sanitize_data(data)

        return {
            "status": "processed",
            "processing_id": sanitized_data.get("id"),
            "sanitized_data": sanitized_data,
        }

    except Exception as e:
        return {"status": "failed", "error": str(e), "processing_id": str(uuid.uuid4())}


@app.get("/sanitize/{processing_id}")
async def get_sanitization_result(processing_id: str):
    """
    Retrieve sanitization result by processing ID.
    """
    # TODO: Implement retrieval from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.get("/sanitize")
async def list_sanitizations(
    limit: int = 100, offset: int = 0, status: Optional[str] = None
):
    """
    List sanitization results with optional filtering.
    """
    # TODO: Implement listing from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.get("/stats")
async def get_sanitization_stats():
    """
    Get sanitization service statistics.
    """
    return {
        "service": "whis_sanitize",
        "total_processed": 0,  # TODO: Implement actual stats
        "success_rate": 0.0,
        "average_processing_time": 0.0,
        "pii_patterns_detected": list(sanitizer.pii_patterns.keys()),
        "supported_formats": ["json", "yaml", "text", "code"],
        "auto_tagging_domains": list(sanitizer.domain_keywords.keys()),
    }


@app.post("/test")
async def test_sanitization():
    """
    Test endpoint with sample data.
    """
    test_data = {
        "id": str(uuid.uuid4()),
        "type": "qna",
        "content": "How do I deploy a Kubernetes pod? My email is test@example.com and phone is 555-123-4567.",
        "source": "test_input",
        "tags": ["test"],
        "timestamp": datetime.utcnow().isoformat(),
    }

    sanitized = sanitize_input(test_data)

    return {
        "message": "Test sanitization completed",
        "original_data": test_data,
        "sanitized_data": sanitized,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
