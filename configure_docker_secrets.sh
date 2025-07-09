#!/bin/bash

# LinkOps Docker Registry Configuration Script
# Helps set up GitHub secrets and configure Docker namespace options

set -e

echo "🔧 LinkOps Docker Registry Configuration"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_step() { echo -e "${CYAN}📋 Step $1:${NC} $2"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

echo ""
print_step "1" "Docker Hub Account Setup"
echo "----------------------------------------"
print_info "You need a Docker Hub account and access token."
echo ""
echo "If you don't have a Docker Hub account:"
echo "1. Go to: https://hub.docker.com"
echo "2. Sign up for a free account"
echo ""
echo "To create an access token:"
echo "1. Login to Docker Hub"
echo "2. Go to: https://hub.docker.com/settings/security"
echo "3. Click 'New Access Token'"
echo "4. Name: 'LinkOps-MLOps-CI'"
echo "5. Permissions: Read, Write, Delete"
echo "6. Copy the token (you won't see it again!)"
echo ""

read -p "Press Enter when you have your Docker Hub username and access token ready..."

echo ""
print_step "2" "Choose Docker Namespace Strategy"
echo "----------------------------------------"
echo "You have two options for where to push Docker images:"
echo ""
echo "Option A: Organization Namespace (linkops/*)"
echo "  - Images: docker.io/linkops/service-name:latest"
echo "  - Requires: 'linkops' organization exists and you have push permissions"
echo "  - Best for: Production/team environments"
echo ""
echo "Option B: Personal Namespace (your-username/*)"
echo "  - Images: docker.io/your-username/service-name:latest"
echo "  - Requires: Only your personal Docker Hub account"
echo "  - Best for: Testing/development"
echo ""

while true; do
    read -p "Choose namespace strategy (A/B): " namespace_choice
    case $namespace_choice in
        [Aa]* ) 
            NAMESPACE_TYPE="organization"
            NAMESPACE="linkops"
            break;;
        [Bb]* ) 
            NAMESPACE_TYPE="personal"
            break;;
        * ) echo "Please answer A or B.";;
    esac
done

echo ""
print_step "3" "Collect Docker Credentials"
echo "----------------------------------------"
read -p "Docker Hub Username: " DOCKER_USER

if [[ "$NAMESPACE_TYPE" == "personal" ]]; then
    NAMESPACE="$DOCKER_USER"
fi

echo ""
echo -e "${CYAN}Selected Configuration:${NC}"
echo "  Username: $DOCKER_USER"
echo "  Namespace: $NAMESPACE"
echo "  Image format: docker.io/$NAMESPACE/service-name:latest"
echo ""

read -s -p "Docker Hub Access Token: " DOCKER_CRED
echo ""

if [[ -z "$DOCKER_USER" || -z "$DOCKER_CRED" ]]; then
    print_error "Username and access token are required"
    exit 1
fi

echo ""
print_step "4" "Validate Docker Credentials"
echo "----------------------------------------"
print_info "Testing Docker Hub authentication..."

echo "$DOCKER_CRED" | docker login docker.io -u "$DOCKER_USER" --password-stdin

if [[ $? -eq 0 ]]; then
    print_success "Docker Hub authentication successful"
    docker logout docker.io
else
    print_error "Docker Hub authentication failed"
    print_info "Please check your username and access token"
    exit 1
fi

echo ""
print_step "5" "Update GitHub Actions Workflow"
echo "----------------------------------------"

if [[ "$NAMESPACE_TYPE" == "personal" ]]; then
    print_info "Updating workflow to use personal namespace..."
    
    # Update the workflow file to use personal namespace
    sed -i.bak 's/image_name="linkops\/$name:latest"/# image_name="linkops\/$name:latest" # Organization namespace\n             image_name="${{ secrets.DOCKER_USER }}\/$name:latest" # Personal namespace/' .github/workflows/main.yml
    
    print_success "Workflow updated to use personal namespace: $DOCKER_USER"
else
    print_info "Workflow already configured for organization namespace: linkops"
    print_warning "Ensure your account '$DOCKER_USER' has push permissions to 'linkops' organization"
    echo ""
    echo "To grant permissions:"
    echo "1. linkops organization owner adds '$DOCKER_USER' as member"
    echo "2. Give 'Write' or 'Admin' permissions"
    echo "3. Or create a team with push permissions and add '$DOCKER_USER'"
fi

echo ""
print_step "6" "GitHub Repository Secrets"
echo "----------------------------------------"
print_info "You need to add these secrets to your GitHub repository:"
echo ""
echo "Repository: https://github.com/jimjrxieb/LinkOps-MLOps"
echo "Path: Settings → Secrets and variables → Actions → New repository secret"
echo ""
echo -e "${YELLOW}Required Secrets:${NC}"
echo "┌─────────────┬─────────────────────────────────────┐"
echo "│ Secret Name │ Value                               │"
echo "├─────────────┼─────────────────────────────────────┤"
echo "│ DOCKER_USER │ $DOCKER_USER"
echo "│ DOCKER_CRED │ [your-access-token-from-step-1]     │"
echo "└─────────────┴─────────────────────────────────────┘"
echo ""
print_warning "IMPORTANT: Use your ACCESS TOKEN as DOCKER_CRED, not your password!"
echo ""

echo ""
print_step "7" "Test Configuration"
echo "----------------------------------------"
print_info "After setting up GitHub secrets, test the configuration:"
echo ""
echo "1. Commit and push any changes:"
echo "   git add ."
echo "   git commit -m 'Configure Docker registry for $NAMESPACE_TYPE namespace'"
echo "   git push origin main"
echo ""
echo "2. Monitor the GitHub Actions workflow:"
echo "   https://github.com/jimjrxieb/LinkOps-MLOps/actions"
echo ""
echo "3. Look for the 'Build + Push Docker Images' job"
echo "4. Verify successful authentication and image pushes"
echo ""

echo ""
print_success "Configuration complete!"
echo ""
print_info "Summary:"
echo "  ✅ Docker credentials validated"
echo "  ✅ Workflow configured for '$NAMESPACE_TYPE' namespace"
echo "  ✅ Target images: docker.io/$NAMESPACE/service-name:latest"
echo ""
print_info "Next: Set up GitHub secrets and push to trigger the workflow"

if [[ "$NAMESPACE_TYPE" == "organization" ]]; then
    echo ""
    print_warning "Remember: Ensure '$DOCKER_USER' has push permissions to 'linkops' organization!"
fi 