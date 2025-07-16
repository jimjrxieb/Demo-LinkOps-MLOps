# 🚀 LinkOps Kubernetes/CD Demo Platform

> **A full-stack platform engineering demo showcasing DevOps, Kubernetes, AI/ML, and MLOps skills**

[![CI/CD Pipeline](https://github.com/your-username/linkops-demo/workflows/LinkOps%20CI/badge.svg)](https://github.com/your-username/linkops-demo/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://hub.docker.com/u/linksrobot)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-CKA%20Certified-blue?logo=kubernetes)](https://www.cncf.io/certification/cka/)
[![MLOps](https://img.shields.io/badge/MLOps-TensorFlow%20%7C%20FastAPI-green?logo=tensorflow)](https://tensorflow.org)

## 🎯 What This Demo Shows

This is a **production-ready platform engineering demo** that simulates how I'd approach end-to-end automation and learning systems in a real job. It demonstrates:

- **DevOps Engineering**: GitHub Actions CI/CD, security scanning, Docker orchestration
- **Kubernetes Expertise**: Helm charts, ArgoCD, multi-service deployments
- **Cloud/Platform Engineering**: Azure VM deployment, Terraform infrastructure
- **AI/ML Engineering**: TensorFlow models, MLOps pipelines, learning systems
- **Full-Stack Development**: Vue.js frontend, FastAPI microservices, modular architecture

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js        │    │   FastAPI       │    │   TensorFlow    │
│   Frontend      │◄──►│   Microservices │◄──►│   ML Models     │
│   (Demo UI)     │    │   (Whis Logic)  │    │   (Training)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub        │    │   Docker        │    │   Kubernetes    │
│   Actions CI/CD  │    │   Containers    │    │   Helm Charts   │
│   (Automation)  │    │   (Orchestration)│   │   (Deployment)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🧠 The Whis Learning Pipeline

The core innovation is the **Whis Pipeline** - an AI-powered system that learns from Kubernetes/CD tasks:

### Pipeline Stages:
1. **Data Input** (`whis_data_input`) - Collects tasks from UI, Q&A, image OCR
2. **Sanitization** (`whis_sanitize`) - Cleans data, removes PII, validates format
3. **AI Processing** (`whis_logic`) - TensorFlow classification + OpenAI fallback
4. **Orchestration** (`mlops_platform`) - Manages workflows, monitoring, logging
5. **Execution** (`whis_execution`) - Deploys resources, manages infrastructure

### AI/ML Integration:
- **TensorFlow Classifier**: Local ML model for task categorization
- **Training Orbs**: Versioned ML models that learn from approved tasks
- **Human-in-Loop**: Approval workflow with feedback for continuous learning
- **Fallback Logic**: OpenAI integration when ML confidence is low

## 🛠️ Technology Stack

### Frontend
- **Vue.js 3** with Composition API
- **Tailwind CSS** for modern UI
- **Vite** for fast development
- **Axios** for API communication

### Backend
- **FastAPI** microservices architecture
- **Python 3.11** with type hints
- **TensorFlow 2.15** for ML models
- **scikit-learn** for data preprocessing
- **Pandas** for data manipulation

### DevOps & Infrastructure
- **GitHub Actions** for CI/CD pipeline
- **Docker** for containerization
- **Kubernetes** with Helm charts
- **ArgoCD** for GitOps deployment
- **Azure VM** for hosting

### Security & Quality
- **Trivy** for vulnerability scanning
- **GitGuardian** for secret detection
- **Bandit** for Python security
- **Ruff** for Python linting
- **ESLint** for JavaScript linting

## 🚀 Quick Start

### Prerequisites
- Docker Desktop with Kubernetes enabled
- Python 3.11+
- Node.js 20+

### Local Development
```bash
# Clone the repository
git clone https://github.com/your-username/linkops-demo.git
cd linkops-demo

# Start the demo
docker-compose up -d

# Access the application
open http://localhost:3000
```

### Production Deployment
```bash
# Deploy to Azure VM (requires setup)
./runes/deploy-demo.sh

# Or use Helm charts
helm install linkops-demo ./helm/demo-stack
```

## 📊 Demo Features

### 1. Task Processing
- Submit Kubernetes/CD tasks through the UI
- Watch real-time processing through the Whis pipeline
- See AI-powered task matching and confidence scoring

### 2. Orb Library
- Browse categorized best practices and solutions
- View Training Orbs (ML models) with versioning and metrics
- Retrain models with new data

### 3. Learning System
- Human-in-loop approval workflow
- Continuous learning from approved tasks
- Versioned model management

### 4. Professional UI
- Modern, responsive design
- Real-time pipeline visualization
- Interactive orb browsing and search

## 🔧 Development Workflow

### Code Quality
```bash
# Python linting and formatting
ruff check mlops/
ruff format mlops/

# Frontend linting
cd frontend && npm run lint

# Security scanning
bandit -r mlops/
trivy fs .
```

### Testing
```bash
# Run tests
pytest mlops/
npm test --prefix frontend

# Build verification
docker-compose build
```

## 📈 MLOps Features

### Model Management
- **Versioned Models**: TensorFlow models with metadata
- **Training Pipeline**: Automated retraining with new data
- **A/B Testing**: Model comparison and selection
- **Monitoring**: Model performance and drift detection

### Data Pipeline
- **Data Validation**: Input sanitization and quality checks
- **Feature Engineering**: Automated feature extraction
- **Label Management**: Human-in-loop labeling workflow
- **Data Versioning**: Tracked data lineage and changes

## 🎯 Interview-Ready Talking Points

### For DevOps Engineers
- "I built a complete CI/CD pipeline with GitHub Actions, including security scanning with Trivy and GitGuardian"
- "The system uses Docker for containerization and can deploy to any Kubernetes cluster"
- "I implemented proper secret management and infrastructure as code"

### For Kubernetes Engineers
- "I designed a multi-service architecture with Helm charts for easy deployment"
- "The system integrates with ArgoCD for GitOps-style deployments"
- "I earned my CKA and this demo shows real-world Kubernetes patterns"

### For AI/ML Engineers
- "I built a custom TensorFlow classifier that learns from engineering tasks"
- "The system includes proper MLOps practices like model versioning and retraining"
- "I implemented human-in-loop workflows for continuous learning"

### For Platform Engineers
- "This demonstrates end-to-end platform engineering from frontend to infrastructure"
- "I used microservices architecture with proper API design and documentation"
- "The system is designed for scalability and maintainability"

## 📚 Learning Resources

### Kubernetes
- [CKA Certification](https://www.cncf.io/certification/cka/)
- [Helm Documentation](https://helm.sh/docs/)
- [ArgoCD User Guide](https://argo-cd.readthedocs.io/)

### AI/ML
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [MLOps Best Practices](https://mlops.community/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### DevOps
- [GitHub Actions](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Security Scanning](https://aquasecurity.github.io/trivy/)

## 🤝 Contributing

This is a demo project showcasing platform engineering skills. For questions or feedback:

1. Review the code and architecture
2. Test the demo functionality
3. Provide constructive feedback on the implementation

## 📄 License

This project is for demonstration purposes. Feel free to use the concepts and patterns in your own work.

---

**Built with ❤️ by a platform engineer passionate about DevOps, Kubernetes, and AI/ML**

*This demo represents the kind of systems I'd build and maintain in a real platform engineering role.*
