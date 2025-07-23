"""
Training Pipeline Package
========================

Secure AI Training + Embedding Flow

This package orchestrates the complete pipeline from data upload to model training or embedding.
"""

__version__ = "1.0.0"
__author__ = "LinkOps Team"
__description__ = "Secure AI Training + Embedding Pipeline"

from .main import TrainingPipeline, run_ml_pipeline, run_pipeline, run_rag_pipeline

__all__ = ["TrainingPipeline", "run_pipeline", "run_rag_pipeline", "run_ml_pipeline"]
