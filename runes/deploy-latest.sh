#!/bin/bash

# LinkOps Demo Deployment Script
# Automatically deploys the latest versioned images from GitHub Actions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOCKER_USER="linksrobot"
SERVICES=(
    "demo-frontend"
    "demo-mlops-platform"
    "demo-whis-data-input"
    "demo-whis-sanitize"
    "demo-whis-logic"
    "demo-ficknury-evaluator"
)

echo -e "${BLUE}🚀 LinkOps Demo Deployment${NC}"
echo "=================================="

# Function to get the latest version tag
get_latest_version() {
    local service=$1
    echo -e "${YELLOW}🔍 Finding latest version for ${service}...${NC}"
    
    # Get the latest tag from Docker Hub
    local latest_tag=$(docker images --format "table {{.Repository}}:{{.Tag}}" | grep "${DOCKER_USER}/${service}" | head -1 | cut -d: -f2)
    
    if [[ -z "$latest_tag" ]]; then
        echo -e "${RED}❌ No local image found for ${service}${NC}"
        echo -e "${YELLOW}📥 Pulling latest image...${NC}"
        docker pull "${DOCKER_USER}/${service}:latest" || {
            echo -e "${RED}❌ Failed to pull ${service}:latest${NC}"
            return 1
        }
        latest_tag="latest"
    fi
    
    echo -e "${GREEN}✅ Found version: ${latest_tag}${NC}"
    echo "$latest_tag"
}

# Function to update docker-compose.yml with specific versions
update_compose_versions() {
    local compose_file="docker-compose.yml"
    local temp_file="docker-compose.yml.tmp"
    
    echo -e "${YELLOW}📝 Updating docker-compose.yml with versioned images...${NC}"
    
    # Create a backup
    cp "$compose_file" "${compose_file}.backup.$(date +%Y%m%d_%H%M%S)"
    
    # Read current compose file
    local content=$(cat "$compose_file")
    
    # Update each service with its latest version
    for service in "${SERVICES[@]}"; do
        local version=$(get_latest_version "$service")
        if [[ $? -eq 0 ]]; then
            # Update the image tag in docker-compose.yml
            content=$(echo "$content" | sed "s|${DOCKER_USER}/${service}:.*|${DOCKER_USER}/${service}:${version}|g")
            echo -e "${GREEN}✅ Updated ${service} to version ${version}${NC}"
        else
            echo -e "${RED}❌ Failed to get version for ${service}${NC}"
            return 1
        fi
    done
    
    # Write updated content
    echo "$content" > "$temp_file"
    mv "$temp_file" "$compose_file"
    
    echo -e "${GREEN}✅ docker-compose.yml updated successfully${NC}"
}

# Function to deploy services
deploy_services() {
    echo -e "${YELLOW}🚀 Deploying LinkOps Demo services...${NC}"
    
    # Pull latest images
    echo -e "${BLUE}📥 Pulling latest images...${NC}"
    docker-compose pull || {
        echo -e "${RED}❌ Failed to pull images${NC}"
        return 1
    }
    
    # Stop existing services
    echo -e "${BLUE}🛑 Stopping existing services...${NC}"
    docker-compose down || true
    
    # Start services
    echo -e "${BLUE}▶️ Starting services...${NC}"
    docker-compose up -d || {
        echo -e "${RED}❌ Failed to start services${NC}"
        return 1
    }
    
    # Wait for services to be ready
    echo -e "${BLUE}⏳ Waiting for services to be ready...${NC}"
    sleep 10
    
    # Check service status
    echo -e "${BLUE}📊 Checking service status...${NC}"
    docker-compose ps
    
    echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
}

# Function to show deployment info
show_deployment_info() {
    echo -e "${BLUE}📋 Deployment Information${NC}"
    echo "=================================="
    echo -e "${GREEN}🌐 Frontend:${NC} http://localhost:3000"
    echo -e "${GREEN}🔧 API:${NC} http://localhost:8000"
    echo -e "${GREEN}📊 Database:${NC} localhost:5432"
    echo -e "${GREEN}🔴 Redis:${NC} localhost:6379"
    echo ""
    echo -e "${YELLOW}📝 Logs:${NC} docker-compose logs -f"
    echo -e "${YELLOW}🛑 Stop:${NC} docker-compose down"
    echo -e "${YELLOW}🔄 Restart:${NC} docker-compose restart"
}

# Main execution
main() {
    # Check if docker-compose.yml exists
    if [[ ! -f "docker-compose.yml" ]]; then
        echo -e "${RED}❌ docker-compose.yml not found in current directory${NC}"
        echo -e "${YELLOW}💡 Make sure you're in the DEMO-LinkOps directory${NC}"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running${NC}"
        exit 1
    fi
    
    # Update compose file with latest versions
    update_compose_versions || {
        echo -e "${RED}❌ Failed to update docker-compose.yml${NC}"
        exit 1
    }
    
    # Deploy services
    deploy_services || {
        echo -e "${RED}❌ Deployment failed${NC}"
        exit 1
    }
    
    # Show deployment info
    show_deployment_info
    
    echo -e "${GREEN}🎉 LinkOps Demo is now running!${NC}"
}

# Run main function
main "$@" 