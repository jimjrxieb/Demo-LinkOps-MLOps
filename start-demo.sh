#!/bin/bash

echo "🚀 Starting LinkOps MLOps Demo Platform"
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.template .env
    echo "✅ Environment file created"
fi

# Start the demo services
echo "🔧 Starting demo services..."
docker-compose up -d --build

echo ""
echo "🎉 Demo platform is starting up!"
echo ""
echo "📱 Access Points:"
echo "   James GUI: http://localhost:3000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "🎯 Demo Workflow:"
echo "   1. Go to http://localhost:3000"
echo "   2. Enter a task (e.g., 'How do I deploy to Kubernetes?')"
echo "   3. Submit and see the results"
echo "   4. Approve or reject generated Orbs"
echo ""
echo "🔍 View logs: docker-compose logs -f"
echo "🛑 Stop: docker-compose down" 