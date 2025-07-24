#!/usr/bin/env python3
"""
RAG Router
=========

Router for RAG (Retrieval-Augmented Generation) service endpoints.
Integrates with the actual RAG service.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse

# Add the RAG service to the path
sys.path.append("/app/rag")

try:
    from logic.embed import DocumentEmbedder
    from logic.search import RAGSearchEngine
    from schemas.query_schema import (
        EmbedRequest,
        EmbedResponse,
        QueryRequest,
        QueryResponse,
        SearchResult,
    )
except ImportError:
    # Fallback for when service is not available
    RAGSearchEngine = None
    DocumentEmbedder = None
    QueryRequest = None
    QueryResponse = None
    SearchResult = None

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize RAG components
search_engine = RAGSearchEngine() if RAGSearchEngine else None
document_embedder = DocumentEmbedder() if DocumentEmbedder else None


@router.get("/health")
async def health_check():
    """Health check for RAG service."""
    try:
        if search_engine:
            status = search_engine.get_status()
            return {
                "status": "healthy",
                "service": "rag",
                "timestamp": datetime.now().isoformat(),
                "details": status,
            }
        else:
            return {
                "status": "degraded",
                "service": "rag",
                "timestamp": datetime.now().isoformat(),
                "error": "RAG service not available",
            }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "service": "rag",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@router.post("/query")
async def query_rag(request: QueryRequest):
    """Query the RAG system with a question."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        # Perform search using the actual service
        search_results = search_engine.search(
            query=request.query,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
            include_metadata=request.include_metadata,
        )

        # Convert to response format
        results = []
        for result in search_results:
            results.append(
                {
                    "content": result.content,
                    "similarity_score": result.similarity_score,
                    "document_id": result.document_id,
                    "chunk_index": result.chunk_index,
                    "metadata": result.metadata,
                }
            )

        return {
            "query": request.query,
            "results": results,
            "total_results": len(results),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"RAG query failed: {e}")
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")


@router.post("/query-llm")
async def query_rag_with_llm(request: QueryRequest):
    """Query the RAG system with LLM-generated answers."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        # Perform LLM-enhanced search
        llm_result = search_engine.search_with_llm(
            query=request.query,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
        )

        # Convert sources to response format
        sources = []
        for result in llm_result["sources"]:
            sources.append(
                {
                    "content": result.content,
                    "similarity_score": result.similarity_score,
                    "document_id": result.document_id,
                    "chunk_index": result.chunk_index,
                    "metadata": result.metadata,
                }
            )

        return {
            "query": request.query,
            "answer": llm_result["answer"],
            "sources": sources,
            "citations": llm_result.get("citations", []),
            "total_sources": len(sources),
            "llm_used": llm_result["llm_used"],
            "model": llm_result["model"],
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"RAG LLM query failed: {e}")
        raise HTTPException(status_code=500, detail=f"RAG LLM query failed: {str(e)}")


@router.get("/memory-log")
async def get_rag_memory_log(
    limit: int = Query(50, description="Number of entries to return")
):
    """Get recent RAG memory log entries."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        # This would need to be implemented in the search engine
        # For now, return a placeholder
        return {
            "entries": [],
            "total": 0,
            "returned": 0,
            "message": "Memory log endpoint available - implementation pending",
        }

    except Exception as e:
        logger.error(f"RAG memory log failed: {e}")
        raise HTTPException(status_code=500, detail=f"RAG memory log failed: {str(e)}")


@router.get("/search")
async def simple_search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(5, description="Number of results to return"),
    similarity_threshold: float = Query(
        0.5, description="Minimum similarity threshold"
    ),
):
    """Simple search endpoint using query parameters."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        # Perform search using the actual service
        search_results = search_engine.search(
            query=query,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
            include_metadata=True,
        )

        # Convert to response format
        results = []
        for result in search_results:
            results.append(
                {
                    "content": result.content,
                    "similarity_score": result.similarity_score,
                    "document_id": result.document_id,
                    "chunk_index": result.chunk_index,
                    "metadata": result.metadata,
                }
            )

        return {
            "query": query,
            "results": results,
            "total_results": len(results),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Simple search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Simple search failed: {str(e)}")


@router.post("/embed")
async def embed_document(
    file: UploadFile = File(...),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(200),
    metadata: str = Form("{}"),
):
    """Embed a document into the vector store."""
    try:
        if not document_embedder:
            raise HTTPException(
                status_code=503, detail="Document embedder not available"
            )

        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Parse metadata
        import json

        try:
            metadata_dict = json.loads(metadata) if metadata else {}
        except json.JSONDecodeError:
            metadata_dict = {}

        # Embed document using the actual service
        result = document_embedder.embed_file(
            file_path=temp_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            metadata=metadata_dict,
        )

        # Clean up temp file
        os.remove(temp_path)

        # Reload search engine
        if search_engine:
            search_engine.reload_index()

        return {
            "status": "success",
            "message": "Document embedded successfully",
            "file_path": temp_path,
            "embedding_stats": result,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Document embedding failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Document embedding failed: {str(e)}"
        )


@router.post("/embed-batch")
async def embed_documents_batch(
    files: List[UploadFile] = File(...),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(200),
):
    """Embed multiple documents in batch."""
    try:
        if not document_embedder:
            raise HTTPException(
                status_code=503, detail="Document embedder not available"
            )

        results = []

        for file in files:
            try:
                # Save uploaded file temporarily
                temp_path = f"/tmp/{file.filename}"
                with open(temp_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)

                # Embed document using the actual service
                result = document_embedder.embed_file(
                    file_path=temp_path,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )

                # Clean up temp file
                os.remove(temp_path)

                results.append(
                    {
                        "file_name": file.filename,
                        "status": "success",
                        "embedding_stats": result,
                    }
                )

            except Exception as e:
                results.append(
                    {"file_name": file.filename, "status": "error", "error": str(e)}
                )

        # Reload search engine
        if search_engine:
            search_engine.reload_index()

        return {
            "status": "success",
            "message": "Batch embedding completed",
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Batch embedding failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch embedding failed: {str(e)}")


@router.get("/documents")
async def list_documents():
    """List all documents in the vector store."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        documents = search_engine.list_documents()

        return {
            "documents": documents,
            "total_documents": len(documents),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Document listing failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Document listing failed: {str(e)}"
        )


@router.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    """Get a specific document by ID."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        document = search_engine.get_document(doc_id)

        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        return {"document": document, "timestamp": datetime.now().isoformat()}

    except Exception as e:
        logger.error(f"Document retrieval failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Document retrieval failed: {str(e)}"
        )


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from the vector store."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        success = search_engine.delete_document(doc_id)

        if not success:
            raise HTTPException(status_code=404, detail="Document not found")

        return {
            "status": "success",
            "message": f"Document {doc_id} deleted successfully",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Document deletion failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Document deletion failed: {str(e)}"
        )


@router.get("/stats")
async def get_rag_stats():
    """Get RAG system statistics."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        stats = {
            "total_documents": search_engine.get_document_count(),
            "total_chunks": search_engine.get_chunk_count(),
            "vectorstore_size_mb": search_engine.get_vectorstore_size(),
            "embedding_model": search_engine.get_model_name(),
            "embedding_dimension": search_engine.get_embedding_dimension(),
            "index_type": search_engine.get_index_type(),
            "last_updated": search_engine.get_last_updated(),
        }

        return {"stats": stats, "timestamp": datetime.now().isoformat()}

    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")


@router.post("/reload")
async def reload_index():
    """Reload the vector store index."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        search_engine.reload_index()

        return {
            "status": "success",
            "message": "Index reloaded successfully",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Index reload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Index reload failed: {str(e)}")


@router.post("/clear")
async def clear_index():
    """Clear all documents from the vector store."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        search_engine.clear_index()

        return {
            "status": "success",
            "message": "Index cleared successfully",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Index clear failed: {e}")
        raise HTTPException(status_code=500, detail=f"Index clear failed: {str(e)}")


@router.get("/models")
async def get_available_models():
    """Get list of available embedding models."""
    models = {
        "available_models": [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-mpnet-base-v2",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        ],
        "current_model": search_engine.get_model_name() if search_engine else "unknown",
        "recommended_model": "sentence-transformers/all-MiniLM-L6-v2",
    }

    return {"models": models, "timestamp": datetime.now().isoformat()}


@router.post("/test-query")
async def test_query(query: str = Form(...)):
    """Test a query without storing results."""
    try:
        if not search_engine:
            raise HTTPException(
                status_code=503, detail="RAG search engine not available"
            )

        # Perform test search using the actual service
        search_results = search_engine.search(
            query=query, top_k=3, similarity_threshold=0.3, include_metadata=False
        )

        # Convert to response format
        results = []
        for result in search_results:
            results.append(
                {
                    "content": (
                        result.content[:200] + "..."
                        if len(result.content) > 200
                        else result.content
                    ),
                    "similarity_score": result.similarity_score,
                }
            )

        return {
            "query": query,
            "test_results": results,
            "total_results": len(results),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Test query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test query failed: {str(e)}")
