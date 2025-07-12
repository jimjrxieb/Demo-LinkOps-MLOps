#!/bin/bash

# Script to tag and push demo-prefixed Docker images
# Usage: ./tag-and-push-demo-images.sh [push]

DOCKER_USERNAME="linksrobot"
PUSH_IMAGES=${1:-false}

echo "🐳 Tagging and pushing demo Docker images..."
echo "Docker Hub username: $DOCKER_USERNAME"
echo "Push images: $PUSH_IMAGES"
echo ""

# Function to tag and push an image
tag_and_push() {
    local service_name=$1
    local demo_name=$2
    local port=$3
    
    echo "📦 Processing $service_name..."
    
    # Tag the image
    docker tag $service_name:latest $DOCKER_USERNAME/demo-$demo_name:latest
    echo "  ✅ Tagged: $service_name:latest → $DOCKER_USERNAME/demo-$demo_name:latest"
    
    # Push if requested
    if [ "$PUSH_IMAGES" = "push" ]; then
        echo "  🚀 Pushing to Docker Hub..."
        docker push $DOCKER_USERNAME/demo-$demo_name:latest
        echo "  ✅ Pushed: $DOCKER_USERNAME/demo-$demo_name:latest"
    fi
    
    echo ""
}

# Tag and push all services
tag_and_push "whis_data_input" "whis-data-input" "8001"
tag_and_push "whis_sanitize" "whis-sanitize" "8002"
tag_and_push "whis_logic" "whis-logic" "8003"
tag_and_push "ficknury_evaluator" "ficknury-evaluator" "8004"
tag_and_push "mlops_platform" "mlops-platform" "8000"
tag_and_push "frontend" "frontend" "3000"

echo "🎉 Demo image tagging complete!"
echo ""
echo "📋 Summary of demo images:"
echo "  - $DOCKER_USERNAME/demo-whis-data-input:latest"
echo "  - $DOCKER_USERNAME/demo-whis-sanitize:latest"
echo "  - $DOCKER_USERNAME/demo-whis-logic:latest"
echo "  - $DOCKER_USERNAME/demo-ficknury-evaluator:latest"
echo "  - $DOCKER_USERNAME/demo-mlops-platform:latest"
echo "  - $DOCKER_USERNAME/demo-frontend:latest"
echo ""

if [ "$PUSH_IMAGES" != "push" ]; then
    echo "💡 To push images to Docker Hub, run:"
    echo "   ./tag-and-push-demo-images.sh push"
    echo ""
    echo "🔐 Make sure you're logged in to Docker Hub:"
    echo "   docker login -u $DOCKER_USERNAME"
fi 