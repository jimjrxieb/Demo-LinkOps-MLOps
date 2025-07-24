<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">📊 ML Model Builder</h1>
            <p class="mt-1 text-sm text-gray-500">
              Train AI models to predict property management outcomes. No coding required.
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="loadModels"
              class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              :disabled="loading"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Loading...' : 'Refresh Models' }}
            </button>
            <button
              @click="showNewModelForm = true"
              class="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              + New Model
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Instructions -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
        <h3 class="text-lg font-semibold text-blue-900 mb-2">🎯 How It Works</h3>
        <p class="text-blue-800 mb-4">
          Upload your property management data and train AI models to predict outcomes like eviction risk, renewal probability, and maintenance needs.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-700">
          <div>
            <strong>Step 1:</strong> Upload CSV with your data
            <ul class="list-disc list-inside mt-1 space-y-1">
              <li>Rent history</li>
              <li>Tenant records</li>
              <li>Maintenance logs</li>
            </ul>
          </div>
          <div>
            <strong>Step 2:</strong> Choose what to predict
            <ul class="list-disc list-inside mt-1 space-y-1">
              <li>Eviction risk</li>
              <li>Renewal probability</li>
              <li>Maintenance needs</li>
            </ul>
          </div>
          <div>
            <strong>Step 3:</strong> Train and deploy
            <ul class="list-disc list-inside mt-1 space-y-1">
              <li>One-click training</li>
              <li>See accuracy scores</li>
              <li>Use for predictions</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- New Model Form -->
      <div v-if="showNewModelForm" class="bg-white rounded-lg shadow-sm border p-6 mb-8">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold text-gray-900">🚀 Create New Model</h2>
          <button
            @click="showNewModelForm = false"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Step 1: Upload CSV -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            📁 Step 1: Upload Your Data (CSV)
          </label>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center" @dragover.prevent @drop.prevent="handleDrop">
            <input
              type="file"
              ref="fileInput"
              @change="handleFileUpload"
              accept=".csv"
              class="hidden"
            />
            <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
            <p class="text-sm text-gray-600 mb-2">
              {{ selectedFile ? selectedFile.name : 'Drop your CSV file here or click to browse' }}
            </p>
            <button
              @click="$refs.fileInput.click()"
              class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Browse Files
            </button>
          </div>
          <p class="mt-2 text-xs text-gray-500">
            Upload a CSV file with your property management data. Include columns like rent_amount, late_payments, tenant_tenure, etc.
          </p>
        </div>

        <!-- Step 2: Data Preview -->
        <div v-if="dataPreview.columns.length" class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            📊 Step 2: Data Preview
          </label>
          <div class="bg-gray-50 rounded-lg p-4">
            <div class="flex justify-between items-center mb-3">
              <span class="text-sm font-medium text-gray-700">
                {{ dataPreview.columns.length }} columns, {{ dataPreview.rowCount }} rows
              </span>
              <span class="text-xs text-gray-500">
                First 5 rows shown
              </span>
            </div>
            
            <!-- Column List -->
            <div class="mb-4">
              <h4 class="text-sm font-medium text-gray-700 mb-2">Available Columns:</h4>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="col in dataPreview.columns"
                  :key="col"
                  class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                >
                  {{ col }}
                </span>
              </div>
            </div>

            <!-- Data Preview Table -->
            <div class="overflow-x-auto">
              <table class="min-w-full text-xs">
                <thead>
                  <tr class="border-b border-gray-200">
                    <th
                      v-for="col in dataPreview.columns.slice(0, 5)"
                      :key="col"
                      class="px-2 py-1 text-left font-medium text-gray-700"
                    >
                      {{ col }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(row, index) in dataPreview.rows.slice(0, 5)"
                    :key="index"
                    class="border-b border-gray-100"
                  >
                    <td
                      v-for="col in dataPreview.columns.slice(0, 5)"
                      :key="col"
                      class="px-2 py-1 text-gray-600"
                    >
                      {{ row[col] }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Step 3: Model Configuration -->
        <div v-if="dataPreview.columns.length" class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            🎯 Step 3: Model Configuration
          </label>
          
          <!-- Target Column Selection -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Target Column (What to Predict)
            </label>
            <select
              v-model="modelConfig.targetColumn"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="">Select a column to predict...</option>
              <option
                v-for="col in dataPreview.columns"
                :key="col"
                :value="col"
              >
                {{ col }}
              </option>
            </select>
            <p class="mt-1 text-xs text-gray-500">
              Choose the column you want the model to predict (e.g., eviction_risk, renewal_probability)
            </p>
          </div>

          <!-- Model Type Selection -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Model Type
            </label>
            <select
              v-model="modelConfig.modelType"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="classification">Classification (Predict categories)</option>
              <option value="regression">Regression (Predict numbers)</option>
            </select>
            <p class="mt-1 text-xs text-gray-500">
              Classification for categories (e.g., high/medium/low risk), Regression for numbers (e.g., rent amount)
            </p>
          </div>

          <!-- Model Name -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Model Name
            </label>
            <input
              v-model="modelConfig.modelName"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="e.g., Eviction Risk Predictor"
            />
            <p class="mt-1 text-xs text-gray-500">
              Give your model a descriptive name for easy identification
            </p>
          </div>

          <!-- Advanced Options -->
          <div class="mb-4">
            <button
              @click="showAdvancedOptions = !showAdvancedOptions"
              class="text-sm text-indigo-600 hover:text-indigo-800 flex items-center"
            >
              <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
              Advanced Options
            </button>
            
            <div v-if="showAdvancedOptions" class="mt-3 p-4 bg-gray-50 rounded-lg">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Test Split (%)
                  </label>
                  <input
                    v-model="modelConfig.testSplit"
                    type="number"
                    min="10"
                    max="50"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <p class="mt-1 text-xs text-gray-500">
                    Percentage of data to use for testing (10-50%)
                  </p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Random State
                  </label>
                  <input
                    v-model="modelConfig.randomState"
                    type="number"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <p class="mt-1 text-xs text-gray-500">
                    For reproducible results (optional)
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 4: Train Model -->
        <div v-if="modelConfig.targetColumn && modelConfig.modelName" class="mb-6">
          <button
            @click="trainModel"
            :disabled="training"
            class="w-full px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <svg v-if="training" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ training ? 'Training Model...' : '🚀 Train Model' }}
          </button>
        </div>
      </div>

      <!-- Training Results -->
      <div v-if="trainingResult" class="bg-white rounded-lg shadow-sm border p-6 mb-8">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-semibold text-gray-900">✅ Training Complete!</h3>
          <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
            {{ trainingResult.accuracy }}% Accuracy
          </span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="font-medium text-gray-900 mb-2">Model Details</h4>
            <dl class="space-y-2 text-sm">
              <div class="flex justify-between">
                <dt class="text-gray-600">Model Name:</dt>
                <dd class="font-medium">{{ trainingResult.model_name }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Target Column:</dt>
                <dd class="font-medium">{{ trainingResult.target_column }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Model Type:</dt>
                <dd class="font-medium">{{ trainingResult.model_type }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Training Time:</dt>
                <dd class="font-medium">{{ trainingResult.training_time }}s</dd>
              </div>
            </dl>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 mb-2">Performance Metrics</h4>
            <dl class="space-y-2 text-sm">
              <div class="flex justify-between">
                <dt class="text-gray-600">Accuracy:</dt>
                <dd class="font-medium text-green-600">{{ trainingResult.accuracy }}%</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Precision:</dt>
                <dd class="font-medium">{{ trainingResult.precision }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">Recall:</dt>
                <dd class="font-medium">{{ trainingResult.recall }}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-gray-600">F1 Score:</dt>
                <dd class="font-medium">{{ trainingResult.f1_score }}</dd>
              </div>
            </dl>
          </div>
        </div>

        <div class="mt-6 flex space-x-4">
          <button
            @click="downloadModel(trainingResult.model_id)"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            📥 Download Model
          </button>
          <button
            @click="testModel(trainingResult.model_id)"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            🧪 Test Predictions
          </button>
          <button
            @click="deployModel(trainingResult.model_id)"
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            🚀 Deploy Model
          </button>
        </div>
      </div>

      <!-- Existing Models -->
      <div class="bg-white rounded-lg shadow-sm border">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">📊 Your Trained Models</h2>
          <p class="text-sm text-gray-600 mt-1">
            View and manage your trained machine learning models
          </p>
        </div>

        <div class="p-6">
          <!-- Empty State -->
          <div v-if="models.length === 0" class="text-center py-12 text-gray-500">
            <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            <p class="text-lg font-medium">No models trained yet</p>
            <p class="text-sm">Create your first model to get started</p>
            <button
              @click="showNewModelForm = true"
              class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Train Your First Model
            </button>
          </div>

          <!-- Models List -->
          <div v-else class="space-y-4">
            <div
              v-for="model in models"
              :key="model.model_id"
              class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-3">
                    <h3 class="text-lg font-medium text-gray-900">{{ model.model_name }}</h3>
                    <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                      {{ model.model_type }}
                    </span>
                    <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                      {{ model.accuracy }}% Accuracy
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">
                    Predicts: <strong>{{ model.target_column }}</strong> • 
                    Trained: {{ formatDate(model.created_at) }} • 
                    {{ model.training_samples }} samples
                  </p>
                </div>
                
                <div class="flex space-x-2">
                  <button
                    @click="testModel(model.model_id)"
                    class="px-3 py-1 text-sm bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors"
                  >
                    Test
                  </button>
                  <button
                    @click="downloadModel(model.model_id)"
                    class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                  >
                    Download
                  </button>
                  <button
                    @click="deleteModel(model.model_id)"
                    class="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Usage Examples -->
      <div class="mt-8 bg-white rounded-lg shadow-sm border p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">💡 Example Use Cases</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="border border-gray-200 rounded-lg p-4">
            <h4 class="font-medium text-gray-900 mb-2">🏠 Eviction Risk Prediction</h4>
            <p class="text-sm text-gray-600 mb-3">
              Predict which tenants are at risk of eviction based on payment history and behavior.
            </p>
            <div class="text-xs text-gray-500">
              <strong>Columns:</strong> rent_amount, late_payments, tenant_tenure, complaints
              <br><strong>Target:</strong> eviction_risk (high/medium/low)
            </div>
          </div>
          
          <div class="border border-gray-200 rounded-lg p-4">
            <h4 class="font-medium text-gray-900 mb-2">📋 Lease Renewal Probability</h4>
            <p class="text-sm text-gray-600 mb-3">
              Predict which tenants are likely to renew their leases based on satisfaction and history.
            </p>
            <div class="text-xs text-gray-500">
              <strong>Columns:</strong> tenant_tenure, rent_paid_on_time, maintenance_requests, satisfaction_score
              <br><strong>Target:</strong> renewal_probability (0-100%)
            </div>
          </div>
          
          <div class="border border-gray-200 rounded-lg p-4">
            <h4 class="font-medium text-gray-900 mb-2">🔧 Maintenance Risk Assessment</h4>
            <p class="text-sm text-gray-600 mb-3">
              Predict which units are likely to need maintenance based on age and usage patterns.
            </p>
            <div class="text-xs text-gray-500">
              <strong>Columns:</strong> unit_age, tenant_count, last_maintenance_date, unit_type
              <br><strong>Target:</strong> maintenance_risk (high/medium/low)
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Reactive data
const loading = ref(false)
const training = ref(false)
const showNewModelForm = ref(false)
const showAdvancedOptions = ref(false)
const selectedFile = ref(null)
const dataPreview = ref({ columns: [], rows: [], rowCount: 0 })
const models = ref([])
const trainingResult = ref(null)

// Model configuration
const modelConfig = ref({
  targetColumn: '',
  modelType: 'classification',
  modelName: '',
  testSplit: 20,
  randomState: 42
})

// Methods
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    await previewData(file)
  }
}

const handleDrop = async (event) => {
  const file = event.dataTransfer.files[0]
  if (file && file.type === 'text/csv') {
    selectedFile.value = file
    await previewData(file)
  }
}

const previewData = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axios.post('/api/ml/preview', formData)
    dataPreview.value = response.data
    
    // Auto-generate model name if empty
    if (!modelConfig.value.modelName) {
      modelConfig.value.modelName = `${modelConfig.value.targetColumn} Predictor`
    }
  } catch (error) {
    console.error('Failed to preview data:', error)
    alert('Failed to preview data. Please check your CSV file.')
  }
}

const trainModel = async () => {
  if (!selectedFile.value || !modelConfig.value.targetColumn || !modelConfig.value.modelName) {
    alert('Please complete all required fields.')
    return
  }

  try {
    training.value = true
    trainingResult.value = null
    
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('target_column', modelConfig.value.targetColumn)
    formData.append('model_type', modelConfig.value.modelType)
    formData.append('model_name', modelConfig.value.modelName)
    formData.append('test_split', modelConfig.value.testSplit)
    formData.append('random_state', modelConfig.value.randomState)
    
    const response = await axios.post('/api/ml/train', formData)
    trainingResult.value = response.data
    
    // Reset form and load updated models
    showNewModelForm.value = false
    await loadModels()
    
  } catch (error) {
    console.error('Failed to train model:', error)
    alert('Failed to train model. Please check your data and try again.')
  } finally {
    training.value = false
  }
}

const loadModels = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/ml/models')
    models.value = response.data.models || []
  } catch (error) {
    console.error('Failed to load models:', error)
  } finally {
    loading.value = false
  }
}

const testModel = async (modelId) => {
  try {
    const response = await axios.get(`/api/ml/test/${modelId}`)
    // Handle test results - could show a modal with test interface
    console.log('Test results:', response.data)
    alert('Test functionality coming soon!')
  } catch (error) {
    console.error('Failed to test model:', error)
    alert('Failed to test model.')
  }
}

const downloadModel = async (modelId) => {
  try {
    const response = await axios.get(`/api/ml/download/${modelId}`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `model_${modelId}.pkl`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Failed to download model:', error)
    alert('Failed to download model.')
  }
}

const deployModel = async (modelId) => {
  try {
    const response = await axios.post(`/api/ml/deploy/${modelId}`)
    alert('Model deployed successfully!')
  } catch (error) {
    console.error('Failed to deploy model:', error)
    alert('Failed to deploy model.')
  }
}

const deleteModel = async (modelId) => {
  if (!confirm('Are you sure you want to delete this model? This action cannot be undone.')) {
    return
  }
  
  try {
    await axios.delete(`/api/ml/models/${modelId}`)
    await loadModels()
  } catch (error) {
    console.error('Failed to delete model:', error)
    alert('Failed to delete model.')
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

// Initialize
onMounted(() => {
  loadModels()
})
</script>

<style scoped>
.modal {
  z-index: 1000;
}
</style> 