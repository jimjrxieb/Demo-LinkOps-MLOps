# unified-api/routers/models.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
from typing import List, Any, Dict, Optional
import pandas as pd
import joblib
import uuid
import datetime
import json
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
import logging

router = APIRouter(prefix="/api")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model storage
MODEL_DIR = Path("db/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
META_FILE = MODEL_DIR / "models.json"

class ModelMeta(BaseModel):
    name: str
    trained_at: str
    accuracy: Optional[float] = None
    mae: Optional[float] = None
    r2: Optional[float] = None
    target_column: str
    feature_columns: List[str]
    model_type: str
    sample_size: int
    training_time: Optional[float] = None

class PredictRequest(BaseModel):
    features: Dict[str, Any]

class PredictResponse(BaseModel):
    prediction: Any
    confidence: Optional[float] = None
    model_name: str
    timestamp: str

class TrainingResponse(BaseModel):
    name: str
    accuracy: Optional[float] = None
    mae: Optional[float] = None
    r2: Optional[float] = None
    model_type: str
    training_time: float
    sample_size: int

def load_meta() -> List[ModelMeta]:
    """Load model metadata from JSON file"""
    if META_FILE.exists():
        try:
            with open(META_FILE, 'r') as f:
                data = json.load(f)
                return [ModelMeta(**m) for m in data]
        except Exception as e:
            logger.error(f"Error loading model metadata: {e}")
            return []
    return []

def save_meta(meta: List[ModelMeta]):
    """Save model metadata to JSON file"""
    try:
        with open(META_FILE, 'w') as f:
            json.dump([m.dict() for m in meta], f, indent=2)
    except Exception as e:
        logger.error(f"Error saving model metadata: {e}")
        raise HTTPException(status_code=500, detail="Failed to save model metadata")

def detect_model_type(y: pd.Series) -> str:
    """Detect if the target is classification or regression"""
    if y.dtype == 'object' or len(y.unique()) < len(y) * 0.1:
        return 'classification'
    return 'regression'

def preprocess_data(df: pd.DataFrame, target_column: str, feature_columns: List[str]):
    """Preprocess data for training"""
    # Handle missing values
    df = df.dropna(subset=[target_column] + feature_columns)
    
    # Prepare features and target
    X = df[feature_columns].copy()
    y = df[target_column].copy()
    
    # Handle categorical features
    label_encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
    
    # Handle categorical target for classification
    model_type = detect_model_type(y)
    if model_type == 'classification':
        le_target = LabelEncoder()
        y = le_target.fit_transform(y.astype(str))
        label_encoders['target'] = le_target
    
    return X, y, label_encoders, model_type

@router.post("/models/train", response_model=TrainingResponse, status_code=201)
async def train_model(
    file: UploadFile = File(...),
    target_column: str = Form(...),
    model_name: Optional[str] = Form(None)
):
    """
    Train a new ML model from uploaded CSV data
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    if not target_column:
        raise HTTPException(status_code=400, detail="Target column is required")
    
    try:
        # Read CSV file
        df = pd.read_csv(file.file)
        logger.info(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
        
        # Validate target column
        if target_column not in df.columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Target column '{target_column}' not found in CSV. Available columns: {list(df.columns)}"
            )
        
        # Use all columns except target as features
        feature_columns = [col for col in df.columns if col != target_column]
        
        if not feature_columns:
            raise HTTPException(
                status_code=400, 
                detail="No feature columns available. CSV must have at least 2 columns."
            )
        
        # Preprocess data
        X, y, label_encoders, model_type = preprocess_data(df, target_column, feature_columns)
        
        if len(X) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Insufficient data. Need at least 10 samples after preprocessing."
            )
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        start_time = datetime.datetime.now()
        
        if model_type == 'classification':
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        model.fit(X_train, y_train)
        
        training_time = (datetime.datetime.now() - start_time).total_seconds()
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        if model_type == 'classification':
            accuracy = accuracy_score(y_test, y_pred)
            mae = None
            r2 = None
        else:
            accuracy = None
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
        
        # Generate model name
        if not model_name:
            model_name = f"model_{uuid.uuid4().hex[:8]}"
        
        # Save model
        model_path = MODEL_DIR / f"{model_name}.joblib"
        model_data = {
            'model': model,
            'label_encoders': label_encoders,
            'feature_columns': feature_columns,
            'model_type': model_type
        }
        joblib.dump(model_data, model_path)
        
        # Update metadata
        meta = load_meta()
        new_meta = ModelMeta(
            name=model_name,
            trained_at=datetime.datetime.utcnow().isoformat(),
            accuracy=accuracy,
            mae=mae,
            r2=r2,
            target_column=target_column,
            feature_columns=feature_columns,
            model_type=model_type,
            sample_size=len(df),
            training_time=training_time
        )
        meta.append(new_meta)
        save_meta(meta)
        
        logger.info(f"Model {model_name} trained successfully")
        
        return TrainingResponse(
            name=model_name,
            accuracy=accuracy,
            mae=mae,
            r2=r2,
            model_type=model_type,
            training_time=training_time,
            sample_size=len(df)
        )
        
    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.get("/models", response_model=List[ModelMeta])
def list_models():
    """
    List all trained models with their metadata
    """
    try:
        return load_meta()
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail="Failed to list models")

@router.get("/models/{model_name}", response_model=ModelMeta)
def get_model(model_name: str):
    """
    Get specific model metadata
    """
    try:
        meta = load_meta()
        for model in meta:
            if model.name == model_name:
                return model
        raise HTTPException(status_code=404, detail="Model not found")
    except Exception as e:
        logger.error(f"Error getting model {model_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model")

@router.post("/models/predict/{model_name}", response_model=PredictResponse)
def predict(model_name: str, payload: PredictRequest):
    """
    Make predictions using a trained model
    """
    try:
        # Load model
        model_path = MODEL_DIR / f"{model_name}.joblib"
        if not model_path.exists():
            raise HTTPException(status_code=404, detail="Model not found")
        
        model_data = joblib.load(model_path)
        model = model_data['model']
        label_encoders = model_data['label_encoders']
        feature_columns = model_data['feature_columns']
        model_type = model_data['model_type']
        
        # Prepare features
        features = payload.features
        
        # Validate features
        missing_features = set(feature_columns) - set(features.keys())
        if missing_features:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required features: {list(missing_features)}"
            )
        
        # Create feature vector
        feature_vector = []
        for col in feature_columns:
            value = features[col]
            
            # Handle categorical features
            if col in label_encoders:
                try:
                    value = label_encoders[col].transform([str(value)])[0]
                except:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Invalid value '{value}' for categorical feature '{col}'"
                    )
            
            feature_vector.append(value)
        
        # Make prediction
        prediction = model.predict([feature_vector])[0]
        
        # Calculate confidence (for classification)
        confidence = None
        if model_type == 'classification':
            proba = model.predict_proba([feature_vector])[0]
            confidence = max(proba)
        
        # Convert prediction back to original format if needed
        if model_type == 'classification' and 'target' in label_encoders:
            prediction = label_encoders['target'].inverse_transform([prediction])[0]
        
        return PredictResponse(
            prediction=prediction,
            confidence=confidence,
            model_name=model_name,
            timestamp=datetime.datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error making prediction with model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.delete("/models/{model_name}")
def delete_model(model_name: str):
    """
    Delete a trained model
    """
    try:
        # Remove model file
        model_path = MODEL_DIR / f"{model_name}.joblib"
        if model_path.exists():
            model_path.unlink()
        
        # Update metadata
        meta = load_meta()
        meta = [m for m in meta if m.name != model_name]
        save_meta(meta)
        
        logger.info(f"Model {model_name} deleted successfully")
        return {"message": f"Model {model_name} deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete model: {str(e)}")

@router.get("/models/{model_name}/info")
def get_model_info(model_name: str):
    """
    Get detailed information about a model
    """
    try:
        # Load model metadata
        meta = load_meta()
        model_meta = None
        for m in meta:
            if m.name == model_name:
                model_meta = m
                break
        
        if not model_meta:
            raise HTTPException(status_code=404, detail="Model not found")
        
        # Load model file for additional info
        model_path = MODEL_DIR / f"{model_name}.joblib"
        if model_path.exists():
            model_data = joblib.load(model_path)
            model = model_data['model']
            
            return {
                "metadata": model_meta.dict(),
                "model_info": {
                    "n_estimators": model.n_estimators,
                    "feature_importance": dict(zip(
                        model_meta.feature_columns, 
                        model.feature_importances_
                    )),
                    "model_type": model_meta.model_type
                }
            }
        else:
            return {"metadata": model_meta.dict()}
            
    except Exception as e:
        logger.error(f"Error getting model info for {model_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}") 