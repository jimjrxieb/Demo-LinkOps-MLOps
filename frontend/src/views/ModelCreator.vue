<template>
  <div class="model-creator">
    <div class="header">
      <h1>🧠 ML Model Creator</h1>
      <p>Train machine learning models with your data - no coding required!</p>
    </div>

    <!-- CSV Upload Section -->
    <div class="upload-section">
      <h2>📁 Step 1: Upload Your Data</h2>
      <div 
        class="upload-dropzone"
        :class="{ 'dragover': isDragOver, 'has-file': uploadedFile }"
        @drop="handleDrop"
        @dragover.prevent="isDragOver = true"
        @dragleave.prevent="isDragOver = false"
        @click="triggerFileInput"
      >
        <input
          ref="fileInput"
          type="file"
          accept=".csv"
          @change="handleFileSelect"
          style="display: none"
        />
        
        <div v-if="!uploadedFile" class="upload-placeholder">
          <div class="upload-icon">📄</div>
          <p>Drop your CSV file here or click to browse</p>
          <p class="upload-hint">Supports .csv files with headers</p>
        </div>
        
        <div v-else class="upload-success">
          <div class="file-info">
            <span class="file-icon">✅</span>
            <span class="file-name">{{ uploadedFile.name }}</span>
            <span class="file-size">({{ formatFileSize(uploadedFile.size) }})</span>
          </div>
          <button @click.stop="removeFile" class="remove-btn">Remove</button>
        </div>
      </div>
    </div>

    <!-- Model Configuration Section -->
    <div v-if="uploadedFile && csvHeaders.length > 0" class="config-section">
      <h2>⚙️ Step 2: Configure Your Model</h2>
      
      <div class="config-grid">
        <!-- Model Name -->
        <div class="config-item">
          <label for="modelName">🏷️ Model Name</label>
          <input
            id="modelName"
            v-model="modelConfig.name"
            type="text"
            placeholder="e.g., maintenance_predictor"
            class="form-input"
          />
        </div>

        <!-- Target Column -->
        <div class="config-item">
          <label for="targetColumn">🎯 Target Column (What to predict)</label>
          <select
            id="targetColumn"
            v-model="modelConfig.targetColumn"
            class="form-select"
          >
            <option value="">Select target column...</option>
            <option
              v-for="header in csvHeaders"
              :key="header"
              :value="header"
            >
              {{ header }}
            </option>
          </select>
        </div>

        <!-- Feature Columns -->
        <div class="config-item full-width">
          <label>🔧 Feature Columns (What to use for prediction)</label>
          <div class="feature-checkboxes">
            <div
              v-for="header in csvHeaders"
              :key="header"
              class="feature-item"
            >
              <input
                :id="`feature-${header}`"
                type="checkbox"
                :value="header"
                v-model="modelConfig.features"
                :disabled="header === modelConfig.targetColumn"
              />
              <label :for="`feature-${header}`">
                {{ header }}
                <span v-if="header === modelConfig.targetColumn" class="target-indicator">
                  (target)
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Training Section -->
    <div v-if="canTrain" class="training-section">
      <h2>🚀 Step 3: Train Your Model</h2>
      
      <div class="training-controls">
        <button
          @click="trainModel"
          :disabled="isTraining"
          class="train-btn"
          :class="{ 'training': isTraining }"
        >
          <span v-if="!isTraining">🚀 Train Model</span>
          <span v-else>🔄 Training... Please wait</span>
        </button>
      </div>

      <!-- Training Progress -->
      <div v-if="isTraining" class="training-progress">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: trainingProgress + '%' }"></div>
        </div>
        <p class="progress-text">{{ trainingStatus }}</p>
      </div>

      <!-- Training Results -->
      <div v-if="trainingResult" class="training-results">
        <div class="result-header">
          <h3>✅ Training Complete!</h3>
          <button @click="downloadSummary" class="download-btn">📥 Download Summary</button>
        </div>

        <div class="result-grid">
          <div class="result-card">
            <h4>📊 Model Performance</h4>
            <div class="metrics">
              <div class="metric">
                <span class="metric-label">Mean Absolute Error:</span>
                <span class="metric-value">{{ trainingResult.mae.toFixed(2) }}</span>
              </div>
              <div class="metric">
                <span class="metric-label">R² Score:</span>
                <span class="metric-value">{{ trainingResult.r2.toFixed(3) }}</span>
              </div>
            </div>
          </div>

          <div class="result-card">
            <h4>🏗️ Top Contractors</h4>
            <div class="contractors-list">
              <div
                v-for="(contractor, index) in trainingResult.contractor_recommendations.slice(0, 5)"
                :key="contractor.contractor"
                class="contractor-item"
              >
                <span class="rank">#{{ index + 1 }}</span>
                <span class="name">{{ contractor.contractor }}</span>
                <span class="score">Score: {{ contractor.quality_score?.toFixed(1) || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Training Error -->
      <div v-if="trainingError" class="training-error">
        <h3>❌ Training Failed</h3>
        <p>{{ trainingError }}</p>
        <button @click="resetTraining" class="retry-btn">🔄 Try Again</button>
      </div>
    </div>

    <!-- Model History Section -->
    <div class="history-section">
      <h2>📋 Trained Models History</h2>
      <div class="history-controls">
        <button @click="loadModelHistory" class="refresh-btn">🔄 Refresh</button>
      </div>
      
      <div v-if="modelHistory.length === 0" class="no-models">
        <p>No trained models found. Train your first model above!</p>
      </div>
      
      <div v-else class="models-grid">
        <div
          v-for="model in modelHistory"
          :key="model.name"
          class="model-card"
        >
          <div class="model-header">
            <h4>{{ model.name }}</h4>
            <span class="model-date">{{ formatDate(model.date) }}</span>
          </div>
          <div class="model-details">
            <p><strong>Target:</strong> {{ model.target }}</p>
            <p><strong>Features:</strong> {{ model.features.length }}</p>
            <p><strong>MAE:</strong> {{ model.mae?.toFixed(2) || 'N/A' }}</p>
            <p><strong>R²:</strong> {{ model.r2?.toFixed(3) || 'N/A' }}</p>
          </div>
          <div class="model-actions">
            <button @click="downloadModelSummary(model.name)" class="action-btn">
              📥 Summary
            </button>
            <button @click="deleteModel(model.name)" class="action-btn delete">
              🗑️ Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useTrainModelStore } from '../store/train_model.js'

export default {
  name: 'ModelCreator',
  setup() {
    const trainModelStore = useTrainModelStore()
    
    // File upload state
    const fileInput = ref(null)
    const uploadedFile = ref(null)
    const isDragOver = ref(false)
    const csvHeaders = ref([])
    
    // Model configuration
    const modelConfig = ref({
      name: '',
      targetColumn: '',
      features: []
    })
    
    // Training state
    const isTraining = ref(false)
    const trainingProgress = ref(0)
    const trainingStatus = ref('')
    const trainingResult = ref(null)
    const trainingError = ref(null)
    
    // Model history
    const modelHistory = ref([])
    
    // Computed properties
    const canTrain = computed(() => {
      return uploadedFile.value && 
             modelConfig.value.name && 
             modelConfig.value.targetColumn && 
             modelConfig.value.features.length > 0
    })
    
    // Methods
    const triggerFileInput = () => {
      fileInput.value?.click()
    }
    
    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        processFile(file)
      }
    }
    
    const handleDrop = (event) => {
      event.preventDefault()
      isDragOver.value = false
      
      const file = event.dataTransfer.files[0]
      if (file && file.type === 'text/csv') {
        processFile(file)
      }
    }
    
    const processFile = async (file) => {
      uploadedFile.value = file
      
      try {
        const text = await file.text()
        const lines = text.split('\n')
        const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''))
        
        csvHeaders.value = headers
        modelConfig.value.features = headers.filter(h => h !== modelConfig.value.targetColumn)
        
        // Auto-generate model name if empty
        if (!modelConfig.value.name) {
          modelConfig.value.name = `${file.name.replace('.csv', '')}_predictor`
        }
      } catch (error) {
        console.error('Error processing CSV:', error)
        alert('Error reading CSV file. Please check the file format.')
      }
    }
    
    const removeFile = () => {
      uploadedFile.value = null
      csvHeaders.value = []
      modelConfig.value = {
        name: '',
        targetColumn: '',
        features: []
      }
      trainingResult.value = null
      trainingError.value = null
    }
    
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const trainModel = async () => {
      if (!canTrain.value) return
      
      isTraining.value = true
      trainingProgress.value = 0
      trainingStatus.value = 'Preparing data...'
      trainingResult.value = null
      trainingError.value = null
      
      try {
        // Upload file first
        trainingProgress.value = 20
        trainingStatus.value = 'Uploading data...'
        
        const formData = new FormData()
        formData.append('file', uploadedFile.value)
        
        const uploadResponse = await fetch('/api/upload-csv', {
          method: 'POST',
          body: formData
        })
        
        if (!uploadResponse.ok) {
          throw new Error('Failed to upload file')
        }
        
        const uploadResult = await uploadResponse.json()
        const csvPath = uploadResult.path
        
        // Train model
        trainingProgress.value = 50
        trainingStatus.value = 'Training model...'
        
        const trainResponse = await fetch('/api/train-model', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            model_name: modelConfig.value.name,
            target_column: modelConfig.value.targetColumn,
            features: modelConfig.value.features,
            csv_path: csvPath
          })
        })
        
        if (!trainResponse.ok) {
          const errorData = await trainResponse.json()
          throw new Error(errorData.detail || 'Training failed')
        }
        
        trainingProgress.value = 100
        trainingStatus.value = 'Training complete!'
        
        const result = await trainResponse.json()
        trainingResult.value = result
        
        // Reload model history
        await loadModelHistory()
        
      } catch (error) {
        console.error('Training error:', error)
        trainingError.value = error.message
      } finally {
        isTraining.value = false
      }
    }
    
    const resetTraining = () => {
      trainingError.value = null
      trainingResult.value = null
    }
    
    const downloadSummary = () => {
      if (!trainingResult.value) return
      
      const dataStr = JSON.stringify(trainingResult.value, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `${modelConfig.value.name}_summary.json`
      link.click()
      
      URL.revokeObjectURL(url)
    }
    
    const loadModelHistory = async () => {
      try {
        const response = await fetch('/api/train-model/models')
        if (response.ok) {
          modelHistory.value = await response.json()
        }
      } catch (error) {
        console.error('Error loading model history:', error)
      }
    }
    
    const downloadModelSummary = async (modelName) => {
      try {
        const response = await fetch(`/api/train-model/models/${modelName}/summary`)
        if (response.ok) {
          const summary = await response.json()
          const dataStr = JSON.stringify(summary, null, 2)
          const dataBlob = new Blob([dataStr], { type: 'application/json' })
          const url = URL.createObjectURL(dataBlob)
          
          const link = document.createElement('a')
          link.href = url
          link.download = `${modelName}_summary.json`
          link.click()
          
          URL.revokeObjectURL(url)
        }
      } catch (error) {
        console.error('Error downloading summary:', error)
      }
    }
    
    const deleteModel = async (modelName) => {
      if (!confirm(`Are you sure you want to delete model "${modelName}"?`)) {
        return
      }
      
      try {
        const response = await fetch(`/api/train-model/${modelName}`, {
          method: 'DELETE'
        })
        
        if (response.ok) {
          await loadModelHistory()
        } else {
          alert('Failed to delete model')
        }
      } catch (error) {
        console.error('Error deleting model:', error)
        alert('Error deleting model')
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }
    
    // Load model history on mount
    onMounted(() => {
      loadModelHistory()
    })
    
    return {
      fileInput,
      uploadedFile,
      isDragOver,
      csvHeaders,
      modelConfig,
      isTraining,
      trainingProgress,
      trainingStatus,
      trainingResult,
      trainingError,
      modelHistory,
      canTrain,
      triggerFileInput,
      handleFileSelect,
      handleDrop,
      removeFile,
      formatFileSize,
      trainModel,
      resetTraining,
      downloadSummary,
      loadModelHistory,
      downloadModelSummary,
      deleteModel,
      formatDate
    }
  }
}
</script>

<style scoped>
.model-creator {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.header p {
  font-size: 1.1rem;
  color: #7f8c8d;
}

.upload-section,
.config-section,
.training-section,
.history-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.upload-section h2,
.config-section h2,
.training-section h2,
.history-section h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.upload-dropzone {
  border: 3px dashed #3498db;
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.upload-dropzone:hover {
  border-color: #2980b9;
  background: #ecf0f1;
}

.upload-dropzone.dragover {
  border-color: #27ae60;
  background: #e8f5e8;
}

.upload-dropzone.has-file {
  border-color: #27ae60;
  background: #e8f5e8;
}

.upload-placeholder .upload-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.upload-placeholder p {
  margin: 0.5rem 0;
  color: #7f8c8d;
}

.upload-hint {
  font-size: 0.9rem;
  color: #95a5a6;
}

.upload-success {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.file-icon {
  font-size: 1.5rem;
}

.file-name {
  font-weight: bold;
  color: #27ae60;
}

.file-size {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.remove-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.remove-btn:hover {
  background: #c0392b;
}

.config-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.config-item {
  display: flex;
  flex-direction: column;
}

.config-item.full-width {
  grid-column: 1 / -1;
}

.config-item label {
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.form-input,
.form-select {
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #3498db;
}

.feature-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
  border: 2px solid #ddd;
  border-radius: 6px;
  padding: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.feature-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.feature-item label {
  margin: 0;
  cursor: pointer;
  font-weight: normal;
}

.target-indicator {
  color: #e74c3c;
  font-size: 0.8rem;
}

.training-controls {
  text-align: center;
  margin-bottom: 2rem;
}

.train-btn {
  background: #27ae60;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.train-btn:hover:not(:disabled) {
  background: #229954;
  transform: translateY(-2px);
}

.train-btn:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.train-btn.training {
  background: #f39c12;
}

.training-progress {
  margin: 2rem 0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3498db, #27ae60);
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  color: #7f8c8d;
  font-weight: bold;
}

.training-results {
  background: #e8f5e8;
  border-radius: 8px;
  padding: 2rem;
  margin-top: 2rem;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.result-header h3 {
  color: #27ae60;
  margin: 0;
}

.download-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.download-btn:hover {
  background: #2980b9;
}

.result-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.result-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-card h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.metrics {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric-label {
  font-weight: bold;
  color: #7f8c8d;
}

.metric-value {
  font-weight: bold;
  color: #27ae60;
  font-size: 1.1rem;
}

.contractors-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contractor-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.rank {
  background: #3498db;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
}

.name {
  flex: 1;
  font-weight: bold;
}

.score {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.training-error {
  background: #fdf2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 2rem;
}

.training-error h3 {
  color: #dc2626;
  margin-bottom: 1rem;
}

.retry-btn {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
}

.retry-btn:hover {
  background: #b91c1c;
}

.history-controls {
  margin-bottom: 1.5rem;
}

.refresh-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.refresh-btn:hover {
  background: #2980b9;
}

.no-models {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
  background: #f8f9fa;
  border-radius: 8px;
}

.models-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.model-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #ecf0f1;
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
}

.model-header h4 {
  color: #2c3e50;
  margin: 0;
}

.model-date {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.model-details {
  margin-bottom: 1.5rem;
}

.model-details p {
  margin: 0.25rem 0;
  color: #7f8c8d;
}

.model-details strong {
  color: #2c3e50;
}

.model-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.action-btn:hover {
  background: #2980b9;
}

.action-btn.delete {
  background: #e74c3c;
}

.action-btn.delete:hover {
  background: #c0392b;
}

@media (max-width: 768px) {
  .model-creator {
    padding: 1rem;
  }
  
  .config-grid {
    grid-template-columns: 1fr;
  }
  
  .result-grid {
    grid-template-columns: 1fr;
  }
  
  .models-grid {
    grid-template-columns: 1fr;
  }
  
  .upload-dropzone {
    padding: 2rem;
  }
  
  .result-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
}
</style> 