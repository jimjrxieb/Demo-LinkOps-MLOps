# 🔒 LinkOps Secure AI Demo - OCI Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the LinkOps Secure AI Demo on Oracle Cloud Infrastructure (OCI). The demo showcases a complete, self-contained AI platform that processes sensitive data locally without external dependencies.

---

## 🎯 What You'll Deploy

| Component | Purpose | Port |
|-----------|---------|------|
| **Frontend** | Vue.js GUI for all AI operations | 8080 |
| **Unified API** | Single backend for all services | 9000 |
| **ML Models** | Classification, regression, clustering | Integrated |
| **AI Agents** | Task automation and workflow orchestration | Integrated |
| **RAG System** | Document intelligence and search | Integrated |
| **Training Pipeline** | Secure data processing and model training | Integrated |

---

## 🛡️ Security Features

- **Zero External Dependencies**: No calls to OpenAI, Anthropic, or cloud AI services
- **Local Processing**: All AI operations happen on-premises
- **Data Encryption**: Sensitive data encrypted at rest and in transit
- **Audit Logging**: Complete trail of all operations
- **Access Controls**: Role-based permissions and monitoring
- **Air-Gapped Ready**: Works in isolated environments

---

## 📋 Prerequisites

### OCI VM Requirements
- **OS**: Ubuntu 20.04 LTS or later
- **CPU**: 4+ cores recommended
- **RAM**: 8GB+ recommended
- **Storage**: 50GB+ available space
- **Network**: Internet access for initial setup

### Software Requirements
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install additional tools
sudo apt install -y curl wget git
```

---

## 🚀 Quick Deployment

### Option 1: Automated Deployment (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd DEMO-LinkOps

# Run automated deployment
./deploy.sh deploy
```

### Option 2: Manual Deployment
```bash
# Clone and setup
git clone <repository-url>
cd DEMO-LinkOps

# Build and start services
docker-compose -f docker/docker-compose.yml up --build -d

# Check status
docker-compose -f docker/docker-compose.yml ps
```

---

## 📊 Verification

### Check Service Health
```bash
# API Health
curl http://localhost:9000/health

# Frontend Accessibility
curl http://localhost:8080

# System Status
./deploy.sh status
```

### Expected Output
```json
{
  "status": "healthy",
  "service": "unified_api",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "model_creator": {"status": "healthy"},
    "agent_creator": {"status": "healthy"},
    "pipeline": {"status": "healthy"},
    "rag": {"status": "healthy"}
  }
}
```

---

## 🎮 Demo Workflows

### 1. ML Model Creation
```
Frontend → Upload CSV → Select Target → Choose Algorithm → Generate Model
```

**Test with**: `sample_data/employee_data.csv`
- Target: `attrition`
- Type: `classifier`
- Algorithm: `random_forest`

### 2. AI Agent Building
```
Frontend → Define Agent Type → Configure Tools → Set Security → Build Agent
```

**Test with**: TaskBot agent
- Type: `taskbot`
- Capabilities: `data_processing, file_operations`
- Security: `medium`

### 3. RAG Document Search
```
Frontend → Upload Documents → Embed → Query → Get Answers
```

**Test with**: `sample_data/company_documents.txt`
- Query: "What are LinkOps core services?"
- Expected: Detailed service descriptions

### 4. HTC Training Pipeline
```
Frontend → Upload Data → Sanitize → Train/Embed → Store Results
```

**Test with**: Any CSV or text file
- Pipeline: Automatic data processing
- Output: Trained models or embeddings

---

## 🔧 Configuration

### Environment Variables
```bash
# Set in docker-compose.yml or .env file
ENVIRONMENT=demo
PYTHONPATH=/app:/app/ml-models:/app/pipeline:/app/rag
```

### Volume Mounts
```yaml
volumes:
  - demo_data:/app/data          # Persistent data storage
  - demo_logs:/app/logs          # Application logs
  - demo_vectorstore:/app/rag/vectorstore  # RAG embeddings
  - demo_models:/app/ml-models/model-creator/output  # ML models
  - demo_agents:/app/ml-models/agent-creator/output  # AI agents
  - demo_pipeline:/app/pipeline/output  # Pipeline outputs
```

### Port Configuration
```yaml
ports:
  - "8080:80"    # Frontend
  - "9000:9000"  # Unified API
```

---

## 📈 Monitoring & Logs

### Service Logs
```bash
# View all logs
docker-compose -f docker/docker-compose.yml logs -f

# View specific service logs
docker-compose -f docker/docker-compose.yml logs -f unified-api
docker-compose -f docker/docker-compose.yml logs -f frontend
```

### Health Monitoring
```bash
# API Health Check
curl http://localhost:9000/health

# System Status
curl http://localhost:9000/system

# Service-specific health
curl http://localhost:9000/model-creator/health
curl http://localhost:9000/rag/health
curl http://localhost:9000/agent-creator/health
curl http://localhost:9000/pipeline/health
```

### Performance Metrics
- **API Response Time**: < 2 seconds for most operations
- **Model Training**: 30-300 seconds depending on dataset size
- **Document Embedding**: ~1000 chunks/second
- **Memory Usage**: 2-8GB depending on workload

---

## 🔒 Security Hardening

### Network Security
```bash
# Configure firewall (if needed)
sudo ufw allow 8080/tcp  # Frontend
sudo ufw allow 9000/tcp  # API
sudo ufw enable
```

### Data Security
```bash
# Encrypt sensitive volumes
sudo cryptsetup luksFormat /dev/sdb
sudo cryptsetup luksOpen /dev/sdb demo_data
sudo mkfs.ext4 /dev/mapper/demo_data
```

### Access Control
```bash
# Create dedicated user
sudo useradd -m -s /bin/bash linkops
sudo usermod -aG docker linkops

# Set proper permissions
sudo chown -R linkops:linkops /opt/linkops
```

---

## 🚨 Troubleshooting

### Common Issues

**Service won't start**
```bash
# Check Docker resources
docker system df
docker system prune

# Check logs
docker-compose -f docker/docker-compose.yml logs
```

**Port conflicts**
```bash
# Check what's using the ports
sudo netstat -tulpn | grep :8080
sudo netstat -tulpn | grep :9000

# Kill conflicting processes
sudo kill -9 <PID>
```

**Memory issues**
```bash
# Increase Docker memory limit
# Edit /etc/docker/daemon.json
{
  "default-shm-size": "2G",
  "memory": "8G"
}
```

**Permission errors**
```bash
# Fix volume permissions
sudo chown -R 1000:1000 /path/to/volumes
```

### Recovery Procedures

**Restart services**
```bash
./deploy.sh restart
```

**Complete reset**
```bash
./deploy.sh cleanup
./deploy.sh deploy
```

**Backup and restore**
```bash
# Backup
docker run --rm -v demo_data:/data -v $(pwd):/backup alpine tar czf /backup/demo_data_backup.tar.gz -C /data .

# Restore
docker run --rm -v demo_data:/data -v $(pwd):/backup alpine tar xzf /backup/demo_data_backup.tar.gz -C /data
```

---

## 📞 Support

### Documentation
- **API Reference**: http://localhost:9000/docs
- **Health Dashboard**: http://localhost:9000/health
- **System Info**: http://localhost:9000/system

### Logs Location
- **Application Logs**: `/app/logs/`
- **Docker Logs**: `docker-compose logs`
- **System Logs**: `/var/log/`

### Contact
- **Technical Issues**: Check logs and health endpoints
- **Security Concerns**: Review audit logs in `/app/logs/`
- **Performance Issues**: Monitor resource usage with `docker stats`

---

## 🎯 Next Steps

### Production Deployment
1. **Load Balancing**: Add Nginx reverse proxy
2. **Database**: Integrate PostgreSQL for metadata
3. **Monitoring**: Add Prometheus/Grafana
4. **Backup**: Implement automated backup strategy
5. **SSL**: Configure HTTPS certificates

### Customization
1. **Branding**: Update frontend with company branding
2. **Models**: Add custom ML models and algorithms
3. **Integrations**: Connect to existing data sources
4. **Workflows**: Create custom automation workflows
5. **Security**: Implement additional security measures

---

**Ready to deploy?** Run `./deploy.sh deploy` to get started! 