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

### Demo Image Naming Convention
All demo images use the `demo-` prefix and are pushed to Docker Hub under the `linksrobot` account:

- `linksrobot/demo-whis-data-input:latest`
- `linksrobot/demo-whis-sanitize:latest`
- `linksrobot/demo-whis-logic:latest`
- `linksrobot/demo-ficknury-evaluator:latest`
- `linksrobot/demo-mlops-platform:latest`
- `linksrobot/demo-frontend:latest`

### Tagging and Pushing Images
Use the provided script to tag and push demo images:

```bash
# Tag images (dry run)
./tag-and-push-demo-images.sh

# Tag and push to Docker Hub
./tag-and-push-demo-images.sh push
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

### GitHub Actions
The demo platform includes automated CI/CD workflows:

- **Build and Push**: `/.github/workflows/demo-build.yml`
  - Builds demo images on push to main/demo branches
  - Pushes to Docker Hub with demo- prefix
  - Updates Helm values with registry information

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
