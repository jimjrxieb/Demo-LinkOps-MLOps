#!/bin/bash

# LinkOps Demo - Build and Push All Images with Docker Compose
# This script builds and pushes all demo images using docker-compose.build.yml

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.build.yml"
DOCKER_REGISTRY="linksrobot"

echo -e "${BLUE}🐳 LinkOps Demo - Build and Push All Images${NC}"
echo "=================================================="
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed or not in PATH${NC}"
    exit 1
fi

# Use docker compose (newer) if available, otherwise docker-compose
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Check if we're logged in to Docker Hub
echo -e "${YELLOW}🔐 Checking Docker login status...${NC}"
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Not logged in to Docker. Please run: docker login${NC}"
    exit 1
fi

# Check if the compose file exists
if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo -e "${RED}❌ Docker Compose file not found: $COMPOSE_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are ready${NC}"
echo ""

# Function to check if Dockerfile exists for a service
check_dockerfile() {
    local service=$1
    local context=$(grep -A 5 "build:" "$COMPOSE_FILE" | grep -A 1 "$service:" | grep "context:" | awk '{print $2}' | tr -d '"')
    
    if [[ -f "$context/Dockerfile" ]]; then
        return 0
    else
        return 1
    fi
}

# Function to get available services
get_available_services() {
    local services=()
    while IFS= read -r line; do
        if [[ $line =~ ^[[:space:]]*([a-zA-Z0-9_-]+): ]]; then
            service_name="${BASH_REMATCH[1]}"
            if check_dockerfile "$service_name"; then
                services+=("$service_name")
            fi
        fi
    done < "$COMPOSE_FILE"
    echo "${services[@]}"
}

# Get list of available services
echo -e "${YELLOW}📋 Scanning for available services...${NC}"
available_services=($(get_available_services))

if [[ ${#available_services[@]} -eq 0 ]]; then
    echo -e "${RED}❌ No services with Dockerfiles found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found ${#available_services[@]} services with Dockerfiles:${NC}"
for service in "${available_services[@]}"; do
    echo "  - $service"
done
echo ""

# Build all images
echo -e "${BLUE}🔨 Building all images...${NC}"
echo "This may take several minutes depending on your system and network."
echo ""

if $COMPOSE_CMD -f "$COMPOSE_FILE" build --parallel --progress=plain; then
    echo -e "${GREEN}✅ All images built successfully!${NC}"
else
    echo -e "${RED}❌ Some images failed to build${NC}"
    exit 1
fi

echo ""

# Push all images
echo -e "${BLUE}📤 Pushing all images to Docker Hub...${NC}"
echo "This may take several minutes depending on your upload speed."
echo ""

if $COMPOSE_CMD -f "$COMPOSE_FILE" push; then
    echo -e "${GREEN}✅ All images pushed successfully!${NC}"
else
    echo -e "${RED}❌ Some images failed to push${NC}"
    exit 1
fi

echo ""

# Summary
echo -e "${GREEN}🎉 Build and Push Complete!${NC}"
echo "=================================="
echo ""
echo -e "${BLUE}📋 Available images on Docker Hub:${NC}"
for service in "${available_services[@]}"; do
    echo "  - $DOCKER_REGISTRY/demo-$service:latest"
done
echo ""
echo -e "${YELLOW}💡 Next steps:${NC}"
echo "  1. Update your Helm values.yaml files to use these images"
echo "  2. Deploy with: helm install demo-stack ./helm/demo-stack"
echo "  3. Or use ArgoCD to sync from Git"
echo ""
echo -e "${GREEN}✅ All done! Your LinkOps demo images are ready for deployment.${NC}" 