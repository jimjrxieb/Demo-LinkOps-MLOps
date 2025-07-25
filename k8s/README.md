# DEMO-LinkOps Kubernetes Deployment

This directory contains all Kubernetes manifests and deployment scripts for the DEMO-LinkOps microservices platform.

## 🏗️ Architecture

The platform consists of the following components:

### Core Infrastructure
- **PostgreSQL** (port 5432) - Primary database
- **Redis** (port 6379) - Cache and session store

### Microservices
- **Unified API** (port 9000) - API Gateway aggregating all services
- **RAG Service** (port 8005) - Retrieval-Augmented Generation for document Q&A
- **ML Models** (port 8002) - Machine Learning model management and inference
- **Pipeline** (port 8003) - Data processing and ML pipelines
- **Sync Engine** (port 8004) - Data synchronization service
- **Frontend** (port 3000) - Vue.js web interface

## 📁 File Structure

### Core Manifests
- `namespace.yaml` - Creates the demo-linkops namespace
- `configmap.yaml` - Environment configuration
- `secrets.yaml` - Sensitive configuration (passwords, tokens)

### Database Services
- `postgres.yaml` - PostgreSQL deployment with persistent storage
- `redis.yaml` - Redis deployment with persistent storage

### Application Services
- `backend-deployment.yaml` / `backend-service.yaml` - Unified API Gateway
- `frontend-deployment.yaml` / `frontend-service.yaml` - Vue.js Frontend
- `rag-deployment.yaml` / `rag-service.yaml` - RAG Service with vector storage
- `ml-models.yaml` - ML Models service with model storage
- `pipeline.yaml` - Pipeline service with data storage
- `sync-engine.yaml` - Sync Engine service

### Networking
- `ingress.yaml` - NGINX Ingress with routing to all services

### Deployment Scripts
- `validate.sh` - Validates all manifests before deployment
- `deploy.sh` - Deploys the entire platform in correct order
- `cleanup.sh` - Removes all deployed resources

## 🚀 Quick Deployment

### Prerequisites
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured
- NGINX Ingress Controller installed
- Docker images built and pushed to registry

### Option 1: Automated Deployment (Recommended)
```bash
# Validate all manifests
./validate.sh

# Deploy everything
./deploy.sh

# To cleanup
./cleanup.sh
```

### Option 2: Manual Deployment
```bash
# 1. Create namespace and config
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml

# 2. Deploy databases
kubectl apply -f postgres.yaml
kubectl apply -f redis.yaml

# 3. Deploy microservices
kubectl apply -f rag-service.yaml
kubectl apply -f rag-deployment.yaml
kubectl apply -f ml-models.yaml
kubectl apply -f pipeline.yaml
kubectl apply -f sync-engine.yaml

# 4. Deploy API gateway
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml

# 5. Deploy frontend
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

# 6. Deploy ingress
kubectl apply -f ingress.yaml
```

## 🌐 Access

After deployment, add this to your `/etc/hosts` file:
```
<INGRESS_IP> demo.local
```

Get the ingress IP:
```bash
kubectl get ingress -n demo-linkops
```

### Service URLs
- **Frontend**: http://demo.local
- **API Gateway**: http://demo.local/api
- **RAG Service**: http://demo.local/rag
- **ML Models**: http://demo.local/ml-models
- **Pipeline**: http://demo.local/pipeline
- **Sync Engine**: http://demo.local/sync

## 📊 Monitoring

Check deployment status:
```bash
# Pod status
kubectl get pods -n demo-linkops

# Service status
kubectl get svc -n demo-linkops

# Ingress status
kubectl get ingress -n demo-linkops

# Persistent volumes  
kubectl get pvc -n demo-linkops

# View logs
kubectl logs -f deployment/demo-unified-api -n demo-linkops
```

## 🔧 Configuration

### Environment Variables
All services use the same ConfigMap for consistent configuration:
- `ENVIRONMENT=demo`
- `DEMO_MODE=true`
- Service discovery URLs for inter-service communication

### Secrets
Sensitive data is stored in Kubernetes secrets:
- Database passwords
- API keys (when configured)

### Storage
Each service has dedicated persistent storage:
- PostgreSQL: 1Gi
- Redis: 500Mi
- RAG vectorstore: 2Gi + 1Gi data
- ML Models: 5Gi models + 2Gi data
- Pipeline: 2Gi + 1Gi input data
- Sync Engine: 1Gi

## 🔒 Security Features

- **Namespace isolation** - All resources in dedicated namespace
- **Network policies** - Controlled inter-service communication
- **Resource limits** - CPU and memory constraints
- **Health checks** - Readiness and liveness probes
- **Secret management** - Sensitive data encrypted at rest
- **CORS configuration** - Proper cross-origin handling

## 🐛 Troubleshooting

### Common Issues

1. **ImagePullBackOff errors**
   ```bash
   # Check if images exist in registry
   docker images | grep demo-linkops
   
   # Update image names in manifests if needed
   ```

2. **Persistent Volume issues**
   ```bash
   # Check PVC status
   kubectl get pvc -n demo-linkops
   
   # Check storage class
   kubectl get storageclass
   ```

3. **Service not accessible**
   ```bash
   # Check ingress controller
   kubectl get pods -n ingress-nginx
   
   # Check service endpoints
   kubectl get endpoints -n demo-linkops
   ```

4. **Database connection issues**
   ```bash
   # Check database pods
   kubectl logs deployment/demo-postgres -n demo-linkops
   
   # Test connection from app pod
   kubectl exec -it deployment/demo-unified-api -n demo-linkops -- wget -O- demo-postgres:5432
   ```

### Useful Commands
```bash
# Port forward for direct access
kubectl port-forward svc/demo-unified-api 9000:9000 -n demo-linkops

# Describe resource for detailed info
kubectl describe pod <pod-name> -n demo-linkops

# Get all resources in namespace
kubectl get all -n demo-linkops

# Delete stuck resources
kubectl delete <resource> <name> -n demo-linkops --force --grace-period=0
```

## 📚 Next Steps

1. **SSL/TLS**: Configure certificates for HTTPS
2. **Monitoring**: Deploy Prometheus and Grafana
3. **Logging**: Set up centralized logging with ELK stack  
4. **Backup**: Configure automated database backups
5. **Scaling**: Implement horizontal pod autoscaling
6. **CI/CD**: Integrate with GitOps tools like ArgoCD

## 🤝 Contributing

When modifying manifests:
1. Run `./validate.sh` to check syntax
2. Test in development environment first
3. Update this README if adding new services
4. Follow Kubernetes best practices for naming and labels