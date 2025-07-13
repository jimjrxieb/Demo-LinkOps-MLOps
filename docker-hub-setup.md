# Docker Hub Setup for LinkOps Demo

This document explains how to use Docker Hub with your LinkOps Demo images.

## 🔧 Configuration

### Environment Variables

Set these environment variables for Docker Hub authentication:

```bash
export DOCKER_USER=linksrobot
export DOCKER_CRED='your-docker-hub-password'
```

### Image Naming Convention

All demo images use the `demo-` prefix to avoid conflicts with production images:

- `docker.io/linksrobot/demo-whis-data-input`
- `docker.io/linksrobot/demo-whis-sanitize`
- `docker.io/linksrobot/demo-whis-logic`
- `docker.io/linksrobot/demo-frontend`
- `docker.io/linksrobot/demo-mlops-platform`

## 🚀 Usage

### 1. Setup Authentication

```bash
# Set environment variables
export DOCKER_CRED='your-docker-hub-password'
export GH_PAT='your-github-pat'

# Setup Docker Hub and GitHub authentication
./docker-login.sh
./github-setup.sh
```

### 2. Build and Push Images

```bash
# Build only (local)
./build-demo-images.sh latest

# Build and push to Docker Hub
./build-demo-images.sh v0.1.0 true docker.io/linksrobot
```

### 3. Deploy with Helm

```bash
# Deploy using Docker Hub images
./deploy-helm.sh
```

## 🔄 GitHub Actions

The GitHub Actions workflow automatically:

1. Uses `DOCKER_CRED` secret for authentication
2. Builds and pushes to `docker.io/linksrobot/`
3. Updates Helm values with registry URLs
4. Commits changes back to the repository

### Required Secrets

In your GitHub repository settings, add:

- `DOCKER_CRED`: Your Docker Hub password/token
- `GH_PAT`: Your GitHub Personal Access Token (for repository access)

**GH_PAT Permissions Required:**

- `repo` (Full control of private repositories)
- `workflow` (Update GitHub Action workflows)

## 📋 Image Registry URLs

After pushing, your images will be available at:

```
https://hub.docker.com/r/linksrobot/demo-whis-data-input
https://hub.docker.com/r/linksrobot/demo-whis-sanitize
https://hub.docker.com/r/linksrobot/demo-whis-logic
https://hub.docker.com/r/linksrobot/demo-frontend
https://hub.docker.com/r/linksrobot/demo-mlops-platform
```

## 🔍 Verification

### Check Local Images

```bash
docker images | grep demo-
```

### Check Docker Hub Images

```bash
docker pull docker.io/linksrobot/demo-whis-data-input:latest
```

### Test Helm Deployment

```bash
cd helm/demo-stack
helm template test-release . --dry-run
```

## 🛠 Troubleshooting

### Authentication Issues

```bash
# Re-login to Docker Hub
docker logout
./docker-login.sh
```

### Image Pull Issues

```bash
# Check if image exists
docker pull docker.io/linksrobot/demo-whis-data-input:latest

# Build locally if needed
./build-demo-images.sh latest
```

### Helm Issues

```bash
# Update dependencies
cd helm/demo-stack
helm dependency build
helm dependency update
```

## 📝 Notes

- All demo images are prefixed with `demo-` to avoid conflicts
- Images are pushed to your Docker Hub account (`linksrobot`)
- Helm values are automatically updated with registry URLs
- GitHub Actions handles CI/CD automatically
