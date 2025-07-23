# Training Pipeline

A comprehensive pipeline for secure AI training and embedding flow that orchestrates the complete process from data upload to model training or document embedding.

## 🚀 Features

- **Data Intake**: Secure file upload and validation
- **Data Sanitization**: PII redaction and data cleaning
- **Document Embedding**: Vector embedding for RAG applications
- **Model Training**: ML model generation and training
- **Pipeline Orchestration**: Complete workflow management
- **Security Controls**: Configurable security levels and validation
- **Service Integration**: Connects with model-creator and agent-creator services

## 📁 Structure

```
pipeline/
├── main.py                    # Main orchestration entrypoint
├── requirements.txt           # Python dependencies
├── Dockerfile                # Docker configuration
├── README.md                 # This file
├── __init__.py               # Package initialization
├── data-intake/
│   └── intake.py             # Data upload and intake logic
├── data-sanitize/
│   └── sanitizer.py          # Data cleaning and PII redaction
├── embedder/
│   └── embedder.py           # Document embedding and vector storage
└── trainer/
    └── trainer.py            # ML model training and generation
```

## 🛠️ Installation

### Local Development

```bash
# Navigate to pipeline directory
cd DEMO-LinkOps/pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python main.py
```

### Docker

```bash
# Build the image
docker build -t training-pipeline .

# Run the container
docker run -p 8004:8004 training-pipeline
```

## 🔄 Pipeline Flow

The pipeline follows this secure flow:

```
Upload → Sanitize → Embed/Train → Store
```

### 1. Data Intake (`data-intake/`)
- **Purpose**: Handle file uploads and initial processing
- **Features**:
  - File validation and security checks
  - Unique filename generation
  - Metadata tracking
  - Upload history management

### 2. Data Sanitization (`data-sanitize/`)
- **Purpose**: Clean data and redact sensitive information
- **Features**:
  - PII redaction (emails, phones, SSNs, credit cards)
  - Data type validation and conversion
  - Missing value handling
  - Duplicate removal

### 3. Document Embedding (`embedder/`)
- **Purpose**: Create vector embeddings for RAG applications
- **Features**:
  - Multi-format document support (CSV, Excel, JSON, TXT)
  - Text chunking and processing
  - Vector storage and management
  - Embedding metadata tracking

### 4. Model Training (`trainer/`)
- **Purpose**: Generate and train ML models
- **Features**:
  - Integration with model-creator service
  - Support for multiple model types
  - Automatic target column detection
  - Model metadata and versioning

## 📚 Usage

### Basic Pipeline Usage

```python
from pipeline import TrainingPipeline

# Initialize pipeline
pipeline = TrainingPipeline()

# Run RAG pipeline
rag_results = pipeline.run_rag_pipeline(
    upload_file="data.csv",
    embedding_params={
        "chunk_size": 1000,
        "model_name": "sentence-transformers/all-MiniLM-L6-v2"
    }
)

# Run ML pipeline
ml_results = pipeline.run_ml_pipeline(
    upload_file="data.csv",
    task_type="classifier",
    target_col="target",
    model_params={
        "algorithm": "random_forest",
        "test_size": 0.2
    }
)
```

### Convenience Functions

```python
from pipeline import run_pipeline, run_rag_pipeline, run_ml_pipeline

# Run complete pipeline
results = run_pipeline(
    upload_file="data.csv",
    task_type="classifier",
    target_col="target"
)

# Run RAG pipeline
rag_results = run_rag_pipeline("documents.csv")

# Run ML pipeline
ml_results = run_ml_pipeline("data.csv", "regression", "target")
```

## 🎯 Supported Tasks

### RAG (Retrieval-Augmented Generation)
- **Input**: Documents (CSV, Excel, JSON, TXT)
- **Output**: Vector embeddings for semantic search
- **Use Cases**: Document search, question answering, knowledge bases

### Classification
- **Input**: Tabular data with categorical target
- **Output**: Classification model
- **Use Cases**: Spam detection, sentiment analysis, fraud detection

### Regression
- **Input**: Tabular data with numeric target
- **Output**: Regression model
- **Use Cases**: Price prediction, demand forecasting, risk assessment

### Clustering
- **Input**: Tabular data without target
- **Output**: Clustering model
- **Use Cases**: Customer segmentation, anomaly detection, data exploration

### Time Series
- **Input**: Time-series data
- **Output**: Time series model
- **Use Cases**: Forecasting, trend analysis, seasonal patterns

## 🔒 Security Features

### Data Intake Security
- File type validation
- Size limits and restrictions
- Malicious content detection
- Secure file storage

### Data Sanitization
- PII redaction patterns
- Dangerous content removal
- Input validation
- Output sanitization

### Embedding Security
- Safe text processing
- Vector storage security
- Access control
- Audit logging

### Model Security
- Secure model generation
- Validation and testing
- Version control
- Access management

## 🔧 Configuration

### Environment Variables
- `ENVIRONMENT`: Set to "demo" for demo mode
- `EMBEDDINGS_DIR`: Directory for storing embeddings
- `MODELS_DIR`: Directory for storing models
- `UPLOADS_DIR`: Directory for storing uploads

### Pipeline Configuration
```python
config = {
    "embeddings_dir": "/tmp/embeddings",
    "models_dir": "/tmp/models",
    "uploads_dir": "/tmp/uploads",
    "model_creator_url": "http://localhost:8002",
    "agent_creator_url": "http://localhost:8003",
    "security_level": "medium"
}

pipeline = TrainingPipeline(config)
```

## 📊 Example Results

### RAG Pipeline Results
```json
{
  "pipeline_id": "pipeline_1234567890",
  "status": "completed",
  "task_type": "rag",
  "execution_time": 45.2,
  "steps_completed": ["data_intake", "data_sanitization", "document_embedding"],
  "outputs": {
    "raw_data_path": "/tmp/uploads/data.csv",
    "clean_data_path": "/tmp/cleaned_data.csv",
    "embedding_path": "/tmp/embeddings/embeddings_123.json"
  }
}
```

### ML Pipeline Results
```json
{
  "pipeline_id": "pipeline_1234567891",
  "status": "completed",
  "task_type": "ml",
  "execution_time": 67.8,
  "steps_completed": ["data_intake", "data_sanitization", "model_training"],
  "outputs": {
    "raw_data_path": "/tmp/uploads/data.csv",
    "clean_data_path": "/tmp/cleaned_data.csv",
    "model_path": "/tmp/models/classifier_model.py"
  }
}
```

## 🔗 Service Integration

### Model Creator Integration
- **URL**: `http://localhost:8002`
- **Purpose**: Generate ML model code
- **Integration**: Automatic model generation via API calls

### Agent Creator Integration
- **URL**: `http://localhost:8003`
- **Purpose**: Create AI agents for models
- **Integration**: Agent generation for trained models

### Demo RAG Integration
- **URL**: `http://localhost:8001`
- **Purpose**: RAG system for document search
- **Integration**: Embedding storage and retrieval

## 🧪 Testing

### Run Pipeline Demo
```bash
# Run the built-in demo
python main.py
```

### Test Individual Components
```python
# Test data intake
from data_intake.intake import DataIntake
intake = DataIntake()
saved_path = intake.save_upload("test.csv")

# Test data sanitization
from data_sanitize.sanitizer import DataSanitizer
sanitizer = DataSanitizer()
clean_path = sanitizer.sanitize_data(saved_path)

# Test embedding
from embedder.embedder import DocumentEmbedder
embedder = DocumentEmbedder()
embedding_path = embedder.embed_document(clean_path)

# Test training
from trainer.trainer import ModelTrainer
trainer = ModelTrainer()
model_path = trainer.train_model(clean_path, "classifier", "target")
```

## 📈 Monitoring

### Pipeline Status
- Execution tracking
- Step completion monitoring
- Error reporting
- Performance metrics

### Data Flow
- File processing status
- Sanitization reports
- Embedding statistics
- Model training metrics

### Security Monitoring
- Access logs
- Validation results
- Redaction reports
- Security alerts

## 🚀 Deployment

### Docker Compose
The pipeline is integrated into the main Docker Compose stack:

```yaml
pipeline:
  build: ../pipeline
  ports:
    - "8004:8004"
  environment:
    - ENVIRONMENT=demo
  volumes:
    - ../pipeline:/app
    - /tmp/uploads:/tmp/uploads
    - /tmp/embeddings:/tmp/embeddings
    - /tmp/models:/tmp/models
  networks:
    - demo-network
```

### Production Deployment
- Use proper volume mounts for persistent storage
- Configure security settings
- Set up monitoring and logging
- Implement backup strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Update tests if needed
5. Submit a pull request

## 📄 License

This project is part of the LinkOps platform. 