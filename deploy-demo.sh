#!/bin/bash

# LinkOps Demo Deployment Script
# This script pulls and deploys the latest versioned Docker images

set -e

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "docker-compose is not installed. Please install it and try again."
        exit 1
    fi
    print_success "docker-compose is available"
}

# Function to get the latest version from GitHub
get_latest_version() {
    print_status "Fetching latest version from GitHub..."
    
    # Try to get the latest version from the VERSION file in the repo
    if command -v curl &> /dev/null; then
        VERSION_URL="https://raw.githubusercontent.com/your-username/DEMO-LinkOps/main/VERSION"
        VERSION=$(curl -s "$VERSION_URL" | grep "IMAGE_TAG=" | cut -d'=' -f2) 2>/dev/null || true
        
        if [[ -n "$VERSION" ]]; then
            print_success "Found version: $VERSION"
            echo "$VERSION"
            return
        fi
    fi
    
    # Fallback: use latest tag
    print_warning "Could not fetch version from GitHub, using 'latest' tag"
    echo "latest"
}

# Function to update docker-compose.yml with specific version
update_compose_version() {
    local VERSION=$1
    
    if [[ "$VERSION" == "latest" ]]; then
        print_status "Using 'latest' tags for all services"
        return
    fi
    
    print_status "Updating docker-compose.yml to use version: $VERSION"
    
    # Create a backup of the original docker-compose.yml
    cp docker-compose.yml docker-compose.yml.backup
    
    # Update the image tags in docker-compose.yml
    sed -i "s|linksrobot/demo-frontend:latest|linksrobot/demo-frontend:$VERSION|g" docker-compose.yml
    sed -i "s|linksrobot/demo-mlops-platform:latest|linksrobot/demo-mlops-platform:$VERSION|g" docker-compose.yml
    sed -i "s|linksrobot/demo-whis-data-input:latest|linksrobot/demo-whis-data-input:$VERSION|g" docker-compose.yml
    sed -i "s|linksrobot/demo-whis-sanitize:latest|linksrobot/demo-whis-sanitize:$VERSION|g" docker-compose.yml
    sed -i "s|linksrobot/demo-whis-logic:latest|linksrobot/demo-whis-logic:$VERSION|g" docker-compose.yml
    sed -i "s|linksrobot/demo-ficknury-evaluator:latest|linksrobot/demo-ficknury-evaluator:$VERSION|g" docker-compose.yml
    
    print_success "Updated docker-compose.yml with version $VERSION"
}

# Function to restore original docker-compose.yml
restore_compose() {
    if [[ -f "docker-compose.yml.backup" ]]; then
        print_status "Restoring original docker-compose.yml"
        mv docker-compose.yml.backup docker-compose.yml
    fi
}

# Function to pull images
pull_images() {
    local VERSION=$1
    
    print_status "Pulling Docker images..."
    
    if [[ "$VERSION" == "latest" ]]; then
        docker-compose pull
    else
        # Pull specific versioned images
        docker pull "linksrobot/demo-frontend:$VERSION"
        docker pull "linksrobot/demo-mlops-platform:$VERSION"
        docker pull "linksrobot/demo-whis-data-input:$VERSION"
        docker pull "linksrobot/demo-whis-sanitize:$VERSION"
        docker pull "linksrobot/demo-whis-logic:$VERSION"
        docker pull "linksrobot/demo-ficknury-evaluator:$VERSION"
    fi
    
    print_success "Images pulled successfully"
}

# Function to deploy services
deploy_services() {
    print_status "Deploying LinkOps Demo services..."
    
    # Stop existing services
    print_status "Stopping existing services..."
    docker-compose down --remove-orphans
    
    # Start services
    print_status "Starting services..."
    docker-compose up -d
    
    print_success "Services deployed successfully"
}

# Function to check service health
check_health() {
    print_status "Checking service health..."
    
    # Wait a bit for services to start
    sleep 10
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "All services are running"
        
        # Show service status
        echo ""
        print_status "Service Status:"
        docker-compose ps
        
        echo ""
        print_status "Service URLs:"
        echo "  Frontend: http://localhost:3000"
        echo "  MLOps Platform: http://localhost:8000"
        echo "  Whis Data Input: http://localhost:8001"
        echo "  Whis Sanitize: http://localhost:8002"
        echo "  Whis Logic: http://localhost:8003"
        echo "  Ficknury Evaluator: http://localhost:8004"
        
    else
        print_error "Some services failed to start"
        docker-compose ps
        exit 1
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing recent logs..."
    docker-compose logs --tail=20
}

# Main deployment function
main() {
    echo "🚀 LinkOps Demo Deployment Script"
    echo "=================================="
    echo ""
    
    # Check prerequisites
    check_docker
    check_docker_compose
    
    # Get the version to deploy
    VERSION=$(get_latest_version)
    
    # Update docker-compose.yml if needed
    update_compose_version "$VERSION"
    
    # Pull images
    pull_images "$VERSION"
    
    # Deploy services
    deploy_services
    
    # Check health
    check_health
    
    # Show logs
    show_logs
    
    echo ""
    print_success "🎉 LinkOps Demo deployment completed successfully!"
    print_success "Access the demo at: http://localhost:3000"
    
    # Cleanup
    restore_compose
}

# Handle script arguments
case "${1:-}" in
    "version")
        get_latest_version
        ;;
    "pull")
        VERSION=$(get_latest_version)
        pull_images "$VERSION"
        ;;
    "deploy")
        VERSION=$(get_latest_version)
        update_compose_version "$VERSION"
        deploy_services
        restore_compose
        ;;
    "health")
        check_health
        ;;
    "logs")
        show_logs
        ;;
    "help"|"-h"|"--help")
        echo "LinkOps Demo Deployment Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)  Full deployment (default)"
        echo "  version    Show latest version"
        echo "  pull       Pull latest images only"
        echo "  deploy     Deploy services only"
        echo "  health     Check service health"
        echo "  logs       Show service logs"
        echo "  help       Show this help"
        echo ""
        echo "Examples:"
        echo "  $0                    # Full deployment"
        echo "  $0 pull               # Pull images only"
        echo "  $0 deploy             # Deploy services only"
        echo "  $0 health             # Check if services are running"
        ;;
    *)
        main
        ;;
esac 