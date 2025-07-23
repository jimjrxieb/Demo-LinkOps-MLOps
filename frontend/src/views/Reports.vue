<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Reports & Saved Assets</h1>
            <p class="mt-1 text-sm text-gray-500">
              View saved models, agents, outputs, and system logs
            </p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="refreshData"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Refresh
            </button>
            <button
              @click="exportReport"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Export Report
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center">
                <svg class="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">ML Models</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.models }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 bg-green-100 rounded-full flex items-center justify-center">
                <svg class="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">AI Agents</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.agents }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 bg-purple-100 rounded-full flex items-center justify-center">
                <svg class="h-5 w-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Pipeline Outputs</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.outputs }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 bg-yellow-100 rounded-full flex items-center justify-center">
                <svg class="h-5 w-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Documents</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.documents }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-white rounded-lg shadow">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8 px-6">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'py-4 px-1 border-b-2 font-medium text-sm',
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <div class="p-6">
          <!-- ML Models Tab -->
          <div v-if="activeTab === 'models'" class="space-y-6">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-medium text-gray-900">Machine Learning Models</h3>
              <div class="flex space-x-2">
                <select v-model="modelFilter" class="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                  <option value="">All Types</option>
                  <option value="classifier">Classification</option>
                  <option value="regression">Regression</option>
                  <option value="clustering">Clustering</option>
                </select>
              </div>
            </div>

            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Model</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="model in filteredModels" :key="model.name">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900">{{ model.name }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                        {{ getModelType(model.name) }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatFileSize(model.size) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatDate(model.created) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        @click="downloadModel(model.name)"
                        class="text-blue-600 hover:text-blue-900 mr-3"
                      >
                        Download
                      </button>
                      <button
                        @click="deleteModel(model.name)"
                        class="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- AI Agents Tab -->
          <div v-if="activeTab === 'agents'" class="space-y-6">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-medium text-gray-900">AI Agents</h3>
              <div class="flex space-x-2">
                <select v-model="agentFilter" class="border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                  <option value="">All Types</option>
                  <option value="taskbot">TaskBot</option>
                  <option value="commandbot">CommandBot</option>
                  <option value="assistant">Assistant</option>
                  <option value="workflow">Workflow</option>
                </select>
              </div>
            </div>

            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Agent</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="agent in filteredAgents" :key="agent.name">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900">{{ agent.name }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                        {{ getAgentType(agent.name) }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatFileSize(agent.size) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatDate(agent.created) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        @click="downloadAgent(agent.name)"
                        class="text-blue-600 hover:text-blue-900 mr-3"
                      >
                        Download
                      </button>
                      <button
                        @click="deleteAgent(agent.name)"
                        class="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Pipeline Outputs Tab -->
          <div v-if="activeTab === 'outputs'" class="space-y-6">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-medium text-gray-900">Pipeline Outputs</h3>
            </div>

            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Output</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="output in outputs" :key="output.name">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900">{{ output.name }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800">
                        {{ getOutputType(output.name) }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatFileSize(output.size) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatDate(output.created) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        @click="downloadOutput(output.name)"
                        class="text-blue-600 hover:text-blue-900 mr-3"
                      >
                        Download
                      </button>
                      <button
                        @click="deleteOutput(output.name)"
                        class="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Documents Tab -->
          <div v-if="activeTab === 'documents'" class="space-y-6">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-medium text-gray-900">RAG Documents</h3>
              <div class="text-sm text-gray-500">
                {{ stats.documents }} documents, {{ stats.chunks }} chunks
              </div>
            </div>

            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Document</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Chunks</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="doc in documents" :key="doc.document_id">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900">{{ doc.filename }}</div>
                      <div class="text-sm text-gray-500">{{ doc.document_id }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ doc.chunks_count }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatFileSize(doc.file_size_bytes) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatDate(doc.created_at) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        @click="viewDocument(doc.document_id)"
                        class="text-blue-600 hover:text-blue-900 mr-3"
                      >
                        View
                      </button>
                      <button
                        @click="deleteDocument(doc.document_id)"
                        class="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Reactive data
const activeTab = ref('models')
const modelFilter = ref('')
const agentFilter = ref('')
const models = ref([])
const agents = ref([])
const outputs = ref([])
const documents = ref([])
const stats = ref({
  models: 0,
  agents: 0,
  outputs: 0,
  documents: 0,
  chunks: 0
})

// Tab configuration
const tabs = [
  { id: 'models', name: 'ML Models' },
  { id: 'agents', name: 'AI Agents' },
  { id: 'outputs', name: 'Pipeline Outputs' },
  { id: 'documents', name: 'RAG Documents' }
]

// Computed properties
const filteredModels = computed(() => {
  if (!modelFilter.value) return models.value
  return models.value.filter(model => 
    getModelType(model.name).toLowerCase() === modelFilter.value
  )
})

const filteredAgents = computed(() => {
  if (!agentFilter.value) return agents.value
  return agents.value.filter(agent => 
    getAgentType(agent.name).toLowerCase() === agentFilter.value
  )
})

// Methods
async function refreshData() {
  try {
    await Promise.all([
      loadModels(),
      loadAgents(),
      loadOutputs(),
      loadDocuments(),
      loadStats()
    ])
  } catch (error) {
    console.error('Failed to refresh data:', error)
  }
}

async function loadModels() {
  try {
    const response = await axios.get('http://localhost:9000/model-creator/models')
    models.value = response.data.models || []
  } catch (error) {
    console.error('Failed to load models:', error)
    models.value = []
  }
}

async function loadAgents() {
  try {
    const response = await axios.get('http://localhost:9000/agent-creator/agents')
    agents.value = response.data.agents || []
  } catch (error) {
    console.error('Failed to load agents:', error)
    agents.value = []
  }
}

async function loadOutputs() {
  try {
    const response = await axios.get('http://localhost:9000/pipeline/outputs')
    outputs.value = response.data.outputs || []
  } catch (error) {
    console.error('Failed to load outputs:', error)
    outputs.value = []
  }
}

async function loadDocuments() {
  try {
    const response = await axios.get('http://localhost:9000/rag/documents')
    documents.value = response.data.documents || []
  } catch (error) {
    console.error('Failed to load documents:', error)
    documents.value = []
  }
}

async function loadStats() {
  try {
    const [modelsRes, agentsRes, outputsRes, ragRes] = await Promise.all([
      axios.get('http://localhost:9000/model-creator/models'),
      axios.get('http://localhost:9000/agent-creator/agents'),
      axios.get('http://localhost:9000/pipeline/outputs'),
      axios.get('http://localhost:9000/rag/stats')
    ])
    
    stats.value = {
      models: modelsRes.data.total || 0,
      agents: agentsRes.data.total || 0,
      outputs: outputsRes.data.total || 0,
      documents: ragRes.data.stats?.total_documents || 0,
      chunks: ragRes.data.stats?.total_chunks || 0
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

function getModelType(filename) {
  if (filename.includes('classifier')) return 'Classification'
  if (filename.includes('regression')) return 'Regression'
  if (filename.includes('clustering')) return 'Clustering'
  return 'Unknown'
}

function getAgentType(filename) {
  if (filename.includes('taskbot')) return 'TaskBot'
  if (filename.includes('commandbot')) return 'CommandBot'
  if (filename.includes('assistant')) return 'Assistant'
  if (filename.includes('workflow')) return 'Workflow'
  return 'Unknown'
}

function getOutputType(filename) {
  if (filename.includes('model')) return 'Model'
  if (filename.includes('embedding')) return 'Embedding'
  if (filename.includes('report')) return 'Report'
  return 'Output'
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleDateString()
}

async function downloadModel(modelName) {
  try {
    window.open(`http://localhost:9000/model-creator/download/${modelName}`, '_blank')
  } catch (error) {
    console.error('Failed to download model:', error)
  }
}

async function deleteModel(modelName) {
  if (!confirm(`Are you sure you want to delete ${modelName}?`)) return
  
  try {
    await axios.delete(`http://localhost:9000/model-creator/models/${modelName}`)
    await loadModels()
    await loadStats()
  } catch (error) {
    console.error('Failed to delete model:', error)
  }
}

async function downloadAgent(agentName) {
  try {
    window.open(`http://localhost:9000/agent-creator/download/${agentName}`, '_blank')
  } catch (error) {
    console.error('Failed to download agent:', error)
  }
}

async function deleteAgent(agentName) {
  if (!confirm(`Are you sure you want to delete ${agentName}?`)) return
  
  try {
    await axios.delete(`http://localhost:9000/agent-creator/agents/${agentName}`)
    await loadAgents()
    await loadStats()
  } catch (error) {
    console.error('Failed to delete agent:', error)
  }
}

async function downloadOutput(outputName) {
  try {
    window.open(`http://localhost:9000/pipeline/download/${outputName}`, '_blank')
  } catch (error) {
    console.error('Failed to download output:', error)
  }
}

async function deleteOutput(outputName) {
  if (!confirm(`Are you sure you want to delete ${outputName}?`)) return
  
  try {
    await axios.delete(`http://localhost:9000/pipeline/outputs/${outputName}`)
    await loadOutputs()
    await loadStats()
  } catch (error) {
    console.error('Failed to delete output:', error)
  }
}

async function viewDocument(docId) {
  try {
    const response = await axios.get(`http://localhost:9000/rag/documents/${docId}`)
    console.log('Document details:', response.data)
    // You could open a modal or navigate to a detail view here
  } catch (error) {
    console.error('Failed to view document:', error)
  }
}

async function deleteDocument(docId) {
  if (!confirm(`Are you sure you want to delete document ${docId}?`)) return
  
  try {
    await axios.delete(`http://localhost:9000/rag/documents/${docId}`)
    await loadDocuments()
    await loadStats()
  } catch (error) {
    console.error('Failed to delete document:', error)
  }
}

function exportReport() {
  const report = {
    timestamp: new Date().toISOString(),
    stats: stats.value,
    models: models.value,
    agents: agents.value,
    outputs: outputs.value,
    documents: documents.value
  }
  
  const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `linkops-report-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// Lifecycle
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
/* Add any component-specific styles here */
</style> 