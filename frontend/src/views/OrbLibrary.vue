<template>
  <div class="orb-library">
    <!-- Header Section -->
    <div class="header-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">📚 Kubernetes/CD Orb Library</h2>
          <p class="text-gray-600">Browse the collection of automated best practices and solutions</p>
        </div>
        <div class="card-body">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-number">{{ orbs.length }}</div>
              <div class="stat-label">Total Orbs</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">{{ categories.length }}</div>
              <div class="stat-label">Categories</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">{{ averageConfidence }}%</div>
              <div class="stat-label">Avg Confidence</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="card">
        <div class="card-body">
          <div class="filter-controls">
            <div class="form-group">
              <label class="form-label">Search Orbs</label>
              <input 
                v-model="searchQuery" 
                type="text" 
                class="form-input" 
                placeholder="Search by title, keywords, or category..."
              />
            </div>
            
            <!-- Category Buttons -->
            <div class="form-group">
              <label class="form-label">Filter by Category</label>
              <div class="category-buttons">
                <button
                  @click="selectedCategory = ''"
                  :class="['category-btn', selectedCategory === '' ? 'category-btn-active' : 'category-btn-inactive']"
                >
                  All Categories
                </button>
                <button
                  v-for="category in categories"
                  :key="category"
                  @click="selectedCategory = category"
                  :class="['category-btn', selectedCategory === category ? 'category-btn-active' : 'category-btn-inactive']"
                >
                  {{ category }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Orbs Grid -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="orb in filteredOrbs"
        :key="orb.rune"
        class="bg-gray-800 text-white rounded-lg p-4 shadow hover:shadow-lg transition-all cursor-pointer"
        @click="openOrbModal(orb)"
      >
        <h3 class="text-lg font-semibold text-teal-300">{{ orb.title }}</h3>
        <p class="text-sm text-gray-300 mb-2 italic">Category: {{ orb.category }}</p>
        <p class="text-sm mb-2">{{ orb.orb }}</p>
        <div class="text-xs text-blue-400 mt-2">
          Tags: <span v-for="keyword in orb.keywords" :key="keyword" class="mr-1">#{{ keyword }}</span>
        </div>
        <div class="text-xs text-gray-400 mt-2 italic">
          Click to view details →
        </div>
      </div>
    </div>

    <!-- No Results -->
    <div v-if="filteredOrbs.length === 0" class="no-results">
      <div class="card">
        <div class="card-body text-center">
          <div class="no-results-icon">🔍</div>
          <h3>No Orbs Found</h3>
          <p>Try adjusting your search criteria or category filter.</p>
        </div>
      </div>
    </div>

    <!-- Orb Detail Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">📚 {{ selectedOrb?.title }}</h2>
          <button @click="closeModal" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="orb-detail-grid">
            <div class="detail-section">
              <h3 class="detail-label">Category</h3>
              <p class="detail-value">{{ selectedOrb?.category }}</p>
            </div>
            
            <div class="detail-section">
              <h3 class="detail-label">Description</h3>
              <p class="detail-value">{{ selectedOrb?.orb }}</p>
            </div>
            
            <div class="detail-section">
              <h3 class="detail-label">Keywords</h3>
              <div class="keyword-tags">
                <span 
                  v-for="keyword in selectedOrb?.keywords" 
                  :key="keyword" 
                  class="keyword-tag"
                >
                  #{{ keyword }}
                </span>
              </div>
            </div>
            
            <div class="detail-section">
              <h3 class="detail-label">Rune ID</h3>
              <code class="rune-code">{{ selectedOrb?.rune || 'R-' + Math.floor(Math.random() * 1000) }}</code>
            </div>
            
            <div class="detail-section">
              <h3 class="detail-label">Confidence Score</h3>
              <div class="confidence-score">
                <span class="score-value">{{ Math.round((selectedOrb?.confidence || 0.85) * 100) }}%</span>
                <div class="confidence-bar">
                  <div 
                    class="confidence-fill" 
                    :style="{ width: Math.round((selectedOrb?.confidence || 0.85) * 100) + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeModal" class="btn btn-secondary">Close</button>
          <button class="btn btn-primary">Use This Orb</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Props for external orb data
const props = defineProps({
  orbs: {
    type: Array,
    default: () => []
  }
})

const searchQuery = ref('')
const selectedCategory = ref('')
const selectedOrb = ref(null)
const showModal = ref(false)

// Use props.orbs if provided, otherwise load from API
const orbs = ref([])

const categories = computed(() => {
  const cats = [...new Set(orbs.value.map(orb => orb.category))]
  return cats.sort()
})

const averageConfidence = computed(() => {
  if (orbs.value.length === 0) return 0
  const total = orbs.value.reduce((sum, orb) => sum + orb.confidence, 0)
  return Math.round((total / orbs.value.length) * 100)
})

const filteredOrbs = computed(() => {
  let filtered = orbs.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(orb => 
      orb.title.toLowerCase().includes(query) ||
      orb.category.toLowerCase().includes(query) ||
      orb.keywords.some(keyword => keyword.toLowerCase().includes(query))
    )
  }

  // Filter by category
  if (selectedCategory.value) {
    filtered = filtered.filter(orb => orb.category === selectedCategory.value)
  }

  return filtered
})

const getCategoryIcon = (category) => {
  const icons = {
    'DevOps': '⚙️',
    'Security': '🛡️',
    'Kubernetes': '☸️',
    'CI/CD': '🔄',
    'GitOps': '📦',
    'Infrastructure': '🏗️',
    'Observability': '📊'
  }
  return icons[category] || '📋'
}

const getConfidenceClass = (confidence) => {
  if (confidence >= 0.9) return 'confidence-high'
  if (confidence >= 0.7) return 'confidence-medium'
  return 'confidence-low'
}

const openOrbModal = (orb) => {
  selectedOrb.value = orb
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedOrb.value = null
}

const loadOrbs = async () => {
  // If orbs are provided via props, use them
  if (props.orbs && props.orbs.length > 0) {
    orbs.value = props.orbs
    return
  }
  
  try {
    const response = await axios.get('/api/demo/orbs')
    orbs.value = response.data.orbs || []
  } catch (error) {
    console.error('Failed to load orbs:', error)
    // Fallback to hardcoded orbs for demo
    orbs.value = [
      {
        title: "CI/CD Pipeline Linting",
        keywords: ["ci", "cd", "pipeline", "lint", "yaml", "gha"],
        orb: "Ensure your CI/CD pipeline is linted using yamllint and GitHub Actions workflow syntax validation.",
        rune: "R-101",
        confidence: 0.96,
        category: "DevOps"
      },
      {
        title: "Container Image Vulnerability Scanning",
        keywords: ["trivy", "container", "image", "vulnerability", "scan"],
        orb: "Scan container images with Trivy to identify OS and dependency vulnerabilities.",
        rune: "R-102",
        confidence: 0.94,
        category: "Security"
      },
      {
        title: "Helm Chart Best Practices",
        keywords: ["helm", "chart", "values.yaml", "templates"],
        orb: "Follow Helm chart conventions: use `values.yaml`, document templates, and validate with `helm lint`.",
        rune: "R-103",
        confidence: 0.93,
        category: "Kubernetes"
      },
      {
        title: "GitOps Compliance Check",
        keywords: ["gitops", "argocd", "flux", "manifests"],
        orb: "Ensure Kubernetes manifests follow GitOps principles and are managed via tools like ArgoCD or Flux.",
        rune: "R-104",
        confidence: 0.91,
        category: "GitOps"
      },
      {
        title: "Secrets Management with Kubernetes",
        keywords: ["secret", "kubernetes", "sealed-secrets", "vault"],
        orb: "Use Sealed Secrets or HashiCorp Vault for secure Kubernetes secret management.",
        rune: "R-105",
        confidence: 0.92,
        category: "Security"
      },
      {
        title: "Shift Left Security",
        keywords: ["shift", "left", "security", "snyk", "bandit"],
        orb: "Integrate Snyk, Bandit, and Checkov into CI pipeline for early security checks.",
        rune: "R-106",
        confidence: 0.93,
        category: "Security"
      },
      {
        title: "Terraform Code Quality",
        keywords: ["terraform", "tfsec", "lint", "infrastructure"],
        orb: "Use `tflint`, `tfsec`, and `checkov` to audit infrastructure as code.",
        rune: "R-107",
        confidence: 0.94,
        category: "Infrastructure"
      },
      {
        title: "Kubernetes Pod Security",
        keywords: ["pod", "security", "psa", "policy", "kubernetes"],
        orb: "Apply Pod Security Standards (restricted, baseline, privileged) via PSA admission controller.",
        rune: "R-108",
        confidence: 0.95,
        category: "Kubernetes"
      },
      {
        title: "API Security Guidelines",
        keywords: ["api", "security", "authentication", "authorization"],
        orb: "Enforce authentication, rate limiting, and secure headers for REST APIs.",
        rune: "R-109",
        confidence: 0.91,
        category: "Security"
      },
      {
        title: "Log Aggregation for Debugging",
        keywords: ["logs", "debug", "grafana", "prometheus", "loki"],
        orb: "Centralize logs using Loki or ELK to enable efficient debugging and alerting.",
        rune: "R-110",
        confidence: 0.90,
        category: "Observability"
      }
    ]
  }
}

onMounted(() => {
  loadOrbs()
})
</script>

<style scoped>
.orb-library {
  space-y: 6;
}

.header-section {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  text-align: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  border-radius: 12px;
  border: 1px solid #cbd5e1;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #64748b;
  font-weight: 500;
}

.filter-section {
  margin-bottom: 2rem;
}

.filter-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.category-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-btn-active {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-color: #1d4ed8;
}

.category-btn-active:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.category-btn-inactive {
  background: #f8fafc;
  color: #475569;
  border-color: #cbd5e1;
}

.category-btn-inactive:hover {
  background: #e2e8f0;
  color: #1e293b;
  border-color: #94a3b8;
}

.orbs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.orb-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.2s ease;
}

.orb-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.orb-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.orb-icon {
  font-size: 2rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.orb-meta {
  flex: 1;
}

.orb-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.orb-category {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.orb-confidence {
  display: flex;
  align-items: center;
}

.confidence-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.confidence-high {
  background: #dcfce7;
  color: #166534;
}

.confidence-medium {
  background: #fef3c7;
  color: #92400e;
}

.confidence-low {
  background: #fee2e2;
  color: #991b1b;
}

.orb-content {
  padding: 1.5rem;
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

.orb-footer {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.rune-id {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rune-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
}

.rune-code {
  background: #1e293b;
  color: #f8fafc;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.no-results {
  margin-top: 2rem;
}

.no-results-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.no-results h3 {
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.no-results p {
  color: #64748b;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.modal-body {
  padding: 1.5rem;
}

.orb-detail-grid {
  display: grid;
  gap: 1.5rem;
}

.detail-section {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 1rem;
}

.detail-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.detail-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-value {
  color: #1e293b;
  line-height: 1.6;
  margin: 0;
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

.rune-code {
  background: #1e293b;
  color: #f8fafc;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  display: inline-block;
}

.confidence-score {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.score-value {
  font-weight: 600;
  color: #059669;
  font-size: 1.125rem;
}

.confidence-bar {
  flex: 1;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #059669);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}

@media (max-width: 768px) {
  .filter-controls {
    grid-template-columns: 1fr;
  }
  
  .orbs-grid {
    grid-template-columns: 1fr;
  }
  
  .orb-header {
    flex-direction: column;
    text-align: center;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}
</style> 