#!/bin/bash

# Docker Hub Login Script for LinkOps Demo
# Uses DOCKER_CRED environment variable for authentication

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Docker Hub Login for LinkOps Demo${NC}"
echo "=========================================="

# Check if DOCKER_CRED is set
if [ -z "$DOCKER_CRED" ]; then
    echo -e "${RED}❌ DOCKER_CRED environment variable is not set${NC}"
    echo -e "${YELLOW}Please set your Docker Hub password:${NC}"
    echo "export DOCKER_CRED='your-docker-hub-password'"
    exit 1
fi

# Check if DOCKER_USER is set
if [ -z "$DOCKER_USER" ]; then
    echo -e "${YELLOW}⚠️  DOCKER_USER not set, using default: linksrobot${NC}"
    export DOCKER_USER=linksrobot
fi

echo -e "${GREEN}✅ Logging in to Docker Hub as: $DOCKER_USER${NC}"

# Login to Docker Hub
echo "$DOCKER_CRED" | docker login -u "$DOCKER_USER" --password-stdin

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Successfully logged in to Docker Hub${NC}"
    echo -e "${BLUE}📝 You can now push demo images:${NC}"
    echo "  ./build-demo-images.sh latest true docker.io/linksrobot"
else
    echo -e "${RED}❌ Failed to login to Docker Hub${NC}"
    exit 1
fi 