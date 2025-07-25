#!/usr/bin/env python3
"""
RAG Service - Secure Retrieval-Augmented Generation
==================================================

FastAPI service for private, local Q&A over embedded documents.
"""

import logging
import shutil

# Import status routes
import sys
import time
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from logic.embed import DocumentEmbedder
from logic.llm_runner import generate_answer

# Import local modules
from logic.search import RAGSearchEngine
from schemas.query_schema import (
    EmbedRequest,
    EmbedResponse,
    QueryRequest,
    QueryResponse,
)

sys.path.append("../backend")
# Import HTC feedback routes
import sys

from routes.status import router as status_router

# Import CSV upload routes
from routes.upload_csv import router as csv_router

sys.path.append(str(Path(__file__).parent.parent / "htc"))
from routes.feedback import router as feedback_router
from routes.prompt_editor import router as prompt_editor_router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Service",
    description="Secure Retrieval-Augmented Generation for local document Q&A",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include status routes
app.include_router(status_router, prefix="/api")

# Include CSV upload routes
app.include_router(csv_router, prefix="/api")

# Include HTC feedback routes
app.include_router(feedback_router, prefix="/api")

# Include HTC prompt editor routes
app.include_router(prompt_editor_router, prefix="/api")

# Initialize RAG components
search_engine = RAGSearchEngine()
document_embedder = DocumentEmbedder()

# Create upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "rag",
        "timestamp": datetime.now().isoformat(),
        "vectorstore_status": search_engine.get_status(),
    }


@app.post("/query/", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the RAG system with a question.

    Args:
        request: Query request with question and optional parameters

    Returns:
        Query response with search results and metadata
    """
    start_time = time.time()

    try:
        logger.info(f"🔍 Processing query: {request.query[:50]}...")

        # Perform search
        search_results = search_engine.search(
            query=request.query,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
            include_metadata=request.include_metadata,
        )

        # Calculate execution time
        execution_time = time.time() - start_time

        # Prepare response
        response = QueryResponse(
            query=request.query,
            results=search_results,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
            total_results=len(search_results),
            search_metadata={
                "vectorstore_size": search_engine.get_document_count(),
                "search_engine": "FAISS",
                "embedding_model": search_engine.get_model_name(),
            },
        )

        logger.info(
            f"✅ Query completed in {execution_time:.3f}s - {len(search_results)} results"
        )
        return response

    except Exception as e:
        logger.error(f"❌ Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/query-llm/")
async def query_with_llm(request: QueryRequest):
    """
    Query the RAG system with LLM-generated answers.

    Args:
        request: Query request with question and optional parameters

    Returns:
        Response with LLM-generated answer and source documents
    """
    start_time = time.time()

    try:
        logger.info(f"🧠 Processing LLM query: {request.query[:50]}...")

        # Perform LLM-enhanced search
        llm_result = search_engine.search_with_llm(
            query=request.query,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
        )

        # Calculate execution time
        execution_time = time.time() - start_time

        # Prepare response
        response = {
            "query": request.query,
            "answer": llm_result["answer"],
            "sources": llm_result["sources"],
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "llm_used": llm_result["llm_used"],
            "model": llm_result["model"],
            "total_sources": len(llm_result["sources"]),
            "search_metadata": {
                "vectorstore_size": search_engine.get_document_count(),
                "search_engine": "FAISS + LangChain",
                "embedding_model": search_engine.get_model_name(),
                "llm_model": llm_result.get("model", "unknown"),
            },
        }

        if "error" in llm_result:
            response["error"] = llm_result["error"]

        logger.info(
            f"🧠 LLM query completed in {execution_time:.3f}s - LLM: {llm_result['llm_used']}"
        )
        return response

    except Exception as e:
        logger.error(f"❌ LLM query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM query failed: {str(e)}")


@app.post("/query-simple/")
async def query_simple(request: QueryRequest):
    """
    Simple query endpoint that uses the standalone LLM runner.

    Args:
        request: Query request with question

    Returns:
        Query response with generated answer
    """
    start_time = time.time()

    try:
        logger.info(f"🔍 Processing simple query: {request.query[:50]}...")

        # First, search for relevant context using MultiQueryRetriever for smarter results
        search_results = search_engine.search_with_multi_query(
            query=request.query,
            top_k=5,
            similarity_threshold=0.5,
            include_metadata=True,
        )

        # Format context with metadata for tenant data
        formatted_context = []
        tenant_sources = []

        for result in search_results:
            content = result.content
            metadata = result.metadata

            # Add metadata info for tenant records
            if metadata and metadata.get("source_type") == "tenant_csv":
                tenant_info = f"[Source: {metadata.get('source', 'Unknown')}] "
                if metadata.get("tenant_name"):
                    tenant_info += f"Tenant: {metadata.get('tenant_name')} "
                if metadata.get("unit"):
                    tenant_info += f"Unit: {metadata.get('unit')} "
                if metadata.get("lease_end"):
                    tenant_info += f"Lease End: {metadata.get('lease_end')} "

                content = f"{tenant_info}\n{content}"
                tenant_sources.append(
                    {
                        "tenant_name": metadata.get("tenant_name", "Unknown"),
                        "unit": metadata.get("unit", "Unknown"),
                        "lease_end": metadata.get("lease_end", "Unknown"),
                        "rent_amount": metadata.get("rent_amount"),
                        "status": metadata.get("status", "Unknown"),
                        "source": metadata.get("source", "Unknown"),
                        "content": result.content,
                        "score": result.score,
                    }
                )

            formatted_context.append(content)

        context = "\n\n".join(formatted_context)

        # Generate answer using LLM runner
        answer = generate_answer(request.query, context)

        # Calculate execution time
        execution_time = time.time() - start_time

        # Prepare response
        response = {
            "query": request.query,
            "answer": answer,
            "results": search_results,
            "tenant_sources": tenant_sources,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "total_results": len(search_results),
            "context_used": context[:200] + "..." if len(context) > 200 else context,
        }

        logger.info(f"✅ Simple query completed in {execution_time:.2f}s")
        return response

    except Exception as e:
        logger.error(f"❌ Simple query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory-log/")
async def get_memory_log(limit: int = 50):
    """
    Get recent memory log entries.

    Args:
        limit: Maximum number of entries to return

    Returns:
        List of recent query/answer pairs
    """
    try:
        log_path = Path("db/query_log.json")
        if not log_path.exists():
            return {"entries": [], "total": 0}

        entries = []
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        entry = json.loads(line.strip())
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue

        # Return most recent entries
        recent_entries = entries[-limit:] if len(entries) > limit else entries

        return {
            "entries": recent_entries,
            "total": len(entries),
            "returned": len(recent_entries),
        }

    except Exception as e:
        logger.error(f"Failed to read memory log: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to read memory log: {str(e)}"
        )


@app.post("/embed/", response_model=EmbedResponse)
async def embed_document(request: EmbedRequest):
    """
    Embed a document into the vector store.

    Args:
        request: Embed request with document path and parameters

    Returns:
        Embed response with embedding statistics
    """
    start_time = time.time()

    try:
        logger.info(f"📄 Embedding document: {request.file_path}")

        # Embed document
        embedding_stats = document_embedder.embed_file(
            file_path=request.file_path,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
            metadata=request.metadata,
        )

        # Reload search engine with new embeddings
        search_engine.reload_index()

        # Calculate execution time
        execution_time = time.time() - start_time

        # Prepare response
        response = EmbedResponse(
            file_path=request.file_path,
            embedding_stats=embedding_stats,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
            status="success",
        )

        logger.info(
            f"✅ Document embedded in {execution_time:.3f}s - {embedding_stats['chunks_created']} chunks"
        )
        return response

    except Exception as e:
        logger.error(f"❌ Embedding failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")


@app.post("/embed-batch/", response_model=list[EmbedResponse])
async def embed_documents_batch(
    file_paths: list[str], chunk_size: int = 1000, chunk_overlap: int = 200
):
    """
    Embed multiple documents in batch.

    Args:
        file_paths: List of file paths to embed
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks

    Returns:
        List of embedding responses
    """
    responses = []

    for file_path in file_paths:
        try:
            request = EmbedRequest(
                file_path=file_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )
            response = await embed_document(request)
            responses.append(response)
        except Exception as e:
            logger.error(f"Failed to embed {file_path}: {e}")
            responses.append(
                EmbedResponse(
                    file_path=file_path,
                    embedding_stats={},
                    execution_time=0,
                    timestamp=datetime.now().isoformat(),
                    status="failed",
                    error=str(e),
                )
            )

    return responses


@app.get("/search/", response_model=QueryResponse)
async def search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(5, description="Number of results to return"),
    similarity_threshold: float = Query(
        0.5, description="Minimum similarity threshold"
    ),
):
    """
    Simple search endpoint using query parameters.

    Args:
        query: Search query
        top_k: Number of results to return
        similarity_threshold: Minimum similarity threshold

    Returns:
        Search results
    """
    request = QueryRequest(
        query=query, top_k=top_k, similarity_threshold=similarity_threshold
    )
    return await query(request)


@app.get("/documents/")
async def list_documents():
    """List all documents in the vector store."""
    try:
        documents = search_engine.list_documents()
        return {
            "documents": documents,
            "total_documents": len(documents),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Failed to list documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    """Get a specific document by ID."""
    try:
        document = search_engine.get_document(doc_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except Exception as e:
        logger.error(f"Failed to get document {doc_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from the vector store."""
    try:
        success = search_engine.delete_document(doc_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"message": f"Document {doc_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete document {doc_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats/")
async def get_stats():
    """Get RAG system statistics."""
    try:
        stats = {
            "total_documents": search_engine.get_document_count(),
            "total_chunks": search_engine.get_chunk_count(),
            "vectorstore_size_mb": search_engine.get_vectorstore_size(),
            "embedding_model": search_engine.get_model_name(),
            "embedding_dimension": search_engine.get_embedding_dimension(),
            "index_type": search_engine.get_index_type(),
            "last_updated": search_engine.get_last_updated(),
            "timestamp": datetime.now().isoformat(),
        }
        return stats
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reload/")
async def reload_index():
    """Reload the vector store index."""
    try:
        search_engine.reload_index()
        return {"message": "Index reloaded successfully"}
    except Exception as e:
        logger.error(f"Failed to reload index: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear/")
async def clear_index():
    """Clear all documents from the vector store."""
    try:
        search_engine.clear_index()
        return {"message": "Index cleared successfully"}
    except Exception as e:
        logger.error(f"Failed to clear index: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a document file for processing and indexing."""
    try:
        # Validate file type
        allowed_extensions = {".pdf", ".txt", ".csv", ".docx"}
        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}",
            )

        # Save file
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process and embed the document
        try:
            # Extract text from the document
            text_content = document_embedder.extract_text(str(file_path))

            # Add to vector store
            search_engine.add_documents(
                documents=[text_content],
                metadata={"document_name": file.filename, "file_path": str(file_path)},
            )

            logger.info(f"✅ Document uploaded and indexed: {file.filename}")

            return {
                "message": "File uploaded and indexed successfully",
                "filename": file.filename,
                "file_path": str(file_path),
                "document_id": f"doc_{len(search_engine.documents)}",
            }

        except Exception as e:
            # Clean up file if processing failed
            if file_path.exists():
                file_path.unlink()
            raise e

    except Exception as e:
        logger.error(f"Failed to upload file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models/")
async def get_available_models():
    """Get list of available embedding models."""
    return {
        "available_models": [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-mpnet-base-v2",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        ],
        "current_model": search_engine.get_model_name(),
        "recommended_model": "sentence-transformers/all-MiniLM-L6-v2",
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Starting RAG Service...")
    uvicorn.run(app, host="0.0.0.0", port=8005)
