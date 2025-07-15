#!/bin/bash

# DEMO-LinkOps Demo Status Check Script
# This script checks the current configuration and service status

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_subheader() {
    echo -e "${CYAN}--- $1 ---${NC}"
}

print_header "DEMO-LinkOps Status Check"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    print_status "Creating from template..."
    cp env.template .env
    echo ""
fi

print_subheader "Environment Configuration"
echo ""

# Check demo mode setting
if grep -q "^DEMO_MODE=true" .env; then
    print_warning "Demo Mode: ENABLED"
    echo "  • AI capabilities are simulated"
    echo "  • No API costs"
    echo "  • Safe for demos"
elif grep -q "^DEMO_MODE=false" .env; then
    print_status "Demo Mode: DISABLED"
    echo "  • Real AI capabilities enabled"
    echo "  • API keys required"
else
    print_warning "Demo Mode: NOT SET (defaults to enabled)"
fi

echo ""

# Check API keys
print_subheader "API Key Configuration"
echo ""

# Check Grok API key
if grep -q "^GROK_API_KEY=" .env && ! grep -q "^GROK_API_KEY=$" .env; then
    grok_key=$(grep "^GROK_API_KEY=" .env | cut -d'=' -f2)
    if [ "$grok_key" = "demo_mode" ]; then
        print_warning "Grok API Key: Demo Mode"
    else
        print_status "Grok API Key: Configured"
    fi
else
    print_warning "Grok API Key: Not configured"
fi

# Check OpenAI API key
if grep -q "^OPENAI_API_KEY=" .env && ! grep -q "^OPENAI_API_KEY=$" .env; then
    print_status "OpenAI API Key: Configured"
else
    print_warning "OpenAI API Key: Not configured"
fi

# Check Anthropic API key
if grep -q "^ANTHROPIC_API_KEY=" .env && ! grep -q "^ANTHROPIC_API_KEY=$" .env; then
    print_status "Anthropic API Key: Configured"
else
    print_warning "Anthropic API Key: Not configured"
fi

echo ""

# Check if services are running
print_subheader "Service Status"
echo ""

# Check if docker-compose is running
if docker-compose ps | grep -q "Up"; then
    print_status "Docker Compose: Running"
    
    # Check individual services
    services=("whis-data-input" "whis-sanitize" "whis-logic" "mlops-platform" "frontend")
    
    for service in "${services[@]}"; do
        if docker-compose ps | grep -q "$service.*Up"; then
            print_status "$service: Running"
        else
            print_error "$service: Not running"
        fi
    done
else
    print_warning "Docker Compose: Not running"
    print_status "To start services: docker-compose up -d"
fi

echo ""

# Check API endpoints if services are running
if docker-compose ps | grep -q "Up"; then
    print_subheader "API Health Check"
    echo ""
    
    # Check main platform
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "MLOps Platform (8000): Healthy"
        
        # Check demo mode status from API
        demo_status=$(curl -s http://localhost:8000/health | grep -o '"demo_mode":[^,]*' | cut -d':' -f2 | tr -d '"' || echo "unknown")
        if [ "$demo_status" = "true" ]; then
            print_warning "  API reports: Demo Mode Active"
        elif [ "$demo_status" = "false" ]; then
            print_status "  API reports: Real AI Mode Active"
        fi
    else
        print_error "MLOps Platform (8000): Unreachable"
    fi
    
    # Check Whis Logic
    if curl -s http://localhost:8003/health > /dev/null 2>&1; then
        print_status "Whis Logic (8003): Healthy"
    else
        print_error "Whis Logic (8003): Unreachable"
    fi
    
    # Check Frontend
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_status "Frontend (3000): Accessible"
    else
        print_error "Frontend (3000): Unreachable"
    fi
fi

echo ""

print_subheader "Recommendations"
echo ""

# Provide recommendations based on current state
if grep -q "^DEMO_MODE=true" .env; then
    print_status "Current state: Demo Mode (Recommended for demos)"
    echo "  • Perfect for presentations and demos"
    echo "  • No API costs or key management required"
    echo "  • Full UI experience with simulated AI responses"
    echo ""
    echo "To enable real AI: ./configure-ai-mode.sh"
else
    print_status "Current state: Real AI Mode"
    echo "  • Real AI capabilities enabled"
    echo "  • API costs may apply"
    echo "  • Requires valid API keys"
    echo ""
    echo "To switch to demo mode: ./configure-ai-mode.sh"
fi

print_header "Status Check Complete" 