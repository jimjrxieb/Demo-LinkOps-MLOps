#!/usr/bin/env python3
"""
RAG Search Engine
================

Core search functionality for retrieval-augmented generation.
"""

import hashlib
import logging
import os
import pickle
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Import schemas
from schemas.query_schema import SearchResult

logger = logging.getLogger(__name__)


class RAGSearchEngine:
    """
    RAG search engine using FAISS for vector similarity search.
    """

    def __init__(
        self,
        vectorstore_path: str = "vectorstore/index.pkl",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        """
        Initialize the RAG search engine.

        Args:
            vectorstore_path: Path to the vector store file
            model_name: Name of the embedding model to use
        """
        self.vectorstore_path = Path(vectorstore_path)
        self.model_name = model_name
        self.embedding_dimension = 384  # Default for all-MiniLM-L6-v2

        # Initialize components
        self.index = None
        self.documents = []
        self.document_metadata = {}
        self.model = None

        # Create vectorstore directory
        self.vectorstore_path.parent.mkdir(parents=True, exist_ok=True)

        # Load or initialize the index
        self._load_or_initialize_index()

        logger.info(f"🔍 RAG search engine initialized")
        logger.info(f"   Model: {self.model_name}")
        logger.info(f"   Vector store: {self.vectorstore_path}")
        logger.info(f"   Documents loaded: {len(self.documents)}")

    def _load_or_initialize_index(self):
        """Load existing index or initialize a new one."""
        try:
            if self.vectorstore_path.exists():
                self._load_index()
                logger.info(
                    f"📂 Loaded existing vector store: {len(self.documents)} documents"
                )
            else:
                self._initialize_index()
                logger.info("🆕 Initialized new vector store")
        except Exception as e:
            logger.error(f"Failed to load/initialize index: {e}")
            self._initialize_index()

    def _initialize_index(self):
        """Initialize a new FAISS index."""
        try:
            import faiss

            # Create FAISS index
            self.index = faiss.IndexFlatL2(self.embedding_dimension)
            self.documents = []
            self.document_metadata = {}

            # Save empty index
            self._save_index()

        except ImportError:
            logger.warning("FAISS not available, using placeholder index")
            self.index = None
            self.documents = []
            self.document_metadata = {}

    def _load_index(self):
        """Load existing FAISS index and documents."""
        try:
            import faiss

            with open(self.vectorstore_path, "rb") as f:
                data = pickle.load(f)

            if isinstance(data, tuple) and len(data) >= 3:
                self.index, self.documents, self.document_metadata = data
            elif isinstance(data, tuple) and len(data) == 2:
                # Backward compatibility
                self.index, self.documents = data
                self.document_metadata = {}
            else:
                raise ValueError("Invalid vector store format")

        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            self._initialize_index()

    def _save_index(self):
        """Save FAISS index and documents."""
        try:
            with open(self.vectorstore_path, "wb") as f:
                pickle.dump((self.index, self.documents, self.document_metadata), f)
        except Exception as e:
            logger.error(f"Failed to save index: {e}")

    def _load_model(self):
        """Load the embedding model."""
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer

                self.model = SentenceTransformer(self.model_name)
                logger.info(f"🤖 Loaded embedding model: {self.model_name}")
            except ImportError:
                logger.error("sentence-transformers not available")
                raise ImportError("sentence-transformers is required for embedding")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise

    def search(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5,
        include_metadata: bool = True,
    ) -> List[SearchResult]:
        """
        Search for similar documents.

        Args:
            query: Search query
            top_k: Number of results to return
            similarity_threshold: Minimum similarity threshold
            include_metadata: Include document metadata in results

        Returns:
            List of search results
        """
        if not self.documents:
            logger.warning("No documents in vector store")
            return []

        if self.index is None:
            logger.error("FAISS index not available")
            return []

        try:
            # Load model if needed
            self._load_model()

            # Encode query
            query_embedding = self.model.encode([query])

            # Search in FAISS index
            distances, indices = self.index.search(
                query_embedding, min(top_k, len(self.documents))
            )

            # Convert distances to similarity scores (1 - normalized distance)
            max_distance = np.max(distances) if np.max(distances) > 0 else 1.0
            similarity_scores = 1.0 - (distances[0] / max_distance)

            # Prepare results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.documents):
                    similarity_score = similarity_scores[i]

                    # Apply similarity threshold
                    if similarity_score >= similarity_threshold:
                        # Get document info
                        doc_id = self._get_document_id(idx)
                        metadata = (
                            self.document_metadata.get(doc_id, {})
                            if include_metadata
                            else None
                        )

                        result = SearchResult(
                            content=self.documents[idx],
                            similarity_score=float(similarity_score),
                            document_id=doc_id,
                            chunk_index=idx,
                            metadata=metadata,
                        )
                        results.append(result)

            logger.info(
                f"🔍 Search completed: {len(results)} results (threshold: {similarity_threshold})"
            )
            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def _get_document_id(self, chunk_index: int) -> str:
        """Get document ID for a chunk index."""
        # This is a simplified implementation
        # In a real system, you'd maintain a mapping from chunk indices to document IDs
        return f"doc_{chunk_index // 10}"  # Assume 10 chunks per document

    def add_documents(
        self, documents: List[str], metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add documents to the vector store.

        Args:
            documents: List of document texts
            metadata: Optional metadata for the documents
        """
        if not documents:
            return

        try:
            # Load model if needed
            self._load_model()

            # Encode documents
            embeddings = self.model.encode(documents)

            # Add to FAISS index
            if self.index is not None:
                self.index.add(embeddings)

            # Add to documents list
            start_idx = len(self.documents)
            self.documents.extend(documents)

            # Add metadata
            if metadata:
                doc_id = f"doc_{len(self.document_metadata)}"
                self.document_metadata[doc_id] = metadata

            # Save updated index
            self._save_index()

            logger.info(f"📄 Added {len(documents)} documents to vector store")

        except Exception as e:
            logger.error(f"Failed to add documents: {e}")

    def reload_index(self):
        """Reload the index from disk."""
        self._load_or_initialize_index()
        logger.info("🔄 Index reloaded")

    def clear_index(self):
        """Clear all documents from the index."""
        self._initialize_index()
        logger.info("🗑️ Index cleared")

    def get_status(self) -> Dict[str, Any]:
        """Get search engine status."""
        return {
            "index_loaded": self.index is not None,
            "document_count": len(self.documents),
            "chunk_count": len(self.documents),
            "model_name": self.model_name,
            "embedding_dimension": self.embedding_dimension,
            "vectorstore_path": str(self.vectorstore_path),
            "last_updated": self._get_last_updated(),
        }

    def get_document_count(self) -> int:
        """Get number of documents in the index."""
        return len(self.documents)

    def get_chunk_count(self) -> int:
        """Get number of chunks in the index."""
        return len(self.documents)

    def get_vectorstore_size(self) -> float:
        """Get vector store size in MB."""
        try:
            if self.vectorstore_path.exists():
                size_bytes = self.vectorstore_path.stat().st_size
                return size_bytes / (1024 * 1024)
            return 0.0
        except Exception:
            return 0.0

    def get_model_name(self) -> str:
        """Get the name of the embedding model."""
        return self.model_name

    def get_embedding_dimension(self) -> int:
        """Get the embedding dimension."""
        return self.embedding_dimension

    def get_index_type(self) -> str:
        """Get the type of vector index."""
        if self.index is not None:
            try:
                import faiss

                if isinstance(self.index, faiss.IndexFlatL2):
                    return "FAISS-FlatL2"
                else:
                    return "FAISS-Other"
            except ImportError:
                return "Unknown"
        return "None"

    def get_last_updated(self) -> str:
        """Get the last update timestamp."""
        try:
            if self.vectorstore_path.exists():
                timestamp = datetime.fromtimestamp(
                    self.vectorstore_path.stat().st_mtime
                )
                return timestamp.isoformat()
        except Exception:
            pass
        return datetime.now().isoformat()

    def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in the index."""
        documents = []

        # Group chunks by document (simplified)
        doc_chunks = {}
        for i, chunk in enumerate(self.documents):
            doc_id = self._get_document_id(i)
            if doc_id not in doc_chunks:
                doc_chunks[doc_id] = []
            doc_chunks[doc_id].append(chunk)

        # Create document info
        for doc_id, chunks in doc_chunks.items():
            doc_info = {
                "document_id": doc_id,
                "filename": f"{doc_id}.txt",
                "file_path": f"/path/to/{doc_id}.txt",
                "file_size_bytes": sum(len(chunk.encode()) for chunk in chunks),
                "chunks_count": len(chunks),
                "embedding_model": self.model_name,
                "created_at": self.get_last_updated(),
                "metadata": self.document_metadata.get(doc_id, {}),
            }
            documents.append(doc_info)

        return documents

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID."""
        documents = self.list_documents()
        for doc in documents:
            if doc["document_id"] == doc_id:
                return doc
        return None

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the index."""
        # This is a simplified implementation
        # In a real system, you'd need to rebuild the index without the document
        logger.warning(f"Document deletion not fully implemented for {doc_id}")
        return False


def search_query(query: str) -> str:
    """
    Convenience function for simple query search.

    Args:
        query: Search query

    Returns:
        Best matching document chunk
    """
    search_engine = RAGSearchEngine()
    results = search_engine.search(query, top_k=1)

    if results:
        return results[0].content
    else:
        return "No relevant documents found."


if __name__ == "__main__":
    # Example usage
    print("🔍 RAG Search Engine Demo")
    print("=" * 30)

    # Initialize search engine
    search_engine = RAGSearchEngine()

    # Add some example documents
    example_docs = [
        "The zero trust model is a security framework that requires all users to be authenticated and authorized before accessing any resources.",
        "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
        "Docker is a platform for developing, shipping, and running applications in containers.",
        "Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.",
    ]

    search_engine.add_documents(example_docs)

    # Test search
    query = "What is zero trust?"
    results = search_engine.search(query, top_k=2)

    print(f"🔍 Query: {query}")
    print(f"📊 Found {len(results)} results:")

    for i, result in enumerate(results, 1):
        print(f"\n{i}. Score: {result.similarity_score:.3f}")
        print(f"   Content: {result.content}")

    # Show status
    status = search_engine.get_status()
    print(
        f"\n📈 Status: {status['document_count']} documents, {status['chunk_count']} chunks"
    )

    print("🎉 RAG search engine demo completed!")
