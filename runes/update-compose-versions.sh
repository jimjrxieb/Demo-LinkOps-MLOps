#!/bin/bash

# LinkOps Demo - Update Docker Compose Versions
# Manually update docker-compose.yml with specific version tags

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCKER_USER="linksrobot"
COMPOSE_FILE="docker-compose.yml"

echo -e "${BLUE}🔧 LinkOps Demo - Update Docker Compose Versions${NC}"
echo "=================================================="

# Check if version argument is provided
if [[ $# -eq 0 ]]; then
    echo -e "${YELLOW}Usage: $0 <version_tag>${NC}"
    echo -e "${YELLOW}Example: $0 20250714-a1b2c3d${NC}"
    echo ""
    echo -e "${BLUE}Available versions:${NC}"
    echo "Check your GitHub Actions workflow or Docker Hub for available tags:"
    echo "  docker images | grep linksrobot/demo-"
    exit 1
fi

VERSION_TAG=$1

echo -e "${YELLOW}📝 Updating docker-compose.yml to version: ${VERSION_TAG}${NC}"

# Create backup
BACKUP_FILE="${COMPOSE_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$COMPOSE_FILE" "$BACKUP_FILE"
echo -e "${GREEN}✅ Backup created: ${BACKUP_FILE}${NC}"

# Update all demo service images to use the specified version
echo -e "${BLUE}🔄 Updating service images...${NC}"

# Services to update
SERVICES=(
    "demo-frontend"
    "demo-mlops-platform"
    "demo-whis-data-input"
    "demo-whis-sanitize"
    "demo-whis-logic"
    "demo-ficknury-evaluator"
)

# Update each service
for service in "${SERVICES[@]}"; do
    echo -e "${YELLOW}  Updating ${service}...${NC}"
    
    # Use sed to replace the image tag
    sed -i "s|${DOCKER_USER}/${service}:.*|${DOCKER_USER}/${service}:${VERSION_TAG}|g" "$COMPOSE_FILE"
    
    echo -e "${GREEN}    ✅ Updated to ${DOCKER_USER}/${service}:${VERSION_TAG}${NC}"
done

echo -e "${GREEN}✅ All services updated successfully!${NC}"

# Show the changes
echo -e "${BLUE}📋 Updated docker-compose.yml:${NC}"
echo "=================================="
grep -E "image: ${DOCKER_USER}/demo-" "$COMPOSE_FILE" | while read line; do
    echo -e "${GREEN}$line${NC}"
done

echo ""
echo -e "${YELLOW}🚀 To deploy with the new versions:${NC}"
echo "  docker-compose pull"
echo "  docker-compose up -d"
echo ""
echo -e "${YELLOW}🔄 To revert changes:${NC}"
echo "  cp ${BACKUP_FILE} ${COMPOSE_FILE}" 