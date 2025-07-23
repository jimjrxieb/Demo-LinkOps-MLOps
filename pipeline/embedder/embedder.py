#!/usr/bin/env python3
"""
Document Embedder Component
==========================

Handles document embedding and vector storage for RAG applications.
"""

import hashlib
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np

logger = logging.getLogger(__name__)


class DocumentEmbedder:
    """
    Document embedder component for creating vector embeddings.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the document embedder.

        Args:
            config: Configuration dictionary for embedding settings
        """
        self.config = config or self._get_default_config()
        self.embeddings_dir = Path(self.config.get("embeddings_dir", "/tmp/embeddings"))
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)

        # Initialize embedding model (placeholder for now)
        self.model_name = self.config.get(
            "model_name", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.embedding_dimension = self.config.get("embedding_dimension", 384)

        logger.info("🔍 Document embedder initialized")
        logger.info(f"   Model: {self.model_name}")
        logger.info(f"   Dimension: {self.embedding_dimension}")
        logger.info(f"   Embeddings directory: {self.embeddings_dir}")

    def embed_document(
        self, file_path: str, params: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Embed a document and store the embeddings.

        Args:
            file_path: Path to the document file
            params: Additional embedding parameters

        Returns:
            Path to the stored embeddings

        Raises:
            FileNotFoundError: If the document file doesn't exist
            ValueError: If the file format is not supported
        """
        input_path = Path(file_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Document file not found: {file_path}")

        # Merge parameters
        embedding_params = {**self.config, **(params or {})}

        logger.info(f"📄 Embedding document: {input_path}")

        # Determine file type and process accordingly
        if input_path.suffix.lower() == ".csv":
            return self._embed_csv_document(input_path, embedding_params)
        elif input_path.suffix.lower() in [".xlsx", ".xls"]:
            return self._embed_excel_document(input_path, embedding_params)
        elif input_path.suffix.lower() == ".json":
            return self._embed_json_document(input_path, embedding_params)
        elif input_path.suffix.lower() == ".txt":
            return self._embed_text_document(input_path, embedding_params)
        else:
            raise ValueError(f"Unsupported file format: {input_path.suffix}")

    def _embed_csv_document(self, file_path: Path, params: Dict[str, Any]) -> str:
        """Embed CSV document."""
        logger.info(f"📊 Embedding CSV document: {file_path}")

        try:
            import pandas as pd

            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Failed to read CSV file: {e}")

        # Extract text columns for embedding
        text_columns = self._get_text_columns(df, params)

        # Create embeddings
        embeddings = self._create_embeddings_from_dataframe(df, text_columns, params)

        # Save embeddings
        output_path = self._save_embeddings(embeddings, file_path, params)

        logger.info(f"✅ CSV embeddings saved: {output_path}")
        return output_path

    def _embed_excel_document(self, file_path: Path, params: Dict[str, Any]) -> str:
        """Embed Excel document."""
        logger.info(f"📊 Embedding Excel document: {file_path}")

        try:
            import pandas as pd

            df = pd.read_excel(file_path)
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {e}")

        # Extract text columns for embedding
        text_columns = self._get_text_columns(df, params)

        # Create embeddings
        embeddings = self._create_embeddings_from_dataframe(df, text_columns, params)

        # Save embeddings
        output_path = self._save_embeddings(embeddings, file_path, params)

        logger.info(f"✅ Excel embeddings saved: {output_path}")
        return output_path

    def _embed_json_document(self, file_path: Path, params: Dict[str, Any]) -> str:
        """Embed JSON document."""
        logger.info(f"📊 Embedding JSON document: {file_path}")

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to read JSON file: {e}")

        # Extract text from JSON
        texts = self._extract_text_from_json(data, params)

        # Create embeddings
        embeddings = self._create_embeddings_from_texts(texts, params)

        # Save embeddings
        output_path = self._save_embeddings(embeddings, file_path, params)

        logger.info(f"✅ JSON embeddings saved: {output_path}")
        return output_path

    def _embed_text_document(self, file_path: Path, params: Dict[str, Any]) -> str:
        """Embed text document."""
        logger.info(f"📊 Embedding text document: {file_path}")

        try:
            with open(file_path, "r") as f:
                text = f.read()
        except Exception as e:
            raise ValueError(f"Failed to read text file: {e}")

        # Split text into chunks
        text_chunks = self._split_text_into_chunks(text, params)

        # Create embeddings
        embeddings = self._create_embeddings_from_texts(text_chunks, params)

        # Save embeddings
        output_path = self._save_embeddings(embeddings, file_path, params)

        logger.info(f"✅ Text embeddings saved: {output_path}")
        return output_path

    def _get_text_columns(self, df, params: Dict[str, Any]) -> List[str]:
        """Get text columns from DataFrame."""
        # Use specified columns or auto-detect
        specified_columns = params.get("text_columns", [])

        if specified_columns:
            # Validate specified columns exist
            available_columns = [col for col in specified_columns if col in df.columns]
            if not available_columns:
                raise ValueError(
                    f"None of the specified text columns found: {specified_columns}"
                )
            return available_columns

        # Auto-detect text columns (object dtype)
        text_columns = df.select_dtypes(include=["object"]).columns.tolist()

        # Filter out columns that are likely not text (e.g., IDs, dates)
        filtered_columns = []
        for col in text_columns:
            # Skip columns that are mostly numeric or have very short values
            sample_values = df[col].dropna().head(100)
            if len(sample_values) > 0:
                avg_length = sample_values.astype(str).str.len().mean()
                if avg_length > 10:  # Average length > 10 characters
                    filtered_columns.append(col)

        return filtered_columns[:3]  # Limit to 3 columns

    def _create_embeddings_from_dataframe(
        self, df, text_columns: List[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create embeddings from DataFrame."""
        logger.info(f"   Creating embeddings from {len(text_columns)} text columns")

        embeddings_data = {
            "metadata": {
                "source_file": str(df),
                "text_columns": text_columns,
                "total_rows": len(df),
                "embedding_model": self.model_name,
                "embedding_dimension": self.embedding_dimension,
                "created_at": datetime.now().isoformat(),
            },
            "embeddings": [],
            "texts": [],
        }

        # Process each row
        for idx, row in df.iterrows():
            # Combine text from all text columns
            combined_text = " ".join(
                [str(row[col]) for col in text_columns if pd.notna(row[col])]
            )

            if combined_text.strip():
                # Create embedding (placeholder for now)
                embedding = self._create_single_embedding(combined_text, params)

                embeddings_data["embeddings"].append(embedding)
                embeddings_data["texts"].append(
                    {
                        "row_index": idx,
                        "text": combined_text,
                        "source_columns": text_columns,
                    }
                )

        logger.info(f"   Created {len(embeddings_data['embeddings'])} embeddings")
        return embeddings_data

    def _extract_text_from_json(self, data: Any, params: Dict[str, Any]) -> List[str]:
        """Extract text from JSON data."""
        texts = []

        def extract_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    extract_recursive(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    extract_recursive(item, new_path)
            elif isinstance(obj, str) and len(obj.strip()) > 10:
                texts.append(f"{path}: {obj}")

        extract_recursive(data)
        return texts

    def _split_text_into_chunks(self, text: str, params: Dict[str, Any]) -> List[str]:
        """Split text into chunks for embedding."""
        chunk_size = params.get("chunk_size", 1000)
        chunk_overlap = params.get("chunk_overlap", 200)

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind(".")
                last_newline = chunk.rfind("\n")
                break_point = max(last_period, last_newline)

                if break_point > start + chunk_size // 2:
                    chunk = chunk[: break_point + 1]
                    end = start + break_point + 1

            chunks.append(chunk.strip())
            start = end - chunk_overlap

        return chunks

    def _create_embeddings_from_texts(
        self, texts: List[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create embeddings from list of texts."""
        logger.info(f"   Creating embeddings from {len(texts)} text chunks")

        embeddings_data = {
            "metadata": {
                "source_type": "text_chunks",
                "total_chunks": len(texts),
                "embedding_model": self.model_name,
                "embedding_dimension": self.embedding_dimension,
                "created_at": datetime.now().isoformat(),
            },
            "embeddings": [],
            "texts": [],
        }

        for i, text in enumerate(texts):
            if text.strip():
                # Create embedding (placeholder for now)
                embedding = self._create_single_embedding(text, params)

                embeddings_data["embeddings"].append(embedding)
                embeddings_data["texts"].append({"chunk_index": i, "text": text})

        logger.info(f"   Created {len(embeddings_data['embeddings'])} embeddings")
        return embeddings_data

    def _create_single_embedding(
        self, text: str, params: Dict[str, Any]
    ) -> List[float]:
        """
        Create a single embedding for text.

        This is a placeholder implementation. In a real system, you would:
        1. Use a proper embedding model (e.g., sentence-transformers)
        2. Handle batching for efficiency
        3. Add error handling and retries

        Args:
            text: Text to embed
            params: Embedding parameters

        Returns:
            Embedding vector
        """
        # Placeholder: create a deterministic "embedding" based on text hash
        text_hash = hashlib.md5(text.encode()).hexdigest()

        # Convert hash to a fixed-size vector
        embedding = []
        for i in range(0, len(text_hash), 2):
            if len(embedding) >= self.embedding_dimension:
                break
            hex_pair = text_hash[i : i + 2]
            embedding.append(int(hex_pair, 16) / 255.0)  # Normalize to [0, 1]

        # Pad or truncate to required dimension
        while len(embedding) < self.embedding_dimension:
            embedding.append(0.0)

        embedding = embedding[: self.embedding_dimension]

        return embedding

    def _save_embeddings(
        self, embeddings_data: Dict[str, Any], source_file: Path, params: Dict[str, Any]
    ) -> str:
        """Save embeddings to file."""
        # Generate output filename
        timestamp = int(time.time())
        file_hash = hashlib.md5(str(source_file).encode()).hexdigest()[:8]
        output_filename = f"embeddings_{timestamp}_{file_hash}.json"
        output_path = self.embeddings_dir / output_filename

        # Add source file info
        embeddings_data["metadata"]["source_file"] = str(source_file)
        embeddings_data["metadata"]["embedding_params"] = params

        # Save to file
        with open(output_path, "w") as f:
            json.dump(embeddings_data, f, indent=2)

        logger.info(f"💾 Embeddings saved: {output_path}")
        return str(output_path)

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "embeddings_dir": "/tmp/embeddings",
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
            "embedding_dimension": 384,
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "batch_size": 32,
            "max_text_length": 512,
        }

    def get_embedding_info(self, embedding_path: str) -> Dict[str, Any]:
        """
        Get information about stored embeddings.

        Args:
            embedding_path: Path to the embedding file

        Returns:
            Embedding information
        """
        embedding_file = Path(embedding_path)

        if not embedding_file.exists():
            raise FileNotFoundError(f"Embedding file not found: {embedding_path}")

        try:
            with open(embedding_file, "r") as f:
                data = json.load(f)

            info = {
                "embedding_file": str(embedding_file),
                "file_size": embedding_file.stat().st_size,
                "total_embeddings": len(data.get("embeddings", [])),
                "embedding_dimension": data.get("metadata", {}).get(
                    "embedding_dimension", 0
                ),
                "model_name": data.get("metadata", {}).get(
                    "embedding_model", "unknown"
                ),
                "created_at": data.get("metadata", {}).get("created_at", "unknown"),
                "source_file": data.get("metadata", {}).get("source_file", "unknown"),
            }

            return info

        except Exception as e:
            raise ValueError(f"Failed to read embedding file: {e}")

    def list_embeddings(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List stored embeddings.

        Args:
            limit: Maximum number of embeddings to return

        Returns:
            List of embedding information
        """
        embeddings = []

        for embedding_file in self.embeddings_dir.glob("embeddings_*.json"):
            try:
                info = self.get_embedding_info(str(embedding_file))
                embeddings.append(info)
            except Exception as e:
                logger.warning(f"Failed to get info for {embedding_file}: {e}")

        # Sort by creation time (newest first)
        embeddings.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        # Apply limit
        if limit:
            embeddings = embeddings[:limit]

        return embeddings


def embed_document(file_path: str, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Convenience function to embed a document.

    Args:
        file_path: Path to the document file
        params: Additional embedding parameters

    Returns:
        Path to the stored embeddings
    """
    embedder = DocumentEmbedder()
    return embedder.embed_document(file_path, params)


if __name__ == "__main__":
    # Example usage
    print("🔍 Document Embedder Demo")
    print("=" * 30)

    # Create example data
    example_data = {
        "title": [
            "Introduction to AI",
            "Machine Learning Basics",
            "Deep Learning Fundamentals",
        ],
        "content": [
            "Artificial Intelligence is a branch of computer science that aims to create intelligent machines.",
            "Machine Learning is a subset of AI that enables computers to learn without being explicitly programmed.",
            "Deep Learning uses neural networks with multiple layers to model complex patterns in data.",
        ],
        "category": ["AI", "ML", "DL"],
    }

    import pandas as pd

    df = pd.DataFrame(example_data)
    input_file = "/tmp/documents.csv"
    df.to_csv(input_file, index=False)

    print(f"📝 Created test documents: {input_file}")

    # Test embedding
    embedder = DocumentEmbedder()
    output_file = embedder.embed_document(input_file)

    print(f"✅ Documents embedded: {output_file}")

    # Show embedding info
    info = embedder.get_embedding_info(output_file)
    print(f"\n📊 Embedding Info:")
    print(f"   Total embeddings: {info['total_embeddings']}")
    print(f"   Dimension: {info['embedding_dimension']}")
    print(f"   Model: {info['model_name']}")

    # List embeddings
    embeddings = embedder.list_embeddings(limit=5)
    print(f"\n📋 Found {len(embeddings)} embedding files")

    print("🎉 Document embedder demo completed!")
