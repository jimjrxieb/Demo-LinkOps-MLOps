from datetime import datetime
from typing import Any


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
from logic.model import (
    WhisLogic,
    find_similar_content,
    generate_embedding,
    generate_recommendations,
)
from pydantic import BaseModel

app = FastAPI(
    title="Whis Logic Service",
    description="Whis's internal ML model brain for embedding generation and similarity search",
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

# Initialize logic engine
logic_engine = WhisLogic()


class EmbeddingRequest(BaseModel):
    content: str
    content_type: str = "text"


class SimilarityRequest(BaseModel):
    query_embedding: list[float]
    content_embeddings: list[dict[str, Any]]
    top_k: int = 5


class RecommendationRequest(BaseModel):
    user_context: dict[str, Any]
    available_assets: list[dict[str, Any]]


@app.get("/")
async def root():
    import os

    demo_mode = os.getenv("GROK_API_KEY", "") == "demo_mode"

    return {
        "service": "whis-logic",
        "status": "healthy",
        "version": "1.0.0",
        "description": "Whis's internal ML model brain for embedding generation and similarity search",
        "demo_mode": demo_mode,
        "ai_capabilities": "disabled" if demo_mode else "enabled",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "whis-logic",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/embedding")
async def create_embedding(request: EmbeddingRequest):
    """
    Generate embedding for content.
    """
    try:
        embedding = generate_embedding(request.content, request.content_type)

        return {
            "message": "Embedding generated successfully",
            "embedding": embedding,
            "content_type": request.content_type,
            "embedding_dimension": len(embedding),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process request: {str(e)}"
        ) from e


@app.post("/similarity")
async def find_similar(request: SimilarityRequest):
    """
    Find similar content based on embeddings.
    """
    try:
        similar_content = find_similar_content(
            request.query_embedding, request.content_embeddings, request.top_k
        )

        return {
            "message": "Similarity search completed",
            "results": similar_content,
            "total_results": len(similar_content),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process request: {str(e)}"
        ) from e


@app.post("/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """
    Generate recommendations based on user context.
    """
    try:
        recommendations = generate_recommendations(
            request.user_context, request.available_assets
        )

        return {
            "message": "Recommendations generated successfully",
            "recommendations": recommendations,
            "total_recommendations": len(recommendations),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process request: {str(e)}"
        ) from e


@app.get("/stats")
async def get_logic_stats():
    """
    Get logic service statistics.
    """
    return {
        "service": "whis-logic",
        "embeddings_generated": len(logic_engine.embeddings_cache),
        "similarity_threshold": logic_engine.similarity_threshold,
        "supported_content_types": ["text", "code", "yaml", "json"],
        "embedding_dimension": 384,
    }


@app.post("/test/embedding")
async def test_embedding():
    """
    Test embedding generation with sample content.
    """
    test_content = "How do I deploy a Kubernetes application?"
    embedding = generate_embedding(test_content)

    return {
        "message": "Test embedding generation completed",
        "test_content": test_content,
        "embedding": embedding,
        "embedding_dimension": len(embedding),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8004)
