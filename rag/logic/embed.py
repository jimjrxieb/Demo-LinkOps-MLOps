#!/usr/bin/env python3
"""
Document Embedder
================

Handles document embedding and vector storage for RAG applications.
"""

import hashlib
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class DocumentEmbedder:
    """
    Document embedder for creating vector embeddings from text files.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the document embedder.

        Args:
            model_name: Name of the embedding model to use
        """
        self.model_name = model_name
        self.model = None
        self.embedding_dimension = 384  # Default for all-MiniLM-L6-v2

        logger.info("📄 Document embedder initialized")
        logger.info(f"   Model: {self.model_name}")
        logger.info(f"   Dimension: {self.embedding_dimension}")

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

    def embed_file(
        self,
        file_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Embed a document file into the vector store.

        Args:
            file_path: Path to the document file
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            metadata: Optional metadata for the document

        Returns:
            Embedding statistics
        """
        start_time = time.time()

        try:
            # Load model if needed
            self._load_model()

            # Read file
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Read file content
            with open(file_path_obj, encoding="utf-8") as f:
                text = f.read()

            # Split text into chunks
            chunks = self._split_text_into_chunks(text, chunk_size, chunk_overlap)

            # Create embeddings
            embeddings = self.model.encode(chunks)

            # Save to vector store
            self._save_to_vectorstore(chunks, embeddings, metadata)

            # Calculate statistics
            processing_time = time.time() - start_time
            file_size_bytes = file_path_obj.stat().st_size

            stats = {
                "chunks_created": len(chunks),
                "vectors_generated": len(embeddings),
                "file_size_bytes": file_size_bytes,
                "processing_time": processing_time,
                "embedding_model": self.model_name,
                "embedding_dimension": self.embedding_dimension,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "file_path": str(file_path_obj),
                "file_hash": self._calculate_file_hash(file_path_obj),
            }

            logger.info(
                f"✅ Document embedded: {len(chunks)} chunks in {processing_time:.2f}s"
            )
            return stats

        except Exception as e:
            logger.error(f"Failed to embed file {file_path}: {e}")
            raise

    def _split_text_into_chunks(
        self, text: str, chunk_size: int, chunk_overlap: int
    ) -> list[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Input text
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks

        Returns:
            List of text chunks
        """
        if not text.strip():
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind(".")
                last_newline = chunk.rfind("\n")
                last_exclamation = chunk.rfind("!")
                last_question = chunk.rfind("?")

                break_point = max(
                    last_period, last_newline, last_exclamation, last_question
                )

                if break_point > start + chunk_size // 2:
                    chunk = chunk[: break_point + 1]
                    end = start + break_point + 1

            # Clean up chunk
            chunk = chunk.strip()
            if chunk:
                chunks.append(chunk)

            start = end - chunk_overlap

        return chunks

    def _save_to_vectorstore(
        self,
        chunks: list[str],
        embeddings: np.ndarray,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Save chunks and embeddings to the vector store.

        Args:
            chunks: List of text chunks
            embeddings: Embedding vectors
            metadata: Optional document metadata
        """
        try:
            # Import FAISS
            import pickle

            import faiss

            # Load existing vector store or create new one
            vectorstore_path = Path("vectorstore/index.pkl")
            vectorstore_path.parent.mkdir(parents=True, exist_ok=True)

            if vectorstore_path.exists():
                # Load existing data
                with open(vectorstore_path, "rb") as f:
                    data = pickle.load(f)

                if isinstance(data, tuple) and len(data) >= 3:
                    index, documents, document_metadata = data
                elif isinstance(data, tuple) and len(data) == 2:
                    index, documents = data
                    document_metadata = {}
                else:
                    raise ValueError("Invalid vector store format")
            else:
                # Create new index
                index = faiss.IndexFlatL2(self.embedding_dimension)
                documents = []
                document_metadata = {}

            # Add new embeddings to index
            index.add(embeddings.astype("float32"))

            # Add documents
            documents.extend(chunks)

            # Add metadata
            if metadata:
                doc_id = f"doc_{len(document_metadata)}"
                document_metadata[doc_id] = {
                    **metadata,
                    "chunks_start": len(documents) - len(chunks),
                    "chunks_end": len(documents),
                    "created_at": datetime.now().isoformat(),
                }

            # Save updated vector store
            with open(vectorstore_path, "wb") as f:
                pickle.dump((index, documents, document_metadata), f)

            logger.info(f"💾 Saved to vector store: {len(chunks)} chunks")

        except Exception as e:
            logger.error(f"Failed to save to vector store: {e}")
            raise

    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate SHA-256 hash of a file.

        Args:
            file_path: Path to the file

        Returns:
            SHA-256 hash string
        """
        hash_sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)

        return hash_sha256.hexdigest()

    def embed_text(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        metadata: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Embed text directly into the vector store.

        Args:
            text: Input text
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            metadata: Optional metadata

        Returns:
            Embedding statistics
        """
        start_time = time.time()

        try:
            # Load model if needed
            self._load_model()

            # Split text into chunks
            chunks = self._split_text_into_chunks(text, chunk_size, chunk_overlap)

            if not chunks:
                raise ValueError("No valid chunks created from text")

            # Create embeddings
            embeddings = self.model.encode(chunks)

            # Save to vector store
            self._save_to_vectorstore(chunks, embeddings, metadata)

            # Calculate statistics
            processing_time = time.time() - start_time

            stats = {
                "chunks_created": len(chunks),
                "vectors_generated": len(embeddings),
                "file_size_bytes": len(text.encode("utf-8")),
                "processing_time": processing_time,
                "embedding_model": self.model_name,
                "embedding_dimension": self.embedding_dimension,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "text_length": len(text),
                "text_hash": hashlib.sha256(text.encode()).hexdigest(),
            }

            logger.info(
                f"✅ Text embedded: {len(chunks)} chunks in {processing_time:.2f}s"
            )
            return stats

        except Exception as e:
            logger.error(f"Failed to embed text: {e}")
            raise

    def embed_batch(
        self, file_paths: list[str], chunk_size: int = 1000, chunk_overlap: int = 200
    ) -> list[dict[str, Any]]:
        """
        Embed multiple files in batch.

        Args:
            file_paths: List of file paths
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks

        Returns:
            List of embedding statistics
        """
        results = []

        for file_path in file_paths:
            try:
                stats = self.embed_file(file_path, chunk_size, chunk_overlap)
                results.append(stats)
            except Exception as e:
                logger.error(f"Failed to embed {file_path}: {e}")
                results.append(
                    {"file_path": file_path, "error": str(e), "status": "failed"}
                )

        return results

    def get_embedding_info(self, text: str) -> dict[str, Any]:
        """
        Get information about embedding a text without saving it.

        Args:
            text: Input text

        Returns:
            Embedding information
        """
        try:
            # Load model if needed
            self._load_model()

            # Create single embedding
            embedding = self.model.encode([text])

            return {
                "text_length": len(text),
                "embedding_dimension": embedding.shape[1],
                "embedding_model": self.model_name,
                "embedding_shape": embedding.shape,
                "text_hash": hashlib.sha256(text.encode()).hexdigest(),
            }

        except Exception as e:
            logger.error(f"Failed to get embedding info: {e}")
            raise


def embed_file(file_path: str) -> dict[str, Any]:
    """
    Convenience function to embed a file.

    Args:
        file_path: Path to the file

    Returns:
        Embedding statistics
    """
    embedder = DocumentEmbedder()
    return embedder.embed_file(file_path)


if __name__ == "__main__":
    # Example usage
    print("📄 Document Embedder Demo")
    print("=" * 30)

    # Create example text file
    example_text = """
    The zero trust model is a security framework that requires all users to be authenticated and authorized before accessing any resources.

    Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.

    Docker is a platform for developing, shipping, and running applications in containers.

    Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.
    """

    example_file = "/tmp/example_document.txt"
    with open(example_file, "w") as f:
        f.write(example_text)

    print(f"📝 Created example document: {example_file}")

    # Test embedding
    embedder = DocumentEmbedder()

    # Embed file
    file_stats = embedder.embed_file(example_file, chunk_size=200, chunk_overlap=50)
    print(f"✅ File embedded: {file_stats['chunks_created']} chunks")

    # Embed text directly
    text_stats = embedder.embed_text(example_text, chunk_size=150, chunk_overlap=30)
    print(f"✅ Text embedded: {text_stats['chunks_created']} chunks")

    # Get embedding info
    info = embedder.get_embedding_info("Sample text for embedding")
    print(f"📊 Embedding info: {info['embedding_dimension']} dimensions")

    print("🎉 Document embedder demo completed!")
