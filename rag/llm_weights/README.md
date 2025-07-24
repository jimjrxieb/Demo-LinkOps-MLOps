# Local LLM Setup Instructions

## 🧠 Download Mistral Model for VM

### Option 1: Full Quality Model (4.1GB)
```bash
# Download the Q4_K_M quantized model (recommended)
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf \
  -O mistral.gguf
```

### Option 2: Smaller Model (2.9GB)
```bash
# Download the Q2_K quantized model (faster, smaller)
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q2_K.gguf \
  -O mistral.gguf
```

### Option 3: Tiny Model (1.1GB) - For Testing
```bash
# Download the Q2_K quantized model (fastest, smallest)
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q2_K.gguf \
  -O mistral.gguf
```

## 🔧 Model Configuration

The system is configured to use `mistral.gguf` by default. The model will be automatically loaded when the RAG service starts.

### Model Parameters
- **Temperature**: 0.1 (low for consistent answers)
- **Max Tokens**: 512 (reasonable response length)
- **Context Window**: 2048 tokens
- **GPU Layers**: 0 (CPU only, set to 1+ for GPU acceleration)

## 🚀 Usage

Once the model is downloaded:

1. **Start the RAG service**:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

2. **Test the LLM**:
   ```bash
   curl -X POST http://localhost:9000/rag/query-llm \
     -H "Content-Type: application/json" \
     -d '{"query": "What is Kubernetes?"}'
   ```

3. **Use the Web Interface**:
   - Go to `http://localhost:8080`
   - Click "RAG Search"
   - Upload documents
   - Click "🧠 Ask AI" for LLM-generated answers

## 🔍 Model Performance

- **Q4_K_M**: Best quality, slower inference
- **Q2_K**: Good quality, faster inference  
- **Q2_K**: Lower quality, fastest inference

## 🛠️ Troubleshooting

### Model Not Found
If you see "LLM model file not found", ensure:
- The model file is named `mistral.gguf`
- It's placed in the `rag/llm_weights/` directory
- The file has proper read permissions

### Memory Issues
If the model fails to load due to memory:
- Use a smaller quantization (Q2_K)
- Increase Docker memory limits
- Use GPU acceleration if available

### Slow Performance
- Consider using GPU acceleration
- Reduce context window size
- Use a smaller model for development

## 📊 System Requirements

### Minimum (CPU Only)
- **RAM**: 8GB+ (16GB recommended)
- **Storage**: 5GB+ for model
- **CPU**: 4+ cores

### Recommended (GPU)
- **RAM**: 16GB+
- **GPU**: 8GB+ VRAM
- **Storage**: 5GB+ for model

## 🔐 Security Benefits

✅ **100% Local**: No data sent to external APIs
✅ **No Internet Required**: Works completely offline
✅ **Data Privacy**: All processing happens locally
✅ **No Rate Limits**: Unlimited queries
✅ **No API Costs**: Free to use 