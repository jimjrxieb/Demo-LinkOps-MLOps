#!/bin/bash

# LinkOps Docker Registry Authentication Test
# Run this script locally to verify your Docker Hub credentials before using them in GitHub Actions

set -e

echo "🐳 LinkOps Docker Registry Authentication Test"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    case $1 in
        "success") echo -e "${GREEN}✅ $2${NC}" ;;
        "error") echo -e "${RED}❌ $2${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️ $2${NC}" ;;
        "info") echo -e "${BLUE}ℹ️ $2${NC}" ;;
    esac
}

# Check if Docker is installed and running
print_status "info" "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    print_status "error" "Docker is not installed or not in PATH"
    exit 1
fi

if ! docker info &> /dev/null; then
    print_status "error" "Docker daemon is not running"
    print_status "info" "Please start Docker and try again"
    exit 1
fi

print_status "success" "Docker is installed and running"

# Get credentials from user
echo ""
print_status "info" "Please provide your Docker Hub credentials:"
read -p "Docker Hub Username: " DOCKER_USER
read -s -p "Docker Hub Password/Token: " DOCKER_CRED
echo ""

if [[ -z "$DOCKER_USER" || -z "$DOCKER_CRED" ]]; then
    print_status "error" "Username and password/token are required"
    exit 1
fi

# Test Docker Hub login
print_status "info" "Testing Docker Hub authentication..."
echo "$DOCKER_CRED" | docker login docker.io -u "$DOCKER_USER" --password-stdin

if [[ $? -eq 0 ]]; then
    print_status "success" "Docker Hub login successful"
else
    print_status "error" "Docker Hub login failed"
    print_status "info" "Please check your username and password/token"
    exit 1
fi

# Test repository access by building and pushing a test image
print_status "info" "Testing repository push access..."

# Create a minimal test image
TEST_IMAGE="$DOCKER_USER/linkops-test:latest"
TEST_DIR=$(mktemp -d)

cat > "$TEST_DIR/Dockerfile" << EOF
FROM alpine:latest
RUN echo "LinkOps test image" > /test.txt
CMD ["cat", "/test.txt"]
EOF

print_status "info" "Building test image: $TEST_IMAGE"
docker build -t "$TEST_IMAGE" "$TEST_DIR"

print_status "info" "Pushing test image to Docker Hub..."
if docker push "$TEST_IMAGE"; then
    print_status "success" "Test image push successful"
    
    # Clean up test image
    print_status "info" "Cleaning up test image..."
    docker rmi "$TEST_IMAGE" || true
    
    # Try to delete from registry (optional)
    print_status "info" "You may want to delete the test image from Docker Hub manually"
    print_status "info" "Visit: https://hub.docker.com/r/$DOCKER_USER/linkops-test"
else
    print_status "error" "Test image push failed"
    print_status "warning" "This could indicate insufficient permissions or repository access issues"
fi

# Clean up
rm -rf "$TEST_DIR"
docker logout docker.io

echo ""
print_status "info" "Testing complete!"
echo ""
print_status "info" "To configure GitHub Actions secrets:"
echo "1. Go to your repository: Settings → Secrets and variables → Actions"
echo "2. Add secret: DOCKER_USER = $DOCKER_USER"
echo "3. Add secret: DOCKER_CRED = [your-password-or-token]"
echo ""
print_status "success" "Your Docker Hub credentials are working correctly!" 