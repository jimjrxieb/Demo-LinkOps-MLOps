#!/bin/bash

# Frontend CI Fix Script
# Handles the triple-layered failure in frontend CI runs

set -e

echo "🔧 Frontend CI Fix Script"
echo "========================="

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo "📁 Project root: $PROJECT_ROOT"
echo "📁 Frontend dir: $FRONTEND_DIR"

# Check if we're in the right directory
if [ ! -f "$FRONTEND_DIR/package.json" ]; then
    echo "❌ Error: package.json not found in frontend directory"
    echo "   Make sure you're running this from the project root"
    exit 1
fi

# Step 1: Fix path issues
echo ""
echo "🔍 Step 1: Checking script paths..."
if [ ! -f "$FRONTEND_DIR/fix_frontend.py" ]; then
    echo "❌ Error: fix_frontend.py not found in frontend directory"
    exit 1
fi
echo "✅ fix_frontend.py found"

# Step 2: Clean corrupted dependencies
echo ""
echo "🧹 Step 2: Cleaning corrupted dependencies..."
cd "$FRONTEND_DIR"

echo "   Removing node_modules and package-lock.json..."
rm -rf node_modules package-lock.json

echo "   Clearing npm cache..."
npm cache clean --force

echo "   Reinstalling dependencies..."
npm install

# Step 3: Check dependency health
echo ""
echo "🔍 Step 3: Checking dependency health..."

# Check ESLint
if npx eslint --version > /dev/null 2>&1; then
    echo "✅ ESLint is working"
else
    echo "❌ ESLint is corrupted"
    exit 1
fi

# Check Vite
if npx vite --version > /dev/null 2>&1; then
    echo "✅ Vite is working"
else
    echo "❌ Vite is corrupted"
    exit 1
fi

# Step 4: Run the auto-fix script
echo ""
echo "🚀 Step 4: Running frontend auto-fix script..."
cd "$PROJECT_ROOT"
python3 frontend/fix_frontend.py

# Step 5: Test the build
echo ""
echo "🏗️ Step 5: Testing build..."
cd "$FRONTEND_DIR"
npm run build

echo ""
echo "🎉 Frontend CI fix completed successfully!"
echo "   All dependencies are clean and builds are working" 