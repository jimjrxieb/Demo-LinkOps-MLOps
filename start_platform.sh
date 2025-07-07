#!/bin/bash

# LinkOps MLOps Platform Startup Script
# This script starts all services and provides testing instructions

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting LinkOps MLOps Platform${NC}"
echo "=================================="

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}⚠️  Port $1 is already in use${NC}"
        return 1
    else
        return 0
    fi
}

# Function to start a service
start_service() {
    local service_name=$1
    local port=$2
    local command=$3
    
    echo -e "${BLUE}Starting $service_name on port $port...${NC}"
    
    if check_port $port; then
        eval "$command" &
        local pid=$!
        echo -e "${GREEN}✅ $service_name started (PID: $pid)${NC}"
        sleep 2
    else
        echo -e "${RED}❌ Failed to start $service_name${NC}"
        return 1
    fi
}

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo -e "${BLUE}🐳 Docker detected - using Docker Compose${NC}"
    
    # Start services with Docker Compose
    if [ -f "docker-compose.yml" ]; then
        echo "Starting services with Docker Compose..."
        docker-compose up -d
        
        echo -e "${GREEN}✅ All services started with Docker Compose${NC}"
        echo ""
        echo -e "${YELLOW}📋 Service URLs:${NC}"
        echo "  MLOps Platform: http://localhost:8000"
        echo "  Audit Assess:   http://localhost:8003"
        echo "  Whis Data Input: http://localhost:8004"
        echo "  Whis Enhance:   http://localhost:8006"
        echo "  Frontend:       http://localhost:3000"
        
    else
        echo -e "${RED}❌ docker-compose.yml not found${NC}"
        exit 1
    fi
    
else
    echo -e "${BLUE}🐍 Using Python services directly${NC}"
    
    # Check Python dependencies
    echo "Checking Python dependencies..."
    python3 -c "import fastapi, uvicorn" 2>/dev/null || {
        echo -e "${RED}❌ FastAPI or uvicorn not installed${NC}"
        echo "Install with: pip install fastapi uvicorn"
        exit 1
    }
    
    # Start MLOps Platform
    start_service "MLOps Platform" 8000 "cd mlops_platform && python -m uvicorn main:app --host 0.0.0.0 --port 8000"
    
    # Start Audit Assess
    start_service "Audit Assess" 8003 "cd audit_assess && python -m uvicorn main:app --host 0.0.0.0 --port 8003"
    
    # Start Whis Data Input
    start_service "Whis Data Input" 8004 "cd whis_data_input && python -m uvicorn main:app --host 0.0.0.0 --port 8004"
    
    # Start Whis Enhance
    start_service "Whis Enhance" 8006 "cd whis_enhance && python -m uvicorn main:app --host 0.0.0.0 --port 8006"
    
    echo ""
    echo -e "${YELLOW}📋 Service URLs:${NC}"
    echo "  MLOps Platform: http://localhost:8000"
    echo "  Audit Assess:   http://localhost:8003"
    echo "  Whis Data Input: http://localhost:8004"
    echo "  Whis Enhance:   http://localhost:8006"
fi

echo ""
echo -e "${BLUE}🧪 Testing Services...${NC}"

# Wait a moment for services to start
sleep 5

# Test services
echo "Testing service health..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ MLOps Platform is healthy${NC}"
else
    echo -e "${RED}❌ MLOps Platform is not responding${NC}"
fi

if curl -s http://localhost:8003/health > /dev/null; then
    echo -e "${GREEN}✅ Audit Assess is healthy${NC}"
else
    echo -e "${RED}❌ Audit Assess is not responding${NC}"
fi

if curl -s http://localhost:8004/health > /dev/null; then
    echo -e "${GREEN}✅ Whis Data Input is healthy${NC}"
else
    echo -e "${RED}❌ Whis Data Input is not responding${NC}"
fi

if curl -s http://localhost:8006/health > /dev/null; then
    echo -e "${GREEN}✅ Whis Enhance is healthy${NC}"
else
    echo -e "${RED}❌ Whis Enhance is not responding${NC}"
fi

echo ""
echo -e "${BLUE}🌐 Starting Frontend...${NC}"

# Check if Node.js is available
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    echo "Starting Vue.js frontend..."
    
    # Check if frontend dependencies are installed
    if [ ! -d "frontend/node_modules" ]; then
        echo "Installing frontend dependencies..."
        cd frontend && npm install && cd ..
    fi
    
    # Start frontend
    cd frontend
    echo -e "${GREEN}✅ Frontend starting on http://localhost:3000${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
    
    # Start frontend in background
    npm run dev &
    FRONTEND_PID=$!
    
    # Wait for frontend to start
    sleep 10
    
    echo ""
    echo -e "${GREEN}🎉 LinkOps MLOps Platform is ready!${NC}"
    echo ""
    echo -e "${BLUE}📱 Access Points:${NC}"
    echo "  Frontend Dashboard: http://localhost:3000"
    echo "  Audit Form:         http://localhost:3000/auditguard"
    echo "  Task Management:    http://localhost:3000/tasks"
    echo ""
    echo -e "${BLUE}🔧 API Endpoints:${NC}"
    echo "  MLOps Platform:     http://localhost:8000/docs"
    echo "  Audit Assess:       http://localhost:8003/docs"
    echo "  Whis Data Input:    http://localhost:8004/docs"
    echo "  Whis Enhance:       http://localhost:8006/docs"
    echo ""
    echo -e "${YELLOW}🧪 Run Integration Test:${NC}"
    echo "  node test_frontend_integration.js"
    echo ""
    echo -e "${YELLOW}📖 Documentation:${NC}"
    echo "  FRONTEND_INTEGRATION.md - Complete integration guide"
    echo "  README.md - Platform overview and setup"
    
    # Keep script running
    wait $FRONTEND_PID
    
else
    echo -e "${RED}❌ Node.js or npm not found${NC}"
    echo "Install Node.js to run the frontend"
    echo ""
    echo -e "${YELLOW}Backend services are running. Install Node.js and run:${NC}"
    echo "  cd frontend && npm install && npm run dev"
fi 