#!/bin/bash
"""
Quick start script for DEMO-LinkOps
"""

set -e

echo "🚀 Starting DEMO-LinkOps Platform..."

# Check if Docker and Docker Compose are available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it with required environment variables."
    exit 1
fi

# Load environment variables
source .env

echo "✅ Environment loaded"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p db/init
mkdir -p nginx/ssl
mkdir -p rag/vectorstore
mkdir -p ml-models/models
mkdir -p pipeline/data
mkdir -p sync_engine/data

echo "✅ Directories created"

# Run linting and formatting
echo "🔧 Running code quality fixes..."
python3 fix_lint_script.py
echo "✅ Code quality checks completed"

# Build and start services
echo "🏗️  Building and starting services..."

# Use docker compose or docker-compose based on availability
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Build images
echo "📦 Building Docker images..."
$COMPOSE_CMD build --parallel

# Start services
echo "🚀 Starting services..."
$COMPOSE_CMD up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
services=("postgres" "redis" "rag" "ml-models" "pipeline" "sync-engine" "unified-api" "frontend")

for service in "${services[@]}"; do
    echo "Checking $service..."
    if $COMPOSE_CMD ps $service | grep -q "Up"; then
        echo "✅ $service is running"
    else
        echo "⚠️  $service might have issues"
        $COMPOSE_CMD logs --tail=10 $service
    fi
done

echo ""
echo "🎉 DEMO-LinkOps Platform Started!"
echo ""
echo "📡 Available Services:"
echo "   - Frontend:     http://localhost:3000"
echo "   - Unified API:  http://localhost:9000"
echo "   - API Docs:     http://localhost:9000/docs"
echo "   - RAG Service:  http://localhost:8005"
echo "   - ML Models:    http://localhost:8002"
echo "   - Pipeline:     http://localhost:8003"
echo "   - Sync Engine:  http://localhost:8004"
echo ""
echo "📊 Monitoring:"
echo "   - Health Check: http://localhost:9000/health"
echo "   - System Info:  http://localhost:9000/system"
echo ""
echo "🛠️  Management Commands:"
echo "   - View logs:    $COMPOSE_CMD logs -f [service_name]"
echo "   - Stop all:     $COMPOSE_CMD down"
echo "   - Restart:      $COMPOSE_CMD restart [service_name]"
echo ""

# Optional: Open browser
if command -v xdg-open &> /dev/null; then
    echo "🌐 Opening frontend in browser..."
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    echo "🌐 Opening frontend in browser..."
    open http://localhost:3000
fi

echo "✅ Setup complete! Check the services above."