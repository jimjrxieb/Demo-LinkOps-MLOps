<template>
  <div class="demo-view">
    <!-- Demo Mode Banner -->
    <div class="demo-banner">
      <div class="banner-content">
        <span class="banner-icon">⚠️</span>
        <span class="banner-text">Running in demo mode. Add AI API Key to enable real-time learning.</span>
      </div>
    </div>
    
    <!-- Hero Section -->
    <div class="hero-section mb-8">
      <h1 class="text-3xl font-extrabold text-white mb-2">Kubernetes/CD Shadow Agent <span class="text-blue-400">DEMO</span></h1>
      
      <p class="text-gray-300 text-sm mb-4 max-w-3xl leading-relaxed">
        This demo is a slimmed-down version of my personal Kubernetes AI/ML model under the LinkOps umbrella.
        Every Kubernetes-related Jira task I'm assigned — or errors I've encountered and solved using tools like ChatGPT and K8sGPT —
        gets entered into this system, where it is structured, learned from, and versioned.
        Over time, it becomes a reflection of my real-world experience, industry best practices, and troubleshooting patterns.
        The long-term goal is to reach a state where this system can autonomously complete any Kubernetes or CD-related task I receive.
      </p>
    </div>
    
    <!-- 1. Task Input -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">🎯 Submit a Kubernetes/CD Task or Error</h2>
        <p class="text-gray-600">Enter a Kubernetes task, goal, or error you've encountered — and see how LinkOps processes it through the AI/ML pipeline.</p>
      </div>
      <div class="card-body">
        <div class="form-group">
          <label class="form-label">Task Description</label>
          <textarea 
            v-model="taskInput" 
            class="form-input form-textarea bg-white text-black px-3 py-2 rounded-md w-full border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
            placeholder="e.g., create a pod named test with image nginx..."
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button 
            @click="submitTask" 
            :disabled="!taskInput.trim() || loading"
            class="btn btn-primary"
          >
            <span v-if="loading" class="btn-icon">⏳</span>
            <span v-else class="btn-icon">🚀</span>
            {{ loading ? 'Processing...' : 'Submit Task' }}
          </button>
          
          <button 
            @click="clearResults" 
            class="btn btn-secondary"
          >
            <span class="btn-icon">🗑️</span>
            Clear
          </button>
        </div>
      </div>
    </div>

    <!-- 2. Orb Match Section -->
    <div v-if="taskInput && !loading && matchingOrb" class="results-section">
      <OrbResultCard :orb="matchingOrb" :confidence="confidenceScore" />
    </div>

    <!-- 3. Whis Pipeline Side Panel -->
    <div v-if="taskInput && !loading" class="mt-4">
      <WhisPipeline :pipeline-data="pipelineData" :current-step="currentStep" />
    </div>

    <!-- 4. Full Orb Library Always Visible -->
    <div class="mt-6">
      <OrbLibrary :orbs="orbLibrary" />
    </div>

    <!-- 5. Demo Information -->
    <div class="card mt-6">
      <div class="card-header">
        <h2 class="card-title">ℹ️ About This Demo</h2>
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
    description: 'Cleans and validates input data, removes sensitive information',
    icon: '🧹',
    tools: 'Data validation, PII detection, format standardization'
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
    title: "Kubernetes Pod Creation",
    category: "Kubernetes",
    orb: "How to define and create a Kubernetes Pod using kubectl or YAML.",
    keywords: ["kubernetes", "pod", "nginx"]
  },
  {
    title: "Helm Chart Best Practices",
    category: "CI/CD",
    orb: "Structuring Helm charts for scalable and secure Kubernetes deployments.",
    keywords: ["helm", "charts", "templates"]
  },
  {
    title: "CI/CD Pipeline Linting",
    category: "CI/CD",
    orb: "Lint your GitHub Actions or GitLab pipelines for security and efficiency.",
    keywords: ["ci", "github", "yaml"]
  },
  {
    title: "Container Image Vulnerability Scanning",
    category: "Security",
    orb: "Scan container images with Trivy to identify OS and dependency vulnerabilities.",
    keywords: ["trivy", "container", "vulnerability", "scan"]
  },
  {
    title: "GitOps Compliance Check",
    category: "GitOps",
    orb: "Ensure Kubernetes manifests follow GitOps principles and are managed via tools like ArgoCD or Flux.",
    keywords: ["gitops", "argocd", "flux", "manifests"]
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
  }
])

const submitTask = async () => {
  loading.value = true
  currentStep.value = 0
  
  try {
    // Demo mode: Simple keyword matching
    const task = taskInput.value.toLowerCase()
    const keywords = ["kubernetes", "pod", "deployment", "nginx", "container", "service", "configmap", "secret", "ingress", "helm", "docker", "cicd", "pipeline", "github", "actions", "jenkins", "gitlab", "argo", "flux", "kustomize"]
    
    // Simple matching logic for demo
    const matchedKeywords = keywords.filter(keyword => task.includes(keyword))
    
    if (matchedKeywords.length > 0) {
      // Create a demo orb match
      matchingOrb.value = {
        title: "Kubernetes Deployment Orb",
        category: "Infrastructure",
        rune: "k8s.deploy.v1",
        orb: "Create and manage Kubernetes deployments with best practices",
        keywords: matchedKeywords.slice(0, 5) // Limit to 5 keywords
      }
      confidenceScore.value = Math.min(85, matchedKeywords.length * 15) // Score based on keyword matches
    } else {
      // No match found
      matchingOrb.value = null
      confidenceScore.value = 0
    }
    
    // Animate through pipeline steps
    for (let i = 0; i < pipelineData.value.length; i++) {
      currentStep.value = i
      await new Promise(resolve => setTimeout(resolve, 800)) // 800ms per step
    }
    
  } catch (error) {
    console.error(error)
    matchingOrb.value = null
    confidenceScore.value = 0
  } finally {
    loading.value = false
  }
}

const clearResults = () => {
  taskInput.value = ''
  matchingOrb.value = null
  confidenceScore.value = null
}
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

