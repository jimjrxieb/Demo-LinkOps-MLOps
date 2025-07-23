<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">HTC: Secure Training Zone</h1>
            <p class="mt-1 text-sm text-gray-500">
              High-Trust Computing environment for secure model training and embedding
            </p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="resetPipeline"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Reset
            </button>
            <button
              @click="runPipeline"
              :disabled="!canRunPipeline"
              class="px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Run Pipeline
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Configuration Panel -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-6">Pipeline Configuration</h2>
            
            <!-- Task Type -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Task Type
              </label>
              <select
                v-model="taskType"
                @change="onTaskTypeChange"
                class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
              >
                <option value="rag">RAG Training (Document Embedding)</option>
                <option value="classification">Classification Model</option>
                <option value="regression">Regression Model</option>
                <option value="clustering">Clustering Model</option>
              </select>
            </div>

            <!-- File Upload -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Data File
              </label>
              <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-gray-400 transition-colors">
                <div class="space-y-1 text-center">
                  <svg
                    class="mx-auto h-12 w-12 text-gray-400"
                    stroke="currentColor"
                    fill="none"
                    viewBox="0 0 48 48"
                    aria-hidden="true"
                  >
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                  <div class="flex text-sm text-gray-600">
                    <label
                      for="file-upload"
                      class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
                    >
                      <span>Upload a file</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        class="sr-only"
                        accept=".csv,.json,.xlsx,.xls,.txt,.pdf"
                        @change="handleFile"
                      />
                    </label>
                    <p class="pl-1">or drag and drop</p>
                  </div>
                  <p class="text-xs text-gray-500">CSV, JSON, Excel, TXT, PDF files up to 50MB</p>
                </div>
              </div>
              <div v-if="selectedFile" class="mt-2 text-sm text-gray-600">
                Selected: {{ selectedFile.name }} ({{ formatFileSize(selectedFile.size) }})
              </div>
            </div>

            <!-- Target Column (for ML tasks) -->
            <div v-if="taskType !== 'rag'" class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Target Column
              </label>
              <input
                v-model="targetColumn"
                type="text"
                placeholder="Enter target column name"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>

            <!-- Advanced Options -->
            <div class="mb-6">
              <button
                @click="showAdvanced = !showAdvanced"
                class="text-sm text-blue-600 hover:text-blue-500 focus:outline-none"
              >
                {{ showAdvanced ? 'Hide' : 'Show' }} Advanced Options
              </button>
              
              <div v-if="showAdvanced" class="mt-4 space-y-4">
                <!-- Chunk Size (for RAG) -->
                <div v-if="taskType === 'rag'">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Chunk Size
                  </label>
                  <input
                    v-model.number="chunkSize"
                    type="number"
                    min="100"
                    max="5000"
                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                </div>

                <!-- Test Size (for ML) -->
                <div v-if="taskType !== 'rag'">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Test Size (%)
                  </label>
                  <input
                    v-model.number="testSize"
                    type="number"
                    min="10"
                    max="50"
                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                </div>

                <!-- Random State -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Random State
                  </label>
                  <input
                    v-model.number="randomState"
                    type="number"
                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  />
                </div>

                <!-- Security Level -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Security Level
                  </label>
                  <select
                    v-model="securityLevel"
                    class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    <option value="low">Low - Basic validation</option>
                    <option value="medium">Medium - Enhanced security</option>
                    <option value="high">High - Maximum security</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pipeline Visualization -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-6">Pipeline Flow</h2>
            
            <!-- Pipeline Steps -->
            <div class="space-y-4">
              <!-- Step 1: Data Intake -->
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div :class="[
                    'h-8 w-8 rounded-full flex items-center justify-center text-sm font-medium',
                    pipelineStatus.intake === 'completed' ? 'bg-green-100 text-green-800' :
                    pipelineStatus.intake === 'running' ? 'bg-blue-100 text-blue-800' :
                    pipelineStatus.intake === 'error' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    <svg v-if="pipelineStatus.intake === 'running'" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span v-else>1</span>
                  </div>
                </div>
                <div class="ml-4 flex-1">
                  <h3 class="text-sm font-medium text-gray-900">Data Intake</h3>
                  <p class="text-sm text-gray-500">Upload and validate data file</p>
                </div>
                <div class="ml-4">
                  <span v-if="pipelineStatus.intake === 'completed'" class="text-green-600 text-sm">✓ Complete</span>
                  <span v-else-if="pipelineStatus.intake === 'running'" class="text-blue-600 text-sm">Running...</span>
                  <span v-else-if="pipelineStatus.intake === 'error'" class="text-red-600 text-sm">Error</span>
                  <span v-else class="text-gray-400 text-sm">Pending</span>
                </div>
              </div>

              <!-- Arrow -->
              <div class="flex justify-center">
                <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
              </div>

              <!-- Step 2: Data Sanitization -->
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div :class="[
                    'h-8 w-8 rounded-full flex items-center justify-center text-sm font-medium',
                    pipelineStatus.sanitize === 'completed' ? 'bg-green-100 text-green-800' :
                    pipelineStatus.sanitize === 'running' ? 'bg-blue-100 text-blue-800' :
                    pipelineStatus.sanitize === 'error' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    <svg v-if="pipelineStatus.sanitize === 'running'" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span v-else>2</span>
                  </div>
                </div>
                <div class="ml-4 flex-1">
                  <h3 class="text-sm font-medium text-gray-900">Data Sanitization</h3>
                  <p class="text-sm text-gray-500">Clean, validate, and prepare data</p>
                </div>
                <div class="ml-4">
                  <span v-if="pipelineStatus.sanitize === 'completed'" class="text-green-600 text-sm">✓ Complete</span>
                  <span v-else-if="pipelineStatus.sanitize === 'running'" class="text-blue-600 text-sm">Running...</span>
                  <span v-else-if="pipelineStatus.sanitize === 'error'" class="text-red-600 text-sm">Error</span>
                  <span v-else class="text-gray-400 text-sm">Pending</span>
                </div>
              </div>

              <!-- Arrow -->
              <div class="flex justify-center">
                <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
              </div>

              <!-- Step 3: Processing -->
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div :class="[
                    'h-8 w-8 rounded-full flex items-center justify-center text-sm font-medium',
                    pipelineStatus.process === 'completed' ? 'bg-green-100 text-green-800' :
                    pipelineStatus.process === 'running' ? 'bg-blue-100 text-blue-800' :
                    pipelineStatus.process === 'error' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    <svg v-if="pipelineStatus.process === 'running'" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span v-else>3</span>
                  </div>
                </div>
                <div class="ml-4 flex-1">
                  <h3 class="text-sm font-medium text-gray-900">
                    {{ taskType === 'rag' ? 'Document Embedding' : 'Model Training' }}
                  </h3>
                  <p class="text-sm text-gray-500">
                    {{ taskType === 'rag' ? 'Create vector embeddings for RAG' : 'Train machine learning model' }}
                  </p>
                </div>
                <div class="ml-4">
                  <span v-if="pipelineStatus.process === 'completed'" class="text-green-600 text-sm">✓ Complete</span>
                  <span v-else-if="pipelineStatus.process === 'running'" class="text-blue-600 text-sm">Running...</span>
                  <span v-else-if="pipelineStatus.process === 'error'" class="text-red-600 text-sm">Error</span>
                  <span v-else class="text-gray-400 text-sm">Pending</span>
                </div>
              </div>

              <!-- Arrow -->
              <div class="flex justify-center">
                <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
              </div>

              <!-- Step 4: Storage -->
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div :class="[
                    'h-8 w-8 rounded-full flex items-center justify-center text-sm font-medium',
                    pipelineStatus.storage === 'completed' ? 'bg-green-100 text-green-800' :
                    pipelineStatus.storage === 'running' ? 'bg-blue-100 text-blue-800' :
                    pipelineStatus.storage === 'error' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    <svg v-if="pipelineStatus.storage === 'running'" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span v-else>4</span>
                  </div>
                </div>
                <div class="ml-4 flex-1">
                  <h3 class="text-sm font-medium text-gray-900">Storage & Output</h3>
                  <p class="text-sm text-gray-500">Save results and generate outputs</p>
                </div>
                <div class="ml-4">
                  <span v-if="pipelineStatus.storage === 'completed'" class="text-green-600 text-sm">✓ Complete</span>
                  <span v-else-if="pipelineStatus.storage === 'running'" class="text-blue-600 text-sm">Running...</span>
                  <span v-else-if="pipelineStatus.storage === 'error'" class="text-red-600 text-sm">Error</span>
                  <span v-else class="text-gray-400 text-sm">Pending</span>
                </div>
              </div>
            </div>

            <!-- Pipeline Results -->
            <div v-if="pipelineResult" class="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-green-800">Pipeline Completed Successfully</h3>
                  <div class="mt-2 text-sm text-green-700">
                    <p><strong>Task:</strong> {{ getTaskTypeLabel(taskType) }}</p>
                    <p><strong>Output:</strong> {{ pipelineResult.output_path }}</p>
                    <p><strong>Duration:</strong> {{ formatDuration(pipelineResult.duration) }}</p>
                  </div>
                  <div class="mt-4">
                    <button
                      @click="downloadResult"
                      class="text-sm font-medium text-green-800 hover:text-green-600"
                    >
                      Download Results →
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Error Display -->
            <div v-if="error" class="mt-8 bg-red-50 border border-red-200 rounded-lg p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800">Pipeline Error</h3>
                  <div class="mt-2 text-sm text-red-700">
                    {{ error }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
            <svg class="animate-spin h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900 mt-4">Running Pipeline</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              Please wait while we process your data...
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

// Reactive data
const taskType = ref('rag')
const selectedFile = ref(null)
const targetColumn = ref('')
const chunkSize = ref(1000)
const testSize = ref(20)
const randomState = ref(42)
const securityLevel = ref('medium')
const showAdvanced = ref(false)
const pipelineStatus = ref({
  intake: 'pending',
  sanitize: 'pending',
  process: 'pending',
  storage: 'pending'
})
const pipelineResult = ref(null)
const error = ref(null)
const isLoading = ref(false)

// Computed properties
const canRunPipeline = computed(() => {
  return selectedFile.value && 
         (taskType.value === 'rag' || targetColumn.value.trim())
})

// Methods
function onTaskTypeChange() {
  // Reset target column when switching to RAG
  if (taskType.value === 'rag') {
    targetColumn.value = ''
  }
  resetPipeline()
}

function handleFile(event) {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    error.value = null
    pipelineResult.value = null
    resetPipelineStatus()
  }
}

function resetPipelineStatus() {
  pipelineStatus.value = {
    intake: 'pending',
    sanitize: 'pending',
    process: 'pending',
    storage: 'pending'
  }
}

function resetPipeline() {
  selectedFile.value = null
  targetColumn.value = ''
  chunkSize.value = 1000
  testSize.value = 20
  randomState.value = 42
  securityLevel.value = 'medium'
  showAdvanced.value = false
  resetPipelineStatus()
  pipelineResult.value = null
  error.value = null
}

async function runPipeline() {
  if (!canRunPipeline.value) return
  
  isLoading.value = true
  error.value = null
  pipelineResult.value = null
  resetPipelineStatus()
  
  try {
    // Step 1: Data Intake
    pipelineStatus.value.intake = 'running'
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('task_type', taskType.value)
    
    if (targetColumn.value) {
      formData.append('target_column', targetColumn.value)
    }
    
    if (taskType.value === 'rag') {
      formData.append('chunk_size', chunkSize.value)
    } else {
      formData.append('test_size', testSize.value)
      formData.append('random_state', randomState.value)
    }
    
    formData.append('security_level', securityLevel.value)
    
    const response = await axios.post('http://localhost:8004/run-pipeline', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Simulate pipeline steps
    await simulatePipelineSteps()
    
    pipelineResult.value = response.data
    
  } catch (err) {
    console.error('Pipeline error:', err)
    error.value = err.response?.data?.detail || 'Pipeline failed. Please try again.'
    
    // Mark current step as error
    const currentStep = Object.keys(pipelineStatus.value).find(key => 
      pipelineStatus.value[key] === 'running'
    )
    if (currentStep) {
      pipelineStatus.value[currentStep] = 'error'
    }
  } finally {
    isLoading.value = false
  }
}

async function simulatePipelineSteps() {
  // Simulate step progression
  await new Promise(resolve => setTimeout(resolve, 1000))
  pipelineStatus.value.intake = 'completed'
  pipelineStatus.value.sanitize = 'running'
  
  await new Promise(resolve => setTimeout(resolve, 1500))
  pipelineStatus.value.sanitize = 'completed'
  pipelineStatus.value.process = 'running'
  
  await new Promise(resolve => setTimeout(resolve, 2000))
  pipelineStatus.value.process = 'completed'
  pipelineStatus.value.storage = 'running'
  
  await new Promise(resolve => setTimeout(resolve, 1000))
  pipelineStatus.value.storage = 'completed'
}

function downloadResult() {
  if (pipelineResult.value?.output_path) {
    const link = document.createElement('a')
    link.href = `http://localhost:8004/download/${pipelineResult.value.output_path}`
    link.download = `htc_result_${Date.now()}.zip`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

function getTaskTypeLabel(type) {
  const labels = {
    rag: 'RAG Training',
    classification: 'Classification Model',
    regression: 'Regression Model',
    clustering: 'Clustering Model'
  }
  return labels[type] || type
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function formatDuration(seconds) {
  if (!seconds) return 'Unknown'
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}m ${remainingSeconds}s`
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style> 