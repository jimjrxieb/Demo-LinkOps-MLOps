# LinkOps MLOps Platform

This directory contains the **Whis** AI training and data processing pipeline, plus comprehensive **audit and migration** services for the LinkOps MLOps platform.

## 🎯 Purpose

This platform allows engineers to capture, refine, and automate everything they want to learn and execute across DevOps, MLOps, GitOps, and platform engineering domains.

## 🔍 Audit & Migration Services

### Audit Assess (`audit_assess`)
- **Input**: Public GitHub repository URL
- **Output**:
  - Security vulnerabilities (Trivy, Snyk, Semgrep)
  - Secrets detection (GitGuardian patterns)
  - Microservice structure report
  - GitOps compliance score (0-100)
  - Comprehensive security analysis

### Audit Migrate (`audit_migrate`)
- **Input**: Audit report from `audit_assess`
- **Output**:
  - Helm chart scaffolding
  - Dockerfile patch suggestions
  - GitOps directory layout
  - ArgoCD-ready templates

## 🧠 Whis Pipeline Overview

## 🧠 Whis Pipeline Overview

Whis is the learning brain of LinkOps, continuously improving through human feedback and automated processing.

### Pipeline Flow

```
Human Input → Data Input → Sanitize → Smith → Enhance → Inject
     ↓           ↓           ↓         ↓        ↓         ↓
  Tasks/    whis_data_   whis_    whis_   whis_   Agent
Solutions   input       sanitize  smith   enhance Logic
```

## 📁 Directory Structure

```
mlops/
├── audit_assess/        # Repository scanning and GitOps assessment
│   ├── logic/          # Security scanner, GitOps scanner, analyzer
│   └── routers/        # API endpoints for scanning
├── audit_migrate/       # GitOps migration and scaffolding
│   ├── logic/          # Migration planners and generators
│   └── orbs/           # Migration templates
├── whis_data_input/     # Receives human task/solution pairs
├── whis_sanitize/       # Cleans and formats raw data
├── whis_smithing/       # Creates Orbs (workflows) and Runes (code)
├── whis_enhance/        # Optimizes and improves Orbs/Runes
├── whis_logic/          # Serves Orbs/Runes to agents
│   ├── orbs/           # Generated workflow templates
│   └── runes/          # Generated code templates
├── whis_webscraper/     # Collects external data
└── mlops_utils/         # Shared utilities
```

## 🔄 Pipeline Stages

### 1. Data Input (`whis_data_input`)
- **Purpose**: Receives high-confidence task/solution pairs from human engineers
- **Input**: JSON with task description and solution
- **Output**: Validated training data
- **Port**: 8001

### 2. Sanitize (`whis_sanitize`)
- **Purpose**: Cleans and standardizes raw input data
- **Input**: Raw task/solution data
- **Output**: Structured, categorized training data
- **Port**: 8002

### 3. Smith (`whis_smithing`)
- **Purpose**: Transforms sanitized data into reusable Orbs and Runes
- **Input**: Sanitized training data
- **Output**: 
  - **Orbs**: YAML workflow templates (e.g., `orb.gha.security.v1.yaml`)
  - **Runes**: Python code templates (e.g., `rune.gha.pipeline.v1.py`)
- **Port**: 8011

### 4. Enhance (`whis_enhance`)
- **Purpose**: Optimizes and improves generated Orbs/Runes
- **Input**: Raw Orbs and Runes
- **Output**: Enhanced, production-ready templates
- **Port**: 8012

### 5. Logic (`whis_logic`)
- **Purpose**: Serves Orbs and Runes to downstream agents
- **Input**: Enhanced Orbs/Runes
- **Output**: API endpoints for agent consumption
- **Port**: 8013

## 🚀 Usage

### Submit a Repository for Auditing

```bash
# Using curl
curl -X POST http://localhost:8003/scan/audit \
  --json '{"repo_url": "https://github.com/xyz/project"}'

# Using the frontend
# Paste your repo URL and click "Audit"
```

### Run Full Assessment + Migration

```bash
# Start audit services
docker-compose up audit_assess audit_migrate

# Or run individual services
docker-compose run audit_assess
docker-compose run audit_migrate
```

### Daytime Mode (Training)
```bash
docker-compose -f docker-compose.daytime.yml up --build
```

### Nighttime Mode (Processing)
```bash
docker-compose -f docker-compose.nighttime.yml up --build
```

### Manual Workflow
1. Submit training data to `whis_data_input`:
   ```json
   {
     "task": "Convert repo to GitOps",
     "answer": "Add helm chart, ArgoCD app, update CI pipeline"
   }
   ```

2. Data flows through the pipeline automatically
3. Check `whis_logic/orbs/` and `whis_logic/runes/` for generated templates

## 🧪 Testing

Each service has its own test suite:
```bash
# Test individual services
cd mlops/whis_data_input && python -m pytest tests/
cd mlops/whis_sanitize && python -m pytest tests/
# ... etc

# Test full pipeline
python scripts/test_complete_pipeline.py
```

## 📊 Monitoring

- Health checks: `GET /health` on each service
- Metrics: Prometheus endpoints available
- Logs: Structured logging with correlation IDs

## 🔧 Development

### Adding a New Service
1. Create directory in `mlops/`
2. Add `main.py`, `Dockerfile`, `README.md`
3. Update docker-compose files
4. Add Helm chart in `helm/`
5. Add tests in `tests/`

### Modifying the Pipeline
1. Update service logic
2. Test with sample data
3. Validate with integration tests
4. Deploy with Helm

## 🎯 Integration with Agents

The Whis pipeline feeds into the shadow agents in `../shadows/`:
- **Igris**: Platform engineering logic
- **Katie**: Kubernetes and cluster management
- **Auditguard**: Security and compliance
- **Ficknury**: Task evaluation and routing

## 📈 Continuous Learning

Whis learns from:
- Human engineer feedback
- Successful deployments
- Failed attempts
- External data sources
- Agent performance metrics

This creates a continuously improving MLOps platform that gets smarter with every interaction. 