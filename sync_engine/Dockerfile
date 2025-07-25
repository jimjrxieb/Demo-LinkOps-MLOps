# Sync Engine Service Dockerfile
FROM python:3.11-slim

LABEL maintainer="LinkOps Team <team@linkops.com>"
LABEL description="DEMO-LinkOps Sync Engine - Data Synchronization Service"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install --no-cache-dir \
    fastapi \
    uvicorn \
    watchdog \
    chromadb \
    python-multipart \
    pydantic \
    requests \
    aiofiles

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p /app/db /app/watch /app/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Expose port (if needed)
EXPOSE 8004

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the sync engine
CMD ["python", "-m", "watcher"]