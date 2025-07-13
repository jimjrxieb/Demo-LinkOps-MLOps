#!/bin/bash

# Build and Push Demo Images Script
# This script builds and pushes all demo images with the demo- prefix

set -e

echo "🐳 Building and Pushing Demo Images"
echo "==================================="
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

# List of services to build
services=(
    "frontend"
    "mlops/whis_data_input"
    "mlops/whis_sanitize" 
    "mlops/whis_logic"
    "shadows/ficknury_evaluator"
)

success_count=0
total_count=${#services[@]}
failed_services=()

echo "📋 Services to build:"
for service in "${services[@]}"; do
    echo "  - $service"
done
echo ""

# Build and push each service
for service in "${services[@]}"; do
    service_name=$(basename "$service")
    image_name="linksrobot/demo-$service_name:latest"
    
    echo "🔨 Building $service_name..."
    echo "📁 Directory: $service"
    echo "🐳 Image: $image_name"
    
    # Check if Dockerfile exists
    if [[ ! -f "$service/Dockerfile" ]]; then
        echo "❌ No Dockerfile found in $service"
        failed_services+=("$service_name")
        continue
    fi
    
    # Build the image
    if docker build -t "$image_name" "$service" --progress=plain; then
        echo "✅ Build successful for $service_name"
        
        # Push the image
        echo "🚀 Pushing $image_name..."
        if docker push "$image_name"; then
            echo "✅ Push successful for $service_name"
            success_count=$((success_count + 1))
        else
            echo "❌ Push failed for $service_name"
            failed_services+=("$service_name")
        fi
    else
        echo "❌ Build failed for $service_name"
        failed_services+=("$service_name")
    fi
    
    echo ""
done

# Summary
echo "📊 Build and Push Summary:"
echo "✅ Successful: $success_count/$total_count services"
echo "❌ Failed: ${#failed_services[@]} services"

if [[ ${#failed_services[@]} -gt 0 ]]; then
    echo "Failed services:"
    for service in "${failed_services[@]}"; do
        echo "  - $service"
    done
fi

if [[ $success_count -eq $total_count ]]; then
    echo "🎉 All demo images built and pushed successfully!"
    echo ""
    echo "📋 Available demo images:"
    for service in "${services[@]}"; do
        service_name=$(basename "$service")
        echo "  - linksrobot/demo-$service_name:latest"
    done
else
    echo "⚠️ Some images failed to build or push"
    exit 1
fi 