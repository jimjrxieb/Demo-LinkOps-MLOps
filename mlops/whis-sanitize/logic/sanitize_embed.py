#!/usr/bin/env python3
"""
TensorFlow embedding module for whis-sanitize service.
Uses Universal Sentence Encoder to generate embeddings for task text.
"""

import logging
from typing import List

import tensorflow as tf
import tensorflow_hub as hub

logger = logging.getLogger(__name__)

# Load the Universal Sentence Encoder model
try:
    model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    logger.info("✅ Universal Sentence Encoder model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load USE model: {e}")
    model = None


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for the given text using Universal Sentence Encoder.

    Args:
        text: Input text to embed

    Returns:
        List of floats representing the embedding vector
    """
    if not text or not text.strip():
        logger.warning("Empty text provided for embedding")
        return []

    if model is None:
        logger.error("Model not loaded, cannot generate embedding")
        return []

    try:
        # Clean and prepare text
        cleaned_text = text.strip()

        # Generate embedding
        embedding = model([cleaned_text])

        # Convert to list of floats
        embedding_list = embedding.numpy()[0].tolist()

        logger.info(
            f"Generated embedding for text (length: {len(cleaned_text)} chars, embedding: {len(embedding_list)} dims)"
        )

        return embedding_list

    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        return []


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a batch of texts.

    Args:
        texts: List of input texts to embed

    Returns:
        List of embedding vectors
    """
    if not texts:
        return []

    if model is None:
        logger.error("Model not loaded, cannot generate embeddings")
        return [[] for _ in texts]

    try:
        # Clean and filter texts
        cleaned_texts = [text.strip() for text in texts if text and text.strip()]

        if not cleaned_texts:
            return []

        # Generate embeddings for batch
        embeddings = model(cleaned_texts)

        # Convert to list of lists
        embedding_list = embeddings.numpy().tolist()

        logger.info(f"Generated {len(embedding_list)} embeddings for batch")

        return embedding_list

    except Exception as e:
        logger.error(f"Failed to generate batch embeddings: {e}")
        return [[] for _ in texts]


def get_embedding_info() -> dict:
    """
    Get information about the embedding model and configuration.

    Returns:
        Dictionary with model information
    """
    return {
        "model_name": "Universal Sentence Encoder v4",
        "model_url": "https://tfhub.dev/google/universal-sentence-encoder/4",
        "embedding_dimensions": 512,
        "model_loaded": model is not None,
        "tensorflow_version": tf.__version__,
        "tensorflow_hub_version": (
            hub.__version__ if hasattr(hub, "__version__") else "unknown"
        ),
    }


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Similarity score between 0 and 1
    """
    if not embedding1 or not embedding2:
        return 0.0

    if len(embedding1) != len(embedding2):
        logger.warning("Embedding dimensions don't match")
        return 0.0

    try:
        # Convert to tensors
        e1 = tf.constant(embedding1, dtype=tf.float32)
        e2 = tf.constant(embedding2, dtype=tf.float32)

        # Calculate cosine similarity
        similarity = tf.keras.losses.cosine_similarity(e1, e2, axis=0)

        # Convert to similarity score (1 - distance)
        similarity_score = 1.0 - abs(similarity.numpy())

        return max(0.0, min(1.0, similarity_score))

    except Exception as e:
        logger.error(f"Failed to calculate similarity: {e}")
        return 0.0


# Health check function
def check_embedding_service() -> dict:
    """
    Check if the embedding service is working properly.

    Returns:
        Health status dictionary
    """
    test_text = "This is a test sentence for embedding generation."

    try:
        embedding = generate_embedding(test_text)

        return {
            "status": "healthy" if embedding else "unhealthy",
            "model_loaded": model is not None,
            "test_embedding_length": len(embedding),
            "test_embedding_sample": embedding[:3] if embedding else [],
            "error": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "model_loaded": model is not None,
            "test_embedding_length": 0,
            "test_embedding_sample": [],
            "error": str(e),
        }
