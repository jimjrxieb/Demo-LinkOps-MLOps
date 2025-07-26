"""
RAG Embedding Module
Supports both Instructor and MiniLM models for text embeddings.
"""

import os
from typing import Union, List
import numpy as np
from pathlib import Path
import torch
from sentence_transformers import SentenceTransformer

# Check if CUDA is available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class EmbeddingModel:
    def __init__(self, model_type: str = "minilm"):
        """
        Initialize the embedding model.
        
        Args:
            model_type: Either "instructor" or "minilm"
        """
        self.model_type = model_type.lower()
        self.model = None
        
        if self.model_type == "instructor":
            try:
                from InstructorEmbedding import INSTRUCTOR
                self.model = INSTRUCTOR('hkunlp/instructor-large')
                print("✅ Loaded Instructor model")
            except ImportError:
                print("⚠️ Instructor not available, falling back to MiniLM")
                self.model_type = "minilm"
                
        if self.model_type == "minilm" or self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("✅ Loaded MiniLM model")
            
        # Move model to GPU if available
        if DEVICE == "cuda":
            self.model = self.model.to(DEVICE)
            print("🚀 Using GPU acceleration")
        
    def get_embedding(
        self,
        text: Union[str, List[str]],
        instruction: str = "Represent a tool or policy"
    ) -> np.ndarray:
        """
        Get embeddings for text using the selected model.
        
        Args:
            text: Text or list of texts to embed
            instruction: Only used for Instructor model
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(text, str):
            text = [text]
            
        if self.model_type == "instructor":
            # Instructor needs text-instruction pairs
            inputs = [[t, instruction] for t in text]
            embeddings = self.model.encode(inputs)
        else:
            # MiniLM just needs text
            embeddings = self.model.encode(text)
            
        return np.array(embeddings)

# Create global instance with MiniLM by default
embedding_model = EmbeddingModel("minilm")
get_embedding = embedding_model.get_embedding

if __name__ == "__main__":
    # Test the embeddings
    test_text = "This is a test document about machine learning and AI"
    embedding = get_embedding(test_text)
    print(f"\nTest embedding shape: {embedding.shape}")
    print(f"First 5 dimensions: {embedding[0][:5]}")
