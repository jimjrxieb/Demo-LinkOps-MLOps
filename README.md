# 🚀 LinkOps MLOps Platform

![CI](https://github.com/jimjrxieb/LinkOps-MLOps/actions/workflows/main.yml/badge.svg)
![Deployment Status](https://img.shields.io/badge/deployment-ready-brightgreen)
![Services](https://img.shields.io/badge/services-18-blue)
![Frontend](https://img.shields.io/badge/frontend-Vue%203-green)

A sophisticated MLOps platform with intelligent AI agents, automated pipelines, and modern web interface. **Fully deployment-ready** with comprehensive service architecture.

## 🎯 **Quick Start**

```bash
# Clone the repository
git clone https://github.com/shadow-link-industries/linkops-mlops.git
cd LinkOps-MLOps

# Quick deployment (recommended)
./start_platform.sh

# Or manual deployment
cp env.template .env  # Edit values as needed
docker-compose up -d --build
```

**Access Points:**
- 🌐 **Frontend Dashboard:** http://localhost:3000
- 🔧 **API Documentation:** http://localhost:8000/docs
- 📊 **Main Platform API:** http://localhost:8000

## 🏗️ **Current Architecture**

### **Infrastructure Services**
- **PostgreSQL** (Port 5432) - Primary database
- **Redis** (Port 6379) - Caching and sessions  
- **Kafka** (Port 9092) - Message queue and streaming
- **Zookeeper** (Port 2181) - Kafka coordination

### **🧠 MLOps Core Services**
- **MLOps Platform** (Port 8000) - Main API and orchestration
- **Whis Data Input** (Port 8001) - Q&A, YouTube transcripts, image text extraction
- **Whis Sanitize** (Port 8002) - PII anonymization and data cleaning
- **Whis Smithing** (Port 8003) - Orbs (best practices) & Runes (scripts) generation  
- **Whis Enhance** (Port 8004) - AI-powered content improvement
- **Whis Logic** (Port 8005) - ML training and inference logic
- **Whis Webscraper** (Port 8006) - Intelligence harvesting and web data collection
- **Audit Assess** (Port 8007) - Security scanning and vulnerability assessment
- **Audit Migrate** (Port 8008) - Migration execution and automation
- **MLOps Utils** (Port 8009) - Shared utilities and helper functions

### **🤖 Shadow Agents (AI Specialists)**
- **Jimmie Logic** (Port 8010) - Personal AI assistant and task coordination
- **Ficknury Evaluator** (Port 8011) - Task evaluation and quality assessment
- **Audit Logic** (Port 8012) - Security and compliance analysis
- **AuditGuard Logic** (Port 8013) - Advanced security monitoring
- **Kubernetes Specialist** (Port 8014) - K8s operations and cluster management
- **ML Data Scientist** (Port 8015) - Data science and model development
- **Platform Engineer** (Port 8016) - Infrastructure and cloud operations
- **DevOps Engineer** (Port 8017) - CI/CD and automation workflows

### **🎨 Frontend Application**
- **Vue 3 Dashboard** (Port 3000) - Modern sci-fi interface with:
  - 🧠 **Whis Console** - AI interaction and pipeline monitoring
  - 📘 **Orbs Library** - Best practices knowledge base
  - 🧪 **Runes Collection** - Automation scripts and tools
  - 🔍 **Audit Interface** - Security scanning and compliance
  - 💻 **Scripts Manager** - Real-time execution and monitoring

## ✨ **Key Features**

### **🔄 Complete MLOps Pipeline**
- **Data Ingestion**: Q&A processing, YouTube transcripts, image OCR
- **Sanitization**: PII removal, data cleaning, quality scoring
- **AI Generation**: Best practices (Orbs) and automation scripts (Runes)
- **Enhancement**: Continuous improvement through feedback loops
- **Human Approval**: Review and categorization workflow

### **🛡️ Advanced Security**
- **Multi-layer Scanning**: Trivy, Bandit, GitGuardian, SonarQube
- **Container Security**: Non-root containers, minimal base images
- **Secrets Management**: Environment-based configuration
- **Network Isolation**: Service mesh with proper networking

### **☸️ Cloud-Native Architecture**
- **Microservices**: 18 independent, scalable services
- **Container-First**: Docker and Kubernetes native
- **Message-Driven**: Kafka-based async communication
- **API-Driven**: RESTful APIs with OpenAPI documentation

### **📊 Observability & Monitoring**
- **Health Checks**: All services with comprehensive health endpoints
- **Structured Logging**: Centralized log management
- **Metrics Collection**: Performance and usage analytics
- **Real-time Status**: Live service monitoring dashboard

## 🛠️ **Technology Stack**

### **Backend**
- **Languages**: Python 3.11+, Go, Bash
- **Frameworks**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL 15, Redis 7
- **Messaging**: Apache Kafka, Zookeeper
- **AI/ML**: OpenAI APIs, Custom training pipelines

### **Frontend**
- **Framework**: Vue 3 with Composition API
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom sci-fi theme
- **Build Tool**: Vite
- **State Management**: Pinia

### **Infrastructure**
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes, Helm charts
- **CI/CD**: GitHub Actions, ArgoCD
- **Monitoring**: Prometheus, Grafana (planned)
- **Security**: Trivy, Bandit, GitGuardian, SonarQube

## 🚀 **Deployment Options**

### **🎯 Option 1: Automated Startup (Recommended)**
```bash
./start_platform.sh
# Intelligent startup with health checks and service dependencies
```

### **⚙️ Option 2: Docker Compose**
```bash
docker-compose up -d --build
# Simple container deployment
```

### **☸️ Option 3: Kubernetes**
```bash
cd helm/linkops
helm install linkops . --namespace linkops --create-namespace
# Production Kubernetes deployment
```

### **📋 Option 4: Staged Deployment**
```bash
# Infrastructure
docker-compose up -d db redis zookeeper kafka

# Core Platform  
docker-compose up -d mlops_platform

# MLOps Services
docker-compose up -d whis_data_input whis_sanitize whis_smithing whis_enhance whis_logic whis_webscraper audit_assess audit_migrate mlops_utils

# Shadow Agents
docker-compose up -d jimmie_logic ficknury_evaluator audit_logic auditguard_logic kubernetes_specialist ml_data_scientist platform_engineer devops_engineer

# Frontend
docker-compose up -d frontend
```

## 📊 **Platform Workflow**

### **1. Data Input Pipeline**
```
User Input → Whis Data Input → Sanitization → Processing
    ↓               ↓              ↓           ↓
Q&A, YouTube,   Data Collection   PII Removal  Quality Check
Images, Text    and Validation    and Cleaning and Scoring
```

### **2. AI Generation Pipeline**
```
Sanitized Data → Whis Smithing → Enhancement → Human Approval
      ↓              ↓             ↓            ↓
  Processed      Generate Orbs   Improve       Review &
  Content        and Runes       Quality       Categorize
```

### **3. Shadow Agent Network**
```
Specialized Tasks → Shadow Agents → Expert Analysis → Recommendations
       ↓               ↓              ↓               ↓
   K8s, ML, DevOps   Domain Expert   Deep Analysis   Actionable
   Security, Audit   Processing      and Insights    Solutions
```

## 🧪 **Development**

### **Local Development Setup**
```bash
# Backend development
cd mlops/[service_name]
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm run dev

# Run tests
python -m pytest tests/
npm run test
```

### **Code Quality**
- **Python**: Black, isort, flake8, mypy
- **Frontend**: ESLint, Prettier, TypeScript
- **YAML**: yamllint
- **Security**: Bandit, safety

## 📚 **Documentation**

- **[Architecture Guide](docs/architecture/)** - System design and components
- **[API Documentation](http://localhost:8000/docs)** - Interactive API explorer
- **[Deployment Guide](DEPLOYMENT_FIXED.md)** - Complete deployment instructions
- **[Frontend Guide](FRONTEND_INTEGRATION.md)** - UI components and features
- **[Development Setup](docs/development/)** - Local development instructions

## 🔧 **Useful Commands**

```bash
# Service management
docker-compose ps                    # Check service status
docker-compose logs -f [service]     # View logs
docker-compose restart [service]     # Restart service
docker-compose down                  # Stop all services

# Health checks
curl http://localhost:8000/health    # Check main API
curl http://localhost:3000           # Check frontend

# Scaling
docker-compose up -d --scale whis_data_input=2

# Cleanup
docker-compose down -v               # Remove volumes
docker system prune -a               # Clean Docker cache
```

## 🎯 **Current Status**

### ✅ **Ready for Production**
- **Configuration**: All Docker Compose issues resolved
- **Services**: 18 services fully configured and tested
- **Frontend**: Complete Vue 3 application with all views
- **CI/CD**: GitHub Actions pipeline operational
- **Security**: Multi-layer security scanning implemented
- **Documentation**: Comprehensive guides and API docs

### 🚧 **In Progress**
- Kubernetes Helm chart optimization
- Advanced monitoring dashboard
- Performance optimization
- Extended test coverage

### 📋 **Planned Features**
- Advanced analytics dashboard
- Multi-tenant support
- Enhanced AI model training
- Integration with external MLOps tools

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- **Documentation**: Complete guides in `/docs`
- **Issues**: [GitHub Issues](https://github.com/shadow-link-industries/linkops-mlops/issues)
- **API Help**: Interactive docs at http://localhost:8000/docs
- **Deployment Issues**: See [DEPLOYMENT_FIXED.md](DEPLOYMENT_FIXED.md)

---

<div align="center">

**🚀 LinkOps MLOps Platform - Your Complete AI-Powered MLOps Solution ✨**

*Ready for deployment • Production-grade • Scalable • Secure*

</div>
