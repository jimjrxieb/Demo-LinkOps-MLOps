<template>
  <div class="orbs-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">📘 Orbs Library</h1>
      <p class="text-gray-300">Best practices and knowledge assets from the Whis AI</p>
    </div>

    <!-- Search and Filters -->
    <div class="glass-panel p-6 mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Search Orbs</label>
          <input
            v-model="searchQuery"
            type="text"
            class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
            placeholder="Search by title, tags, or content..."
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Category</label>
          <select
            v-model="selectedCategory"
            class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">All Categories</option>
            <option value="kubernetes">Kubernetes</option>
            <option value="docker">Docker</option>
            <option value="mlops">MLOps</option>
            <option value="security">Security</option>
            <option value="general">General</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Quality Score</label>
          <select
            v-model="selectedQuality"
            class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">Any Quality</option>
            <option value="90">Excellent (90+)</option>
            <option value="80">Good (80+)</option>
            <option value="70">Fair (70+)</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Status</label>
          <select
            v-model="selectedStatus"
            class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">All Status</option>
            <option value="approved">Approved</option>
            <option value="pending">Pending Review</option>
            <option value="generated">Recently Generated</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-blue-400 mb-2">{{ stats.total }}</div>
        <div class="text-sm text-gray-300">Total Orbs</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-green-400 mb-2">{{ stats.approved }}</div>
        <div class="text-sm text-gray-300">Approved</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-yellow-400 mb-2">{{ stats.pending }}</div>
        <div class="text-sm text-gray-300">Pending Review</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-purple-400 mb-2">{{ stats.avgQuality }}%</div>
        <div class="text-sm text-gray-300">Avg Quality</div>
      </div>
    </div>

    <!-- Orbs Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
      <div
        v-for="orb in filteredOrbs"
        :key="orb.id"
        class="glass-panel p-6 rounded-lg hover:neon-border transition-all duration-300"
        :class="`orb-${orb.category}`"
      >
        <!-- Orb Header -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-2">
            <span class="text-2xl">{{ getCategoryIcon(orb.category) }}</span>
            <div>
              <h3 class="futuristic-subtitle text-lg">{{ orb.title }}</h3>
              <div class="flex items-center space-x-2 text-xs text-gray-400">
                <span>{{ orb.category }}</span>
                <span>•</span>
                <span>{{ orb.timestamp }}</span>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <div class="quality-score" :class="getQualityClass(orb.qualityScore)">
              {{ orb.qualityScore }}%
            </div>
            <div class="status-badge" :class="orb.status">
              {{ orb.status }}
            </div>
          </div>
        </div>

        <!-- Orb Content Preview -->
        <div class="mb-4">
          <p class="text-sm text-gray-300 line-clamp-3">{{ orb.description }}</p>
        </div>

        <!-- Best Practices Preview -->
        <div class="mb-4">
          <h4 class="text-sm font-medium text-gray-200 mb-2">Best Practices:</h4>
          <ul class="text-xs text-gray-400 space-y-1">
            <li v-for="practice in orb.bestPractices.slice(0, 3)" :key="practice" class="flex items-start space-x-2">
              <span class="text-green-400">✓</span>
              <span>{{ practice }}</span>
            </li>
            <li v-if="orb.bestPractices.length > 3" class="text-gray-500">
              ... and {{ orb.bestPractices.length - 3 }} more
            </li>
          </ul>
        </div>

        <!-- Tags -->
        <div class="mb-4">
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tag in orb.tags.slice(0, 4)"
              :key="tag"
              class="px-2 py-1 text-xs glass-panel rounded"
            >
              {{ tag }}
            </span>
            <span v-if="orb.tags.length > 4" class="px-2 py-1 text-xs text-gray-500">
              +{{ orb.tags.length - 4 }}
            </span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-between">
          <div class="flex space-x-2">
            <button
              @click="viewOrb(orb)"
              class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
            >
              View Details
            </button>
            <button
              v-if="orb.status === 'pending'"
              @click="approveOrb(orb)"
              class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300 text-green-400"
            >
              Approve
            </button>
          </div>
          <div class="flex items-center space-x-1 text-xs text-gray-400">
            <span>{{ orb.usageCount }} uses</span>
            <span>•</span>
            <span>{{ orb.relatedRunes }} runes</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Load More -->
    <div v-if="hasMore" class="text-center mt-8">
      <button
        @click="loadMore"
        class="glass-panel px-6 py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300"
      >
        Load More Orbs
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'Orbs',
  setup() {
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const selectedQuality = ref('')
    const selectedStatus = ref('')
    const hasMore = ref(true)

    const stats = ref({
      total: 47,
      approved: 32,
      pending: 15,
      avgQuality: 84
    })

    const orbs = ref([
      {
        id: 1,
        title: 'Kubernetes Deployment Best Practices',
        category: 'kubernetes',
        description: 'Comprehensive guide for deploying applications to Kubernetes with security, scalability, and reliability in mind.',
        qualityScore: 92,
        status: 'approved',
        timestamp: '2 hours ago',
        usageCount: 15,
        relatedRunes: 8,
        tags: ['k8s', 'deployment', 'security', 'best-practices', 'production'],
        bestPractices: [
          'Always specify resource limits and requests',
          'Use rolling update strategy for zero-downtime deployments',
          'Implement proper health checks and readiness probes',
          'Use non-root containers for security',
          'Set appropriate replica count for high availability'
        ]
      },
      {
        id: 2,
        title: 'Docker Multi-Stage Build Optimization',
        category: 'docker',
        description: 'Efficient Docker image building techniques using multi-stage builds to reduce image size and improve security.',
        qualityScore: 88,
        status: 'approved',
        timestamp: '4 hours ago',
        usageCount: 12,
        relatedRunes: 5,
        tags: ['docker', 'optimization', 'security', 'multi-stage'],
        bestPractices: [
          'Use specific base image tags, not latest',
          'Copy requirements first for better layer caching',
          'Remove unnecessary packages and files',
          'Use minimal base images like Alpine',
          'Run as non-root user'
        ]
      },
      {
        id: 3,
        title: 'MLOps Pipeline Security Framework',
        category: 'mlops',
        description: 'Security considerations and best practices for machine learning operations pipelines.',
        qualityScore: 85,
        status: 'pending',
        timestamp: '6 hours ago',
        usageCount: 8,
        relatedRunes: 12,
        tags: ['mlops', 'security', 'pipeline', 'framework'],
        bestPractices: [
          'Implement data validation and sanitization',
          'Use secure model storage and versioning',
          'Monitor for model drift and anomalies',
          'Implement access controls for model endpoints'
        ]
      },
      {
        id: 4,
        title: 'Infrastructure as Code Guidelines',
        category: 'general',
        description: 'Best practices for managing infrastructure using code with version control and automation.',
        qualityScore: 90,
        status: 'approved',
        timestamp: '1 day ago',
        usageCount: 20,
        relatedRunes: 6,
        tags: ['iac', 'terraform', 'automation', 'version-control'],
        bestPractices: [
          'Use version control for all infrastructure code',
          'Implement automated testing for infrastructure changes',
          'Use state backends for team collaboration',
          'Follow naming conventions and documentation standards'
        ]
      },
      {
        id: 5,
        title: 'Container Security Scanning',
        category: 'security',
        description: 'Comprehensive approach to scanning container images for vulnerabilities and security issues.',
        qualityScore: 87,
        status: 'generated',
        timestamp: '2 days ago',
        usageCount: 6,
        relatedRunes: 4,
        tags: ['security', 'scanning', 'vulnerabilities', 'containers'],
        bestPractices: [
          'Scan images for known vulnerabilities',
          'Use trusted base images from official sources',
          'Implement runtime security monitoring',
          'Regular updates and patch management'
        ]
      }
    ])

    const filteredOrbs = computed(() => {
      return orbs.value.filter(orb => {
        const matchesSearch = searchQuery.value === '' || 
          orb.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          orb.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          orb.tags.some(tag => tag.toLowerCase().includes(searchQuery.value.toLowerCase()))
        
        const matchesCategory = selectedCategory.value === '' || orb.category === selectedCategory.value
        const matchesQuality = selectedQuality.value === '' || orb.qualityScore >= parseInt(selectedQuality.value)
        const matchesStatus = selectedStatus.value === '' || orb.status === selectedStatus.value
        
        return matchesSearch && matchesCategory && matchesQuality && matchesStatus
      })
    })

    const getCategoryIcon = (category) => {
      const icons = {
        kubernetes: '☸️',
        docker: '🐳',
        mlops: '🧠',
        security: '🛡️',
        general: '📋'
      }
      return icons[category] || '📘'
    }

    const getQualityClass = (score) => {
      if (score >= 90) return 'quality-excellent'
      if (score >= 80) return 'quality-good'
      if (score >= 70) return 'quality-fair'
      return 'quality-poor'
    }

    const viewOrb = (orb) => {
      console.log('Viewing orb:', orb.title)
      // Navigate to detailed orb view
    }

    const approveOrb = (orb) => {
      orb.status = 'approved'
      stats.value.approved++
      stats.value.pending--
      console.log('Approved orb:', orb.title)
    }

    const loadMore = () => {
      console.log('Loading more orbs...')
      hasMore.value = false
    }

    return {
      searchQuery,
      selectedCategory,
      selectedQuality,
      selectedStatus,
      stats,
      orbs,
      filteredOrbs,
      hasMore,
      getCategoryIcon,
      getQualityClass,
      viewOrb,
      approveOrb,
      loadMore
    }
  }
}
</script>

<style scoped>
@import '../assets/futuristic.css';

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.quality-score {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.quality-excellent { background-color: rgba(34, 197, 94, 0.2); color: #22c55e; }
.quality-good { background-color: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.quality-fair { background-color: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.quality-poor { background-color: rgba(239, 68, 68, 0.2); color: #ef4444; }

.status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.status-badge.approved { background-color: rgba(34, 197, 94, 0.2); color: #22c55e; }
.status-badge.pending { background-color: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.status-badge.generated { background-color: rgba(139, 92, 246, 0.2); color: #8b5cf6; }

.orb-kubernetes { border-left: 3px solid #3b82f6; }
.orb-docker { border-left: 3px solid #0ea5e9; }
.orb-mlops { border-left: 3px solid #8b5cf6; }
.orb-security { border-left: 3px solid #ef4444; }
.orb-general { border-left: 3px solid #6b7280; }
</style> 