# LinkOps Demo - Helm Charts

This directory contains the Helm charts for deploying the LinkOps Demo platform to Kubernetes.

## 📁 Structure

```
helm/
├── demo-stack/              # Umbrella chart
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── templates/
│   │   ├── _helpers.tpl
│   │   └── secret.yaml
│   └── charts/              # Auto-generated dependencies
├── whis-data-input/         # Individual service chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── whis-sanitize/           # Individual service chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── whis-logic/              # Individual service chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── frontend/                # Individual service chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
└── argocd/                  # ArgoCD Application manifest
    └── Application.yaml
```

## 🚀 Quick Start

### Prerequisites

- Kubernetes cluster (local or remote)
- Helm 3.x
- kubectl configured
- Docker images built and pushed to registry

### 1. Build and Push Images

First, build and push your Docker images:

```bash
# Build images
docker build -t linkops/whis-data-input:latest ./mlops/whis-data-input/
docker build -t linkops/whis-sanitize:latest ./mlops/whis-sanitize/
docker build -t linkops/whis-logic:latest ./mlops/whis-logic/
docker build -t linkops/frontend:latest ./frontend/

# Push to your registry (replace with your registry)
docker tag linkops/whis-data-input:latest your-registry/linkops/whis-data-input:latest
docker tag linkops/whis-sanitize:latest your-registry/linkops/whis-sanitize:latest
docker tag linkops/whis-logic:latest your-registry/linkops/whis-logic:latest
docker tag linkops/frontend:latest your-registry/linkops/frontend:latest

docker push your-registry/linkops/whis-data-input:latest
docker push your-registry/linkops/whis-sanitize:latest
docker push your-registry/linkops/whis-logic:latest
docker push your-registry/linkops/frontend:latest
```

### 2. Configure Values

Update the image repositories in `demo-stack/values.yaml`:

```yaml
whis-data-input:
  image:
    repository: your-registry/linkops/whis-data-input
    tag: "latest"

whis-sanitize:
  image:
    repository: your-registry/linkops/whis-sanitize
    tag: "latest"

whis-logic:
  image:
    repository: your-registry/linkops/whis-logic
    tag: "latest"

frontend:
  image:
    repository: your-registry/linkops/frontend
    tag: "latest"
```

### 3. Set Grok API Key

Update the Grok API key in `demo-stack/values.yaml`:

```yaml
grokApiKey: "your-actual-grok-api-key"
```

### 4. Deploy

Use the deployment script:

```bash
./deploy-helm.sh
```

Or deploy manually:

```bash
# Update dependencies
cd helm/demo-stack
helm dependency update
cd ../..

# Deploy
helm upgrade --install linkops-demo ./helm/demo-stack \
  --namespace linkops-demo \
  --create-namespace \
  --wait \
  --timeout 10m
```

## 🔧 Configuration

### Environment Variables

Each service can be configured via environment variables in the respective `values.yaml`:

```yaml
whis-logic:
  env:
    - name: LOG_LEVEL
      value: "DEBUG"
    - name: GROK_API_KEY
      valueFrom:
        secretKeyRef:
          name: grok-api-secret
          key: api-key
```

### Resource Limits

Adjust resource limits in the values files:

```yaml
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 200m
    memory: 256Mi
```

### Ingress Configuration

The frontend includes an Ingress resource. Configure it in `frontend/values.yaml`:

```yaml
ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
  hosts:
    - host: demo.linkops.local
      paths:
        - path: /
          pathType: Prefix
```

## 🔍 Monitoring

### Check Deployment Status

```bash
kubectl get pods -n linkops-demo
kubectl get services -n linkops-demo
kubectl get ingress -n linkops-demo
```

### View Logs

```bash
# Frontend logs
kubectl logs -n linkops-demo -f deployment/linkops-demo-frontend

# Whis Logic logs
kubectl logs -n linkops-demo -f deployment/linkops-demo-whis-logic

# All service logs
kubectl logs -n linkops-demo -l app.kubernetes.io/part-of=linkops-demo
```

### Port Forwarding

```bash
# Frontend
kubectl port-forward -n linkops-demo svc/linkops-demo-frontend 3000:3000

# Whis Logic
kubectl port-forward -n linkops-demo svc/linkops-demo-whis-logic 8003:8003
```

## 🗑️ Cleanup

To uninstall the deployment:

```bash
helm uninstall linkops-demo -n linkops-demo
kubectl delete namespace linkops-demo
```

## 🔄 ArgoCD Integration

The `argocd/Application.yaml` file provides an ArgoCD Application manifest for GitOps deployment.

To deploy via ArgoCD:

1. Apply the Application manifest:

   ```bash
   kubectl apply -f helm/argocd/Application.yaml
   ```

2. ArgoCD will automatically sync the application and deploy the demo stack.

## 🐛 Troubleshooting

### Common Issues

1. **Images not found**: Ensure images are built and pushed to the correct registry
2. **API key issues**: Verify the Grok API key is set correctly in values.yaml
3. **Ingress not working**: Check if your cluster has an Ingress controller installed
4. **Services not communicating**: Verify service names and ports match the configuration

### Debug Commands

```bash
# Check Helm release status
helm status linkops-demo -n linkops-demo

# Check Helm values
helm get values linkops-demo -n linkops-demo

# Describe resources
kubectl describe pod -n linkops-demo -l app.kubernetes.io/name=frontend
kubectl describe service -n linkops-demo linkops-demo-frontend

# Check events
kubectl get events -n linkops-demo --sort-by='.lastTimestamp'
```

## 📚 Additional Resources

- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
