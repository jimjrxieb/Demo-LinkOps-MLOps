#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
VERSION="v1.0.0"  # bump as needed

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose >/dev/null 2>&1; then
        log_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
}

# Create necessary directories
setup_directories() {
    log_info "Setting up directories..."
    mkdir -p "${APP_DIR}/db/mcp_tools"
    mkdir -p "${APP_DIR}/db/logs"
    mkdir -p "${APP_DIR}/db/sqlite"
    mkdir -p "${APP_DIR}/rag_data"
    log_success "Directories created"
}

# Check environment file
check_env() {
    if [[ ! -f "${APP_DIR}/.env" ]]; then
        if [[ -f "${APP_DIR}/.env.example" ]]; then
            log_warning ".env file not found. Copying from .env.example..."
            cp "${APP_DIR}/.env.example" "${APP_DIR}/.env"
            log_success ".env file created from example"
        else
            log_warning ".env file not found. Creating default .env..."
            cat > "${APP_DIR}/.env" << EOF
# AI Box Configuration
API_PORT=8000
API_HOST=0.0.0.0
FRONTEND_PORT=3000
FRONTEND_HOST=0.0.0.0
DB_PATH=/app/db
SQLITE_PATH=/app/db/sqlite
RAG_DATA_PATH=/app/rag_data
RAG_MODEL=sentence-transformers/all-MiniLM-L6-v2
LOG_LEVEL=INFO
LOG_PATH=/app/db/logs
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
            log_success "Default .env file created"
        fi
    fi
}

cmd_up() {
    log_info "Starting AI Box services..."
    
    check_docker
    check_docker_compose
    setup_directories
    check_env
    
    cd "${APP_DIR}"
    
    # Build and start services
    log_info "Building and starting containers..."
    docker-compose up -d --build
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 10
    
    # Check service health
    if curl -f http://localhost:8000/api/health >/dev/null 2>&1; then
        log_success "Backend API is healthy"
    else
        log_warning "Backend API health check failed, but services may still be starting..."
    fi
    
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        log_success "Frontend is accessible"
    else
        log_warning "Frontend health check failed, but services may still be starting..."
    fi
    
    log_success "AI Box services started successfully!"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "Use './package.sh logs' to view service logs"
    echo "Use './package.sh down' to stop services"
}

cmd_down() {
    log_info "Stopping AI Box services..."
    cd "${APP_DIR}"
    docker-compose down
    log_success "AI Box services stopped"
}

cmd_restart() {
    log_info "Restarting AI Box services..."
    cmd_down
    sleep 2
    cmd_up
}

cmd_logs() {
    cd "${APP_DIR}"
    if [[ "${1:-}" == "follow" ]]; then
        docker-compose logs -f
    else
        docker-compose logs
    fi
}

cmd_status() {
    log_info "Checking AI Box service status..."
    cd "${APP_DIR}"
    
    echo ""
    echo "📊 Container Status:"
    docker-compose ps
    
    echo ""
    echo "🔍 Service Health:"
    
    # Check API health
    if curl -f http://localhost:8000/api/health >/dev/null 2>&1; then
        echo "✅ Backend API: Healthy"
    else
        echo "❌ Backend API: Unhealthy"
    fi
    
    # Check frontend health
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        echo "✅ Frontend: Accessible"
    else
        echo "❌ Frontend: Unreachable"
    fi
    
    echo ""
    echo "📈 Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
}

cmd_bundle() {
    TARGET="${APP_DIR}/demo-linkops-${VERSION}.tar.gz"
    log_info "Bundling AI Box into ${TARGET}..."
    
    cd "${APP_DIR}"
    
    # Create temporary directory for bundling
    TEMP_DIR=$(mktemp -d)
    BUNDLE_DIR="${TEMP_DIR}/demo-linkops-${VERSION}"
    mkdir -p "${BUNDLE_DIR}"
    
    # Copy files to bundle directory
    log_info "Copying files..."
    rsync -av --exclude='node_modules' \
              --exclude='frontend/node_modules' \
              --exclude='.git' \
              --exclude='*.tar.gz' \
              --exclude='db/logs/*' \
              --exclude='db/sqlite/*' \
              --exclude='.env' \
              . "${BUNDLE_DIR}/"
    
    # Create sample data
    log_info "Creating sample data..."
    mkdir -p "${BUNDLE_DIR}/db/mcp_tools"
    mkdir -p "${BUNDLE_DIR}/rag_data"
    
    # Create sample MCP tool
    cat > "${BUNDLE_DIR}/db/mcp_tools/sample_tool.json" << EOF
{
  "name": "sample_tool",
  "description": "A sample MCP tool for demonstration",
  "task_type": "demo",
  "command": "echo 'Hello from AI Box!'",
  "tags": ["demo", "sample"],
  "auto": false,
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
    
    # Create sample RAG document
    cat > "${BUNDLE_DIR}/rag_data/sample_document.txt" << EOF
Sample Document for AI Box

This is a sample document that demonstrates the RAG (Retrieval-Augmented Generation) capabilities of the AI Box.

Key Features:
- Document embedding and search
- AI-powered question answering
- Source attribution and citations
- Real-time chat interface

The AI Box can process various document types including:
- Text files (.txt)
- Markdown files (.md)
- PDF documents (.pdf)
- Word documents (.docx)

This sample document will help you get started with the AI Box RAG functionality.
EOF
    
    # Create .env.example
    cat > "${BUNDLE_DIR}/.env.example" << EOF
# AI Box Configuration
API_PORT=8000
API_HOST=0.0.0.0
FRONTEND_PORT=3000
FRONTEND_HOST=0.0.0.0
DB_PATH=/app/db
SQLITE_PATH=/app/db/sqlite
RAG_DATA_PATH=/app/rag_data
RAG_MODEL=sentence-transformers/all-MiniLM-L6-v2
LOG_LEVEL=INFO
LOG_PATH=/app/db/logs
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
    
    # Create bundle
    cd "${TEMP_DIR}"
    tar -czf "${TARGET}" "demo-linkops-${VERSION}"
    
    # Clean up
    rm -rf "${TEMP_DIR}"
    
    log_success "Bundle created at ${TARGET}"
    echo ""
    echo "📦 Bundle contents:"
    tar -tzf "${TARGET}" | head -20
    echo "..."
    echo ""
    echo "🚀 To deploy:"
    echo "   tar -xzf ${TARGET}"
    echo "   cd demo-linkops-${VERSION}"
    echo "   ./package.sh up"
}

cmd_backup() {
    BACKUP_FILE="${APP_DIR}/ai-box-backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    log_info "Creating backup: ${BACKUP_FILE}"
    
    cd "${APP_DIR}"
    
    if [[ -d "db" ]]; then
        tar -czf "${BACKUP_FILE}" db/
        log_success "Backup created: ${BACKUP_FILE}"
        echo "📊 Backup size: $(du -h "${BACKUP_FILE}" | cut -f1)"
    else
        log_warning "No data directory found to backup"
    fi
}

cmd_restore() {
    if [[ -z "${1:-}" ]]; then
        log_error "Please specify backup file to restore"
        echo "Usage: $0 restore <backup-file.tar.gz>"
        exit 1
    fi
    
    BACKUP_FILE="$1"
    if [[ ! -f "${BACKUP_FILE}" ]]; then
        log_error "Backup file not found: ${BACKUP_FILE}"
        exit 1
    fi
    
    log_info "Restoring from backup: ${BACKUP_FILE}"
    
    cd "${APP_DIR}"
    
    # Stop services if running
    if docker-compose ps | grep -q "Up"; then
        log_warning "Services are running. Stopping before restore..."
        cmd_down
    fi
    
    # Restore data
    tar -xzf "${BACKUP_FILE}"
    log_success "Backup restored successfully"
    
    echo "🔄 Restart services with: ./package.sh up"
}

cmd_clean() {
    log_info "Cleaning up AI Box..."
    cd "${APP_DIR}"
    
    # Stop services
    docker-compose down
    
    # Remove containers and images
    docker-compose down --rmi all --volumes --remove-orphans
    
    # Clean up data (WARNING: this will delete all data)
    if [[ "${1:-}" == "data" ]]; then
        log_warning "Removing all data directories..."
        rm -rf db/
        rm -rf rag_data/
        log_success "Data directories removed"
    fi
    
    log_success "Cleanup completed"
}

cmd_help() {
    echo "AI Box Package Manager - Version ${VERSION}"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  up                    Start AI Box services"
    echo "  down                  Stop AI Box services"
    echo "  restart               Restart AI Box services"
    echo "  logs [follow]         View service logs (add 'follow' for real-time)"
    echo "  status                Check service status and health"
    echo "  bundle                Create distributable package"
    echo "  backup                Create backup of data"
    echo "  restore <file>        Restore from backup file"
    echo "  clean [data]          Clean up containers (add 'data' to remove data)"
    echo "  help                  Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 up                 # Start services"
    echo "  $0 logs follow        # Follow logs in real-time"
    echo "  $0 bundle             # Create deployment package"
    echo "  $0 backup             # Create data backup"
    echo "  $0 restore backup.tar.gz  # Restore from backup"
    echo ""
}

# Main command dispatcher
case "${1:-help}" in
    up)         cmd_up ;;
    down)       cmd_down ;;
    restart)    cmd_restart ;;
    logs)       cmd_logs "${2:-}" ;;
    status)     cmd_status ;;
    bundle)     cmd_bundle ;;
    backup)     cmd_backup ;;
    restore)    cmd_restore "${2:-}" ;;
    clean)      cmd_clean "${2:-}" ;;
    help)       cmd_help ;;
    *)          log_error "Unknown command: $1"; cmd_help; exit 1 ;;
esac 