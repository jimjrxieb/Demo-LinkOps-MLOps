# 🔒 Secure AI Deployment Demo for OCI

## Overview

This demo showcases a fully self-contained, secure AI automation platform designed for clients handling **top-secret or sensitive data**. It allows internal teams to train models, build agents, and query private documents using AI — **all without data ever leaving the client's environment.**

---

## 🚀 What It Does

| Feature | Description |
|--------|-------------|
| 🧠 **ML Model Builder** | Build classification or regression models from internal CSVs |
| 🤖 **AI Agent Creator** | Build task or command agents that automate internal tasks |
| 🔎 **RAG Search** | Query embedded documents locally (PDFs, TXT, CSVs, etc) |
| ⏱️ **HTC Training Hub** | Upload → sanitize → train → store results privately |
| 📊 **Reports & Logs** | View saved models, agents, outputs — nothing leaves disk |

---

## 🛡️ Why It's Secure

- **No data leaves the machine** - All processing happens locally
- **No external API calls** - No OpenAI, Anthropic, or cloud dependencies
- **Private vector search** - FAISS-based embeddings stay on-premises
- **Secure document handling** - PII redaction and data sanitization
- **Audit trail** - Complete logging of all operations
- **Air-gapped ready** - Works in isolated environments

---

## 🎮 How to Use

```bash
# 1. Launch everything locally
docker-compose up --build

# 2. Open the frontend GUI
http://localhost:8080

# 3. Use the tabs:
# - ML Creator: train predictive models
# - Agent Creator: automate tasks  
# - HTC: train RAG or improve outputs
# - Reports: view saved agents, tools, and training logs
```

---

## 📁 Architecture

```
DEMO-LinkOps/
├── frontend/           # Vue 3 + Tailwind CSS GUI
│   ├── src/views/      # Main application tabs
│   └── src/components/ # Reusable UI components
├── ml-models/          # ML and Agent creation services
│   ├── model-creator/  # Classification/regression models
│   └── agent-creator/  # Task/command automation agents
├── pipeline/           # Secure training pipeline
│   ├── data-intake/    # File upload and validation
│   ├── data-sanitize/  # PII redaction and cleaning
│   ├── embedder/       # Document vectorization
│   └── trainer/        # ML model training
├── rag/                # Retrieval-Augmented Generation
│   ├── logic/          # FAISS vector search engine
│   ├── schemas/        # API request/response models
│   └── vectorstore/    # Local document embeddings
├── unified-api/        # Single backend router (port 9000)
├── docker/             # Container orchestration
└── docker-compose.yml  # Unified launcher
```

---

## 🔧 Technical Stack

### Frontend
- **Vue 3** - Modern reactive framework
- **Tailwind CSS** - Utility-first styling
- **Vite** - Fast build tool
- **Pinia** - State management

### Backend Services
- **FastAPI** - High-performance Python web framework
- **FAISS** - Facebook AI Similarity Search for vectors
- **Sentence Transformers** - Local embedding models
- **Scikit-learn** - Machine learning algorithms
- **Pandas** - Data manipulation and analysis

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-service orchestration
- **Nginx** - Reverse proxy and static serving

---

## 🧠 Demo Workflows

### 1. ML Model Creation
```
1. Upload CSV file → 2. Select target column → 3. Choose algorithm → 4. Generate model
```

### 2. AI Agent Building
```
1. Define agent type → 2. Configure tools → 3. Set security level → 4. Build agent
```

### 3. RAG Document Search
```
1. Upload documents → 2. Embed into vectors → 3. Query knowledge base → 4. Get answers
```

### 4. HTC Training Pipeline
```
1. Upload data → 2. Sanitize → 3. Train/Embed → 4. Store results
```

---

## 🛡️ Security Features

### Data Privacy
- **Local Processing**: All AI operations happen on-premises
- **No External Calls**: Zero dependencies on external AI services
- **Encrypted Storage**: Sensitive data encrypted at rest
- **Access Controls**: Role-based permissions and audit logs

### Input Validation
- **File Type Validation**: Whitelist of allowed file formats
- **Content Scanning**: Malware and malicious content detection
- **Size Limits**: Configurable file size restrictions
- **PII Detection**: Automatic sensitive data identification

### Output Security
- **Sanitized Results**: All outputs cleaned of sensitive information
- **Audit Logging**: Complete trail of all operations
- **Secure Downloads**: Encrypted file transfers
- **Access Logs**: User activity monitoring

---

## 📊 Performance Metrics

| Operation | Speed | Memory | Storage |
|-----------|-------|--------|---------|
| Document Embedding | ~1000 chunks/sec | ~4MB/1000 chunks | ~1.5MB/1000 chunks |
| Vector Search | ~1ms per query | Minimal | FAISS index |
| Model Training | Varies by dataset | 2-8GB RAM | Model files |
| Agent Generation | ~5-10 seconds | ~500MB | Python scripts |

---

## 🔧 Configuration

### Environment Variables
```bash
# Security
SECURITY_LEVEL=high
ENCRYPTION_ENABLED=true
AUDIT_LOGGING=true

# Performance
MAX_FILE_SIZE=50MB
CHUNK_SIZE=1000
SIMILARITY_THRESHOLD=0.7

# Storage
VECTOR_STORE_PATH=/app/vectorstore
MODEL_STORE_PATH=/app/models
LOG_STORE_PATH=/app/logs
```

### Customization
- **Embedding Models**: Switch between different sentence transformers
- **ML Algorithms**: Add custom scikit-learn models
- **Security Policies**: Configure PII detection rules
- **Storage Backends**: Integrate with existing databases

---

## 🚀 Deployment Options

### Local Development
```bash
git clone <repository>
cd DEMO-LinkOps
docker-compose up --build
```

### OCI VM Deployment
```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy the demo
git clone <repository>
cd DEMO-LinkOps
docker-compose up -d
```

### Air-Gapped Deployment
```bash
# Export images for offline deployment
docker save demo-frontend demo-unified-api -o demo-images.tar

# Transfer to air-gapped system
scp demo-images.tar user@air-gapped-server:/tmp/

# Load and run on air-gapped system
docker load -i /tmp/demo-images.tar
docker-compose up -d
```

---

## 📈 Scaling Considerations

### Horizontal Scaling
- **Load Balancer**: Nginx for frontend distribution
- **API Gateway**: Unified backend router for service discovery
- **Database**: PostgreSQL for metadata storage
- **Cache**: Redis for session management

### Vertical Scaling
- **GPU Support**: CUDA-enabled containers for faster training
- **Memory Optimization**: Configurable resource limits
- **Storage**: Distributed file systems for large datasets

---

## 🔍 Monitoring & Logging

### Health Checks
```bash
# Service health
curl http://localhost:9000/health

# Individual service status
curl http://localhost:9000/pipeline/health
curl http://localhost:9000/rag/health
curl http://localhost:9000/model-creator/health
```

### Logs
```bash
# View all logs
docker-compose logs -f

# Service-specific logs
docker-compose logs -f unified-api
docker-compose logs -f frontend
```

### Metrics
- **API Response Times**: Average and 95th percentile
- **Error Rates**: Failed requests and exceptions
- **Resource Usage**: CPU, memory, and disk utilization
- **User Activity**: Page views and feature usage

---

## 🛠️ Troubleshooting

### Common Issues

**Service won't start**
```bash
# Check Docker resources
docker system df
docker system prune

# Verify ports are available
netstat -tulpn | grep :9000
```

**File upload fails**
```bash
# Check file permissions
ls -la /tmp/uploads/

# Verify file size limits
docker-compose logs unified-api | grep "file size"
```

**Search returns no results**
```bash
# Check vector store
ls -la rag/vectorstore/

# Verify embeddings exist
curl http://localhost:9000/rag/stats
```

---

## 📞 Support

### Documentation
- **API Reference**: `/docs` endpoint for interactive documentation
- **Code Examples**: Sample scripts in `/examples`
- **Configuration**: Environment variable reference

### Contact
- **Technical Issues**: GitHub Issues
- **Security Concerns**: Private security channel
- **Deployment Help**: OCI support team

---

## 🔄 Updates & Maintenance

### Version Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose down
docker-compose up --build -d
```

### Data Backup
```bash
# Backup vector store
tar -czf vectorstore-backup.tar.gz rag/vectorstore/

# Backup models
tar -czf models-backup.tar.gz ml-models/output/

# Backup logs
tar -czf logs-backup.tar.gz logs/
```

---

## 📄 License

This demo is provided as-is for evaluation purposes. Production deployment requires appropriate licensing and support agreements.

---

**Ready to deploy to OCI?** This stack runs on bare metal servers, OCI VMs, and air-gapped machines with full security compliance.
