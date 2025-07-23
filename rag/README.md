# RAG Service

A secure, local retrieval-augmented generation (RAG) service that provides private Q&A over embedded documents with fully offline vector search capabilities.

## 🚀 Features

- **Private & Local**: All processing happens locally, no data sent to external services
- **Vector Search**: FAISS-based similarity search for fast document retrieval
- **Document Embedding**: Automatic text chunking and vector embedding
- **Multiple Formats**: Support for TXT, CSV, JSON, and other text formats
- **RESTful API**: Full FastAPI interface with comprehensive endpoints
- **Security**: Configurable similarity thresholds and access controls
- **Offline Operation**: Works completely offline with optional LLM fallback
- **Real-time Search**: Fast query processing with configurable result limits

## 📁 Structure

```
rag/
├── main.py                    # FastAPI entrypoint
├── requirements.txt           # Python dependencies
├── Dockerfile                # Docker configuration
├── README.md                 # This file
├── logic/
│   ├── __init__.py           # Package initialization
│   ├── search.py             # RAG search engine
│   └── embed.py              # Document embedding
├── schemas/
│   ├── __init__.py           # Package initialization
│   └── query_schema.py       # Pydantic models
├── test/
│   ├── __init__.py           # Package initialization
│   └── test_query.py         # Test suite
└── vectorstore/              # Vector store directory (auto-created)
    └── index.pkl             # FAISS index and documents
```

## 🛠️ Installation

### Local Development

```bash
# Navigate to RAG directory
cd DEMO-LinkOps/rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python main.py
```

### Docker

```bash
# Build the image
docker build -t rag-service .

# Run the container
docker run -p 8005:8005 rag-service
```

## 🔄 API Endpoints

### Health & Status

#### `GET /health`
Health check endpoint.
```bash
curl http://localhost:8005/health
```

#### `GET /stats/`
Get system statistics.
```bash
curl http://localhost:8005/stats/
```

### Document Management

#### `POST /embed/`
Embed a document into the vector store.
```bash
curl -X POST http://localhost:8005/embed/ \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/document.txt",
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "metadata": {
      "source": "documentation",
      "author": "team"
    }
  }'
```

#### `POST /embed-batch/`
Embed multiple documents in batch.
```bash
curl -X POST http://localhost:8005/embed-batch/ \
  -H "Content-Type: application/json" \
  -d '{
    "file_paths": ["/path/to/doc1.txt", "/path/to/doc2.txt"],
    "chunk_size": 1000,
    "chunk_overlap": 200
  }'
```

#### `GET /documents/`
List all documents in the vector store.
```bash
curl http://localhost:8005/documents/
```

#### `GET /documents/{doc_id}`
Get a specific document by ID.
```bash
curl http://localhost:8005/documents/doc_123
```

#### `DELETE /documents/{doc_id}`
Delete a document from the vector store.
```bash
curl -X DELETE http://localhost:8005/documents/doc_123
```

### Search & Query

#### `POST /query/`
Query the RAG system with a question.
```bash
curl -X POST http://localhost:8005/query/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the zero trust model?",
    "top_k": 5,
    "similarity_threshold": 0.7,
    "include_metadata": true
  }'
```

#### `GET /search/`
Simple search using query parameters.
```bash
curl "http://localhost:8005/search/?query=zero%20trust&top_k=3&similarity_threshold=0.5"
```

### System Management

#### `POST /reload/`
Reload the vector store index.
```bash
curl -X POST http://localhost:8005/reload/
```

#### `POST /clear/`
Clear all documents from the vector store.
```bash
curl -X POST http://localhost:8005/clear/
```

#### `GET /models/`
Get available embedding models.
```bash
curl http://localhost:8005/models/
```

## 📚 Usage Examples

### Python Client

```python
import requests

# Initialize client
RAG_BASE_URL = "http://localhost:8005"

# Embed a document
embed_response = requests.post(f"{RAG_BASE_URL}/embed/", json={
    "file_path": "/path/to/document.txt",
    "chunk_size": 1000,
    "chunk_overlap": 200
})

# Query the system
query_response = requests.post(f"{RAG_BASE_URL}/query/", json={
    "query": "What is machine learning?",
    "top_k": 3,
    "similarity_threshold": 0.6
})

results = query_response.json()
for result in results['results']:
    print(f"Score: {result['similarity_score']:.3f}")
    print(f"Content: {result['content']}")
```

### JavaScript/Node.js Client

```javascript
const axios = require('axios');

const RAG_BASE_URL = 'http://localhost:8005';

// Embed document
async function embedDocument(filePath) {
    const response = await axios.post(`${RAG_BASE_URL}/embed/`, {
        file_path: filePath,
        chunk_size: 1000,
        chunk_overlap: 200
    });
    return response.data;
}

// Query system
async function queryRAG(question) {
    const response = await axios.post(`${RAG_BASE_URL}/query/`, {
        query: question,
        top_k: 5,
        similarity_threshold: 0.6
    });
    return response.data;
}

// Usage
embedDocument('/path/to/document.txt')
    .then(() => queryRAG('What is zero trust?'))
    .then(results => console.log(results));
```

## 🎯 Supported Tasks

### Document Embedding
- **Input**: Text files (TXT, CSV, JSON, etc.)
- **Process**: Text chunking → Vector embedding → FAISS storage
- **Output**: Searchable vector representations
- **Use Cases**: Knowledge base creation, document indexing

### Semantic Search
- **Input**: Natural language queries
- **Process**: Query embedding → Vector similarity search → Result ranking
- **Output**: Ranked document chunks with similarity scores
- **Use Cases**: Q&A systems, document search, information retrieval

### Knowledge Management
- **Input**: Document collections
- **Process**: Batch embedding → Index management → Metadata tracking
- **Output**: Organized knowledge base
- **Use Cases**: Documentation search, research assistance

## 🔒 Security Features

### Data Privacy
- **Local Processing**: All embeddings and searches happen locally
- **No External Calls**: No data sent to external services
- **Secure Storage**: Vector store with access controls

### Access Control
- **Similarity Thresholds**: Configurable minimum similarity scores
- **Result Limits**: Configurable maximum result counts
- **Query Validation**: Input sanitization and validation

### Audit Trail
- **Query Logging**: Track all search queries and results
- **Embedding History**: Document embedding timestamps and metadata
- **System Monitoring**: Performance and usage statistics

## 🔧 Configuration

### Environment Variables
- `ENVIRONMENT`: Set to "demo" for demo mode
- `MODEL_NAME`: Embedding model to use (default: sentence-transformers/all-MiniLM-L6-v2)
- `CHUNK_SIZE`: Default text chunk size (default: 1000)
- `CHUNK_OVERLAP`: Default chunk overlap (default: 200)

### Embedding Models
The service supports various sentence transformer models:
- `sentence-transformers/all-MiniLM-L6-v2` (default, 384 dimensions)
- `sentence-transformers/all-mpnet-base-v2` (768 dimensions)
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (multilingual)

### Search Parameters
- **top_k**: Number of results to return (1-50)
- **similarity_threshold**: Minimum similarity score (0.0-1.0)
- **include_metadata**: Include document metadata in results

## 📊 Performance

### Benchmarks
- **Embedding Speed**: ~1000 chunks/second (depends on model)
- **Search Speed**: ~1ms per query (with FAISS index)
- **Memory Usage**: ~4MB per 1000 chunks (384-dimensional vectors)
- **Storage**: ~1.5MB per 1000 chunks (compressed FAISS index)

### Optimization Tips
- Use appropriate chunk sizes for your documents
- Set reasonable similarity thresholds
- Monitor vector store size and performance
- Use batch embedding for multiple documents

## 🧪 Testing

### Run Test Suite
```bash
# Run all tests
python test/test_query.py

# Test individual components
python -c "from logic.search import RAGSearchEngine; print('Search engine OK')"
python -c "from logic.embed import DocumentEmbedder; print('Embedder OK')"
```

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8005/health

# Test search with example
curl -X POST http://localhost:8005/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "top_k": 1}'
```

## 🔗 Service Integration

### Pipeline Integration
The RAG service integrates with the training pipeline:
- Receives embedded documents from the pipeline
- Provides search capabilities for the demo system
- Supports batch document processing

### Frontend Integration
The service provides RESTful APIs for frontend integration:
- Real-time search capabilities
- Document management interface
- System monitoring and statistics

### Docker Integration
The service is containerized and integrated into the Docker Compose stack:
- Port 8005 exposed for external access
- Volume mounts for persistent storage
- Health checks for monitoring

## 🚀 Deployment

### Docker Compose
The RAG service is integrated into the main Docker Compose stack:

```yaml
rag:
  build: ../rag
  ports:
    - "8005:8005"
  environment:
    - ENVIRONMENT=demo
  volumes:
    - ../rag:/app
    - ../rag/vectorstore:/app/vectorstore
  networks:
    - demo-network
```

### Production Deployment
- Use persistent volumes for vector store
- Configure proper security settings
- Set up monitoring and logging
- Implement backup strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Update tests if needed
5. Submit a pull request

## 📄 License

This project is part of the LinkOps platform. 