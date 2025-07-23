#!/usr/bin/env python3
"""
Model Trainer Component
======================

Handles ML model training and generation using the model creator service.
"""

import hashlib
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests

logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Model trainer component for ML model training and generation.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the model trainer.

        Args:
            config: Configuration dictionary for training settings
        """
        self.config = config or self._get_default_config()
        self.models_dir = Path(self.config.get("models_dir", "/tmp/models"))
        self.models_dir.mkdir(parents=True, exist_ok=True)

        # Model creator service configuration
        self.model_creator_url = self.config.get(
            "model_creator_url", "http://localhost:8002"
        )
        self.agent_creator_url = self.config.get(
            "agent_creator_url", "http://localhost:8003"
        )

        logger.info("🤖 Model trainer initialized")
        logger.info(f"   Models directory: {self.models_dir}")
        logger.info(f"   Model creator URL: {self.model_creator_url}")
        logger.info(f"   Agent creator URL: {self.agent_creator_url}")

    def train_model(
        self,
        data_path: str,
        model_type: str,
        target_col: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Train a machine learning model.

        Args:
            data_path: Path to the training data
            model_type: Type of model (classifier, regression, clustering, time_series)
            target_col: Target column for supervised learning
            params: Additional training parameters

        Returns:
            Path to the trained model

        Raises:
            FileNotFoundError: If the data file doesn't exist
            ValueError: If the model type is not supported
        """
        input_path = Path(data_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")

        # Merge parameters
        training_params = {**self.config, **(params or {})}

        logger.info(f"🎯 Training {model_type} model with data: {input_path}")

        # Validate model type
        supported_types = ["classifier", "regression", "clustering", "time_series"]
        if model_type not in supported_types:
            raise ValueError(
                f"Unsupported model type: {model_type}. Supported: {supported_types}"
            )

        # Determine target column if not provided
        if target_col is None and model_type in ["classifier", "regression"]:
            target_col = self._detect_target_column(input_path)

        # Generate model using model creator service
        model_path = self._generate_model_via_service(
            input_path, model_type, target_col, training_params
        )

        # Save training metadata
        metadata_path = self._save_training_metadata(
            input_path, model_type, target_col, training_params, model_path
        )

        logger.info(f"✅ Model training completed: {model_path}")
        return model_path

    def _detect_target_column(self, data_path: Path) -> str:
        """
        Automatically detect target column from data.

        Args:
            data_path: Path to the data file

        Returns:
            Detected target column name
        """
        try:
            import pandas as pd

            if data_path.suffix.lower() == ".csv":
                df = pd.read_csv(data_path)
            elif data_path.suffix.lower() in [".xlsx", ".xls"]:
                df = pd.read_excel(data_path)
            else:
                raise ValueError(f"Unsupported file format: {data_path.suffix}")

            # Look for common target column names
            target_candidates = [
                "target",
                "label",
                "class",
                "category",
                "outcome",
                "result",
                "prediction",
                "y",
                "dependent",
                "response",
            ]

            for candidate in target_candidates:
                if candidate in df.columns:
                    logger.info(f"   Detected target column: {candidate}")
                    return candidate

            # If no common names found, use the last column
            last_column = df.columns[-1]
            logger.info(f"   Using last column as target: {last_column}")
            return last_column

        except Exception as e:
            logger.warning(f"Failed to detect target column: {e}")
            return "target"  # Default fallback

    def _generate_model_via_service(
        self, data_path: Path, model_type: str, target_col: str, params: Dict[str, Any]
    ) -> str:
        """
        Generate model using the model creator service.

        Args:
            data_path: Path to the data file
            model_type: Type of model
            target_col: Target column
            params: Training parameters

        Returns:
            Path to the generated model
        """
        logger.info(f"🔧 Generating model via service: {model_type}")

        try:
            # Prepare request data
            request_data = {
                "model_type": model_type,
                "target_column": target_col,
                "algorithm": params.get("algorithm", "auto"),
                "data_path": str(data_path),
            }

            # Add additional parameters
            if "algorithm" in params:
                request_data["algorithm"] = params["algorithm"]

            # Make request to model creator service
            response = requests.post(
                f"{self.model_creator_url}/generate-model/",
                data=request_data,
                timeout=60,
            )

            if response.status_code == 200:
                result = response.json()
                model_path = result.get("output_path", "")

                if model_path and Path(model_path).exists():
                    logger.info(f"   Model generated successfully: {model_path}")
                    return model_path
                else:
                    raise ValueError("Model generation failed: no output path returned")
            else:
                raise ValueError(
                    f"Model generation failed: {response.status_code} - {response.text}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Service request failed: {e}")
            # Fallback to local generation
            return self._generate_model_locally(
                data_path, model_type, target_col, params
            )

    def _generate_model_locally(
        self, data_path: Path, model_type: str, target_col: str, params: Dict[str, Any]
    ) -> str:
        """
        Generate model locally (fallback method).

        Args:
            data_path: Path to the data file
            model_type: Type of model
            target_col: Target column
            params: Training parameters

        Returns:
            Path to the generated model
        """
        logger.info(f"🔧 Generating model locally: {model_type}")

        # Generate unique filename
        timestamp = int(time.time())
        file_hash = hashlib.md5(str(data_path).encode()).hexdigest()[:8]
        model_filename = f"{model_type}_model_{timestamp}_{file_hash}.py"
        model_path = self.models_dir / model_filename

        # Create a simple model template
        model_code = self._create_model_template(
            model_type, target_col, str(data_path), params
        )

        # Save model code
        with open(model_path, "w") as f:
            f.write(model_code)

        logger.info(f"   Local model generated: {model_path}")
        return str(model_path)

    def _create_model_template(
        self, model_type: str, target_col: str, data_path: str, params: Dict[str, Any]
    ) -> str:
        """
        Create a model template based on type.

        Args:
            model_type: Type of model
            target_col: Target column
            data_path: Path to data
            params: Training parameters

        Returns:
            Model code template
        """
        algorithm = params.get("algorithm", "auto")

        template = f'''#!/usr/bin/env python3
"""
Generated {model_type.title()} Model
==================================

Generated by Model Trainer
Data: {data_path}
Target: {target_col}
Algorithm: {algorithm}
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class {model_type.title()}Model:
    """
    Generated {model_type} model for {target_col} prediction.
    """
    
    def __init__(self):
        self.model = None
        self.feature_columns = None
        self.target_column = "{target_col}"
        self.data_path = "{data_path}"
        self.algorithm = "{algorithm}"
        
    def load_data(self):
        """Load and prepare data."""
        logger.info(f"📊 Loading data from {{self.data_path}}")
        
        # Load data
        if self.data_path.endswith('.csv'):
            df = pd.read_csv(self.data_path)
        elif self.data_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(self.data_path)
        else:
            raise ValueError(f"Unsupported file format: {{self.data_path}}")
        
        # Prepare features and target
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{{self.target_column}}' not found in data")
        
        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]
        
        # Handle categorical features
        categorical_columns = X.select_dtypes(include=['object']).columns
        if len(categorical_columns) > 0:
            X = pd.get_dummies(X, columns=categorical_columns)
        
        self.feature_columns = X.columns.tolist()
        
        return X, y
    
    def train(self):
        """Train the model."""
        logger.info(f"🤖 Training {model_type} model with {{self.algorithm}}")
        
        X, y = self.load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Select and train model
        if "{model_type}" == "classifier":
            from sklearn.ensemble import RandomForestClassifier
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif "{model_type}" == "regression":
            from sklearn.ensemble import RandomForestRegressor
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif "{model_type}" == "clustering":
            from sklearn.cluster import KMeans
            self.model = KMeans(n_clusters=3, random_state=42)
        else:
            raise ValueError(f"Unsupported model type: {{model_type}}")
        
        # Train model
        if "{model_type}" == "clustering":
            self.model.fit(X_train)
            predictions = self.model.predict(X_test)
        else:
            self.model.fit(X_train, y_train)
            predictions = self.model.predict(X_test)
        
        # Evaluate model
        self._evaluate_model(y_test, predictions)
        
        logger.info("✅ Model training completed")
    
    def _evaluate_model(self, y_true, y_pred):
        """Evaluate model performance."""
        if "{model_type}" == "classifier":
            accuracy = accuracy_score(y_true, y_pred)
            logger.info(f"📊 Model Accuracy: {{accuracy:.4f}}")
            logger.info(f"📊 Classification Report:\\n{{classification_report(y_true, y_pred)}}")
        elif "{model_type}" == "regression":
            mse = mean_squared_error(y_true, y_pred)
            r2 = r2_score(y_true, y_pred)
            logger.info(f"📊 Mean Squared Error: {{mse:.4f}}")
            logger.info(f"📊 R² Score: {{r2:.4f}}")
        elif "{model_type}" == "clustering":
            logger.info(f"📊 Clustering completed with {{len(set(y_pred))}} clusters")
    
    def predict(self, X):
        """Make predictions."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Handle categorical features
        categorical_columns = X.select_dtypes(include=['object']).columns
        if len(categorical_columns) > 0:
            X = pd.get_dummies(X, columns=categorical_columns)
        
        return self.model.predict(X)
    
    def save_model(self, filepath):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        model_data = {{
            'model': self.model,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column,
            'algorithm': self.algorithm
        }}
        
        joblib.dump(model_data, filepath)
        logger.info(f"💾 Model saved to {{filepath}}")
    
    def load_model(self, filepath):
        """Load a trained model."""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.feature_columns = model_data['feature_columns']
        self.target_column = model_data['target_column']
        self.algorithm = model_data['algorithm']
        logger.info(f"📂 Model loaded from {{filepath}}")

def main():
    """Demo function to train and test the model."""
    print("🤖 {model_type.title()} Model Demo")
    print("=" * 40)
    
    # Create and train model
    model = {model_type.title()}Model()
    model.train()
    
    # Save model
    model_path = "trained_{model_type}_model.pkl"
    model.save_model(model_path)
    
    print(f"✅ Model training completed and saved to {{model_path}}")
    return model

if __name__ == "__main__":
    model = main()
'''

        return template

    def _save_training_metadata(
        self,
        data_path: Path,
        model_type: str,
        target_col: str,
        params: Dict[str, Any],
        model_path: str,
    ) -> str:
        """
        Save training metadata.

        Args:
            data_path: Path to training data
            model_type: Type of model
            target_col: Target column
            params: Training parameters
            model_path: Path to trained model

        Returns:
            Path to metadata file
        """
        metadata = {
            "model_type": model_type,
            "target_column": target_col,
            "data_path": str(data_path),
            "model_path": model_path,
            "training_params": params,
            "created_at": datetime.now().isoformat(),
            "pipeline_version": "1.0.0",
        }

        # Generate metadata filename
        timestamp = int(time.time())
        file_hash = hashlib.md5(str(data_path).encode()).hexdigest()[:8]
        metadata_filename = f"{model_type}_metadata_{timestamp}_{file_hash}.json"
        metadata_path = self.models_dir / metadata_filename

        # Save metadata
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"📝 Training metadata saved: {metadata_path}")
        return str(metadata_path)

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "models_dir": "/tmp/models",
            "model_creator_url": "http://localhost:8002",
            "agent_creator_url": "http://localhost:8003",
            "algorithm": "auto",
            "test_size": 0.2,
            "random_state": 42,
            "timeout": 60,
        }

    def get_model_info(self, model_path: str) -> Dict[str, Any]:
        """
        Get information about a trained model.

        Args:
            model_path: Path to the model file

        Returns:
            Model information
        """
        model_file = Path(model_path)

        if not model_file.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        info = {
            "model_file": str(model_file),
            "file_size": model_file.stat().st_size,
            "file_size_mb": model_file.stat().st_size / (1024 * 1024),
            "created_time": datetime.fromtimestamp(
                model_file.stat().st_ctime
            ).isoformat(),
            "modified_time": datetime.fromtimestamp(
                model_file.stat().st_mtime
            ).isoformat(),
        }

        # Try to load metadata
        metadata_files = list(self.models_dir.glob("*_metadata_*.json"))
        for metadata_file in metadata_files:
            try:
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)

                if metadata.get("model_path") == model_path:
                    info["metadata"] = metadata
                    break
            except Exception as e:
                logger.warning(f"Failed to load metadata from {metadata_file}: {e}")

        return info

    def list_models(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List trained models.

        Args:
            limit: Maximum number of models to return

        Returns:
            List of model information
        """
        models = []

        # Find model files
        model_files = list(self.models_dir.glob("*.py")) + list(
            self.models_dir.glob("*.pkl")
        )

        for model_file in model_files:
            try:
                info = self.get_model_info(str(model_file))
                models.append(info)
            except Exception as e:
                logger.warning(f"Failed to get info for {model_file}: {e}")

        # Sort by creation time (newest first)
        models.sort(key=lambda x: x.get("created_time", ""), reverse=True)

        # Apply limit
        if limit:
            models = models[:limit]

        return models

    def create_agent_for_model(
        self,
        model_path: str,
        agent_type: str = "taskbot",
        agent_name: Optional[str] = None,
    ) -> str:
        """
        Create an agent for a trained model.

        Args:
            model_path: Path to the trained model
            agent_type: Type of agent to create
            agent_name: Name for the agent

        Returns:
            Path to the created agent
        """
        if agent_name is None:
            model_file = Path(model_path)
            agent_name = f"{model_file.stem}_Agent"

        logger.info(f"🤖 Creating {agent_type} agent for model: {agent_name}")

        try:
            # Prepare request data
            request_data = {
                "agent_type": agent_type,
                "agent_name": agent_name,
                "tools": "model_prediction,data_loading,preprocessing",
                "capabilities": "ml_inference,data_processing,model_management",
                "security_level": "medium",
                "description": f"AI agent for {agent_name} model inference",
            }

            # Make request to agent creator service
            response = requests.post(
                f"{self.agent_creator_url}/generate-agent/",
                data=request_data,
                timeout=60,
            )

            if response.status_code == 200:
                result = response.json()
                agent_path = result.get("output_path", "")

                if agent_path and Path(agent_path).exists():
                    logger.info(f"   Agent created successfully: {agent_path}")
                    return agent_path
                else:
                    raise ValueError("Agent creation failed: no output path returned")
            else:
                raise ValueError(
                    f"Agent creation failed: {response.status_code} - {response.text}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Service request failed: {e}")
            raise


def train_model(
    data_path: str,
    model_type: str,
    target_col: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Convenience function to train a model.

    Args:
        data_path: Path to the training data
        model_type: Type of model (classifier, regression, clustering, time_series)
        target_col: Target column for supervised learning
        params: Additional training parameters

    Returns:
        Path to the trained model
    """
    trainer = ModelTrainer()
    return trainer.train_model(data_path, model_type, target_col, params)


if __name__ == "__main__":
    # Example usage
    print("🤖 Model Trainer Demo")
    print("=" * 30)

    # Create example data
    import numpy as np
    import pandas as pd

    # Create sample classification data
    np.random.seed(42)
    n_samples = 1000

    data = {
        "feature1": np.random.randn(n_samples),
        "feature2": np.random.randn(n_samples),
        "feature3": np.random.randn(n_samples),
        "target": np.random.randint(0, 3, n_samples),  # 3 classes
    }

    df = pd.DataFrame(data)
    input_file = "/tmp/classification_data.csv"
    df.to_csv(input_file, index=False)

    print(f"📝 Created test data: {input_file}")

    # Test model training
    trainer = ModelTrainer()

    # Train classifier
    model_path = trainer.train_model(input_file, "classifier", "target")
    print(f"✅ Model trained: {model_path}")

    # Show model info
    info = trainer.get_model_info(model_path)
    print(f"\n📊 Model Info:")
    print(f"   File size: {info['file_size_mb']:.2f}MB")
    print(f"   Created: {info['created_time']}")

    # List models
    models = trainer.list_models(limit=5)
    print(f"\n📋 Found {len(models)} model files")

    print("🎉 Model trainer demo completed!")
