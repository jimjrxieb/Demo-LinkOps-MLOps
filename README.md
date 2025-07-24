# LinkOps - Secure AI Platform for Top-Secret Organizations

## 🎯 Overview

**LinkOps** is a secure, air-gapped AI GUI platform designed for top-secret organizations like ZRS. This platform provides comprehensive AI capabilities including document memory, tool execution, model training, and agent creation - all within a secure, isolated environment.

---

## 🏗️ Architecture

### Core Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Unified API** | Single FastAPI backend for all services | FastAPI, Python 3.11 |
| **Frontend** | Modern Vue.js GUI with real-time updates | Vue 3, Tailwind CSS |
| **RAG System** | Vector memory and document search | ChromaDB, Sentence Transformers |
| **ML Models** | Agent and model generation | LangChain, Jinja2 Templates |
| **Pipeline** | ML training and data processing | Custom Python pipeline |
| **HTC** | Feedback collection and prompt training | Custom feedback system |
| **MCP Tools** | Tool creation and execution system | Custom executor with security |

---

## 📁 Optimized Directory Structure

```
DEMO-LinkOps/
├── unified-api/                 # 🚀 Single FastAPI backend
│   ├── routers/                # All API endpoints
│   │   ├── agent_builder.py    # AI agent creation
│   │   ├── agent_creator.py    # Agent templates
│   │   ├── executor.py         # MCP tool execution
│   │   ├── htc.py             # Document memory system
│   │   ├── mcp_tool.py        # Tool creation/management
│   │   ├── ml_builder.py      # ML model building
│   │   ├── model_creator.py   # Model generation
│   │   ├── pipeline.py        # Training pipeline
│   │   ├── rag.py             # RAG search endpoints
│   │   ├── status.py          # System status
│   │   ├── tenant_sync.py     # Multi-tenant sync
│   │   └── train_model.py     # Model training
│   ├── logic/                 # Business logic
│   │   └── executor.py        # Tool execution engine
│   └── main.py               # FastAPI application
├── frontend/                  # 🎨 Vue.js GUI
│   ├── src/
│   │   ├── views/            # Page components
│   │   ├── components/       # Reusable components
│   │   ├── store/           # State management
│   │   └── router/          # Navigation
│   └── dist/                # Build output
├── rag/                      # 🧠 Vector memory system
│   ├── config/              # Configuration files
│   ├── uploads/             # Document storage
│   ├── chroma_db/           # Vector database
│   ├── llm_weights/         # Model weights
│   ├── logic/               # RAG business logic
│   ├── tests/               # Test files
│   └── routes/              # RAG-specific endpoints
├── ml-models/               # 🤖 AI model generation
│   ├── agent-creator/       # Agent templates
│   ├── model-creator/       # Model templates
│   ├── api/                 # Model APIs
│   └── templates/           # Jinja2 templates
├── pipeline/                # ⚙️ ML training pipeline
│   ├── data-intake/         # Data ingestion
│   ├── data-sanitize/       # Data cleaning
│   ├── embedder/           # Embedding generation
│   └── trainer/            # Model training
├── htc/                     # 📝 Feedback system
│   ├── routes/             # Feedback endpoints
│   └── feedback_collector.py
├── db/                      # 💾 Data storage
│   ├── mcp_tools/          # Saved MCP tools
│   └── execution_logs/     # Tool execution history
├── docker/                  # 🐳 Containerization
│   ├── docker-compose.yml
│   ├── docker-compose.demo.yml
│   └── docker-compose.override.yml
├── docs/                    # 📚 Documentation
│   ├── architecture/       # System architecture
│   ├── deployment/         # Deployment guides
│   ├── services/           # Service documentation
│   └── archive/            # Historical docs
├── sample_data/            # 📊 Sample datasets
└── scripts/                # 🔧 Utility scripts
```

---

## 🚀 Key Features

### 🔒 **Security-First Design**
- **Air-gapped deployment** - No external internet access
- **Command validation** - Prevents dangerous operations
- **Secure execution** - Isolated tool execution environment
- **Multi-tenant isolation** - Separate data per organization

### 🧠 **AI Capabilities**
- **Document Memory** - Vector-based document storage and retrieval
- **Tool Execution** - Secure MCP tool creation and execution
- **Agent Creation** - AI agent generation with templates
- **Model Training** - Offline ML model training pipeline
- **RAG Search** - Retrieval-augmented generation

### 🎨 **User Interface**
- **Modern GUI** - Vue.js with Tailwind CSS
- **Real-time updates** - Live execution feedback
- **Responsive design** - Works on desktop and mobile
- **Dark theme** - Professional appearance

---

## 🛠️ Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 20+

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd DEMO-LinkOps

# Start the platform
docker-compose up -d

# Access the application
open http://localhost:8080
```

### Production Deployment
```bash
# Deploy with authentication
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Deploy demo version
docker-compose -f docker-compose.demo.yml up -d
```

---

## 🔧 API Endpoints

### Core Services
- `GET /` - Platform status and information
- `GET /health` - Health check for all services
- `GET /docs` - Interactive API documentation

### MCP Tool System
- `POST /mcp-tool/mcp-tool` - Create new tool
- `GET /mcp-tool/mcp-tool/list` - List all tools
- `POST /executor/execute-tool` - Execute custom command
- `POST /executor/execute-saved-tool/{name}` - Execute saved tool

### RAG System
- `POST /rag/upload` - Upload documents
- `POST /rag/search` - Search documents
- `GET /rag/status` - RAG system status

### AI Services
- `POST /agent-creator/create` - Create AI agent
- `POST /model-creator/generate` - Generate ML model
- `POST /pipeline/train` - Train ML model

---

## 📊 Monitoring & Logging

### Execution History
- All tool executions are logged to `db/execution_logs/`
- Success/failure rates tracked
- Performance metrics available

### System Status
- Real-time health monitoring
- Service status dashboard
- Error tracking and reporting

---

## 🔮 Roadmap

### Phase 1: Core Platform ✅
- [x] Unified API backend
- [x] Vue.js frontend
- [x] MCP tool system
- [x] RAG document memory
- [x] Basic security features

### Phase 2: Advanced Features 🚧
- [ ] SQLite logging system
- [ ] Automated tool scheduling
- [ ] Advanced agent capabilities
- [ ] Multi-model support

### Phase 3: Enterprise Features 📋
- [ ] Advanced authentication
- [ ] Audit logging
- [ ] Backup and recovery
- [ ] Performance optimization

---

## 🤝 Contributing

This platform is designed for secure, air-gapped environments. All contributions must follow security best practices:

1. **Security review** - All code changes require security review
2. **Testing** - Comprehensive testing required
3. **Documentation** - Update documentation for all changes
4. **Validation** - Command validation and sanitization

---

## 📄 License

This project is proprietary and confidential. Unauthorized distribution is prohibited.

---

## 🆘 Support

For support and questions:
- **Documentation**: Check `/docs/` directory
- **Issues**: Review existing issues and create new ones
- **Security**: Report security issues immediately

---

**🎯 Mission**: Providing secure, powerful AI capabilities for top-secret organizations while maintaining the highest standards of security and reliability.
