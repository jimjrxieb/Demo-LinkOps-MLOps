#!/usr/bin/env python3
"""
ML Model Training Module
========================

Comprehensive machine learning model training for property management data.
Supports classification and regression tasks with multiple algorithms.
"""

import logging
import pickle
import time
import uuid
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

# Configuration
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Model registry for tracking trained models
MODEL_REGISTRY_FILE = MODEL_DIR / "model_registry.json"


class ModelTrainer:
    """Comprehensive ML model trainer for property management data."""

    def __init__(self):
        self.model_registry = self._load_model_registry()

    def _load_model_registry(self) -> Dict[str, Any]:
        """Load model registry from file."""
        try:
            if MODEL_REGISTRY_FILE.exists():
                import json

                with open(MODEL_REGISTRY_FILE, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load model registry: {e}")
        return {}

    def _save_model_registry(self):
        """Save model registry to file."""
        try:
            import json

            with open(MODEL_REGISTRY_FILE, "w") as f:
                json.dump(self.model_registry, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save model registry: {e}")

    def train_from_csv(
        self,
        file_path: str,
        target_column: str,
        model_type: str = "classification",
        model_name: str = None,
        test_split: float = 0.2,
        random_state: int = 42,
        algorithm: str = "auto",
    ) -> Dict[str, Any]:
        """
        Train a machine learning model from CSV data.

        Args:
            file_path: Path to CSV file
            target_column: Column to predict
            model_type: "classification" or "regression"
            model_name: Name for the model
            test_split: Fraction of data for testing
            random_state: Random seed for reproducibility
            algorithm: ML algorithm to use ("auto", "random_forest", "logistic_regression", "linear_regression")

        Returns:
            Dictionary with training results and model metadata
        """
        start_time = time.time()

        try:
            logger.info(f"🚀 Starting model training for target: {target_column}")

            # Load and prepare data
            df = self._load_and_prepare_data(file_path, target_column)

            # Split data
            X, y = self._prepare_features_target(df, target_column)
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=test_split,
                random_state=random_state,
                stratify=y if model_type == "classification" else None,
            )

            # Select algorithm
            model = self._select_algorithm(model_type, algorithm)

            # Train model
            logger.info(f"📊 Training {model_type} model with {len(X_train)} samples")
            model.fit(X_train, y_train)

            # Evaluate model
            metrics = self._evaluate_model(model, X_test, y_test, model_type)

            # Generate model ID and save
            model_id = str(uuid.uuid4())
            model_path = MODEL_DIR / f"{model_id}.pkl"

            # Save model
            self._save_model(model, model_path, target_column, X.columns.tolist())

            # Calculate training time
            training_time = round(time.time() - start_time, 2)

            # Prepare results
            results = {
                "model_id": model_id,
                "model_name": model_name or f"{target_column}_{model_type}_predictor",
                "target_column": target_column,
                "model_type": model_type,
                "algorithm": algorithm,
                "accuracy": metrics.get("accuracy", 0),
                "precision": metrics.get("precision", 0),
                "recall": metrics.get("recall", 0),
                "f1_score": metrics.get("f1_score", 0),
                "mse": metrics.get("mse", 0),
                "r2_score": metrics.get("r2_score", 0),
                "training_time": training_time,
                "training_samples": len(X_train),
                "test_samples": len(X_test),
                "feature_count": len(X.columns),
                "feature_columns": X.columns.tolist(),
                "model_path": str(model_path),
                "created_at": datetime.now().isoformat(),
                "cross_validation_score": metrics.get("cv_score", 0),
            }

            # Update registry
            self.model_registry[model_id] = results
            self._save_model_registry()

            logger.info(f"✅ Model training completed successfully")
            logger.info(f"   Model ID: {model_id}")
            logger.info(f"   Accuracy: {results['accuracy']:.4f}")
            logger.info(f"   Training time: {training_time}s")

            return results

        except Exception as e:
            logger.error(f"❌ Model training failed: {e}")
            raise

    def _load_and_prepare_data(
        self, file_path: str, target_column: str
    ) -> pd.DataFrame:
        """Load and prepare data for training."""
        logger.info(f"📁 Loading data from {file_path}")

        # Load CSV
        df = pd.read_csv(file_path)
        logger.info(f"   Loaded {len(df)} rows, {len(df.columns)} columns")

        # Check target column exists
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset")

        # Remove rows with missing target values
        initial_rows = len(df)
        df = df.dropna(subset=[target_column])
        if len(df) < initial_rows:
            logger.warning(
                f"   Removed {initial_rows - len(df)} rows with missing target values"
            )

        # Basic data cleaning
        df = self._clean_data(df)

        logger.info(f"   Final dataset: {len(df)} rows, {len(df.columns)} columns")
        return df

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare data for ML training."""
        # Remove duplicate rows
        initial_rows = len(df)
        df = df.drop_duplicates()
        if len(df) < initial_rows:
            logger.info(f"   Removed {initial_rows - len(df)} duplicate rows")

        # Handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        categorical_columns = df.select_dtypes(include=["object"]).columns

        # Fill numeric missing values with median
        if len(numeric_columns) > 0:
            df[numeric_columns] = df[numeric_columns].fillna(
                df[numeric_columns].median()
            )

        # Fill categorical missing values with mode
        if len(categorical_columns) > 0:
            for col in categorical_columns:
                if df[col].isnull().sum() > 0:
                    mode_value = (
                        df[col].mode().iloc[0] if len(df[col].mode()) > 0 else "Unknown"
                    )
                    df[col] = df[col].fillna(mode_value)

        return df

    def _prepare_features_target(
        self, df: pd.DataFrame, target_column: str
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features and target for training."""
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Handle categorical features
        X = self._encode_categorical_features(X)

        # Handle numeric features
        X = self._scale_numeric_features(X)

        return X, y

    def _encode_categorical_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical features for ML training."""
        categorical_columns = X.select_dtypes(include=["object"]).columns

        if len(categorical_columns) > 0:
            logger.info(f"   Encoding {len(categorical_columns)} categorical features")

            # Create a copy to avoid modifying original
            X_encoded = X.copy()

            for col in categorical_columns:
                # Handle high cardinality (too many unique values)
                unique_count = X_encoded[col].nunique()
                if unique_count > 50:
                    logger.warning(
                        f"   Column '{col}' has {unique_count} unique values, keeping top 20"
                    )
                    # Keep only top 20 most frequent values, replace others with "Other"
                    top_values = X_encoded[col].value_counts().head(20).index
                    X_encoded[col] = X_encoded[col].apply(
                        lambda x: x if x in top_values else "Other"
                    )

                # One-hot encode
                dummies = pd.get_dummies(X_encoded[col], prefix=col, drop_first=True)
                X_encoded = pd.concat([X_encoded, dummies], axis=1)
                X_encoded = X_encoded.drop(columns=[col])

            return X_encoded

        return X

    def _scale_numeric_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Scale numeric features for better model performance."""
        numeric_columns = X.select_dtypes(include=[np.number]).columns

        if len(numeric_columns) > 0:
            logger.info(f"   Scaling {len(numeric_columns)} numeric features")

            # Create a copy to avoid modifying original
            X_scaled = X.copy()

            # Standardize numeric features
            scaler = StandardScaler()
            X_scaled[numeric_columns] = scaler.fit_transform(X_scaled[numeric_columns])

            return X_scaled

        return X

    def _select_algorithm(self, model_type: str, algorithm: str) -> Any:
        """Select the appropriate ML algorithm."""
        if algorithm == "auto":
            if model_type == "classification":
                algorithm = "random_forest"
            else:
                algorithm = "random_forest"

        algorithms = {
            "classification": {
                "random_forest": RandomForestClassifier(
                    n_estimators=100, random_state=42
                ),
                "logistic_regression": LogisticRegression(
                    random_state=42, max_iter=1000
                ),
            },
            "regression": {
                "random_forest": RandomForestRegressor(
                    n_estimators=100, random_state=42
                ),
                "linear_regression": LinearRegression(),
            },
        }

        if algorithm not in algorithms[model_type]:
            raise ValueError(f"Algorithm '{algorithm}' not supported for {model_type}")

        logger.info(f"   Selected algorithm: {algorithm}")
        return algorithms[model_type][algorithm]

    def _evaluate_model(
        self, model: Any, X_test: pd.DataFrame, y_test: pd.Series, model_type: str
    ) -> Dict[str, float]:
        """Evaluate model performance."""
        y_pred = model.predict(X_test)

        metrics = {}

        if model_type == "classification":
            # Classification metrics
            metrics["accuracy"] = round(accuracy_score(y_test, y_pred) * 100, 2)

            # Handle binary vs multiclass
            if len(y_test.unique()) == 2:
                metrics["precision"] = round(
                    precision_score(y_test, y_pred, average="binary") * 100, 2
                )
                metrics["recall"] = round(
                    recall_score(y_test, y_pred, average="binary") * 100, 2
                )
                metrics["f1_score"] = round(
                    f1_score(y_test, y_pred, average="binary") * 100, 2
                )
            else:
                metrics["precision"] = round(
                    precision_score(y_test, y_pred, average="weighted") * 100, 2
                )
                metrics["recall"] = round(
                    recall_score(y_test, y_pred, average="weighted") * 100, 2
                )
                metrics["f1_score"] = round(
                    f1_score(y_test, y_pred, average="weighted") * 100, 2
                )

            # Cross-validation score
            cv_scores = cross_val_score(model, X_test, y_test, cv=5, scoring="accuracy")
            metrics["cv_score"] = round(cv_scores.mean() * 100, 2)

        else:
            # Regression metrics
            metrics["mse"] = round(mean_squared_error(y_test, y_pred), 4)
            metrics["r2_score"] = round(r2_score(y_test, y_pred) * 100, 2)
            metrics["accuracy"] = metrics[
                "r2_score"
            ]  # Use R² as accuracy for regression

            # Cross-validation score
            cv_scores = cross_val_score(model, X_test, y_test, cv=5, scoring="r2")
            metrics["cv_score"] = round(cv_scores.mean() * 100, 2)

        return metrics

    def _save_model(
        self,
        model: Any,
        model_path: Path,
        target_column: str,
        feature_columns: List[str],
    ):
        """Save trained model to disk."""
        model_data = {
            "model": model,
            "target_column": target_column,
            "feature_columns": feature_columns,
            "model_info": {
                "created_at": datetime.now().isoformat(),
                "model_type": type(model).__name__,
            },
        }

        with open(model_path, "wb") as f:
            pickle.dump(model_data, f)

        logger.info(f"   Model saved to: {model_path}")

    def load_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Load a trained model."""
        if model_id not in self.model_registry:
            logger.error(f"Model {model_id} not found in registry")
            return None

        model_info = self.model_registry[model_id]
        model_path = Path(model_info["model_path"])

        if not model_path.exists():
            logger.error(f"Model file not found: {model_path}")
            return None

        try:
            with open(model_path, "rb") as f:
                model_data = pickle.load(f)

            return {
                "model": model_data["model"],
                "target_column": model_data["target_column"],
                "feature_columns": model_data["feature_columns"],
                "model_info": model_data["model_info"],
                "registry_info": model_info,
            }
        except Exception as e:
            logger.error(f"Failed to load model {model_id}: {e}")
            return None

    def predict(self, model_id: str, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions using a trained model."""
        model_data = self.load_model(model_id)
        if not model_data:
            raise ValueError(f"Model {model_id} not found or could not be loaded")

        model = model_data["model"]
        feature_columns = model_data["feature_columns"]

        # Prepare features
        X = self._prepare_prediction_features(features, feature_columns)

        # Make prediction
        prediction = model.predict(X)[0]

        # Get prediction probability for classification
        probability = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0]
            probability = float(max(proba))

        return {
            "prediction": prediction,
            "probability": probability,
            "model_id": model_id,
            "target_column": model_data["target_column"],
        }

    def _prepare_prediction_features(
        self, features: Dict[str, Any], feature_columns: List[str]
    ) -> pd.DataFrame:
        """Prepare features for prediction."""
        # Create DataFrame with expected columns
        X = pd.DataFrame(columns=feature_columns)

        # Fill with provided features
        for col in feature_columns:
            if col in features:
                X[col] = [features[col]]
            else:
                # Fill missing features with 0 (for one-hot encoded features)
                X[col] = [0]

        return X

    def list_models(self) -> List[Dict[str, Any]]:
        """List all trained models."""
        return list(self.model_registry.values())

    def delete_model(self, model_id: str) -> bool:
        """Delete a trained model."""
        if model_id not in self.model_registry:
            return False

        try:
            # Remove model file
            model_info = self.model_registry[model_id]
            model_path = Path(model_info["model_path"])
            if model_path.exists():
                model_path.unlink()

            # Remove from registry
            del self.model_registry[model_id]
            self._save_model_registry()

            logger.info(f"✅ Model {model_id} deleted successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to delete model {model_id}: {e}")
            return False

    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        return self.model_registry.get(model_id)


# Global trainer instance
trainer = ModelTrainer()


def train_from_csv(
    file_path: str,
    target_column: str,
    model_type: str = "classification",
    model_name: str = None,
    test_split: float = 0.2,
    random_state: int = 42,
    algorithm: str = "auto",
) -> Dict[str, Any]:
    """
    Convenience function to train a model from CSV.

    Args:
        file_path: Path to CSV file
        target_column: Column to predict
        model_type: "classification" or "regression"
        model_name: Name for the model
        test_split: Fraction of data for testing
        random_state: Random seed for reproducibility
        algorithm: ML algorithm to use

    Returns:
        Dictionary with training results
    """
    return trainer.train_from_csv(
        file_path=file_path,
        target_column=target_column,
        model_type=model_type,
        model_name=model_name,
        test_split=test_split,
        random_state=random_state,
        algorithm=algorithm,
    )


def predict(model_id: str, features: Dict[str, Any]) -> Dict[str, Any]:
    """Make predictions using a trained model."""
    return trainer.predict(model_id, features)


def list_models() -> List[Dict[str, Any]]:
    """List all trained models."""
    return trainer.list_models()


def delete_model(model_id: str) -> bool:
    """Delete a trained model."""
    return trainer.delete_model(model_id)


def get_model_info(model_id: str) -> Optional[Dict[str, Any]]:
    """Get information about a specific model."""
    return trainer.get_model_info(model_id)


if __name__ == "__main__":
    # Test the model trainer
    print("🧠 ML Model Trainer Test")
    print("=" * 50)

    # Create sample data
    sample_data = pd.DataFrame(
        {
            "rent_amount": [1200, 1500, 1800, 2000, 1600],
            "late_payments": [0, 2, 1, 3, 0],
            "tenant_tenure": [12, 6, 24, 3, 18],
            "eviction_risk": ["low", "medium", "low", "high", "low"],
        }
    )

    sample_file = "sample_tenant_data.csv"
    sample_data.to_csv(sample_file, index=False)

    try:
        # Train a model
        result = train_from_csv(
            file_path=sample_file,
            target_column="eviction_risk",
            model_type="classification",
            model_name="Sample Eviction Predictor",
        )

        print(f"✅ Model trained successfully!")
        print(f"   Model ID: {result['model_id']}")
        print(f"   Accuracy: {result['accuracy']}%")
        print(f"   Training time: {result['training_time']}s")

        # Test prediction
        prediction = predict(
            result["model_id"],
            {"rent_amount": 1700, "late_payments": 1, "tenant_tenure": 15},
        )

        print(f"🧪 Test prediction: {prediction['prediction']}")
        print(f"   Probability: {prediction['probability']:.2f}")

        # List models
        models = list_models()
        print(f"📊 Total models: {len(models)}")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    finally:
        # Cleanup
        if Path(sample_file).exists():
            Path(sample_file).unlink()

    print("\n🎉 Test completed!")
