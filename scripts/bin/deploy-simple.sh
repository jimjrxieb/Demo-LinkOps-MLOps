#!/bin/bash

# LinkOps Demo - Simple Deployment
# ================================

set -e

echo "🚀 LinkOps Demo - Quick Start"
echo "=============================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo -e "${BLUE}[STEP]${NC} Stopping any existing containers..."
docker-compose -f docker/docker-compose.yml down 2>/dev/null || true

echo -e "${BLUE}[STEP]${NC} Building containers (this may take a few minutes)..."
docker-compose -f docker/docker-compose.yml build --no-cache

echo -e "${BLUE}[STEP]${NC} Starting services..."
docker-compose -f docker/docker-compose.yml up -d

echo -e "${BLUE}[STEP]${NC} Waiting for services to be ready..."
sleep 10

echo ""
echo -e "${GREEN}✅ LinkOps Demo is now running!${NC}"
echo "================================"
echo ""
echo "🌐 Frontend: http://localhost:8080"
echo "🔧 API: http://localhost:9000"
echo "📚 API Docs: http://localhost:9000/docs"
echo "❤️ Health Check: http://localhost:9000/health"
echo ""
echo "📁 Sample Data:"
echo "   - ML Training: sample_data/employee_data.csv"
echo "   - RAG Testing: sample_data/company_documents.txt"
echo ""
echo "🎯 Demo Workflows:"
echo "   1. Upload CSV → Train ML Model"
echo "   2. Create AI Agent → Configure Tools"
echo "   3. Upload Documents → RAG Search"
echo "   4. Run HTC Pipeline → End-to-End Training"
echo ""
echo -e "${YELLOW}💡 Tip: Open http://localhost:8080 in your browser to start!${NC}"
echo ""
echo "To stop the demo: docker-compose -f docker/docker-compose.yml down" 