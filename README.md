# DEMO-LinkOps - Simplified MLOps Platform

A streamlined demo version of the LinkOps MLOps platform, focusing on core services with simplified deployment.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Kubernetes cluster (for Helm deployment)
- Docker Hub account (for image registry)

### Local Development
```bash
# Clone and setup
git clone <repository-url>
cd DEMO-LinkOps

# Copy environment template
cp env.template .env

# Start services
./start.sh
```

### Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🏗️ Architecture

### Core Services
- **whis-data-input** (Port 8001) - Data ingestion service
- **whis-sanitize** (Port 8002) - Data cleaning and validation
- **whis-logic** (Port 8003) - Business logic and AI processing
- **ficknury-evaluator** (Port 8004) - Evaluation and scoring
- **mlops-platform** (Port 8000) - Main API platform
- **frontend** (Port 3000) - Vue.js web interface

### Infrastructure
- **PostgreSQL** (Port 5432) - Primary database
- **Redis** (Port 6379) - Caching and sessions

## 🐳 Docker Images

### Auto-Versioning System
The DEMO-LinkOps platform uses an **auto-versioning system** that generates unique tags for each build using the format `YYYYMMDD-commit_hash` (e.g., `20250714-a1b2c3d`). This ensures:

- ✅ **No Stale Images** - Each deployment uses a specific, immutable version
- ✅ **Easy Rollbacks** - Quickly revert to any previous version
- ✅ **Build Traceability** - Link deployments to specific code commits
- ✅ **Parallel Deployments** - Multiple environments can run different versions

### Demo Image Naming Convention
All demo images use the `demo-` prefix and are pushed to Docker Hub under the `linksrobot` account:

- `linksrobot/demo-whis-data-input:20250714-a1b2c3d`
- `linksrobot/demo-whis-sanitize:20250714-a1b2c3d`
- `linksrobot/demo-whis-logic:20250714-a1b2c3d`
- `linksrobot/demo-ficknury-evaluator:20250714-a1b2c3d`
- `linksrobot/demo-mlops-platform:20250714-a1b2c3d`
- `linksrobot/demo-frontend:20250714-a1b2c3d`

### Deployment Scripts
The platform includes automated deployment scripts in the `runes/` directory:

#### Automatic Deployment (Recommended)
```bash
# Deploy with latest versioned images
./runes/deploy-latest.sh
```

This script will:
- 🔍 Find the latest versioned images
- 📝 Update docker-compose.yml automatically
- 🚀 Pull and deploy the services
- 📊 Show deployment status

#### Manual Version Update
```bash
# Update to a specific version
./runes/update-compose-versions.sh 20250714-a1b2c3d

# Then deploy
docker-compose pull
docker-compose up -d
```

#### Manual Deployment
```bash
# Pull latest images
docker-compose pull

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

**Note:** Make sure you're logged in to Docker Hub:
```bash
docker login -u linksrobot
```

## ☸️ Helm Deployment

### Prerequisites
- Kubernetes cluster
- Helm 3.x
- ArgoCD (optional, for GitOps)

### Deploy with Helm
```bash
# Navigate to helm directory
cd helm

# Build dependencies
cd demo-stack
helm dependency build

# Install the demo stack
helm install demo-stack . --namespace demo-linkops --create-namespace

# Upgrade existing deployment
helm upgrade demo-stack . --namespace demo-linkops
```

### Helm Chart Structure
```
helm/
├── demo-stack/           # Umbrella chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
├── whis-data-input/      # Individual service charts
├── whis-sanitize/
├── whis-logic/
└── frontend/
```

### Kubernetes Metadata Compliance
All Helm templates use DNS-1123 compliant names with dashes instead of underscores:
- ✅ `whis-data-input` (correct)
- ❌ `whis-data-input` (incorrect)

## 🔧 Configuration

### Environment Variables
Copy `env.template` to `.env` and configure:
```bash
# Database
POSTGRES_PASSWORD=your_secure_password

# Demo Mode Configuration
DEMO_MODE=true  # Set to false to enable real AI capabilities

# AI Model Configuration (Optional)
# Uncomment and set one of the following to enable real AI capabilities:
# GROK_API_KEY=your_grok_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Helm Values
Customize deployment in `helm/demo-stack/values.yaml`:
```yaml
# Example: Scale services
whis-logic:
  replicaCount: 2
  resources:
    limits:
      cpu: 2000m
      memory: 2Gi
```

## 🚀 CI/CD

### GitHub Actions Auto-Versioning
The demo platform includes an automated CI/CD workflow that builds and versions images on every push to the main branch:

#### Workflow Features
- **Auto-Versioning**: Generates `YYYYMMDD-commit_hash` tags (e.g., `20250714-a1b2c3d`)
- **Multi-Service Build**: Builds all 6 demo services in parallel
- **Docker Hub Push**: Automatically pushes versioned images to `linksrobot/demo-*`
- **Version Tracking**: Creates a `VERSION` file with deployment information
- **Security Scanning**: Includes Trivy and GitGuardian security scans

#### Workflow Steps
1. **Code Quality Checks**: Linting, formatting, and security scans
2. **Version Generation**: Creates unique version tag from commit SHA and date
3. **Docker Builds**: Builds all services with the generated version tag
4. **Image Push**: Pushes versioned images to Docker Hub
5. **Version Tracking**: Commits version information for deployment tracking

#### Example Version Output
```
✅ Successfully built and pushed:
  - linksrobot/demo-frontend:20250714-a1b2c3d
  - linksrobot/demo-mlops-platform:20250714-a1b2c3d
  - linksrobot/demo-whis-data-input:20250714-a1b2c3d
  - linksrobot/demo-whis-sanitize:20250714-a1b2c3d
  - linksrobot/demo-whis-logic:20250714-a1b2c3d
  - linksrobot/demo-ficknury-evaluator:20250714-a1b2c3d
```

### ArgoCD Integration
For GitOps deployment, use the provided ArgoCD Application manifest:
```bash
kubectl apply -f helm/argocd/Application.yaml
```

## 📊 Monitoring

### Health Checks
All services include health check endpoints:
- `GET /health` - Service health status
- `GET /ready` - Readiness probe

### Logging
Services use structured logging with configurable levels:
```bash
# Set log level
LOG_LEVEL=DEBUG
```

## 🔒 Security

### Secrets Management
- Grok API key stored as Kubernetes secret
- Database credentials managed via environment variables
- Docker registry authentication via secrets

### Network Security
- Services communicate via internal network
- External access through ingress controllers
- Database and Redis not exposed externally

## 🤖 Demo Mode

### What is Demo Mode?
The DEMO-LinkOps platform runs in **demo mode** by default, which provides a complete simulation of the platform's capabilities without requiring real AI API keys.

### Demo Mode Features
- ✅ **Full UI Experience** - All interfaces work as expected
- ✅ **Simulated AI Responses** - Realistic AI-generated content without API calls
- ✅ **Complete Workflow** - End-to-end task processing simulation
- ✅ **No API Costs** - Zero external API usage or costs
- ✅ **Safe for Demos** - No risk of exposing real API keys

### Enabling Real AI Capabilities
To enable real AI model integration:

#### Option 1: Interactive Configuration Script (Recommended)
```bash
# Run the interactive configuration script
./configure-ai-mode.sh
```

#### Option 2: Manual Configuration
1. **Set Demo Mode to False**
   ```bash
   DEMO_MODE=false
   ```

2. **Add Your API Key** (choose one):
   ```bash
   # For Grok (xAI)
   GROK_API_KEY=your_grok_api_key_here
   
   # For OpenAI (ChatGPT/GPT-4)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # For Anthropic (Claude)
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

3. **Restart the Platform**
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

### Supported AI Models
- **Grok (xAI)** - Advanced reasoning and task analysis
- **OpenAI (ChatGPT/GPT-4)** - Natural language processing and generation
- **Anthropic (Claude)** - Safe and helpful AI assistance

### Demo Mode Indicators
The platform clearly indicates when running in demo mode:
- ⚠️ **Yellow warning banners** in the UI
- **"Demo Mode Active"** messages in responses
- **Disabled API key inputs** (visual only)
- **Simulated AI responses** with clear labeling

### Checking Demo Status
Use the status check script to verify your configuration:
```bash
./check-demo-status.sh
```

This script will show:
- Current demo mode status
- API key configuration
- Service health status
- Recommendations for your setup

## 🧪 Testing

### Integration Testing
```bash
# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8001/health
```

## 📝 Development

### Adding New Services
1. Create service directory in `mlops/`
2. Add Dockerfile and requirements
3. Create Helm chart in `helm/`
4. Update umbrella chart dependencies
5. Add to docker-compose.yml

### Code Style
- Python: Black, flake8
- JavaScript/Vue: Prettier, ESLint
- YAML: yamllint with 4-space indentation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper formatting
4. Test locally
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the logs: `docker-compose logs [service]`
- Verify configuration: `helm template . --debug`
- Review health endpoints: `curl http://localhost:[port]/health`
