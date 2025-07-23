# ML Model Creator

A FastAPI-based service for generating ML models and AI agents using Jinja2 templates.

## 🚀 Features

- **Model Generation**: Create ML models for classification, regression, clustering, and time series
- **Agent Generation**: Generate AI agents for task evaluation, data analysis, and model training
- **Template System**: Jinja2-based templates for customizable code generation
- **File Upload**: Support for CSV file uploads
- **Multiple Algorithms**: Support for various ML algorithms
- **RESTful API**: Clean REST API with comprehensive documentation

## 📁 Structure

```
model-creator/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── README.md           # This file
├── logic/
│   └── model_generator.py  # Core generation logic
├── templates/
│   ├── classification_model.py.jinja
│   ├── regression_model.py.jinja
│   ├── clustering_model.py.jinja
│   ├── time_series_model.py.jinja
│   └── task_evaluator_agent.py.jinja
└── api/
    └── __init__.py
```

## 🛠️ Installation

### Local Development

```bash
# Clone the repository
cd ml-models/model-creator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build the image
docker build -t model-creator .

# Run the container
docker run -p 8000:8000 model-creator
```

## 📚 API Endpoints

### Health Check
```bash
GET /health
```

### Generate ML Model
```bash
POST /generate-model/
```

**Parameters:**
- `model_type` (str): Type of model (classification, regression, clustering, time_series)
- `target_column` (str): Name of the target column
- `algorithm` (str, optional): ML algorithm to use (default: "auto")
- `file` (file, optional): CSV file containing the dataset

**Example:**
```bash
curl -X POST "http://localhost:8000/generate-model/" \
  -F "model_type=classification" \
  -F "target_column=target" \
  -F "algorithm=random_forest" \
  -F "file=@data.csv"
```

### Generate AI Agent
```bash
POST /generate-agent/
```

**Parameters:**
- `agent_type` (str): Type of agent (task_evaluator, data_analyzer, model_trainer, pipeline_orchestrator)
- `capabilities` (str): Comma-separated list of capabilities
- `model_type` (str, optional): Type of model the agent will work with (default: "classification")

**Example:**
```bash
curl -X POST "http://localhost:8000/generate-agent/" \
  -F "agent_type=task_evaluator" \
  -F "capabilities=classification,scoring,recommendation" \
  -F "model_type=classification"
```

### Get Supported Models
```bash
GET /supported-models
```

### Get Supported Agents
```bash
GET /supported-agents
```

## 🎯 Supported Model Types

### Classification
- Random Forest
- Support Vector Machine (SVM)
- Neural Network
- Logistic Regression
- Decision Tree
- Gradient Boosting
- Naive Bayes
- K-Nearest Neighbors

### Regression
- Linear Regression
- Random Forest
- Neural Network
- XGBoost
- Gradient Boosting
- Support Vector Regression (SVR)
- Ridge Regression
- Lasso Regression

### Clustering
- K-Means
- DBSCAN
- Hierarchical Clustering
- Gaussian Mixture
- Spectral Clustering
- Agglomerative Clustering

### Time Series
- ARIMA
- LSTM
- Prophet
- Exponential Smoothing
- SARIMA
- VAR

## 🤖 Supported Agent Types

### Task Evaluator
Evaluates ML tasks and provides scoring and recommendations.

**Capabilities:**
- Classification scoring
- Regression scoring
- Clustering scoring
- Task complexity assessment
- Resource requirement estimation
- Risk assessment

### Data Analyzer
Analyzes datasets and provides insights.

**Capabilities:**
- Data quality assessment
- Feature analysis
- Statistical summaries
- Visualization recommendations
- Data preprocessing suggestions

### Model Trainer
Manages model training pipelines.

**Capabilities:**
- Hyperparameter optimization
- Cross-validation
- Model selection
- Training monitoring
- Performance evaluation

### Pipeline Orchestrator
Orchestrates ML pipelines and workflows.

**Capabilities:**
- Pipeline design
- Workflow automation
- Resource management
- Monitoring and alerting
- Pipeline optimization

## 📊 Example Usage

### Generate a Classification Model

```python
import requests

# Generate classification model
response = requests.post(
    "http://localhost:8000/generate-model/",
    data={
        "model_type": "classification",
        "target_column": "target",
        "algorithm": "random_forest"
    },
    files={"file": open("data.csv", "rb")}
)

result = response.json()
print(f"Model generated: {result['output_path']}")
print(f"Model code:\n{result['model_code']}")
```

### Generate a Task Evaluator Agent

```python
import requests

# Generate task evaluator agent
response = requests.post(
    "http://localhost:8000/generate-agent/",
    data={
        "agent_type": "task_evaluator",
        "capabilities": "classification,scoring,recommendation",
        "model_type": "classification"
    }
)

result = response.json()
print(f"Agent generated: {result['output_path']}")
print(f"Agent code:\n{result['agent_code']}")
```

## 🔧 Configuration

The service can be configured using environment variables:

- `ENVIRONMENT`: Set to "demo" for demo mode
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `TEMPLATE_DIR`: Custom template directory path

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test model generation
curl -X POST "http://localhost:8000/generate-model/" \
  -F "model_type=classification" \
  -F "target_column=target" \
  -F "algorithm=random_forest"

# Test agent generation
curl -X POST "http://localhost:8000/generate-agent/" \
  -F "agent_type=task_evaluator" \
  -F "capabilities=classification,scoring"
```

## 📈 Monitoring

The service includes health checks and logging:

- Health endpoint: `GET /health`
- Logs are written to stdout/stderr
- Docker health checks are configured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Update tests if needed
5. Submit a pull request

## 📄 License

This project is part of the LinkOps platform. 