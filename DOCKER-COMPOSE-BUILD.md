# 🐳 Docker Compose Build System for LinkOps Demo

This guide shows you how to build and push all LinkOps demo images using Docker Compose.

## 📁 Files Created

- `docker-compose.build.yml` - Docker Compose configuration for building all images
- `build-and-push-all.sh` - Automated script for building and pushing all images
- `DOCKER-COMPOSE-BUILD.md` - This guide

## 🚀 Quick Start

### 1. Login to Docker Hub
```bash
docker login
```

### 2. Build and Push All Images
```bash
./build-and-push-all.sh
```

## 📋 Available Services

The following services are configured for building:

| Service | Image Name | Context Path |
|---------|------------|--------------|
| Frontend | `linksrobot/demo-frontend:latest` | `./frontend` |
| Whis Data Input | `linksrobot/demo-whis-data-input:latest` | `./mlops/whis-data-input` |
| Whis Sanitize | `linksrobot/demo-whis-sanitize:latest` | `./mlops/whis-sanitize` |
| Whis Logic | `linksrobot/demo-whis-logic:latest` | `./mlops/whis-logic` |
| Ficknury Evaluator | `linksrobot/demo-ficknury-evaluator:latest` | `./shadows/ficknury-evaluator` |
| MLOps Platform | `linksrobot/demo-mlops-platform:latest` | `./mlops/mlops-platform` |

## 🔧 Manual Commands

### Build All Images
```bash
docker compose -f docker-compose.build.yml build
```

### Build Specific Service
```bash
docker compose -f docker-compose.build.yml build demo-frontend
```

### Push All Images
```bash
docker compose -f docker-compose.build.yml push
```

### Build and Push in One Command
```bash
docker compose -f docker-compose.build.yml build && docker compose -f docker-compose.build.yml push
```

## 🎯 Advanced Usage

### Build with Different Tags
```bash
# Build with version tag
docker compose -f docker-compose.build.yml build
docker tag linksrobot/demo-frontend:latest linksrobot/demo-frontend:v1.0.0
docker push linksrobot/demo-frontend:v1.0.0
```

### Build with Build Arguments
```bash
docker compose -f docker-compose.build.yml build --build-arg BUILD_ENV=production
```

### Parallel Building
```bash
docker compose -f docker-compose.build.yml build --parallel
```

## 🔍 Troubleshooting

### Check Docker Login Status
```bash
docker info
```

### Verify Images Built
```bash
docker images | grep linksrobot/demo
```

### Check Build Contexts
```bash
# Verify Dockerfiles exist
find . -name "Dockerfile" -type f
```

### Clean Up
```bash
# Remove all demo images
docker images | grep linksrobot/demo | awk '{print $3}' | xargs docker rmi

# Remove all unused images
docker image prune -a
```

## 📊 Integration with Helm

After building and pushing images, update your Helm values:

```yaml
# helm/demo-stack/values.yaml
whis-data-input:
  image:
    repository: linksrobot/demo-whis-data-input
    tag: latest

whis-sanitize:
  image:
    repository: linksrobot/demo-whis-sanitize
    tag: latest

whis-logic:
  image:
    repository: linksrobot/demo-whis-logic
    tag: latest

frontend:
  image:
    repository: linksrobot/demo-frontend
    tag: latest
```

## 🚀 Deployment

### With Helm
```bash
cd helm/demo-stack
helm install demo-stack . --namespace linkops-demo
```

### With ArgoCD
1. Commit and push your changes
2. ArgoCD will automatically sync the new images
3. Monitor the sync status in ArgoCD UI

## 💡 Tips

- **Parallel Building**: Use `--parallel` flag for faster builds
- **Caching**: Docker Compose automatically caches layers for faster rebuilds
- **Registry**: All images are pushed to `linksrobot` Docker Hub account
- **Tags**: Use semantic versioning for production releases
- **Security**: Always scan images before pushing to production

## 🔗 Related Files

- `build-and-push-demo-images.sh` - Original build script (legacy)
- `docker-compose.yml` - Runtime Docker Compose configuration
- `helm/` - Helm charts for Kubernetes deployment
- `README.md` - Main project documentation 