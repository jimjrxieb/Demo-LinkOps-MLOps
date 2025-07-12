# 🚀 LinkOps MLOps Platform - Demo Version

A simplified demo version of the LinkOps MLOps platform focused on the core task processing workflow.

## 🎯 **Demo Workflow**

This demo version allows users to:

1. **Input a task** - Submit a task description through the James GUI
2. **Query Orb library** - Search existing best practices (Orbs)
3. **Match found** → Display the matching Orb
4. **No match** → Use Whis with Grok API to generate a new Orb
5. **Approval** → Save approved Orbs to the demo library
6. **Rejection** → Show "refinement not available in demo" message

## 🏗️ **Simplified Architecture**

### **Core Services (6 instead of 18)**
- **Frontend** (Port 3000) - James GUI with task input and Orb display
- **MLOps Platform** (Port 8000) - Main API orchestration
- **Whis Data Input** (Port 8001) - Task input processing
- **Whis Sanitize** (Port 8002) - Task cleaning and preparation
- **Whis Logic** (Port 8005) - Orb library matching logic
- **Ficknury Evaluator** (Port 8011) - Basic matching and evaluation
- **PostgreSQL** (Port 5432) - Database for Orbs and tasks
- **Redis** (Port 6379) - Caching and sessions

### **Removed Components**
- ❌ All shadow agents except Ficknury Evaluator
- ❌ Whis Enhance, Whis Smithing, Whis Webscraper
- ❌ Audit services and complex security scanning
- ❌ Kafka, Zookeeper, and message queuing
- ❌ Complex retry logic and background processors
- ❌ Runes generation and autonomous execution
- ❌ Agent enhancement and training loops

## 🚀 **Quick Start**

### Option 1: Docker Compose (Local Development)

```bash
# Clone and setup
cd DEMO-LinkOps

# Start the demo platform
docker-compose up -d

# Access the platform
# Frontend: http://localhost:3000
# API: http://localhost:8000
```

### Option 2: Kubernetes with Helm (Production Ready)

```bash
# Prerequisites: Kubernetes cluster, Helm 3.x, kubectl
cd DEMO-LinkOps

# Deploy with Helm
./deploy-helm.sh

# Access the platform
# Frontend: http://demo.linkops.local (add to /etc/hosts)
# API: Available via port-forward or ingress
```

For detailed Helm deployment instructions, see [helm/README.md](helm/README.md).

## 🎨 **Demo Features**

### **James GUI Tab**
- **Task Input Field** - Submit task descriptions
- **Orb Results** - Display matching or generated Orbs
- **Approval Interface** - Accept or reject generated Orbs
- **Demo Limitations** - Clear messaging about demo constraints

### **Simplified API Endpoints**
- `/api/task/submit` - Submit new tasks
- `/api/orbs/search` - Search existing Orbs
- `/api/orbs/generate` - Generate new Orbs with Whis
- `/api/orbs/approve` - Approve and save Orbs
- `/api/orbs/reject` - Handle rejections

## 🛠️ **Technology Stack**

- **Backend**: Python FastAPI (simplified)
- **Frontend**: Vue 3 with James GUI focus
- **Database**: PostgreSQL (Orbs storage)
- **Cache**: Redis (session management)
- **AI**: Grok API integration for Orb generation

## 📁 **Project Structure**

```
DEMO-LinkOps/
├── frontend/                    # Vue 3 frontend (James GUI)
├── mlops/
│   ├── mlops_platform/         # Main API orchestration
│   ├── whis_data_input/        # Task input processing
│   ├── whis_sanitize/          # Task cleaning
│   └── whis_logic/             # Orb matching logic
├── shadows/
│   └── ficknury_evaluator/     # Basic evaluation
├── docker-compose.yml          # Simplified orchestration
├── env.template                # Environment variables
└── README.md                   # This file
```

## 🎯 **Demo Limitations**

- **No Refinement Loop**: Rejected Orbs show demo limitation message
- **No Agent Execution**: No autonomous task execution
- **No Complex Pipelines**: Simplified processing workflow
- **No Training**: No model training or enhancement
- **No Runes**: No script generation or execution

## 🔄 **Workflow Example**

1. User submits: "How do I deploy a Kubernetes application?"
2. System searches existing Orbs for matches
3. If match found → Display existing Orb
4. If no match → Whis generates new Orb using Grok API
5. User reviews generated Orb
6. If approved → Save to demo Orbs library
7. If rejected → Show "refinement not available in demo"

This demo version maintains the core concept while removing complexity for demonstration purposes.
