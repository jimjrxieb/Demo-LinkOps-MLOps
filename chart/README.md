# DEMO-LinkOps Helm Chart

This Helm chart deploys the complete DEMO-LinkOps stack in a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Ingress controller (e.g., nginx-ingress)

## Installation

1. Add your Docker registry credentials:
```bash
kubectl create secret docker-registry regcred \
  --docker-server=docker.io \
  --docker-username=your-username \
  --docker-password=your-password
```

2. Install the chart:
```bash
# From the chart directory
helm install demo-release .

# Or from the project root
helm install demo-release chart/
```

## Configuration

### Image Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.frontend.repository` | Frontend image repository | `demo-linkops-frontend` |
| `image.frontend.tag` | Frontend image tag | `latest` |
| `image.unifiedApi.repository` | API image repository | `demo-linkops-unified-api` |
| `image.unifiedApi.tag` | API image tag | `latest` |
| `image.rag.repository` | RAG service image repository | `demo-linkops-rag` |
| `image.rag.tag` | RAG service image tag | `latest` |

### Service Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Service type | `ClusterIP` |
| `service.frontend.port` | Frontend service port | `80` |
| `service.unifiedApi.port` | API service port | `8000` |
| `service.rag.port` | RAG service port | `8001` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.hosts[0].host` | Hostname | `demo.local` |

## Usage

1. Access the application:
```bash
# Add to /etc/hosts
127.0.0.1 demo.local

# Access in browser
http://demo.local
```

2. Default credentials:
- Slim demo: `demo-slim` / `demo`
- Full demo: `demo-full` / `arise!`

## Monitoring

The chart includes built-in monitoring for:
- Session metrics
- Service health
- API performance

Access the monitoring dashboard at:
```
http://demo.local/monitoring
```

## Troubleshooting

1. Check pod status:
```bash
kubectl get pods -l app=demo-linkops
```

2. View logs:
```bash
# Frontend logs
kubectl logs -l component=frontend

# API logs
kubectl logs -l component=unified-api
```

3. Common issues:
- Image pull errors: Check registry credentials
- Ingress not working: Verify ingress controller installation
- Service unreachable: Check service and pod labels

## Uninstallation

```bash
helm uninstall demo-release
```

## Development

1. Make changes to values:
```bash
# Create a values override file
cp values.yaml custom-values.yaml
edit custom-values.yaml

# Install with custom values
helm install -f custom-values.yaml demo-release .
```

2. Test the chart:
```bash
# Lint the chart
helm lint .

# Test the installation
helm install --dry-run --debug demo-release .
```

3. Package the chart:
```bash
helm package .
``` 