#!/bin/bash

# Auto Tool Runner Launcher
# ========================

set -e

echo "🚀 Starting Auto Tool Runner..."
echo "📁 Working directory: $(pwd)"

# Check if we're in the right directory
if [ ! -f "scripts/auto_runner.py" ]; then
    echo "❌ Error: auto_runner.py not found in scripts/ directory"
    echo "Please run this script from the DEMO-LinkOps directory"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    exit 1
fi

# Check if required directories exist
if [ ! -d "db/mcp_tools" ]; then
    echo "❌ Error: db/mcp_tools directory not found"
    exit 1
fi

echo "✅ Environment check passed"
echo "🔧 Starting Auto Tool Runner..."
echo ""

# Run the auto runner
python3 scripts/auto_runner.py 