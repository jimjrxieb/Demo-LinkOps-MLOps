#!/bin/bash

# Quick Frontend Demo Image Build
# This script builds and pushes just the frontend demo image

set -e

echo "🐳 Building Frontend Demo Image"
echo "==============================="
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    exit 1
fi

# Check if we're logged in to Docker Hub
if ! docker info &> /dev/null; then
    echo "❌ Not logged in to Docker. Please run: docker login"
    exit 1
fi

# Build and push frontend
echo "🔨 Building frontend demo image..."
echo "📁 Directory: frontend/"
echo "🐳 Image: linksrobot/demo-frontend:latest"

# Check if Dockerfile exists
if [[ ! -f "frontend/Dockerfile" ]]; then
    echo "❌ No Dockerfile found in frontend/"
    exit 1
fi

# Build the image
echo "🚀 Building..."
if docker build -t linksrobot/demo-frontend:latest frontend/ --progress=plain; then
    echo "✅ Build successful"
    
    # Push the image
    echo "🚀 Pushing to Docker Hub..."
    if docker push linksrobot/demo-frontend:latest; then
        echo "✅ Push successful!"
        echo ""
        echo "🎉 Frontend demo image is now available at:"
        echo "   linksrobot/demo-frontend:latest"
        echo ""
        echo "📋 Your ArgoCD deployment should now be able to pull this image."
    else
        echo "❌ Push failed"
        exit 1
    fi
else
    echo "❌ Build failed"
    exit 1
fi 