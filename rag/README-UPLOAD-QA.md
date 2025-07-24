# Drag-and-Drop Upload & Local RAG Q&A

This document describes the new drag-and-drop upload functionality and local RAG Q&A system implemented in the DEMO-LinkOps project.

## 🚀 Features

### 1. Drag-and-Drop File Upload
- **DropZone Component**: Modern, responsive drag-and-drop interface
- **File Validation**: Supports PDF, TXT, CSV, DOCX files (max 10MB)
- **Progress Tracking**: Real-time upload progress with visual feedback
- **Error Handling**: Comprehensive error messages and validation
- **Auto-indexing**: Uploaded files are automatically processed and added to the vector store

### 2. Local RAG Q&A System
- **SearchMemory View**: Complete Q&A interface with document search
- **Local LLM Integration**: Multiple backend support (llama-cpp, Ollama, Transformers)
- **Context-Aware Answers**: Generates answers based on retrieved document chunks
- **Source Attribution**: Shows which documents were used to generate answers
- **Recent Queries**: Keeps track of recent questions for quick access

## 📁 File Structure

```
frontend/src/
├── components/
│   └── DropZone.vue              # Drag-and-drop upload component
└── views/
    └── SearchMemory.vue          # Q&A interface

rag/
├── logic/
│   ├── llm_runner.py            # Local LLM inference engine
│   ├── search.py                # RAG search engine (existing)
│   └── embed.py                 # Document embedding (existing)
├── config/
│   └── llm_config.yaml          # LLM configuration
├── main.py                      # FastAPI service with upload/query endpoints
└── requirements.txt             # Updated dependencies
```

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
# RAG service dependencies
cd rag
pip install -r requirements.txt

# Frontend dependencies
cd ../frontend
npm install
```

### 2. Download LLM Model (Optional)

For local LLM inference, download a model:

```bash
# Option 1: Download Mistral GGUF model
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf -O rag/llm_weights/mistral.gguf

# Option 2: Use Ollama
ollama pull mistral
```

### 3. Start Services

```bash
# Start RAG service
cd rag
python main.py

# Start frontend (in another terminal)
cd frontend
npm run dev
```

## 🎯 Usage

### Upload Documents

1. Navigate to `/search-memory` in the frontend
2. Drag and drop files into the upload area or click "Browse Files"
3. Files are automatically processed and indexed
4. View upload progress and status messages

### Ask Questions

1. Type your question in the query input
2. Click "Ask" or press Enter
3. View the generated answer with source attribution
4. Browse recent queries in the sidebar

## 🔌 API Endpoints

### Upload
- `POST /api/upload` - Upload and index a document file

### Query
- `POST /api/query-simple` - Simple Q&A with local LLM
- `POST /api/query-llm` - Advanced LLM integration
- `GET /api/documents` - List indexed documents
- `GET /api/stats` - System statistics

## ⚙️ Configuration

### LLM Backend Selection

Edit `rag/config/llm_config.yaml`:

```yaml
default_backend: "llama-cpp"  # or "ollama", "transformers", "fallback"
```

### Model Parameters

```yaml
generation:
  max_tokens: 512
  temperature: 0.7
  top_p: 0.9
```

## 🛠️ Customization

### Adding New File Types

1. Update `allowed_extensions` in `rag/main.py`
2. Add text extraction logic in `rag/logic/embed.py`
3. Update frontend file validation in `DropZone.vue`

### Custom LLM Backend

1. Implement backend methods in `LLMRunner` class
2. Add configuration in `llm_config.yaml`
3. Update initialization logic

### UI Customization

- Modify `DropZone.vue` for upload interface changes
- Update `SearchMemory.vue` for Q&A interface changes
- Customize styling in component `<style>` sections

## 🔍 Troubleshooting

### Common Issues

1. **Upload fails**: Check file size and type restrictions
2. **LLM not working**: Verify model files and dependencies
3. **Slow responses**: Consider using smaller models or GPU acceleration
4. **Memory issues**: Reduce `max_tokens` or use fallback mode

### Debug Mode

Enable debug logging in the RAG service:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Performance Tips

1. **Use GPU acceleration** for LLM inference
2. **Optimize chunk sizes** for better retrieval
3. **Use smaller models** for faster responses
4. **Enable caching** for repeated queries

## 📊 Monitoring

- Check `/api/stats` for system metrics
- Monitor upload directory size
- Track query response times
- Review error logs for issues

## 🔒 Security Considerations

- File upload validation prevents malicious files
- Local processing keeps data private
- No external API calls for LLM inference
- Configurable file size limits

## 🎉 Next Steps

1. Add support for more document types
2. Implement document versioning
3. Add collaborative features
4. Integrate with external knowledge bases
5. Add advanced query capabilities 