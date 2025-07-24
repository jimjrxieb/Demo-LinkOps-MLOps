#!/usr/bin/env python3
"""
ML Model Generator
=================

Core logic for training machine learning models from CSV data.
Supports classification and regression with scikit-learn.
"""

import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
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

logger = logging.getLogger(__name__)


class ModelGenerator:
    """
    ML Model Generator for training models from CSV data.
    """

    def __init__(self, models_dir: str = "output/models"):
        """
        Initialize the model generator.

        Args:
            models_dir: Directory to save trained models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        # Available model types
        self.classification_models = {
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "logistic_regression": LogisticRegression(random_state=42, max_iter=1000),
        }

        self.regression_models = {
            "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
            "linear_regression": LinearRegression(),
        }

        logger.info(
            f"🧠 Model Generator initialized with models directory: {self.models_dir}"
        )

    def analyze_dataset(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze CSV dataset and return column information.

        Args:
            file_path: Path to CSV file

        Returns:
            Dictionary with dataset analysis
        """
        try:
            df = pd.read_csv(file_path)

            analysis = {
                "rows": len(df),
                "columns": len(df.columns),
                "column_info": {},
                "missing_values": {},
                "data_types": {},
                "unique_counts": {},
                "suggested_targets": [],
            }

            for col in df.columns:
                col_data = df[col]
                analysis["column_info"][col] = {
                    "dtype": str(col_data.dtype),
                    "unique_count": col_data.nunique(),
                    "missing_count": col_data.isnull().sum(),
                    "missing_percent": (col_data.isnull().sum() / len(df)) * 100,
                }

                analysis["missing_values"][col] = col_data.isnull().sum()
                analysis["data_types"][col] = str(col_data.dtype)
                analysis["unique_counts"][col] = col_data.nunique()

                # Suggest potential target columns
                if (
                    col_data.dtype in ["object", "category"]
                    and col_data.nunique() <= 10
                ):
                    analysis["suggested_targets"].append(
                        {
                            "column": col,
                            "type": "classification",
                            "reason": f"Categorical with {col_data.nunique()} unique values",
                        }
                    )
                elif col_data.dtype in ["int64", "float64"] and col_data.nunique() > 10:
                    analysis["suggested_targets"].append(
                        {
                            "column": col,
                            "type": "regression",
                            "reason": f"Numerical with {col_data.nunique()} unique values",
                        }
                    )

            logger.info(
                f"📊 Dataset analysis complete: {len(df)} rows, {len(df.columns)} columns"
            )
            return analysis

        except Exception as e:
            logger.error(f"Dataset analysis failed: {e}")
            return {"error": f"Failed to analyze dataset: {str(e)}"}

    def preprocess_data(
        self, df: pd.DataFrame, target_column: str
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Preprocess the dataset for training.

        Args:
            df: Input dataframe
            target_column: Target column name

        Returns:
            Tuple of (features, target)
        """
        # Handle missing values
        imputer = SimpleImputer(strategy="mean")

        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Handle categorical features
        categorical_columns = X.select_dtypes(include=["object", "category"]).columns
        numerical_columns = X.select_dtypes(include=["int64", "float64"]).columns

        # Encode categorical variables
        label_encoders = {}
        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le

        # Impute missing values
        X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

        # Handle target variable encoding for classification
        if y.dtype == "object":
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y.astype(str))
            label_encoders["target"] = target_encoder

        return X, y, label_encoders

    def train_model(
        self,
        file_path: str,
        target_column: str,
        model_type: str = "classification",
        model_name: str = "random_forest",
        test_size: float = 0.2,
    ) -> Dict[str, Any]:
        """
        Train a machine learning model from CSV data.

        Args:
            file_path: Path to CSV file
            target_column: Target column name
            model_type: 'classification' or 'regression'
            model_name: Name of the model to use
            test_size: Fraction of data for testing

        Returns:
            Dictionary with training results
        """
        try:
            logger.info(f"🚀 Starting model training: {model_type} with {model_name}")

            # Load data
            df = pd.read_csv(file_path)

            if target_column not in df.columns:
                return {
                    "error": f"Target column '{target_column}' not found in dataset"
                }

            # Preprocess data
            X, y, label_encoders = self.preprocess_data(df, target_column)

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )

            # Select model
            if model_type == "classification":
                if model_name not in self.classification_models:
                    return {"error": f"Unknown classification model: {model_name}"}
                model = self.classification_models[model_name]
            else:
                if model_name not in self.regression_models:
                    return {"error": f"Unknown regression model: {model_name}"}
                model = self.regression_models[model_name]

            # Train model
            model.fit(X_train, y_train)

            # Make predictions
            y_pred = model.predict(X_test)
            y_pred_proba = None
            if hasattr(model, "predict_proba"):
                y_pred_proba = model.predict_proba(X_test)

            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred, model_type)

            # Cross-validation
            cv_scores = cross_val_score(
                model,
                X,
                y,
                cv=5,
                scoring="accuracy" if model_type == "classification" else "r2",
            )

            # Generate unique model ID
            model_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().isoformat()

            # Save model and metadata
            model_filename = f"{model_type}_{model_name}_{target_column}_{model_id}.pkl"
            model_path = self.models_dir / model_filename

            # Save model with metadata
            model_data = {
                "model": model,
                "label_encoders": label_encoders,
                "feature_columns": list(X.columns),
                "target_column": target_column,
                "model_type": model_type,
                "model_name": model_name,
                "training_timestamp": timestamp,
                "model_id": model_id,
            }

            joblib.dump(model_data, model_path)

            # Prepare response
            result = {
                "success": True,
                "model_id": model_id,
                "model_path": str(model_path),
                "model_type": model_type,
                "model_name": model_name,
                "target_column": target_column,
                "training_timestamp": timestamp,
                "dataset_info": {
                    "total_rows": len(df),
                    "training_rows": len(X_train),
                    "test_rows": len(X_test),
                    "features": len(X.columns),
                },
                "metrics": metrics,
                "cross_validation": {
                    "mean_score": cv_scores.mean(),
                    "std_score": cv_scores.std(),
                    "scores": cv_scores.tolist(),
                },
            }

            logger.info(f"✅ Model training completed successfully: {model_id}")
            return result

        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return {"error": f"Training failed: {str(e)}"}

    def _calculate_metrics(
        self, y_true: np.ndarray, y_pred: np.ndarray, model_type: str
    ) -> Dict[str, float]:
        """
        Calculate model performance metrics.

        Args:
            y_true: True values
            y_pred: Predicted values
            model_type: 'classification' or 'regression'

        Returns:
            Dictionary of metrics
        """
        if model_type == "classification":
            return {
                "accuracy": accuracy_score(y_true, y_pred),
                "precision": precision_score(y_true, y_pred, average="weighted"),
                "recall": recall_score(y_true, y_pred, average="weighted"),
                "f1_score": f1_score(y_true, y_pred, average="weighted"),
            }
        else:
            return {
                "mse": mean_squared_error(y_true, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
                "r2_score": r2_score(y_true, y_pred),
            }

    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all trained models.

        Returns:
            List of model information
        """
        models = []

        for model_file in self.models_dir.glob("*.pkl"):
            try:
                model_data = joblib.load(model_file)
                models.append(
                    {
                        "model_id": model_data.get("model_id", "unknown"),
                        "filename": model_file.name,
                        "model_type": model_data.get("model_type", "unknown"),
                        "model_name": model_data.get("model_name", "unknown"),
                        "target_column": model_data.get("target_column", "unknown"),
                        "training_timestamp": model_data.get(
                            "training_timestamp", "unknown"
                        ),
                        "feature_count": len(model_data.get("feature_columns", [])),
                        "file_size": model_file.stat().st_size,
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to load model info for {model_file}: {e}")

        return sorted(models, key=lambda x: x["training_timestamp"], reverse=True)

    def predict(self, model_id: str, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make predictions using a trained model.

        Args:
            model_id: Model ID to use for prediction
            features: Dictionary of feature values

        Returns:
            Prediction result
        """
        try:
            # Find model file
            model_files = list(self.models_dir.glob(f"*{model_id}*.pkl"))
            if not model_files:
                return {"error": f"Model with ID {model_id} not found"}

            model_file = model_files[0]
            model_data = joblib.load(model_file)

            # Prepare features
            feature_columns = model_data["feature_columns"]
            label_encoders = model_data["label_encoders"]

            # Create feature vector
            feature_vector = []
            for col in feature_columns:
                if col in features:
                    value = features[col]
                    # Encode if necessary
                    if col in label_encoders:
                        value = label_encoders[col].transform([str(value)])[0]
                    feature_vector.append(value)
                else:
                    feature_vector.append(0)  # Default value

            # Make prediction
            model = model_data["model"]
            prediction = model.predict([feature_vector])[0]

            # Decode prediction if necessary
            if "target" in label_encoders:
                prediction = label_encoders["target"].inverse_transform([prediction])[0]

            # Get prediction probability if available
            probability = None
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba([feature_vector])[0]
                probability = float(max(proba))

            return {
                "prediction": prediction,
                "probability": probability,
                "model_id": model_id,
                "model_type": model_data["model_type"],
            }

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"error": f"Prediction failed: {str(e)}"}


# Convenience function for backward compatibility
def train_model(
    file_path: str, target_column: str, model_type: str = "classification"
) -> Dict[str, Any]:
    """
    Convenience function for training a model.

    Args:
        file_path: Path to CSV file
        target_column: Target column name
        model_type: 'classification' or 'regression'

    Returns:
        Training result dictionary
    """
    generator = ModelGenerator()
    return generator.train_model(file_path, target_column, model_type)
