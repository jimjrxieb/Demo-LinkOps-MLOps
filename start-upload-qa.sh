#!/bin/bash

# Start Upload and Q&A Services
# =============================

set -e

echo "🚀 Starting Upload and Q&A Services for DEMO-LinkOps"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "rag/main.py" ]; then
    print_error "Please run this script from the DEMO-LinkOps root directory"
    exit 1
fi

# Check Python dependencies
print_status "Checking Python dependencies..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "rag/venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    cd rag
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    print_success "Virtual environment created and dependencies installed"
else
    print_status "Using existing virtual environment"
fi

# Check Node.js dependencies
print_status "Checking Node.js dependencies..."
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed"
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    print_warning "Frontend dependencies not found. Installing..."
    cd frontend
    npm install
    cd ..
    print_success "Frontend dependencies installed"
else
    print_status "Frontend dependencies found"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p rag/uploads
mkdir -p rag/vectorstore
mkdir -p rag/llm_weights
mkdir -p rag/db

# Check if LLM model exists
if [ ! -f "rag/llm_weights/mistral.gguf" ]; then
    print_warning "LLM model not found. You can download it manually:"
    echo "  wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf -O rag/llm_weights/mistral.gguf"
    echo "  Or use Ollama: ollama pull mistral"
    echo ""
    print_status "Continuing with fallback mode (no local LLM)"
else
    print_success "LLM model found"
fi

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down services..."
    if [ ! -z "$RAG_PID" ]; then
        kill $RAG_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    print_success "Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start RAG service
print_status "Starting RAG service..."
cd rag
source venv/bin/activate
python main.py &
RAG_PID=$!
cd ..

# Wait for RAG service to start
print_status "Waiting for RAG service to start..."
sleep 5

# Check if RAG service is running
if ! curl -s http://localhost:8005/health > /dev/null; then
    print_error "RAG service failed to start"
    cleanup
fi

print_success "RAG service started on http://localhost:8005"

# Start frontend service
print_status "Starting frontend service..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend service to start
print_status "Waiting for frontend service to start..."
sleep 10

print_success "Frontend service started"

# Display service information
echo ""
echo "🎉 Services are running!"
echo "========================"
echo "📄 Frontend: http://localhost:5173"
echo "🔍 RAG API:  http://localhost:8005"
echo "📚 Document Q&A: http://localhost:5173/search-memory"
echo ""
echo "📋 Available endpoints:"
echo "  - POST /api/upload          - Upload documents"
echo "  - POST /api/query-simple     - Simple Q&A"
echo "  - POST /api/query-llm        - Advanced LLM Q&A"
echo "  - GET  /api/documents        - List documents"
echo "  - GET  /api/stats            - System statistics"
echo ""
echo "🧪 Run tests: python rag/test_upload_qa.py"
echo ""
echo "Press Ctrl+C to stop all services"

# Keep the script running
wait 