<template>
  <div class="demo-view">
    <!-- Task Input Section -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">🎯 Submit DevSecOps Task</h2>
        <p class="text-gray-600">Enter a task and see how LinkOps processes it through the Whis pipeline</p>
      </div>
      <div class="card-body">
        <div class="form-group">
          <label class="form-label">Task Description</label>
          <textarea 
            v-model="taskInput" 
            class="form-input form-textarea"
            placeholder="e.g., create a pod named test with image nginx, set up CI/CD pipeline, scan for vulnerabilities..."
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

    <!-- Results Section -->
    <div v-if="taskInput && !loading" class="results-section">
      <!-- Orb Match Found -->
      <div v-if="matchingOrb" class="card">
        <div class="card-header">
          <h3 class="card-title">✅ Orb Match Found</h3>
          <span class="confidence-badge success">{{ confidenceScore }}% Confidence</span>
        </div>
        <div class="card-body">
          <div class="orb-details">
            <div class="orb-header">
              <div class="orb-icon">📚</div>
              <div class="orb-info">
                <h4>{{ matchingOrb.title }}</h4>
                <div class="orb-meta">
                  <span class="orb-category">{{ matchingOrb.category }}</span>
                  <span class="orb-rune">{{ matchingOrb.rune }}</span>
                </div>
              </div>
            </div>
            
            <div class="orb-content">
              <p class="orb-description">{{ matchingOrb.orb }}</p>
              
              <div class="orb-keywords">
                <span class="keywords-label">Keywords:</span>
                <div class="keyword-tags">
                  <span 
                    v-for="keyword in matchingOrb.keywords" 
                    :key="keyword" 
                    class="keyword-tag"
                  >
                    {{ keyword }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Match Found - Show Whis Pipeline -->
      <div v-else-if="confidenceScore === 0" class="card">
        <div class="card-header">
          <h3 class="card-title">🔍 No Orb Match Found</h3>
          <span class="confidence-badge warning">0% Confidence</span>
        </div>
        <div class="card-body">
          <div class="no-match-content">
            <div class="no-match-icon">🔍</div>
            <h4>Task: {{ taskInput }}</h4>
            <p>This task doesn't match any existing Orbs in our library. Here's what happens next:</p>
            
            <div class="whis-pipeline-demo">
              <WhisPipeline />
            </div>
            
            <div class="suggestions">
              <h5>Suggested Keywords:</h5>
              <div class="suggestion-tags">
                <span class="suggestion-tag">kubernetes</span>
                <span class="suggestion-tag">pod</span>
                <span class="suggestion-tag">deployment</span>
                <span class="suggestion-tag">container</span>
                <span class="suggestion-tag">nginx</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- API Keys Section -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">🔑 AI API Key Management</h2>
        <p class="text-gray-600">Configure API keys to enable enhanced AI features</p>
      </div>
      <div class="card-body">
        <div class="demo-notice">
          <div class="notice-icon">🎯</div>
          <div class="notice-content">
            <h4>Demo Mode Active</h4>
            <p>Currently running with simulated responses. Add API keys to enable real AI processing.</p>
          </div>
        </div>
        
        <div class="form-group">
          <label class="form-label">OpenAI / Grok API Key</label>
          <input 
            v-model="aiApiKey" 
            type="password"
            placeholder="sk-... or gsk_..." 
            class="form-input"
            disabled
          />
          <p class="form-help">Your API key is stored locally and never sent to our servers</p>
        </div>
        
        <div class="form-actions">
          <button 
            @click="saveApiKey" 
            :disabled="!aiApiKey.trim()"
            class="btn btn-success"
          >
            <span class="btn-icon">💾</span>
            Save Key
          </button>
          
          <button 
            @click="clearApiKey" 
            class="btn btn-secondary"
          >
            <span class="btn-icon">🗑️</span>
            Clear Key
          </button>
        </div>
        
        <div v-if="apiKeyStatus" class="status-message" :class="apiKeyStatus.type">
          {{ apiKeyStatus.message }}
        </div>
      </div>
    </div>

    <!-- Demo Information -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">ℹ️ About This Demo</h2>
      </div>
      <div class="card-body">
        <div class="info-grid">
          <div class="info-item">
            <h4>What You're Seeing</h4>
            <p>A fully functional demo of the LinkOps platform running in demo mode with simulated responses.</p>
          </div>
          
          <div class="info-item">
            <h4>Try These Tasks</h4>
            <ul>
              <li>"create a pod named test with image nginx"</li>
              <li>"set up CI/CD pipeline with GitHub Actions"</li>
              <li>"scan container images for vulnerabilities"</li>
              <li>"configure Kubernetes secrets management"</li>
            </ul>
          </div>
          
          <div class="info-item">
            <h4>Demo Features</h4>
            <ul>
              <li>Orb matching and confidence scoring</li>
              <li>Whis pipeline visualization</li>
              <li>Professional admin interface</li>
              <li>API key management</li>
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

const taskInput = ref('')
const matchingOrb = ref(null)
const confidenceScore = ref(null)
const loading = ref(false)
const aiApiKey = ref('')
const apiKeyStatus = ref(null)

// Load API key from localStorage on mount
onMounted(() => {
  const savedKey = localStorage.getItem('linkops_ai_api_key')
  if (savedKey) {
    aiApiKey.value = savedKey
  }
})

const submitTask = async () => {
  loading.value = true
  try {
    const response = await axios.post('/api/demo/search-orb', {
      task: taskInput.value
    })
    
    // Handle the new response format (no Grok fallback)
    if (response.data.match) {
      matchingOrb.value = response.data.match
      confidenceScore.value = response.data.confidence
    } else {
      // No match found - show empty state
      matchingOrb.value = null
      confidenceScore.value = 0
    }
  } catch (error) {
    console.error(error)
    // Show error state
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

const saveApiKey = () => {
  if (aiApiKey.value.trim()) {
    localStorage.setItem('linkops_ai_api_key', aiApiKey.value)
    apiKeyStatus.value = {
      type: 'success',
      message: '✅ API key saved successfully! You can now enable AI fallback features.'
    }
    setTimeout(() => {
      apiKeyStatus.value = null
    }, 3000)
  }
}

const clearApiKey = () => {
  aiApiKey.value = ''
  localStorage.removeItem('linkops_ai_api_key')
  apiKeyStatus.value = {
    type: 'success',
    message: '🗑️ API key cleared successfully!'
  }
  setTimeout(() => {
    apiKeyStatus.value = null
  }, 3000)
}
</script>

<style scoped>
.demo-view {
  space-y: 6;
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

