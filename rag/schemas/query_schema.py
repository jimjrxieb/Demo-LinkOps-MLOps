#!/usr/bin/env python3
"""
Query Schemas for RAG Service
============================

Pydantic models for request/response validation.
"""

from typing import Any, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for RAG queries."""

    query: str = Field(..., description="The search query/question")
    top_k: int = Field(5, ge=1, le=50, description="Number of results to return")
    similarity_threshold: float = Field(
        0.5, ge=0.0, le=1.0, description="Minimum similarity threshold"
    )
    include_metadata: bool = Field(
        True, description="Include document metadata in results"
    )

    class Config:
        schema_extra = {
            "example": {
                "query": "What is the zero trust model?",
                "top_k": 5,
                "similarity_threshold": 0.7,
                "include_metadata": True,
            }
        }


class SearchResult(BaseModel):
    """Model for individual search results."""

    content: str = Field(..., description="The text content of the result")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")
    document_id: str = Field(..., description="ID of the source document")
    chunk_index: int = Field(..., description="Index of the text chunk")
    metadata: Optional[dict[str, Any]] = Field(None, description="Document metadata")

    class Config:
        schema_extra = {
            "example": {
                "content": "The zero trust model is a security framework that requires all users to be authenticated and authorized before accessing any resources.",
                "similarity_score": 0.85,
                "document_id": "doc_123",
                "chunk_index": 5,
                "metadata": {"source_file": "security_guide.txt", "chunk_size": 1000},
            }
        }


class QueryResponse(BaseModel):
    """Response model for RAG queries."""

    query: str = Field(..., description="The original query")
    results: list[SearchResult] = Field(..., description="Search results")
    execution_time: float = Field(..., description="Query execution time in seconds")
    timestamp: str = Field(..., description="Query timestamp")
    total_results: int = Field(..., description="Total number of results")
    search_metadata: dict[str, Any] = Field(..., description="Search engine metadata")

    class Config:
        schema_extra = {
            "example": {
                "query": "What is the zero trust model?",
                "results": [
                    {
                        "content": "The zero trust model is a security framework...",
                        "similarity_score": 0.85,
                        "document_id": "doc_123",
                        "chunk_index": 5,
                        "metadata": {"source_file": "security_guide.txt"},
                    }
                ],
                "execution_time": 0.125,
                "timestamp": "2024-01-15T10:30:00Z",
                "total_results": 1,
                "search_metadata": {
                    "vectorstore_size": 1000,
                    "search_engine": "FAISS",
                    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                },
            }
        }


class EmbedRequest(BaseModel):
    """Request model for document embedding."""

    file_path: str = Field(..., description="Path to the document file")
    chunk_size: int = Field(1000, ge=100, le=5000, description="Size of text chunks")
    chunk_overlap: int = Field(200, ge=0, le=1000, description="Overlap between chunks")
    metadata: Optional[dict[str, Any]] = Field(None, description="Document metadata")

    class Config:
        schema_extra = {
            "example": {
                "file_path": "/path/to/document.txt",
                "chunk_size": 1000,
                "chunk_overlap": 200,
                "metadata": {
                    "source": "security_documentation",
                    "author": "Security Team",
                    "version": "1.0",
                },
            }
        }


class EmbeddingStats(BaseModel):
    """Model for embedding statistics."""

    chunks_created: int = Field(..., description="Number of text chunks created")
    vectors_generated: int = Field(
        ..., description="Number of embedding vectors generated"
    )
    file_size_bytes: int = Field(..., description="Original file size in bytes")
    processing_time: float = Field(..., description="Processing time in seconds")
    embedding_model: str = Field(..., description="Model used for embeddings")
    embedding_dimension: int = Field(..., description="Dimension of embedding vectors")

    class Config:
        schema_extra = {
            "example": {
                "chunks_created": 25,
                "vectors_generated": 25,
                "file_size_bytes": 50000,
                "processing_time": 2.5,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "embedding_dimension": 384,
            }
        }


class EmbedResponse(BaseModel):
    """Response model for document embedding."""

    file_path: str = Field(..., description="Path to the embedded file")
    embedding_stats: EmbeddingStats = Field(..., description="Embedding statistics")
    execution_time: float = Field(..., description="Total execution time in seconds")
    timestamp: str = Field(..., description="Embedding timestamp")
    status: str = Field(..., description="Embedding status")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        schema_extra = {
            "example": {
                "file_path": "/path/to/document.txt",
                "embedding_stats": {
                    "chunks_created": 25,
                    "vectors_generated": 25,
                    "file_size_bytes": 50000,
                    "processing_time": 2.5,
                    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                    "embedding_dimension": 384,
                },
                "execution_time": 3.2,
                "timestamp": "2024-01-15T10:30:00Z",
                "status": "success",
            }
        }


class DocumentInfo(BaseModel):
    """Model for document information."""

    document_id: str = Field(..., description="Unique document ID")
    filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="Path to the document")
    file_size_bytes: int = Field(..., description="File size in bytes")
    chunks_count: int = Field(..., description="Number of text chunks")
    embedding_model: str = Field(..., description="Model used for embeddings")
    created_at: str = Field(..., description="Document creation timestamp")
    metadata: Optional[dict[str, Any]] = Field(None, description="Document metadata")

    class Config:
        schema_extra = {
            "example": {
                "document_id": "doc_123",
                "filename": "security_guide.txt",
                "file_path": "/path/to/security_guide.txt",
                "file_size_bytes": 50000,
                "chunks_count": 25,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "created_at": "2024-01-15T10:30:00Z",
                "metadata": {
                    "source": "security_documentation",
                    "author": "Security Team",
                },
            }
        }


class SystemStats(BaseModel):
    """Model for system statistics."""

    total_documents: int = Field(..., description="Total number of documents")
    total_chunks: int = Field(..., description="Total number of text chunks")
    vectorstore_size_mb: float = Field(..., description="Vector store size in MB")
    embedding_model: str = Field(..., description="Current embedding model")
    embedding_dimension: int = Field(..., description="Embedding dimension")
    index_type: str = Field(..., description="Type of vector index")
    last_updated: str = Field(..., description="Last update timestamp")
    timestamp: str = Field(..., description="Stats timestamp")

    class Config:
        schema_extra = {
            "example": {
                "total_documents": 10,
                "total_chunks": 250,
                "vectorstore_size_mb": 15.5,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "embedding_dimension": 384,
                "index_type": "FAISS",
                "last_updated": "2024-01-15T10:30:00Z",
                "timestamp": "2024-01-15T10:35:00Z",
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    timestamp: str = Field(..., description="Health check timestamp")
    vectorstore_status: dict[str, Any] = Field(..., description="Vector store status")

    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "service": "rag",
                "timestamp": "2024-01-15T10:30:00Z",
                "vectorstore_status": {
                    "index_loaded": True,
                    "document_count": 10,
                    "chunk_count": 250,
                },
            }
        }
