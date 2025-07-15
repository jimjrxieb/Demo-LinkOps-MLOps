#!/bin/bash

# LinkOps Demo Deployment Script
# This script deploys the demo services with version tracking

set -e

echo "🚀 LinkOps Demo Deployment Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "docker-compose.yml" ]]; then
    print_error "docker-compose.yml not found. Please run this script from the DEMO-LinkOps directory."
    exit 1
fi

# Check if VERSION file exists
if [[ -f "VERSION" ]]; then
    print_status "Found VERSION file, loading current version..."
    source VERSION
    print_success "Current version: $IMAGE_TAG"
else
    print_warning "No VERSION file found, using 'latest' tags"
    IMAGE_TAG="latest"
fi

# Function to check if Docker images exist
check_image_exists() {
    local image_name=$1
    if docker image inspect "$image_name" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to pull specific image
pull_image() {
    local image_name=$1
    print_status "Pulling $image_name..."
    if docker pull "$image_name"; then
        print_success "Successfully pulled $image_name"
    else
        print_error "Failed to pull $image_name"
        return 1
    fi
}

# Pull all demo images
print_status "Pulling demo images..."
images=(
    "linksrobot/demo-frontend:$IMAGE_TAG"
    "linksrobot/demo-mlops-platform:$IMAGE_TAG"
    "linksrobot/demo-whis-data-input:$IMAGE_TAG"
    "linksrobot/demo-whis-sanitize:$IMAGE_TAG"
    "linksrobot/demo-whis-logic:$IMAGE_TAG"
    "linksrobot/demo-ficknury-evaluator:$IMAGE_TAG"
)

for image in "${images[@]}"; do
    if ! pull_image "$image"; then
        print_error "Failed to pull $image. Deployment aborted."
        exit 1
    fi
done

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down --remove-orphans

# Start services
print_status "Starting demo services..."
if docker-compose up -d; then
    print_success "Demo services started successfully!"
else
    print_error "Failed to start demo services"
    exit 1
fi

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Check service health
print_status "Checking service health..."
if docker-compose ps | grep -q "Up"; then
    print_success "All services are running!"
    
    echo ""
    echo "🎉 LinkOps Demo Deployment Complete!"
    echo "=================================="
    echo "Version: $IMAGE_TAG"
    echo "Frontend: http://localhost:3000 (or your VM's public IP)"
    echo "API Docs: http://localhost:8000/docs"
    echo ""
    echo "Services Status:"
    docker-compose ps
    
    echo ""
    echo "📊 Quick Health Check:"
    echo "Frontend: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "unreachable")"
    echo "MLOps Platform: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "unreachable")"
    
else
    print_error "Some services failed to start"
    docker-compose logs --tail=20
    exit 1
fi

echo ""
print_success "Deployment completed successfully!"
echo "Run 'docker-compose logs -f' to monitor logs"
echo "Run 'docker-compose down' to stop services" 