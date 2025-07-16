<template>
  <div class="demo-view">
    <!-- Demo Mode Banner removed -->
    
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="card">
        <div class="card-body">
          <h1 class="hero-title">
            LinkOps AI/ML Platform <span class="hero-highlight">DEMO</span>
          </h1>
          
          <p class="hero-description">
            This demo is a slimmed-down version of my personal Kubernetes AI/ML model under the LinkOps umbrella.
            Every Kubernetes-related Jira task I'm assigned — or errors I've encountered and solved using tools like ChatGPT and K8sGPT —
            gets entered into this system, where it is structured, learned from, and versioned.
            Over time, it becomes a reflection of my real-world experience, industry best practices, and troubleshooting patterns.
            The long-term goal is to reach a state where this system can autonomously complete any Kubernetes or CD-related task I receive.
          </p>
        </div>
      </div>
    </div>
    
    <!-- 1. Task Input -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">
          🎯 Submit a Kubernetes/CD Task or Error
        </h2>
        <p class="card-subtitle">
          Enter a Kubernetes task, goal, or error you've encountered — and see how LinkOps processes it through the AI/ML pipeline.
        </p>
      </div>
      <div class="card-body">
        <div class="form-group">
          <label class="form-label">Task Description</label>
          <textarea 
            v-model="taskInput" 
            class="form-input form-textarea"
            placeholder="e.g., create a pod named test with image nginx..."
            rows="4"
          />
        </div>
        
        <div class="form-actions">
          <button 
            :disabled="!taskInput.trim() || loading" 
            class="btn btn-primary"
            @click="submitTask"
          >
            <span
              v-if="loading"
              class="btn-icon"
            >⏳</span>
            <span
              v-else
              class="btn-icon"
            >🚀</span>
            {{ loading ? 'Processing...' : 'Submit Task' }}
          </button>
          
          <button 
            class="btn btn-secondary" 
            @click="clearResults"
          >
            <span class="btn-icon">🗑️</span>
            Clear
          </button>
        </div>
      </div>
    </div>

    <!-- 2. Orb Match Section -->
    <div
      v-if="taskInput && !loading && matchingOrb"
      class="results-section"
    >
      <OrbResultCard
        :orb="matchingOrb"
        :confidence="confidenceScore"
      />
    </div>

    <!-- 3. Whis Pipeline Side Panel -->
    <div
      v-if="taskInput && !loading"
      class="pipeline-section"
    >
      <WhisPipeline
        :pipeline-data="pipelineData"
        :current-step="currentStep"
        @approve-solution="approveSolution"
        @reject-solution="rejectSolution"
      />
    </div>

    <!-- 4. Full Orb Library Always Visible -->
    <div class="library-section">
      <OrbLibrary
        :orbs="orbLibrary"
        @retrain="retrainModel"
      />
    </div>

    <!-- 5. Demo Information -->
    <div class="card demo-info-card">
      <div class="card-header">
        <h2 class="card-title">
          ℹ️ About This Demo
        </h2>
      </div>
      <div class="card-body">
        <div class="info-grid">
          <div class="info-item">
            <h4>What You're Seeing</h4>
            <p>A fully functional demo of my personal Kubernetes AI/ML model that learns from real-world tasks and errors.</p>
          </div>
          
          <div class="info-item">
            <h4>Try These Tasks</h4>
            <ul>
              <li>"create a pod named test with image nginx"</li>
              <li>"set up CD pipeline with GitHub Actions"</li>
              <li>"scan container images for vulnerabilities"</li>
              <li>"configure Kubernetes secrets management"</li>
            </ul>
          </div>
          
          <div class="info-item">
            <h4>Demo Features</h4>
            <ul>
              <li>AI-powered task matching and confidence scoring</li>
              <li>Real-time Whis pipeline visualization</li>
              <li>Professional Kubernetes/CD interface</li>
              <li>Learning from Jira tasks and K8sGPT solutions</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import WhisPipeline from '../components/WhisPipeline.vue'
import OrbLibrary from './OrbLibrary.vue'
import OrbResultCard from '../components/OrbResultCard.vue'

const taskInput = ref('')
const matchingOrb = ref(null)
const confidenceScore = ref(null)
const loading = ref(false)
const currentStep = ref(0)

// Whis Pipeline data with detailed tool descriptions
const pipelineData = ref([
  {
    id: 1,
    name: 'whis_data_input',
    description: 'Collects inputs from task bar, Q&A, image OCR, and transcript tools',
    icon: '📥',
    tools: 'FastAPI, JSON Schema, CLI agent intake'
  },
  {
    id: 2,
    name: 'whis_sanitize',
    description: 'Cleans and validates input data, removes sensitive information, generates TensorFlow embeddings',
    icon: '🧹',
    tools: 'Data validation, PII detection, format standardization, TensorFlow USE embeddings'
  },
  {
    id: 3,
    name: 'whis_logic',
    description: 'Processes task through AI models, generates execution plans',
    icon: '🧠',
    tools: 'LLM integration, task analysis, plan generation'
  },
  {
    id: 4,
    name: 'whis_mlops_platform',
    description: 'Orchestrates execution, manages workflows and monitoring',
    icon: '⚙️',
    tools: 'Workflow engine, monitoring, logging, metrics'
  },
  {
    id: 5,
    name: 'whis_execution',
    description: 'Executes tasks, deploys resources, manages infrastructure',
    icon: '🚀',
    tools: 'Kubernetes API, Helm charts, Terraform, CI/CD tools'
  }
])

// Pre-seeded Orb Library data
const orbLibrary = ref([
  {
    title: "ML Task Classifier",
    category: "AI/ML Engineer",
    orb: "Predicts the category of engineering tasks using a trained TensorFlow model. Used in whis_smithing to reduce LLM reliance.",
    keywords: ["classification", "ai", "tensorflow", "tokenizer"],
    type: "training",
    version: "v1",
    confidence: 0.92,
    last_trained: "2025-07-15 14:00 UTC"
  },
  {
    title: "TensorFlow USE Embeddings",
    category: "AI/ML Engineer",
    orb: "Generates Universal Sentence Encoder embeddings for task text using TensorFlow. Used in whis_sanitize for semantic similarity.",
    keywords: ["embeddings", "tensorflow", "use", "semantic", "similarity"],
    type: "training",
    version: "v4",
    confidence: 0.95,
    last_trained: "2025-07-15 14:00 UTC"
  },
  {
    title: "Kubernetes Pod Creation - Production Ready",
    category: "Kubernetes",
    orb: "Complete solution for creating production-ready Kubernetes pods with proper resource limits, health checks, and security contexts.",
    keywords: ["kubernetes", "pod", "production", "security", "resources"],
    rune_id: "R-112",
    confidence: 0.85,
    declarative_template: `# nginx-pod.yaml - Production Ready Pod
apiVersion: v1
kind: Pod
metadata:
  name: nginx-prod
  labels:
    app: nginx
    environment: production
    tier: frontend
  annotations:
    kubernetes.io/created-by: "LinkOps Platform"
spec:
  serviceAccountName: nginx-sa
  securityContext:
    runAsNonRoot: true
    runAsUser: 101
    fsGroup: 101
  containers:
  - name: nginx
    image: nginx:1.25-alpine
    ports:
    - containerPort: 8080
      name: http
    resources:
      requests:
        memory: "64Mi"
        cpu: "100m"
      limits:
        memory: "128Mi"
        cpu: "200m"
    livenessProbe:
      httpGet:
        path: /
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: nginx-config
      mountPath: /etc/nginx/conf.d
      readOnly: true
    - name: tmp-volume
      mountPath: /tmp
    - name: var-cache-nginx
      mountPath: /var/cache/nginx
    - name: var-run
      mountPath: /var/run
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config
  - name: tmp-volume
    emptyDir: {}
  - name: var-cache-nginx
    emptyDir: {}
  - name: var-run
    emptyDir: {}
  restartPolicy: Always
  nodeSelector:
    kubernetes.io/os: linux`,
    imperative_commands: [
      "# Create namespace for the pod",
      "kubectl create namespace nginx-demo",
      "",
      "# Create service account",
      "kubectl create serviceaccount nginx-sa -n nginx-demo",
      "",
      "# Create ConfigMap for nginx configuration",
      "kubectl create configmap nginx-config --from-literal=default.conf='server { listen 8080; location / { root /usr/share/nginx/html; index index.html; } }' -n nginx-demo",
      "",
      "# Apply the pod manifest",
      "kubectl apply -f nginx-pod.yaml -n nginx-demo",
      "",
      "# Monitor pod creation",
      "kubectl get pods nginx-prod -n nginx-demo -w",
      "",
      "# Check pod details and logs",
      "kubectl describe pod nginx-prod -n nginx-demo",
      "kubectl logs nginx-prod -n nginx-demo",
      "",
      "# Port forward to test locally",
      "kubectl port-forward nginx-prod 8080:8080 -n nginx-demo",
      "",
      "# Create a service to expose the pod",
      "kubectl expose pod nginx-prod --port=80 --target-port=8080 --name=nginx-service -n nginx-demo",
      "",
      "# Clean up resources",
      "kubectl delete pod nginx-prod -n nginx-demo",
      "kubectl delete service nginx-service -n nginx-demo",
      "kubectl delete configmap nginx-config -n nginx-demo",
      "kubectl delete serviceaccount nginx-sa -n nginx-demo",
      "kubectl delete namespace nginx-demo"
    ]
  },
  {
    title: "Helm Chart Best Practices",
    category: "CI/CD",
    orb: "Structuring Helm charts for scalable and secure Kubernetes deployments.",
    keywords: ["helm", "charts", "templates"],
    rune_id: "R-103",
    confidence: 0.93,
    declarative_template: `# Chart.yaml
apiVersion: v2
name: myapp
description: A Helm chart for Kubernetes
version: 0.1.0
appVersion: "1.16.0"

# values.yaml
replicaCount: 1
image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: ""
service:
  type: ClusterIP
  port: 80`,
    imperative_commands: [
      "helm create myapp",
      "helm lint myapp/",
      "helm install myapp ./myapp",
      "helm upgrade myapp ./myapp",
      "helm uninstall myapp"
    ]
  },
  {
    title: "CI/CD Pipeline Linting",
    category: "CI/CD",
    orb: "Lint your GitHub Actions or GitLab pipelines for security and efficiency.",
    keywords: ["ci", "github", "yaml"]
  },
  {
    title: "Container Security Scanning Pipeline",
    category: "Security",
    orb: "Complete container security scanning solution with Trivy, integrated CI/CD pipeline, and vulnerability remediation workflow.",
    keywords: ["trivy", "container", "vulnerability", "security", "cicd", "scanning"],
    rune_id: "R-102",
    confidence: 0.94,
    declarative_template: `# .github/workflows/container-security.yml
name: Container Security Pipeline
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: \${{ github.repository }}

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
      
    - name: Log into registry
      uses: docker/login-action@v3
      with:
        registry: \${{ env.REGISTRY }}
        username: \${{ github.actor }}
        password: \${{ secrets.GITHUB_TOKEN }}
        
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: \${{ env.REGISTRY }}/\${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
          
    - name: Build container image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: false
        tags: \${{ steps.meta.outputs.tags }}
        labels: \${{ steps.meta.outputs.labels }}
        load: true
        cache-from: type=gha
        cache-to: type=gha,mode=max
        
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: \${{ steps.meta.outputs.tags }}
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH,MEDIUM'
        
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v3
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
        
    - name: Run Trivy vulnerability scanner (table format)
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: \${{ steps.meta.outputs.tags }}
        format: 'table'
        output: 'trivy-results.txt'
        
    - name: Check for critical vulnerabilities
      run: |
        if grep -q "CRITICAL" trivy-results.txt; then
          echo "❌ Critical vulnerabilities found! Review and fix before deploying."
          cat trivy-results.txt
          exit 1
        else
          echo "✅ No critical vulnerabilities found."
        fi
        
    - name: Push image if security scan passes
      if: success() && github.event_name != 'pull_request'
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: \${{ steps.meta.outputs.tags }}
        labels: \${{ steps.meta.outputs.labels }}
        
  policy-check:
    runs-on: ubuntu-latest
    needs: security-scan
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Run OPA Conftest for Dockerfile policies
      uses: instrumenta/conftest-action@master
      with:
        files: Dockerfile
        policy: security-policies/docker-policy.rego
        
# security-policies/docker-policy.rego
package docker.security

# Deny running as root
deny[msg] {
  input[i].Cmd == "user"
  val := input[i].Value
  val[0] == "root"
  msg := "Image should not run as root user"
}

# Require specific base images
deny[msg] {
  input[i].Cmd == "from"
  val := input[i].Value
  not startswith(val[0], "alpine:")
  not startswith(val[0], "ubuntu:")
  not startswith(val[0], "distroless/")
  msg := "Base image should be alpine, ubuntu, or distroless"
}

# Deny privileged mode
deny[msg] {
  input[i].Cmd == "run"
  contains(input[i].Value[0], "--privileged")
  msg := "Privileged mode is not allowed"
}`,
    imperative_commands: [
      "# Install Trivy locally",
      "sudo apt-get update && sudo apt-get install wget apt-transport-https gnupg lsb-release",
      "wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -",
      "echo \"deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main\" | sudo tee -a /etc/apt/sources.list.d/trivy.list",
      "sudo apt-get update && sudo apt-get install trivy",
      "",
      "# Scan local Docker image",
      "trivy image nginx:latest",
      "",
      "# Scan with severity filter",
      "trivy image --severity HIGH,CRITICAL nginx:latest",
      "",
      "# Scan filesystem for vulnerabilities",
      "trivy fs --security-checks vuln,config .",
      "",
      "# Generate detailed JSON report",
      "trivy image --format json --output results.json nginx:latest",
      "",
      "# Scan specific image layers",
      "trivy image --format table --output scan-report.txt myapp:latest",
      "",
      "# Continuous scanning with exit codes",
      "trivy image --exit-code 1 --severity CRITICAL nginx:latest",
      "",
      "# Scan container registry",
      "trivy image registry.example.com/myapp:latest",
      "",
      "# Scan with custom policies",
      "trivy config --policy ./policies .",
      "",
      "# Generate SARIF for GitHub integration",
      "trivy image --format sarif --output trivy-results.sarif nginx:latest",
      "",
      "# Scan Kubernetes manifests",
      "trivy config ./k8s-manifests/",
      "",
      "# Database update",
      "trivy image --download-db-only",
      "",
      "# Offline scanning",
      "trivy image --offline-scan nginx:latest"
    ]
  },
  {
    title: "ArgoCD Installation & GitOps Setup Guide",
    category: "GitOps",
    orb: "Complete step-by-step checklist for installing ArgoCD and setting up GitOps workflow to deploy applications to Kubernetes.",
    keywords: ["gitops", "argocd", "installation", "deployment", "kubernetes"],
    rune_id: "R-201",
    confidence: 0.96,
    best_practice_checklist: [
      "📋 **PREREQUISITES**",
      "□ Kubernetes cluster running (minikube, kind, or cloud cluster)",
      "□ kubectl configured and connected to cluster",
      "□ Helm 3.x installed",
      "□ Git repository with Kubernetes manifests prepared",
      "",
      "🔧 **STEP 1: Install ArgoCD**",
      "□ Create argocd namespace: `kubectl create namespace argocd`",
      "□ Install ArgoCD: `kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`",
      "□ Wait for pods to be ready: `kubectl wait --for=condition=ready pod --all -n argocd --timeout=300s`",
      "□ Verify installation: `kubectl get pods -n argocd`",
      "",
      "🔐 **STEP 2: Access ArgoCD UI**",
      "□ Get initial admin password: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath=\"{.data.password}\" | base64 -d`",
      "□ Port forward to UI: `kubectl port-forward svc/argocd-server -n argocd 8080:443`",
      "□ Access UI at https://localhost:8080",
      "□ Login with username: admin, password: (from step above)",
      "",
      "⚙️ **STEP 3: Configure Git Repository**",
      "□ Prepare Git repo with application manifests in proper structure:",
      "   ```",
      "   my-app-repo/",
      "   ├── environments/",
      "   │   ├── dev/",
      "   │   │   └── kustomization.yaml",
      "   │   └── prod/",
      "   │       └── kustomization.yaml",
      "   ├── base/",
      "   │   ├── deployment.yaml",
      "   │   ├── service.yaml",
      "   │   └── kustomization.yaml",
      "   └── README.md",
      "   ```",
      "□ Ensure manifests are valid: `kubectl apply --dry-run=client -f ./base/`",
      "□ Push changes to Git repository",
      "",
      "🚀 **STEP 4: Create ArgoCD Application**",
      "□ Create application YAML manifest:",
      "   ```yaml",
      "   apiVersion: argoproj.io/v1alpha1",
      "   kind: Application",
      "   metadata:",
      "     name: my-app",
      "     namespace: argocd",
      "   spec:",
      "     project: default",
      "     source:",
      "       repoURL: https://github.com/YOUR_ORG/YOUR_REPO",
      "       targetRevision: HEAD",
      "       path: environments/dev",
      "     destination:",
      "       server: https://kubernetes.default.svc",
      "       namespace: my-app",
      "     syncPolicy:",
      "       automated:",
      "         prune: true",
      "         selfHeal: true",
      "   ```",
      "□ Apply application: `kubectl apply -f my-app-application.yaml`",
      "□ Create target namespace: `kubectl create namespace my-app`",
      "",
      "🔄 **STEP 5: Verify GitOps Workflow**",
      "□ Check application status: `argocd app get my-app`",
      "□ Sync if needed: `argocd app sync my-app`",
      "□ Verify deployment: `kubectl get all -n my-app`",
      "□ Test change workflow:",
      "  - Make change in Git repo",
      "  - Commit and push changes",
      "  - Verify ArgoCD detects and syncs changes",
      "",
      "🔒 **STEP 6: Security & Production Setup**",
      "□ Change default admin password: `argocd account update-password`",
      "□ Set up RBAC: Configure `argocd-rbac-cm` ConfigMap",
      "□ Configure SSO (optional): Set up OIDC/SAML integration",
      "□ Set up TLS certificates for production",
      "□ Configure repository credentials securely",
      "□ Set up monitoring and alerts for sync failures",
      "",
      "✅ **VERIFICATION CHECKLIST**",
      "□ ArgoCD UI accessible and functional",
      "□ Application shows 'Synced' and 'Healthy' status",
      "□ Git changes trigger automatic syncs",
      "□ Rollback functionality tested",
      "□ Monitoring and alerting configured",
      "□ Team has access and training completed"
    ],
    imperative_commands: [
      "# Quick Installation Script",
      "kubectl create namespace argocd",
      "kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml",
      "",
      "# Get admin password",
      "kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath=\"{.data.password}\" | base64 -d; echo",
      "",
      "# Port forward to access UI",
      "kubectl port-forward svc/argocd-server -n argocd 8080:443",
      "",
      "# Install ArgoCD CLI (Linux)",
      "curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64",
      "sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd",
      "",
      "# Login via CLI",
      "argocd login localhost:8080",
      "",
      "# Create application via CLI",
      "argocd app create my-app --repo https://github.com/YOUR_ORG/YOUR_REPO --path environments/dev --dest-server https://kubernetes.default.svc --dest-namespace my-app"
    ]
  },
  {
    title: "Secrets Management with Kubernetes",
    category: "Security",
    orb: "Use Sealed Secrets or HashiCorp Vault for secure Kubernetes secret management.",
    keywords: ["secret", "kubernetes", "sealed-secrets", "vault"]
  },
  {
    title: "Shift Left Security",
    category: "Security",
    orb: "Integrate Snyk, Bandit, and Checkov into CI pipeline for early security checks.",
    keywords: ["shift", "left", "security", "snyk", "bandit"]
  },
  {
    title: "Terraform Code Quality",
    category: "Infrastructure",
    orb: "Use `tflint`, `tfsec`, and `checkov` to audit infrastructure as code.",
    keywords: ["terraform", "tfsec", "lint", "infrastructure"]
  },
  {
    title: "Kubernetes Pod Security",
    category: "Kubernetes",
    orb: "Apply Pod Security Standards (restricted, baseline, privileged) via PSA admission controller.",
    keywords: ["pod", "security", "psa", "policy", "kubernetes"]
  },
  {
    title: "How would you set up a CI/CD pipeline?",
    category: "Interview Guide",
    orb: "Comprehensive interview-style explanation of CI/CD pipeline design, components, and best practices.",
    keywords: ["interview", "cicd", "pipeline", "explain", "how", "setup"],
    rune_id: "R-301",
    confidence: 0.95,
    interview_style: true,
    best_practice_checklist: [
      "🎯 **UNDERSTANDING THE REQUIREMENTS**",
      "□ **What is CI/CD?**",
      "  - Continuous Integration: Automated building and testing of code changes",
      "  - Continuous Deployment: Automated deployment to production environments",
      "  - Goal: Reduce manual errors, increase deployment frequency, faster feedback",
      "",
      "□ **Key Components to Consider:**",
      "  - Source control (Git repositories)",
      "  - Build automation (compile, package)",
      "  - Testing automation (unit, integration, security)",
      "  - Deployment automation (staging, production)",
      "  - Monitoring and rollback capabilities",
      "",
      "🏗️ **PIPELINE DESIGN APPROACH**",
      "□ **1. Source Control Strategy**",
      "  - Git branching strategy (GitFlow, GitHub Flow, or trunk-based)",
      "  - Feature branches for development",
      "  - Main/master branch for production-ready code",
      "  - Pull request reviews and approval process",
      "",
      "□ **2. Build Stage Architecture**",
      "  - Triggered on code push or pull request",
      "  - Compile code and resolve dependencies",
      "  - Build Docker images with proper tagging",
      "  - Store artifacts in registry (Docker Hub, ECR, ACR)",
      "",
      "□ **3. Testing Strategy**",
      "  - **Unit Tests**: Fast, isolated component testing",
      "  - **Integration Tests**: Service-to-service communication",
      "  - **Security Tests**: SAST/DAST scanning with tools like Snyk, SonarQube",
      "  - **Performance Tests**: Load testing with tools like k6 or JMeter",
      "  - **Infrastructure Tests**: Validate Terraform/CloudFormation",
      "",
      "🚀 **DEPLOYMENT STRATEGIES**",
      "□ **Environment Progression**",
      "  - **Development**: Continuous deployment from feature branches",
      "  - **Staging**: Mirror production environment for final testing",
      "  - **Production**: Controlled deployment with approval gates",
      "",
      "□ **Deployment Patterns**",
      "  - **Blue-Green**: Zero-downtime deployment with full environment swap",
      "  - **Rolling Updates**: Gradual replacement of instances",
      "  - **Canary Releases**: Deploy to small subset, gradually increase traffic",
      "  - **Feature Flags**: Runtime control of feature visibility",
      "",
      "🔧 **TOOL SELECTION & IMPLEMENTATION**",
      "□ **Platform Choices**",
      "  - **GitHub Actions**: Native Git integration, good for GitHub repos",
      "  - **GitLab CI/CD**: Built-in, comprehensive DevOps platform",
      "  - **Jenkins**: Highly customizable, plugin ecosystem",
      "  - **Azure DevOps**: Microsoft ecosystem integration",
      "  - **CircleCI/Travis**: Cloud-hosted, easy setup",
      "",
      "□ **Infrastructure as Code**",
      "  - Use Terraform/CloudFormation for infrastructure",
      "  - Kubernetes manifests or Helm charts for application deployment",
      "  - Environment configuration via environment variables or config maps",
      "",
      "🔒 **SECURITY & COMPLIANCE**",
      "□ **Security Integration**",
      "  - Secrets management (HashiCorp Vault, AWS Secrets Manager)",
      "  - Container scanning (Trivy, Clair, Aqua)",
      "  - Code quality gates (SonarQube, CodeClimate)",
      "  - Dependency vulnerability scanning",
      "",
      "□ **Compliance & Governance**",
      "  - Audit trails for all deployments",
      "  - Role-based access control (RBAC)",
      "  - Environment isolation and access controls",
      "  - Compliance reporting and documentation",
      "",
      "📊 **MONITORING & OBSERVABILITY**",
      "□ **Pipeline Monitoring**",
      "  - Build success/failure rates and trends",
      "  - Deployment frequency and lead times",
      "  - Mean time to recovery (MTTR) metrics",
      "  - Pipeline performance optimization",
      "",
      "□ **Application Monitoring**",
      "  - APM tools (New Relic, Datadog, AppDynamics)",
      "  - Log aggregation (ELK stack, Splunk)",
      "  - Infrastructure monitoring (Prometheus, Grafana)",
      "  - Alerting and incident response automation",
      "",
      "🎯 **INTERVIEW TALKING POINTS**",
      "□ **Demonstrate Understanding**",
      "  - 'I would start by understanding the current development workflow and pain points'",
      "  - 'Consider the team size, deployment frequency, and compliance requirements'",
      "  - 'Choose tools that integrate well with existing infrastructure'",
      "",
      "□ **Show Best Practices Knowledge**",
      "  - 'Implement pipeline as code for version control and reproducibility'",
      "  - 'Start with simple pipeline, then iterate and improve'",
      "  - 'Focus on fast feedback loops and developer experience'",
      "  - 'Plan for failure - rollback strategies and incident response'",
      "",
      "✅ **SUCCESS CRITERIA**",
      "□ Reduced manual deployment errors",
      "□ Faster time from code to production",
      "□ Consistent environments across dev/staging/prod",
      "□ Improved code quality through automated testing",
      "□ Better visibility into deployment process",
      "□ Team confidence in deploying frequently"
    ]
  },
  {
    title: "Explain Kubernetes architecture and components",
    category: "Interview Guide", 
    orb: "In-depth explanation of Kubernetes architecture, master/worker nodes, and core components for technical interviews.",
    keywords: ["interview", "kubernetes", "architecture", "explain", "components", "master", "worker"],
    rune_id: "R-302",
    confidence: 0.98,
    interview_style: true,
    best_practice_checklist: [
      "🏗️ **KUBERNETES ARCHITECTURE OVERVIEW**",
      "□ **What is Kubernetes?**",
      "  - Container orchestration platform",
      "  - Automates deployment, scaling, and management of containerized applications", 
      "  - Provides declarative configuration and self-healing capabilities",
      "  - Originally developed by Google, now maintained by CNCF",
      "",
      "□ **High-Level Architecture**",
      "  - **Master Node(s)**: Control plane components that manage the cluster",
      "  - **Worker Nodes**: Run application workloads in pods",
      "  - **etcd**: Distributed key-value store for cluster state",
      "  - **Networking**: Pod-to-pod and service-to-service communication",
      "",
      "🎛️ **CONTROL PLANE COMPONENTS (Master Node)**",
      "□ **API Server (kube-apiserver)**",
      "  - Central management entity and entry point for all REST commands",
      "  - Validates and configures data for pods, services, replication controllers",
      "  - Serves as frontend to the cluster's shared state",
      "  - Handles authentication, authorization, and admission control",
      "",
      "□ **etcd**", 
      "  - Consistent and highly-available key-value store",
      "  - Stores all cluster configuration data and state",
      "  - Backing store for all cluster data",
      "  - Can run on master node or separate dedicated machines",
      "",
      "□ **Controller Manager (kube-controller-manager)**",
      "  - Runs controller processes that regulate cluster state",
      "  - **Node Controller**: Monitors node health and responds to failures",
      "  - **Replication Controller**: Maintains correct number of pods",
      "  - **Endpoints Controller**: Populates service endpoints",
      "  - **Service Account & Token Controllers**: Handle API access tokens",
      "",
      "□ **Scheduler (kube-scheduler)**",
      "  - Assigns pods to nodes based on resource requirements",
      "  - Considers factors like resource availability, constraints, affinity rules",
      "  - Makes scheduling decisions but doesn't run the pods itself",
      "  - Can be customized with scheduling policies and priorities",
      "",
      "⚙️ **WORKER NODE COMPONENTS**",
      "□ **Kubelet**",
      "  - Primary node agent that runs on each worker node",
      "  - Communicates with API server to receive pod specifications",
      "  - Ensures containers are running and healthy via PodSpecs",
      "  - Reports node and pod status back to control plane",
      "  - Manages pod lifecycle and container runtime",
      "",
      "□ **Container Runtime**",
      "  - Software responsible for running containers",
      "  - **Docker**: Most common, but being deprecated",
      "  - **containerd**: Docker's underlying runtime, becoming standard",
      "  - **CRI-O**: Lightweight alternative designed for Kubernetes",
      "  - **rkt**: CoreOS container runtime (less common)",
      "",
      "□ **Kube-proxy**",
      "  - Network proxy running on each node",
      "  - Maintains network rules for pod communication",
      "  - Implements Services abstraction via iptables or IPVS",
      "  - Handles load balancing for service traffic",
      "",
      "🌐 **NETWORKING ARCHITECTURE**",
      "□ **Pod Networking**",
      "  - Each pod gets its own IP address",
      "  - Containers within pod share network namespace",
      "  - Pod-to-pod communication without NAT",
      "  - Implemented via CNI (Container Network Interface) plugins",
      "",
      "□ **CNI Plugins**",
      "  - **Flannel**: Simple overlay network",
      "  - **Calico**: Network policy and security features",
      "  - **Weave**: Easy setup with encryption",
      "  - **Cilium**: eBPF-based networking and security",
      "",
      "□ **Services & Ingress**",
      "  - **ClusterIP**: Internal cluster communication",
      "  - **NodePort**: Exposes service on each node's IP",
      "  - **LoadBalancer**: Cloud provider integration",
      "  - **Ingress**: HTTP/HTTPS routing and SSL termination",
      "",
      "💾 **STORAGE ARCHITECTURE**",
      "□ **Volume Types**",
      "  - **emptyDir**: Temporary storage tied to pod lifecycle",
      "  - **hostPath**: Mount host filesystem into pod",
      "  - **PersistentVolume (PV)**: Cluster-level storage resource",
      "  - **PersistentVolumeClaim (PVC)**: Request for storage by pod",
      "",
      "□ **Storage Classes**",
      "  - Define different types of storage (SSD, HDD, NFS)",
      "  - Enable dynamic provisioning of persistent volumes",
      "  - Provider-specific implementations (AWS EBS, GCE PD, Azure Disk)",
      "",
      "🎯 **INTERVIEW EXPLANATION STRATEGY**",
      "□ **Start with Big Picture**",
      "  - 'Kubernetes follows a master-worker architecture'",
      "  - 'Control plane manages cluster state, workers run applications'",
      "  - 'Everything is API-driven and declarative'",
      "",
      "□ **Dive into Components**",
      "  - Explain each component's role and interactions",
      "  - Emphasize the distributed, resilient nature",
      "  - Mention how components can be scaled and made highly available",
      "",
      "□ **Real-World Context**",
      "  - 'In production, you typically have multiple master nodes for HA'",
      "  - 'Worker nodes can be scaled based on workload demands'",
      "  - 'Networking and storage choices depend on requirements'",
      "",
      "✅ **KEY INTERVIEW POINTS**",
      "□ Understanding of distributed systems concepts",
      "□ Knowledge of container orchestration challenges",
      "□ Familiarity with cloud-native architecture patterns",
      "□ Awareness of production considerations (HA, scaling, monitoring)",
      "□ Understanding of security and network isolation concepts"
    ]
  },
  {
    title: "What is the difference between Docker and Kubernetes?",
    category: "Interview Guide",
    orb: "Clear comparison between Docker and Kubernetes, addressing common interview confusion about containerization vs orchestration.",
    keywords: ["interview", "docker", "kubernetes", "difference", "what", "comparison", "containers"],
    rune_id: "R-303",
    confidence: 0.96,
    interview_style: true,
    best_practice_checklist: [
      "🔍 **FUNDAMENTAL DIFFERENCE**",
      "□ **Docker: Containerization Platform**",
      "  - Packages applications and dependencies into containers",
      "  - Provides container runtime and image management",
      "  - Solves 'it works on my machine' problem",
      "  - Focus: Building, shipping, and running individual containers",
      "",
      "□ **Kubernetes: Container Orchestration Platform**",
      "  - Manages multiple containers across multiple hosts",
      "  - Automates deployment, scaling, and operations",
      "  - Solves distributed systems challenges",
      "  - Focus: Managing containerized applications at scale",
      "",
      "📦 **DOCKER CAPABILITIES**",
      "□ **Core Functions**",
      "  - **Build**: Create container images from Dockerfiles",
      "  - **Ship**: Push/pull images to/from registries",
      "  - **Run**: Execute containers on single host",
      "  - **Manage**: Basic container lifecycle management",
      "",
      "□ **What Docker Provides**",
      "  - Container runtime (containerd)",
      "  - Image format and registry",
      "  - Dockerfile for reproducible builds",
      "  - Docker Compose for multi-container applications",
      "  - Basic networking and volume management",
      "",
      "□ **Docker Limitations**",
      "  - Single host focused (Docker Swarm adds clustering)",
      "  - Limited high availability and failover",
      "  - Basic load balancing capabilities",
      "  - Manual scaling and health management",
      "  - No built-in service discovery at scale",
      "",
      "☸️ **KUBERNETES CAPABILITIES**",
      "□ **Orchestration Features**",
      "  - **Deployment**: Declarative application deployment",
      "  - **Scaling**: Horizontal and vertical scaling automation",
      "  - **Load Balancing**: Built-in service discovery and load balancing",
      "  - **Health Management**: Self-healing and rollback capabilities",
      "  - **Configuration**: ConfigMaps and Secrets management",
      "",
      "□ **Advanced Features**",
      "  - **Multi-host networking**: Pod-to-pod communication across nodes",
      "  - **Storage orchestration**: Persistent volume management",
      "  - **Resource management**: CPU/memory limits and requests",
      "  - **Security**: RBAC, network policies, pod security standards",
      "  - **Extensibility**: Custom resources and operators",
      "",
      "🤝 **HOW THEY WORK TOGETHER**",
      "□ **Complementary Relationship**",
      "  - Docker builds the containers",
      "  - Kubernetes orchestrates those containers",
      "  - Docker creates the 'packages' (images)",
      "  - Kubernetes manages the 'deployment' of those packages",
      "",
      "□ **Typical Workflow**",
      "  1. Developer writes Dockerfile",
      "  2. Docker builds container image",
      "  3. Image pushed to registry (Docker Hub, ECR, etc.)",
      "  4. Kubernetes pulls and runs images across cluster",
      "  5. Kubernetes manages lifecycle, scaling, networking",
      "",
      "📊 **COMPARISON TABLE**",
      "□ **Scope & Purpose**",
      "  - **Docker**: Single host containerization",
      "  - **Kubernetes**: Multi-host container orchestration",
      "",
      "□ **Learning Curve**",
      "  - **Docker**: Easier to start, simpler concepts",
      "  - **Kubernetes**: Steeper learning curve, complex architecture",
      "",
      "□ **Use Cases**",
      "  - **Docker**: Development, testing, simple deployments",
      "  - **Kubernetes**: Production-grade, enterprise applications",
      "",
      "□ **Networking**",
      "  - **Docker**: Bridge networks, basic port mapping",
      "  - **Kubernetes**: Advanced networking, service mesh integration",
      "",
      "□ **Storage**",
      "  - **Docker**: Volumes and bind mounts",
      "  - **Kubernetes**: Persistent volumes, storage classes, CSI",
      "",
      "🎯 **INTERVIEW RESPONSE STRATEGY**",
      "□ **Start with Core Difference**",
      "  - 'Docker is containerization, Kubernetes is orchestration'",
      "  - 'Docker packages applications, Kubernetes manages them at scale'",
      "  - 'They solve different problems but work together'",
      "",
      "□ **Use Analogies**",
      "  - 'Docker is like shipping containers, Kubernetes is like the port management system'",
      "  - 'Docker creates the standardized packages, Kubernetes is the logistics system'",
      "",
      "□ **Address Common Misconceptions**",
      "  - 'Kubernetes doesn't replace Docker, it uses container runtimes'",
      "  - 'Docker can run without Kubernetes, but Kubernetes needs container runtime'",
      "  - 'For small applications, Docker might be sufficient'",
      "  - 'For enterprise scale, you typically need both'",
      "",
      "🏢 **WHEN TO USE WHAT**",
      "□ **Use Docker When:**",
      "  - Single application deployment",
      "  - Development and testing environments",
      "  - Simple multi-container apps (Docker Compose)",
      "  - Learning containerization concepts",
      "",
      "□ **Use Kubernetes When:**",
      "  - Multiple applications/microservices",
      "  - High availability requirements",
      "  - Auto-scaling needs",
      "  - Production enterprise workloads",
      "  - Complex networking and storage requirements",
      "",
      "✅ **KEY TAKEAWAYS FOR INTERVIEW**",
      "□ They're complementary technologies, not competitors",
      "□ Docker = containerization, Kubernetes = orchestration",
      "□ Docker for packaging, Kubernetes for managing at scale",
      "□ Most production environments use both together",
      "□ Choice depends on scale and complexity requirements"
    ]
  }
])

const submitTask = async () => {
  loading.value = true
  currentStep.value = 0
  matchingOrb.value = null
  confidenceScore.value = null
  
  try {
    const task = taskInput.value.toLowerCase()
    
    // Step 1: Input Processing & Interview Detection
    currentStep.value = 0
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Detect interview-style questions
    const interviewPatterns = [
      /how would you/i,
      /explain/i,
      /what is/i,
      /what are/i,
      /describe/i,
      /tell me about/i,
      /walk me through/i,
      /difference between/i,
      /compare/i,
      /vs\.?/i,
      /versus/i
    ]
    
    const isInterviewQuestion = interviewPatterns.some(pattern => pattern.test(taskInput.value))
    
    // Step 2: Search Orb Library
    currentStep.value = 1
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Search through the orb library for matches
    let bestMatch = null
    let bestScore = 0
    
    for (const orb of orbLibrary.value) {
      let score = 0
      
      // Boost score for interview-style orbs when interview question detected
      if (isInterviewQuestion && orb.interview_style) {
        score += 50
      }
      
      // Check title match
      if (orb.title.toLowerCase().includes(task) || task.includes(orb.title.toLowerCase())) {
        score += 30
      }
      
      // Enhanced keyword matching for interview questions
      const matchedKeywords = orb.keywords.filter(keyword => 
        task.includes(keyword.toLowerCase()) || keyword.toLowerCase().includes(task)
      )
      score += matchedKeywords.length * (isInterviewQuestion ? 15 : 10)
      
      // Check description match
      if (orb.orb && (orb.orb.toLowerCase().includes(task) || task.includes(orb.orb.toLowerCase()))) {
        score += 20
      }
      
      // Check category match
      if (task.includes(orb.category.toLowerCase())) {
        score += 15
      }
      
      // Special boost for Interview Guide category
      if (isInterviewQuestion && orb.category === "Interview Guide") {
        score += 40
      }
      
      if (score > bestScore) {
        bestScore = score
        bestMatch = orb
      }
    }
    
    // Convert score to confidence percentage
    const confidence = Math.min(100, bestScore)
    confidenceScore.value = confidence
    
    // Step 3: Decision Point
    currentStep.value = 2
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (confidence >= 70 && bestMatch) {
      // High confidence: Use existing orb
      matchingOrb.value = {
        ...bestMatch,
        matched: true,
        confidence: confidence / 100
      }
      
      // Show success - no need to go through Whis pipeline
      console.log(`✅ High confidence match found: ${bestMatch.title} (${confidence}%)`)
      
    } else {
      // Low confidence: Send to Whis Pipeline for training
      console.log(`⚠️ Low confidence (${confidence}%), sending to Whis pipeline...`)
      
      // Store the task for Whis training
      const trainingTask = {
        id: Date.now(),
        originalInput: taskInput.value,
        sanitizedInput: task,
        confidence: confidence,
        timestamp: new Date().toISOString(),
        status: 'pending_training'
      }
      
      // Add to training queue (store in localStorage for demo)
      const trainingQueue = JSON.parse(localStorage.getItem('whisTrainingQueue') || '[]')
      trainingQueue.push(trainingTask)
      localStorage.setItem('whisTrainingQueue', JSON.stringify(trainingQueue))
      
      // Show message directing to Whis tab
      matchingOrb.value = {
        title: '⚠️ Low Confidence Match',
        category: 'Training Required',
        orb: `All orbs scored ${confidence}% confidence or less. Task has been sent to Whis pipeline for learning.`,
        needsTraining: true,
        confidence: confidence / 100,
        trainingMessage: {
          title: '🧠 Whis Learning Required',
          message: 'Head to Whis Pipeline tab to start training with this task.',
          action: 'Go to Whis Training',
          taskId: trainingTask.id
        }
      }
    }
    
  } catch (error) {
    console.error('Task processing error:', error)
    matchingOrb.value = null
    confidenceScore.value = 0
  } finally {
    loading.value = false
  }
}

// Helper functions for Whis pipeline processing
const generateOrbTitle = (task, isInterview = false) => {
  if (isInterview) {
    // Interview-style titles
    if (task.includes('cicd') || task.includes('pipeline')) return 'How would you design a CI/CD pipeline?'
    if (task.includes('kubernetes') && task.includes('architecture')) return 'Explain Kubernetes architecture'
    if (task.includes('docker') && task.includes('kubernetes')) return 'What is the difference between Docker and Kubernetes?'
    if (task.includes('monitoring')) return 'How would you implement monitoring and observability?'
    if (task.includes('security')) return 'Explain security best practices in DevOps'
    if (task.includes('microservices')) return 'How would you design a microservices architecture?'
    return `How would you approach: ${taskInput.value}?`
  }
  
  // Implementation-focused titles
  if (task.includes('pod')) return 'Kubernetes Pod Management'
  if (task.includes('deploy')) return 'Deployment Configuration'
  if (task.includes('service')) return 'Service Setup'
  if (task.includes('secret')) return 'Secrets Management'
  if (task.includes('pipeline')) return 'CI/CD Pipeline Configuration'
  return 'Custom Kubernetes Solution'
}

const determineCategory = (task, isInterview = false) => {
  if (isInterview) return 'Interview Guide'
  
  if (task.includes('security') || task.includes('secret')) return 'Security'
  if (task.includes('ci') || task.includes('pipeline')) return 'CI/CD'
  if (task.includes('helm')) return 'CI/CD'
  return 'Kubernetes'
}

const generateOrbDescription = (task, isInterview = false) => {
  if (isInterview) {
    return `Comprehensive interview-style explanation covering concepts, best practices, and real-world implementation strategies for: "${taskInput.value}"`
  }
  return `AI-generated solution for: "${taskInput.value}". This orb provides automated best practices and step-by-step guidance.`
}

const extractKeywords = (task, isInterview = false) => {
  const baseKeywords = ['kubernetes', 'pod', 'deployment', 'service', 'secret', 'configmap', 'ingress', 'helm', 'docker', 'ci', 'cd', 'pipeline', 'security']
  const interviewKeywords = ['interview', 'explain', 'how', 'what', 'architecture', 'design', 'best-practices']
  
  if (isInterview) {
    return [...baseKeywords.filter(keyword => task.includes(keyword)), ...interviewKeywords]
  }
  return baseKeywords.filter(keyword => task.includes(keyword))
}

const generateInterviewGuide = (task) => {
  // Generate interview-style comprehensive guides based on the question
  const baseGuide = [
    "🎯 **UNDERSTANDING THE QUESTION**",
    "□ **Break down the requirements**",
    "  - Identify key components and scope",
    "  - Consider scalability and reliability needs",
    "  - Think about security and compliance requirements",
    "",
    "🏗️ **ARCHITECTURE & DESIGN APPROACH**",
    "□ **High-level design principles**",
    "  - Start with business requirements",
    "  - Design for scalability and maintainability",
    "  - Consider failure modes and recovery strategies",
    "  - Plan for monitoring and observability",
    "",
    "🔧 **IMPLEMENTATION STRATEGY**",
    "□ **Step-by-step approach**",
    "  - Phase implementation to reduce risk",
    "  - Start with MVP and iterate",
    "  - Implement proper testing at each stage",
    "  - Document decisions and trade-offs",
    "",
    "🔒 **SECURITY & BEST PRACTICES**",
    "□ **Security considerations**",
    "  - Apply principle of least privilege",
    "  - Implement defense in depth",
    "  - Regular security audits and updates",
    "  - Compliance with industry standards",
    "",
    "📊 **MONITORING & MAINTENANCE**",
    "□ **Operational excellence**",
    "  - Implement comprehensive monitoring",
    "  - Set up alerting and incident response",
    "  - Plan for capacity management",
    "  - Regular performance optimization",
    "",
    "🎯 **INTERVIEW TALKING POINTS**",
    "□ **Demonstrate expertise**",
    "  - Show understanding of trade-offs",
    "  - Mention real-world experience",
    "  - Discuss lessons learned",
    "  - Ask clarifying questions",
    "",
    "✅ **SUCCESS CRITERIA**",
    `□ Successfully addresses: "${taskInput.value}"`,
    "□ Demonstrates comprehensive understanding",
    "□ Shows practical implementation experience",
    "□ Covers operational and security aspects"
  ]
  
  return baseGuide
}

const generateTemplate = (task) => {
  if (task.includes('pod')) {
    return `apiVersion: v1
kind: Pod
metadata:
  name: example-pod
  labels:
    app: example
spec:
  containers:
  - name: main
    image: nginx:latest
    ports:
    - containerPort: 80`
  }
  
  if (task.includes('service')) {
    return `apiVersion: v1
kind: Service
metadata:
  name: example-service
spec:
  selector:
    app: example
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP`
  }
  
  return `# Generated Kubernetes manifest
# Based on task: ${taskInput.value}
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-config
data:
  key: value`
}

const generateCommands = (task) => {
  if (task.includes('pod')) {
    return [
      'kubectl run example-pod --image=nginx',
      'kubectl get pods',
      'kubectl describe pod example-pod',
      'kubectl logs example-pod'
    ]
  }
  
  if (task.includes('service')) {
    return [
      'kubectl create service clusterip example-service --tcp=80:80',
      'kubectl get services',
      'kubectl describe service example-service'
    ]
  }
  
  return [
    'kubectl apply -f manifest.yaml',
    'kubectl get all',
    'kubectl describe <resource-type> <resource-name>'
  ]
}

const clearResults = () => {
  taskInput.value = ''
  matchingOrb.value = null
  confidenceScore.value = null
}

const approveSolution = () => {
  if (matchingOrb.value && matchingOrb.value.needsApproval) {
    // Save to orb library
    const newOrb = {
      ...matchingOrb.value,
      needsApproval: false,
      approved: true,
      saved_at: new Date().toISOString()
    }
    
    // Add to orb library
    orbLibrary.value.push(newOrb)
    
    console.log("✅ Solution approved and saved to Orb Library:", newOrb.title)
    alert(`✅ Solution approved! "${newOrb.title}" has been saved to the Orb Library.`)
    
    // Update the matching orb to show it's been saved
    matchingOrb.value = newOrb
  }
}

const rejectSolution = () => {
  console.log("❌ Solution rejected - requesting API key input")
  
  // Show API key prompt
  const useApiKey = confirm(
    "❌ Solution rejected. Would you like to:\n\n" +
    "✅ YES - Add your AI API key for improved results\n" +
    "❌ NO - This is where my pipeline falls back to AI help to refine"
  )
  
  if (useApiKey) {
    // Redirect to API keys page
    window.location.href = "/keys"
  } else {
    alert("💡 Pipeline fallback: In a real implementation, this would engage AI assistance to help refine and improve the solution quality.")
  }
}

const retrainModel = () => {
  console.log("🧠 Simulating model retraining...");
  const now = new Date().toISOString().replace("T", " ").split(".")[0] + " UTC";
  const orb = orbLibrary.value.find(o => o.title === "ML Task Classifier");
  if (orb) orb.last_trained = now;
  alert(`✅ Training Orb 'ML Task Classifier' retrained at ${now}`);
};
</script>

<style scoped>
.demo-view {
  space-y: 6;
}

.hero-section {
  text-align: center;
  padding: 2rem 0;
}

.hero-section h1 {
  background: linear-gradient(135deg, #ffffff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.demo-banner {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1px solid #f59e0b;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 1.5rem;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.banner-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.banner-text {
  color: #92400e;
  font-weight: 500;
  font-size: 0.875rem;
}

.results-section {
  margin-bottom: 2rem;
}

.orb-details {
  space-y: 2;
}

.orb-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.orb-icon {
  font-size: 2rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.orb-info h4 {
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
}

.orb-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
}

.orb-category {
  color: #3b82f6;
  font-weight: 500;
}

.orb-rune {
  color: #64748b;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.orb-content {
  padding: 1rem 0;
}

.orb-description {
  color: #374151;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.orb-keywords {
  margin-bottom: 1rem;
}

.keywords-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  margin-bottom: 0.5rem;
  display: block;
}

.keyword-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-tag {
  background: #f1f5f9;
  color: #475569;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid #e2e8f0;
}

.confidence-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.confidence-badge.success {
  background: #dcfce7;
  color: #166534;
}

.confidence-badge.warning {
  background: #fef3c7;
  color: #92400e;
}

.no-match-content {
  text-align: center;
  padding: 2rem;
}

.no-match-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-match-content h4 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-weight: 600;
}

.no-match-content p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.whis-pipeline-demo {
  margin: 2rem 0;
}

.suggestions {
  margin-top: 2rem;
}

.suggestions h5 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-weight: 600;
}

.suggestion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.suggestion-tag {
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid #bae6fd;
}

.demo-notice {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1px solid #f59e0b;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.notice-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.notice-content h4 {
  color: #92400e;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.notice-content p {
  color: #78350f;
  line-height: 1.6;
  margin: 0;
}

.status-message {
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-weight: 500;
}

.status-message.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.status-message.error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.info-item {
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.info-item h4 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-weight: 600;
}

.info-item p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.info-item ul {
  color: #64748b;
  line-height: 1.6;
  padding-left: 1.5rem;
}

.info-item li {
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .orb-header {
    flex-direction: column;
    text-align: center;
  }
  
  .orb-meta {
    justify-content: center;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .demo-notice {
    flex-direction: column;
    text-align: center;
  }
}
</style>

