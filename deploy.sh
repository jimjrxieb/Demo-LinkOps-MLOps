#!/bin/bash

# LinkOps Demo Deployment Script
# =============================
# This script deploys the complete LinkOps demo stack for OCI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEMO_NAME="linkops-demo"
FRONTEND_PORT=8080
API_PORT=9000
DOCKER_COMPOSE_FILE="docker/docker-compose.yml"

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "=========================================="
    echo "  LinkOps Secure AI Demo Deployment"
    echo "=========================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${YELLOW}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    print_step "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if ports are available
    if lsof -Pi :$FRONTEND_PORT -sTCP:LISTEN -t >/dev/null ; then
        print_error "Port $FRONTEND_PORT is already in use. Please free up the port."
        exit 1
    fi
    
    if lsof -Pi :$API_PORT -sTCP:LISTEN -t >/dev/null ; then
        print_error "Port $API_PORT is already in use. Please free up the port."
        exit 1
    fi
    
    print_success "System requirements met"
}

build_images() {
    print_step "Building Docker images..."
    
    # Build frontend
    print_step "Building frontend image..."
    docker build -t linkops-frontend:latest frontend/
    
    # Build unified API
    print_step "Building unified API image..."
    docker build -t linkops-unified-api:latest unified-api/
    
    print_success "All images built successfully"
}

start_services() {
    print_step "Starting services..."
    
    # Start with docker-compose
    docker-compose -f $DOCKER_COMPOSE_FILE up -d
    
    print_success "Services started successfully"
}

wait_for_services() {
    print_step "Waiting for services to be ready..."
    
    # Wait for API
    print_step "Waiting for API service..."
    timeout=60
    counter=0
    while ! curl -f http://localhost:$API_PORT/health >/dev/null 2>&1; do
        if [ $counter -ge $timeout ]; then
            print_error "API service failed to start within $timeout seconds"
            exit 1
        fi
        echo -n "."
        sleep 2
        counter=$((counter + 2))
    done
    echo ""
    print_success "API service is ready"
    
    # Wait for frontend
    print_step "Waiting for frontend service..."
    timeout=30
    counter=0
    while ! curl -f http://localhost:$FRONTEND_PORT >/dev/null 2>&1; do
        if [ $counter -ge $timeout ]; then
            print_error "Frontend service failed to start within $timeout seconds"
            exit 1
        fi
        echo -n "."
        sleep 2
        counter=$((counter + 2))
    done
    echo ""
    print_success "Frontend service is ready"
}

run_tests() {
    print_step "Running system tests..."
    
    # Test API health
    if curl -f http://localhost:$API_PORT/health >/dev/null 2>&1; then
        print_success "API health check passed"
    else
        print_error "API health check failed"
        exit 1
    fi
    
    # Test frontend
    if curl -f http://localhost:$FRONTEND_PORT >/dev/null 2>&1; then
        print_success "Frontend accessibility test passed"
    else
        print_error "Frontend accessibility test failed"
        exit 1
    fi
    
    print_success "All system tests passed"
}

show_status() {
    print_step "Checking service status..."
    
    echo ""
    echo -e "${BLUE}Service Status:${NC}"
    echo "=================="
    
    # Check containers
    docker-compose -f $DOCKER_COMPOSE_FILE ps
    
    echo ""
    echo -e "${BLUE}Service URLs:${NC}"
    echo "==============="
    echo "Frontend: http://localhost:$FRONTEND_PORT"
    echo "API: http://localhost:$API_PORT"
    echo "API Docs: http://localhost:$API_PORT/docs"
    echo "Health Check: http://localhost:$API_PORT/health"
    
    echo ""
    echo -e "${BLUE}Sample Data:${NC}"
    echo "============="
    echo "ML Training: sample_data/employee_data.csv"
    echo "RAG Testing: sample_data/company_documents.txt"
    
    echo ""
    echo -e "${GREEN}Demo is ready!${NC}"
    echo "Open http://localhost:$FRONTEND_PORT in your browser to start using the demo."
}

stop_services() {
    print_step "Stopping services..."
    docker-compose -f $DOCKER_COMPOSE_FILE down
    print_success "Services stopped"
}

cleanup() {
    print_step "Cleaning up..."
    docker-compose -f $DOCKER_COMPOSE_FILE down -v
    docker system prune -f
    print_success "Cleanup completed"
}

show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy    - Deploy the complete demo stack (default)"
    echo "  start     - Start services only"
    echo "  stop      - Stop services"
    echo "  restart   - Restart services"
    echo "  status    - Show service status"
    echo "  test      - Run system tests"
    echo "  cleanup   - Stop services and clean up volumes"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Full deployment"
    echo "  $0 status    # Check service status"
    echo "  $0 cleanup   # Clean up everything"
}

# Main script logic
main() {
    case "${1:-deploy}" in
        "deploy")
            print_header
            check_requirements
            build_images
            start_services
            wait_for_services
            run_tests
            show_status
            ;;
        "start")
            print_header
            start_services
            wait_for_services
            show_status
            ;;
        "stop")
            print_header
            stop_services
            ;;
        "restart")
            print_header
            stop_services
            start_services
            wait_for_services
            show_status
            ;;
        "status")
            print_header
            show_status
            ;;
        "test")
            print_header
            run_tests
            ;;
        "cleanup")
            print_header
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 