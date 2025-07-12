#!/bin/bash

# LinkOps Demo Image Build Script
# This script builds demo-prefixed Docker images to avoid conflicts with production images

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_TAG=${1:-"latest"}
PUSH_IMAGES=${2:-"false"}
REGISTRY=${3:-"docker.io/linksrobot"}  # Docker Hub registry with your username

echo -e "${BLUE}🐳 LinkOps Demo Image Builder${NC}"
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is running${NC}"

# Build images
echo -e "${YELLOW}🔨 Building demo images with tag: ${IMAGE_TAG}${NC}"

# Whis Data Input
echo -e "${BLUE}📦 Building demo-whis-data-input...${NC}"
docker build -t demo-whis-data-input:${IMAGE_TAG} ./mlops/whis_data_input/
echo -e "${GREEN}✅ Built demo-whis-data-input:${IMAGE_TAG}${NC}"

# Whis Sanitize
echo -e "${BLUE}📦 Building demo-whis-sanitize...${NC}"
docker build -t demo-whis-sanitize:${IMAGE_TAG} ./mlops/whis_sanitize/
echo -e "${GREEN}✅ Built demo-whis-sanitize:${IMAGE_TAG}${NC}"

# Whis Logic
echo -e "${BLUE}📦 Building demo-whis-logic...${NC}"
docker build -t demo-whis-logic:${IMAGE_TAG} ./mlops/whis_logic/
echo -e "${GREEN}✅ Built demo-whis-logic:${IMAGE_TAG}${NC}"

# Frontend
echo -e "${BLUE}📦 Building demo-frontend...${NC}"
docker build -t demo-frontend:${IMAGE_TAG} ./frontend/
echo -e "${GREEN}✅ Built demo-frontend:${IMAGE_TAG}${NC}"

# MLOps Platform (if needed)
echo -e "${BLUE}📦 Building demo-mlops-platform...${NC}"
docker build -t demo-mlops-platform:${IMAGE_TAG} ./mlops/mlops_platform/
echo -e "${GREEN}✅ Built demo-mlops-platform:${IMAGE_TAG}${NC}"

echo -e "${GREEN}🎉 All demo images built successfully!${NC}"

# List built images
echo -e "${BLUE}📋 Built Images:${NC}"
docker images | grep demo-

# Push images if requested
if [ "$PUSH_IMAGES" = "true" ]; then
    if [ -z "$REGISTRY" ]; then
        echo -e "${RED}❌ Registry prefix required for pushing. Usage: $0 <tag> true <registry>${NC}"
        echo -e "${YELLOW}Example: $0 latest true docker.io/linksrobot${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}🚀 Pushing images to registry: ${REGISTRY}${NC}"
    
    # Tag and push each image
    for image in demo-whis-data-input demo-whis-sanitize demo-whis-logic demo-frontend demo-mlops-platform; do
        echo -e "${BLUE}📤 Pushing ${image}...${NC}"
        docker tag ${image}:${IMAGE_TAG} ${REGISTRY}/${image}:${IMAGE_TAG}
        docker push ${REGISTRY}/${image}:${IMAGE_TAG}
        echo -e "${GREEN}✅ Pushed ${REGISTRY}/${image}:${IMAGE_TAG}${NC}"
    done
    
    echo -e "${GREEN}🎉 All images pushed successfully!${NC}"
    
    # Update Helm values with registry
    echo -e "${YELLOW}📝 Updating Helm values with registry...${NC}"
    sed -i "s|repository: demo-|repository: ${REGISTRY}/demo-|g" helm/demo-stack/values.yaml
    echo -e "${GREEN}✅ Helm values updated${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Demo image build complete!${NC}"
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Update Helm values if using a registry"
echo "2. Deploy with: ./deploy-helm.sh"
echo "3. Or run locally with: docker-compose up -d"
echo ""
echo -e "${YELLOW}🔧 Usage:${NC}"
echo "  Build only: $0 <tag>"
echo "  Build and push: $0 <tag> true <registry>"
echo "  Example: $0 v0.1.0 true docker.io/linksrobot" 