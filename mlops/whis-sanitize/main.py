import uuid
from datetime import datetime
from typing import Any, Optional


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


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logic.sanitizer import WhisSanitizer, batch_sanitize, sanitize_input
from pydantic import BaseModel

# Import TensorFlow embedding functionality
try:
    from logic.sanitize_embed import (
        check_embedding_service,
        generate_embedding,
        generate_embeddings_batch,
        get_embedding_info,
    )

    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("Warning: TensorFlow embedding module not available")

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
    data: dict[str, Any]


class BatchSanitizeRequest(BaseModel):
    data_list: list[dict[str, Any]]


class SanitizeResponse(BaseModel):
    message: str
    processing_id: str
    sanitized_data: dict[str, Any]


@app.get("/")
async def root():
    return {
        "service": "whis-sanitize",
        "status": "healthy",
        "version": "1.0.0",
        "description": "Cleans, structures, and tags data like a pro data scientist",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "whis-sanitize",
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
        raise HTTPException(
            status_code=500, detail=f"Sanitization failed: {str(e)}"
        ) from e


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
        ) from e


@app.post("/sanitize/stream")
async def sanitize_stream(data: dict[str, Any]):
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
    list sanitization results with optional filtering.
    """
    # TODO: Implement listing from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.get("/stats")
async def get_sanitization_stats():
    """
    Get sanitization service statistics.
    """
    stats = {
        "service": "whis-sanitize",
        "total_processed": 0,  # TODO: Implement actual stats
        "success_rate": 0.0,
        "average_processing_time": 0.0,
        "pii_patterns_detected": list(sanitizer.pii_patterns.keys()),
        "supported_formats": ["json", "yaml", "text", "code"],
        "auto_tagging_domains": list(sanitizer.domain_keywords.keys()),
    }

    # Add TensorFlow embedding info if available
    if TENSORFLOW_AVAILABLE:
        stats["tensorflow_available"] = True
        stats["embedding_info"] = get_embedding_info()
    else:
        stats["tensorflow_available"] = False

    return stats


@app.get("/embedding/health")
async def embedding_health_check():
    """
    Check TensorFlow embedding service health.
    """
    if not TENSORFLOW_AVAILABLE:
        return {
            "status": "unavailable",
            "error": "TensorFlow embedding module not available",
            "service": "whis-sanitize-embedding",
        }

    try:
        health_status = check_embedding_service()
        return {
            "status": health_status["status"],
            "model_loaded": health_status["model_loaded"],
            "test_embedding_length": health_status["test_embedding_length"],
            "test_embedding_sample": health_status["test_embedding_sample"],
            "error": health_status["error"],
            "service": "whis-sanitize-embedding",
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "service": "whis-sanitize-embedding",
        }


@app.post("/embedding/generate")
async def generate_text_embedding(text: str):
    """
    Generate TensorFlow embedding for a single text.
    """
    if not TENSORFLOW_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="TensorFlow embedding service not available"
        )

    try:
        embedding = generate_embedding(text)

        return {
            "text": text,
            "embedding": embedding,
            "embedding_length": len(embedding),
            "model_info": get_embedding_info(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate embedding: {str(e)}"
        ) from e


@app.post("/embedding/batch")
async def generate_batch_embeddings(texts: list[str]):
    """
    Generate TensorFlow embeddings for multiple texts.
    """
    if not TENSORFLOW_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="TensorFlow embedding service not available"
        )

    try:
        embeddings = generate_embeddings_batch(texts)

        return {
            "texts": texts,
            "embeddings": embeddings,
            "batch_size": len(texts),
            "embedding_dimensions": len(embeddings[0]) if embeddings else 0,
            "model_info": get_embedding_info(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate batch embeddings: {str(e)}"
        ) from e


@app.get("/embedding/info")
async def get_embedding_model_info():
    """
    Get information about the TensorFlow embedding model.
    """
    if not TENSORFLOW_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="TensorFlow embedding service not available"
        )

    try:
        return get_embedding_info()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get embedding info: {str(e)}"
        ) from e


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

    uvicorn.run(app, host="127.0.0.1", port=8002)
