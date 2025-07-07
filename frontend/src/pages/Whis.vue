<template>
  <div class="whis-container">
    <!-- Header -->
    <div class="whis-header">
      <h1 class="whis-title">
        <span class="title-glow">Whis</span> Pipeline
      </h1>
      <div class="pipeline-status">
        <div class="status-indicator">
          <div class="status-dot active"></div>
          <span>Pipeline Active</span>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="whis-content">
      <!-- Input Section -->
      <div class="input-section">
        <div class="input-card">
          <h2>📝 Input Data</h2>
          
          <!-- Tab Navigation -->
          <div class="input-tabs">
            <button 
              v-for="tab in inputTabs" 
              :key="tab.id"
              :class="['tab-button', { active: activeTab === tab.id }]"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>

          <!-- Q&A Input -->
          <div v-if="activeTab === 'qa'" class="tab-content">
            <div class="input-group">
              <label>Question:</label>
              <textarea 
                v-model="qaInput.question" 
                placeholder="Enter your question here..."
                rows="3"
              ></textarea>
            </div>
            <div class="input-group">
              <label>Context (Optional):</label>
              <textarea 
                v-model="qaInput.context" 
                placeholder="Provide additional context..."
                rows="4"
              ></textarea>
            </div>
            <button class="btn-primary" @click="processQA">Process Question</button>
          </div>

          <!-- CSV Upload -->
          <div v-if="activeTab === 'csv'" class="tab-content">
            <div class="upload-area" @click="triggerFileUpload" @drop="handleFileDrop" @dragover.prevent>
              <div class="upload-icon">📁</div>
              <p>Drop your CSV file here or click to browse</p>
              <input 
                ref="fileInput" 
                type="file" 
                accept=".csv" 
                @change="handleFileSelect" 
                style="display: none"
              >
            </div>
            <div v-if="selectedFile" class="file-info">
              <p>Selected: {{ selectedFile.name }}</p>
              <button class="btn-secondary" @click="uploadFile">Upload & Process</button>
            </div>
          </div>

          <!-- Text Input -->
          <div v-if="activeTab === 'text'" class="tab-content">
            <div class="input-group">
              <label>Raw Text:</label>
              <textarea 
                v-model="textInput.content" 
                placeholder="Enter or paste your text here..."
                rows="8"
              ></textarea>
            </div>
            <button class="btn-primary" @click="processText">Process Text</button>
          </div>
        </div>
      </div>

      <!-- Pipeline Visualization -->
      <div class="pipeline-section">
        <div class="pipeline-card">
          <h2>🔄 Pipeline Flow</h2>
          <div class="pipeline-steps">
            <div 
              v-for="step in pipelineSteps" 
              :key="step.id"
              :class="['pipeline-step', step.status]"
            >
              <div class="step-icon">{{ step.icon }}</div>
              <div class="step-info">
                <h3>{{ step.name }}</h3>
                <p>{{ step.description }}</p>
                <div class="step-status">
                  <span class="status-badge" :class="step.status">
                    {{ step.status }}
                  </span>
                </div>
              </div>
              <div class="step-arrow" v-if="step.id < pipelineSteps.length">→</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div class="results-section">
        <div class="results-card">
          <h2>📊 Results</h2>
          <div v-if="results.length === 0" class="no-results">
            <p>No results yet. Start processing data to see results here.</p>
          </div>
          <div v-else class="results-list">
            <div v-for="result in results" :key="result.id" class="result-item">
              <div class="result-header">
                <h3>{{ result.title }}</h3>
                <span class="result-timestamp">{{ result.timestamp }}</span>
              </div>
              <div class="result-content">
                <p>{{ result.content }}</p>
              </div>
              <div class="result-metrics">
                <span class="metric">Confidence: {{ result.confidence }}%</span>
                <span class="metric">Processing Time: {{ result.processingTime }}s</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Whis',
  data() {
    return {
      activeTab: 'qa',
      inputTabs: [
        { id: 'qa', label: 'Q&A' },
        { id: 'csv', label: 'CSV Upload' },
        { id: 'text', label: 'Text Input' }
      ],
      qaInput: {
        question: '',
        context: ''
      },
      textInput: {
        content: ''
      },
      selectedFile: null,
      pipelineSteps: [
        {
          id: 1,
          name: 'Data Input',
          description: 'Receiving and validating input data',
          icon: '📥',
          status: 'pending'
        },
        {
          id: 2,
          name: 'Sanitize',
          description: 'Cleaning and preprocessing data',
          icon: '🧹',
          status: 'pending'
        },
        {
          id: 3,
          name: 'Smithing',
          description: 'Processing and transforming data',
          icon: '⚒️',
          status: 'pending'
        },
        {
          id: 4,
          name: 'Enhance',
          description: 'Adding context and improvements',
          icon: '✨',
          status: 'pending'
        },
        {
          id: 5,
          name: 'Logic',
          description: 'Applying business logic and rules',
          icon: '🧠',
          status: 'pending'
        },
        {
          id: 6,
          name: 'Output',
          description: 'Generating final results',
          icon: '📤',
          status: 'pending'
        }
      ],
      results: []
    }
  },
  methods: {
    processQA() {
      if (!this.qaInput.question.trim()) {
        alert('Please enter a question');
        return;
      }
      this.startPipeline();
    },
    processText() {
      if (!this.textInput.content.trim()) {
        alert('Please enter some text');
        return;
      }
      this.startPipeline();
    },
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file && file.type === 'text/csv') {
        this.selectedFile = file;
      } else {
        alert('Please select a valid CSV file');
      }
    },
    handleFileDrop(event) {
      event.preventDefault();
      const file = event.dataTransfer.files[0];
      if (file && file.type === 'text/csv') {
        this.selectedFile = file;
      } else {
        alert('Please drop a valid CSV file');
      }
    },
    uploadFile() {
      if (!this.selectedFile) {
        alert('Please select a file first');
        return;
      }
      this.startPipeline();
    },
    startPipeline() {
      // Reset pipeline status
      this.pipelineSteps.forEach(step => {
        step.status = 'pending';
      });

      // Simulate pipeline execution
      this.pipelineSteps.forEach((step, index) => {
        setTimeout(() => {
          step.status = 'running';
          this.$forceUpdate();
          
          setTimeout(() => {
            step.status = 'completed';
            this.$forceUpdate();
            
            // If this is the last step, add a result
            if (index === this.pipelineSteps.length - 1) {
              this.addResult();
            }
          }, 2000);
        }, index * 1000);
      });
    },
    addResult() {
      const result = {
        id: Date.now(),
        title: 'Processing Complete',
        content: 'Data has been successfully processed through the Whis pipeline.',
        timestamp: new Date().toLocaleString(),
        confidence: Math.floor(Math.random() * 30) + 70,
        processingTime: Math.floor(Math.random() * 10) + 5
      };
      this.results.unshift(result);
    }
  }
}
</script>

<style scoped>
.whis-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  padding: 2rem;
}

.whis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.whis-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.title-glow {
  background: linear-gradient(45deg, #00ff88, #00ffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
}

.pipeline-status {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ff4444;
  animation: pulse 2s infinite;
}

.status-dot.active {
  background: #00ff88;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.whis-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.input-section {
  grid-column: 1;
}

.pipeline-section {
  grid-column: 2;
}

.results-section {
  grid-column: 1 / -1;
  margin-top: 2rem;
}

.input-card, .pipeline-card, .results-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: fit-content;
}

.input-card h2, .pipeline-card h2, .results-card h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}

/* Input Tabs */
.input-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tab-button {
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-button.active {
  background: linear-gradient(45deg, #00ff88, #00ffff);
  color: #000;
  border-color: transparent;
}

.tab-button:hover {
  transform: translateY(-2px);
}

/* Input Groups */
.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

.input-group textarea {
  width: 100%;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #fff;
  font-family: inherit;
  resize: vertical;
}

.input-group textarea:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
}

/* Upload Area */
.upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.05);
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.upload-area p {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
}

.file-info {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.file-info p {
  margin: 0 0 1rem 0;
  color: rgba(255, 255, 255, 0.9);
}

/* Buttons */
.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(45deg, #00ff88, #00ffff);
  color: #000;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-primary:hover, .btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
}

/* Pipeline Steps */
.pipeline-steps {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pipeline-step {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.pipeline-step.running {
  border-color: #ffaa00;
  background: rgba(255, 170, 0, 0.1);
  animation: pulse 1s infinite;
}

.pipeline-step.completed {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.1);
}

.step-icon {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
}

.step-info {
  flex: 1;
}

.step-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.step-info p {
  margin: 0 0 0.5rem 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.step-arrow {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.5);
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.pending {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
}

.status-badge.running {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
}

.status-badge.completed {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
}

/* Results */
.no-results {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.5);
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.result-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.result-header h3 {
  margin: 0;
  font-size: 1.1rem;
}

.result-timestamp {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
}

.result-content p {
  margin: 0 0 1rem 0;
  color: rgba(255, 255, 255, 0.9);
}

.result-metrics {
  display: flex;
  gap: 1rem;
}

.metric {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .whis-content {
    grid-template-columns: 1fr;
  }
  
  .input-section, .pipeline-section {
    grid-column: 1;
  }
}

@media (max-width: 768px) {
  .whis-container {
    padding: 1rem;
  }
  
  .whis-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .whis-title {
    font-size: 2rem;
  }
  
  .pipeline-step {
    flex-direction: column;
    text-align: center;
  }
  
  .step-arrow {
    transform: rotate(90deg);
  }
}
</style> 