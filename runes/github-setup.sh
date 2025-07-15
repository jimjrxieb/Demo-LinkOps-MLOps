#!/bin/bash

# GitHub Setup Script for LinkOps Demo
# Uses GH_PAT environment variable for authentication

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐙 GitHub Setup for LinkOps Demo${NC}"
echo "=================================="

# Check if GH_PAT is set
if [ -z "$GH_PAT" ]; then
    echo -e "${RED}❌ GH_PAT environment variable is not set${NC}"
    echo -e "${YELLOW}Please set your GitHub Personal Access Token:${NC}"
    echo "export GH_PAT='your-github-pat'"
    echo ""
    echo -e "${YELLOW}Required permissions:${NC}"
    echo "  - repo (Full control of private repositories)"
    echo "  - workflow (Update GitHub Action workflows)"
    exit 1
fi

# Check if git is configured
if ! git config --global user.name > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Git user.name not configured${NC}"
    echo -e "${BLUE}Please configure git:${NC}"
    echo "git config --global user.name 'Your Name'"
    echo "git config --global user.email 'your.email@example.com'"
fi

# Test GitHub API access
echo -e "${GREEN}✅ Testing GitHub API access...${NC}"
RESPONSE=$(curl -s -H "Authorization: token $GH_PAT" https://api.github.com/user)

if echo "$RESPONSE" | grep -q "login"; then
    USERNAME=$(echo "$RESPONSE" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✅ Successfully authenticated as: $USERNAME${NC}"
else
    echo -e "${RED}❌ Failed to authenticate with GitHub${NC}"
    echo -e "${YELLOW}Please check your GH_PAT token${NC}"
    exit 1
fi

# Configure git to use token for HTTPS
echo -e "${GREEN}✅ Configuring git for token-based authentication${NC}"
git config --global credential.helper store

# Test repository access
REPO_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -n "$REPO_URL" ]; then
    echo -e "${GREEN}✅ Repository URL: $REPO_URL${NC}"
    
    # Update remote URL to use token if it's HTTPS
    if [[ "$REPO_URL" == https://* ]]; then
        NEW_URL="https://$GH_PAT@github.com/$(echo $REPO_URL | sed 's|https://github.com/||')"
        git remote set-url origin "$NEW_URL"
        echo -e "${GREEN}✅ Updated remote URL to use token authentication${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No git remote found${NC}"
fi

echo ""
echo -e "${GREEN}🎉 GitHub setup complete!${NC}"
echo -e "${BLUE}📝 You can now:${NC}"
echo "  - Push changes with token authentication"
echo "  - Trigger GitHub Actions workflows"
echo "  - Access private repositories"
echo ""
echo -e "${YELLOW}🔧 Next steps:${NC}"
echo "  ./docker-login.sh"
echo "  ./build-demo-images.sh latest true docker.io/linksrobot" 