#!/bin/bash

# LinkOps MLOps Platform - Demo Startup Script

echo "🚀 Starting LinkOps MLOps Platform - Demo Version"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.template .env
    echo "✅ Environment file created"
fi

# Start the services
echo "🔧 Starting demo services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Check service status
echo "📊 Checking service status..."
docker-compose ps

echo ""
echo "🎉 LinkOps MLOps Demo Platform is starting up!"
echo ""
echo "📱 Access Points:"
echo "   Frontend (James GUI): http://localhost:3000"
echo "   API Documentation:    http://localhost:8000/docs"
echo "   API Base URL:         http://localhost:8000"
echo ""
echo "🎯 Demo Workflow:"
echo "   1. Go to http://localhost:3000"
echo "   2. Use the James GUI to submit tasks"
echo "   3. Search for existing Orbs"
echo "   4. Generate new Orbs with Whis"
echo "   5. Approve or reject generated Orbs"
echo ""
echo "🔍 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo ""
echo "✨ Enjoy exploring the demo platform!" 