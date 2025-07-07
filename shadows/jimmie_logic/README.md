# Jimmie Logic - Unified Control Brain

Jimmie Logic is the centralized control brain for the LinkOps MLOps platform, consolidating all logic, orbs, runes, and models in one location.

## 🧠 Overview

Jimmie Logic serves as the unified interface for:
- **Task Management**: MLOps tasks, audit flows, infrastructure work
- **Script Management**: CLI workflows and infrastructure scripts
- **Orb Management**: Best practices and workflow templates
- **Rune Management**: Reusable solutions and code templates
- **Daily Logs**: Daily work logs and digests
- **Model Management**: AI models and ML artifacts

## 📁 Structure

```
jimmie_logic/
├── main.py                     # FastAPI application
├── routers/                    # API route handlers
│   ├── task_router.py         # Task management
│   ├── script_router.py       # Script management
│   ├── orb_router.py          # Orb management
│   ├── rune_router.py         # Rune management
│   ├── daily_router.py        # Daily logs
│   └── model_router.py        # Model management
├── logic/
│   └── storage.py             # JSON storage helper
├── data/                      # Data storage (auto-created)
│   ├── tasks.json            # Task data
│   ├── scripts.json          # Script data
│   ├── orbs.json             # Orb data
│   ├── runes.json            # Rune data
│   ├── daily_logs.json       # Daily log data
│   ├── models.json           # Model data
│   └── history.csv           # Activity history
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Local Development
```bash
cd shadows/jimmie_logic
pip install -r requirements.txt
uvicorn main:app --reload
```

### Docker
```bash
docker build -t jimmie_logic .
docker run -p 8000:8000 jimmie_logic
```

## 📊 API Endpoints

### Tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/` - Get all tasks (with filters)
- `GET /api/tasks/{task_id}` - Get specific task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `GET /api/tasks/stats/summary` - Task statistics

### Scripts
- `POST /api/scripts/` - Create a new script
- `GET /api/scripts/` - Get all scripts (with filters)
- `GET /api/scripts/{script_id}` - Get specific script
- `PUT /api/scripts/{script_id}` - Update script
- `DELETE /api/scripts/{script_id}` - Delete script
- `POST /api/scripts/{script_id}/execute` - Execute script
- `GET /api/scripts/templates/{category}` - Get script templates

### Orbs
- `POST /api/orbs/` - Create a new orb
- `GET /api/orbs/` - Get all orbs (with filters)
- `GET /api/orbs/{orb_id}` - Get specific orb
- `PUT /api/orbs/{orb_id}` - Update orb
- `DELETE /api/orbs/{orb_id}` - Delete orb
- `POST /api/orbs/{orb_id}/use` - Mark orb as used
- `POST /api/orbs/{orb_id}/rate` - Rate orb
- `GET /api/orbs/templates/{category}` - Get orb templates

### Runes
- `POST /api/runes/` - Create a new rune
- `GET /api/runes/` - Get all runes (with filters)
- `GET /api/runes/{rune_id}` - Get specific rune
- `PUT /api/runes/{rune_id}` - Update rune
- `DELETE /api/runes/{rune_id}` - Delete rune
- `POST /api/runes/{rune_id}/execute` - Execute rune
- `POST /api/runes/{rune_id}/feedback` - Provide feedback
- `GET /api/runes/templates/{category}` - Get rune templates

### Daily Logs
- `POST /api/daily/` - Create a new daily log
- `GET /api/daily/` - Get all daily logs (with filters)
- `GET /api/daily/{log_id}` - Get specific log
- `PUT /api/daily/{log_id}` - Update log
- `DELETE /api/daily/{log_id}` - Delete log
- `GET /api/daily/today/summary` - Today's summary
- `GET /api/daily/stats/weekly` - Weekly statistics
- `GET /api/daily/stats/monthly` - Monthly statistics

### Models
- `POST /api/models/` - Create a new model
- `GET /api/models/` - Get all models (with filters)
- `GET /api/models/{model_id}` - Get specific model
- `PUT /api/models/{model_id}` - Update model
- `DELETE /api/models/{model_id}` - Delete model
- `POST /api/models/{model_id}/predict` - Make prediction
- `POST /api/models/{model_id}/evaluate` - Evaluate model
- `GET /api/models/templates/{category}` - Get model templates

### General
- `GET /` - Root endpoint with service info
- `GET /health` - Health check with data statistics
- `GET /api/stats` - Comprehensive statistics
- `POST /api/classify` - Classify input content

## 🔄 Data Flow

```
User Input → Jimmie Logic → Classification → Storage → Whis Training
     ↓              ↓              ↓           ↓           ↓
  Tasks/        Centralized    MLOps/K8s/   JSON Files   History
Solutions       Processing     Infra/Audit              CSV Export
```

## 📈 Usage Examples

### Create a Task
```bash
curl -X POST "http://localhost:8000/api/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement GitOps pipeline",
    "description": "Set up ArgoCD for automated deployments",
    "category": "kubernetes",
    "priority": "high",
    "tags": ["gitops", "argocd", "deployment"]
  }'
```

### Create a Script
```bash
curl -X POST "http://localhost:8000/api/scripts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "deploy_to_k8s",
    "description": "Deploy application to Kubernetes",
    "category": "kubernetes",
    "content": "kubectl apply -f k8s/",
    "language": "bash",
    "tags": ["kubernetes", "deployment"]
  }'
```

### Create an Orb
```bash
curl -X POST "http://localhost:8000/api/orbs/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Security Scan",
    "description": "Automated security scanning",
    "category": "ci_cd",
    "content": "name: Security Scan\nversion: 1.0.0\n...",
    "tags": ["security", "ci_cd"]
  }'
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL` - Database connection string (optional)
- `LOG_LEVEL` - Logging level (default: INFO)
- `DATA_DIR` - Data directory path (default: ./data)

### Data Backup
```python
from logic.storage import storage

# Create backup
storage.backup_data("backups/")

# Restore from backup
storage.restore_data("backups/jimmie_logic_backup_20231201_120000/")
```

## 🔗 Integration

### With Whis Pipeline
Jimmie Logic feeds data to the Whis training pipeline:
- Task completions → Training data
- Script usage → Pattern recognition
- Orb ratings → Best practice refinement
- Rune feedback → Solution improvement

### With Shadow Agents
Other agents can query Jimmie Logic for:
- **Igris**: Infrastructure scripts and orbs
- **Katie**: Kubernetes runes and templates
- **AuditGuard**: Security orbs and compliance scripts
- **Ficknury**: Task evaluation and routing

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Statistics
```bash
curl http://localhost:8000/api/stats
```

## 🚀 Deployment

### Docker Compose
Add to your docker-compose.yml:
```yaml
jimmie_logic:
  build: ./shadows/jimmie_logic
  ports:
    - "8008:8000"
  volumes:
    - ./shadows/jimmie_logic/data:/app/data
  environment:
    - DATABASE_URL=postgresql://linkops:password@db:5432/linkops
```

### Kubernetes
Use the provided Helm chart in `helm/jimmie_logic/`.

## 🔮 Future Enhancements

- **Real-time Collaboration**: WebSocket support for live updates
- **Advanced Analytics**: ML-powered insights and recommendations
- **Integration APIs**: Connect with external tools (Jira, GitHub, etc.)
- **Mobile App**: React Native app for mobile access
- **Voice Interface**: Voice commands and responses
- **AI Assistant**: Built-in AI for task suggestions and automation

---

**Jimmie Logic** - One Logic to Rule Them All! 🧠⚡ 