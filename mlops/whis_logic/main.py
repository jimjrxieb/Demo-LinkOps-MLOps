from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from logic.model import (
    WhisLogic,
    generate_embedding,
    find_similar_content,
    generate_recommendations,
)

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
    query_embedding: List[float]
    content_embeddings: List[Dict[str, Any]]
    top_k: int = 5


class RecommendationRequest(BaseModel):
    user_context: Dict[str, Any]
    available_assets: List[Dict[str, Any]]


@app.get("/")
async def root():
    return {
        "service": "whis_logic",
        "status": "healthy",
        "version": "1.0.0",
        "description": "Whis's internal ML model brain for embedding generation and similarity search",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "whis_logic",
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
            status_code=500, detail=f"Embedding generation failed: {str(e)}"
        )


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
            status_code=500, detail=f"Similarity search failed: {str(e)}"
        )


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
            status_code=500, detail=f"Recommendation generation failed: {str(e)}"
        )


@app.get("/stats")
async def get_logic_stats():
    """
    Get logic service statistics.
    """
    return {
        "service": "whis_logic",
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

    uvicorn.run(app, host="0.0.0.0", port=8004)
