FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy unified API code
COPY . .

# Create necessary directories (will be mounted as volumes)
RUN mkdir -p /app/ml-models /app/pipeline /app/rag /tmp /app/logs /app/data

# Set environment variables
ENV PYTHONPATH=/app:/app/ml-models:/app/pipeline:/app/rag
ENV ENVIRONMENT=demo

# Expose port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:9000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"] 