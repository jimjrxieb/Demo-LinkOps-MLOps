#!/usr/bin/env python3
"""
Training Pipeline - Secure AI Training + Embedding Flow
======================================================

This module orchestrates the complete pipeline from data upload to model training or embedding.
"""

import logging
import os
import time
from datetime import datetime
from typing import Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import pipeline components
from data_intake.intake import DataIntake
from data_sanitize.sanitizer import DataSanitizer
from embedder.embedder import DocumentEmbedder
from trainer.trainer import ModelTrainer


class TrainingPipeline:
    """
    Secure AI Training + Embedding Pipeline

    Orchestrates the complete flow: upload → sanitize → embed/train → store
    """

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """Initialize the training pipeline."""
        self.config = config or {}
        self.pipeline_id = None
        self.start_time = None
        self.end_time = None
        self.status = "idle"
        self.steps_completed = []
        self.errors = []

        # Initialize pipeline components
        self.data_intake = DataIntake()
        self.data_sanitizer = DataSanitizer()
        self.document_embedder = DocumentEmbedder()
        self.model_trainer = ModelTrainer()

        # Pipeline state
        self.raw_data_path = None
        self.clean_data_path = None
        self.embedding_path = None
        self.model_path = None

        logger.info("🚀 Training pipeline initialized")

    def run_pipeline(
        self,
        upload_file: str,
        task_type: str,
        target_col: Optional[str] = None,
        model_params: Optional[dict[str, Any]] = None,
        embedding_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Run the complete training pipeline.

        Args:
            upload_file: Path to uploaded file
            task_type: Type of task (rag, classifier, regression, clustering, time_series)
            target_col: Target column for supervised learning
            model_params: Parameters for model training
            embedding_params: Parameters for document embedding

        Returns:
            Pipeline execution results
        """
        self.pipeline_id = f"pipeline_{int(time.time())}"
        self.start_time = datetime.now()
        self.status = "running"
        self.steps_completed = []
        self.errors = []

        logger.info(f"🔄 Starting pipeline {self.pipeline_id}")
        logger.info(f"   Task type: {task_type}")
        logger.info(f"   Upload file: {upload_file}")

        try:
            # Step 1: Data Intake
            logger.info("📥 Step 1: Data Intake")
            self.raw_data_path = self.data_intake.save_upload(upload_file)
            self.steps_completed.append("data_intake")
            logger.info(f"   Raw data saved to: {self.raw_data_path}")

            # Step 2: Data Sanitization
            logger.info("🧹 Step 2: Data Sanitization")
            self.clean_data_path = self.data_sanitizer.sanitize_data(self.raw_data_path)
            self.steps_completed.append("data_sanitization")
            logger.info(f"   Clean data saved to: {self.clean_data_path}")

            # Step 3: Task-specific processing
            if task_type == "rag":
                logger.info("🔍 Step 3: Document Embedding")
                self.embedding_path = self.document_embedder.embed_document(
                    self.clean_data_path, params=embedding_params
                )
                self.steps_completed.append("document_embedding")
                logger.info(f"   Embeddings saved to: {self.embedding_path}")

            elif task_type in ["classifier", "regression", "clustering", "time_series"]:
                logger.info("🤖 Step 3: Model Training")
                self.model_path = self.model_trainer.train_model(
                    self.clean_data_path, task_type, target_col, params=model_params
                )
                self.steps_completed.append("model_training")
                logger.info(f"   Model saved to: {self.model_path}")

            else:
                raise ValueError(f"Invalid task type: {task_type}")

            # Pipeline completed successfully
            self.status = "completed"
            self.end_time = datetime.now()

            # Prepare results
            results = self._prepare_results()
            logger.info(f"✅ Pipeline {self.pipeline_id} completed successfully")

            return results

        except Exception as e:
            self.status = "failed"
            self.end_time = datetime.now()
            self.errors.append(str(e))

            logger.error(f"❌ Pipeline {self.pipeline_id} failed: {str(e)}")

            # Return error results
            return self._prepare_error_results(str(e))

    def run_rag_pipeline(
        self, upload_file: str, embedding_params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Run RAG-specific pipeline.

        Args:
            upload_file: Path to uploaded file
            embedding_params: Parameters for document embedding

        Returns:
            RAG pipeline results
        """
        return self.run_pipeline(upload_file, "rag", embedding_params=embedding_params)

    def run_ml_pipeline(
        self,
        upload_file: str,
        task_type: str,
        target_col: str,
        model_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Run ML training pipeline.

        Args:
            upload_file: Path to uploaded file
            task_type: Type of ML task (classifier, regression, clustering, time_series)
            target_col: Target column for supervised learning
            model_params: Parameters for model training

        Returns:
            ML pipeline results
        """
        return self.run_pipeline(
            upload_file, task_type, target_col, model_params=model_params
        )

    def _prepare_results(self) -> dict[str, Any]:
        """Prepare pipeline results."""
        execution_time = (self.end_time - self.start_time).total_seconds()

        return {
            "pipeline_id": self.pipeline_id,
            "status": self.status,
            "task_type": self._get_task_type_from_steps(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "execution_time": execution_time,
            "steps_completed": self.steps_completed,
            "errors": self.errors,
            "outputs": {
                "raw_data_path": self.raw_data_path,
                "clean_data_path": self.clean_data_path,
                "embedding_path": self.embedding_path,
                "model_path": self.model_path,
            },
            "metadata": {
                "pipeline_version": "1.0.0",
                "components": {
                    "data_intake": "DataIntake",
                    "data_sanitizer": "DataSanitizer",
                    "document_embedder": "DocumentEmbedder",
                    "model_trainer": "ModelTrainer",
                },
            },
        }

    def _prepare_error_results(self, error_message: str) -> dict[str, Any]:
        """Prepare error results."""
        execution_time = (self.end_time - self.start_time).total_seconds()

        return {
            "pipeline_id": self.pipeline_id,
            "status": self.status,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "execution_time": execution_time,
            "steps_completed": self.steps_completed,
            "errors": self.errors,
            "outputs": {
                "raw_data_path": self.raw_data_path,
                "clean_data_path": self.clean_data_path,
                "embedding_path": self.embedding_path,
                "model_path": self.model_path,
            },
            "error_message": error_message,
        }

    def _get_task_type_from_steps(self) -> str:
        """Determine task type from completed steps."""
        if "document_embedding" in self.steps_completed:
            return "rag"
        elif "model_training" in self.steps_completed:
            return "ml"
        else:
            return "unknown"

    def get_status(self) -> dict[str, Any]:
        """Get current pipeline status."""
        return {
            "pipeline_id": self.pipeline_id,
            "status": self.status,
            "steps_completed": self.steps_completed,
            "errors": self.errors,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
        }


def run_pipeline(
    upload_file: str,
    task_type: str,
    target_col: Optional[str] = None,
    model_params: Optional[dict[str, Any]] = None,
    embedding_params: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Convenience function to run the training pipeline.

    Args:
        upload_file: Path to uploaded file
        task_type: Type of task (rag, classifier, regression, clustering, time_series)
        target_col: Target column for supervised learning
        model_params: Parameters for model training
        embedding_params: Parameters for document embedding

    Returns:
        Pipeline execution results
    """
    pipeline = TrainingPipeline()
    return pipeline.run_pipeline(
        upload_file, task_type, target_col, model_params, embedding_params
    )


def run_rag_pipeline(
    upload_file: str, embedding_params: Optional[dict[str, Any]] = None
) -> dict[str, Any]:
    """Run RAG-specific pipeline."""
    return run_pipeline(upload_file, "rag", embedding_params=embedding_params)


def run_ml_pipeline(
    upload_file: str,
    task_type: str,
    target_col: str,
    model_params: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Run ML training pipeline."""
    return run_pipeline(upload_file, task_type, target_col, model_params=model_params)


if __name__ == "__main__":
    # Example usage
    print("🚀 Training Pipeline Demo")
    print("=" * 40)

    # Example file path (would be provided by upload)
    example_file = "/tmp/example_data.csv"

    # Create example data if it doesn't exist
    if not os.path.exists(example_file):
        import numpy as np
        import pandas as pd

        # Create sample data
        data = {
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100),
            "target": np.random.randint(0, 2, 100),
        }
        df = pd.DataFrame(data)
        df.to_csv(example_file, index=False)
        print(f"📝 Created example data: {example_file}")

    # Run RAG pipeline
    print("\n🔍 Running RAG Pipeline...")
    rag_results = run_rag_pipeline(example_file)
    print(f"✅ RAG Pipeline completed: {rag_results['status']}")
    print(f"   Execution time: {rag_results['execution_time']:.2f}s")

    # Run ML pipeline
    print("\n🤖 Running ML Pipeline...")
    ml_results = run_ml_pipeline(example_file, "classifier", "target")
    print(f"✅ ML Pipeline completed: {ml_results['status']}")
    print(f"   Execution time: {ml_results['execution_time']:.2f}s")

    print("\n🎉 Pipeline demo completed!")
