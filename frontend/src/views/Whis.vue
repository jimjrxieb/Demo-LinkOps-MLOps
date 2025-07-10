<template>
  <div class="whis-page">
    <div class="page-header">
      <h1 class="page-title">Whis Pipeline</h1>
      <p class="page-subtitle">Data Processing & Enhancement Workflow</p>
    </div>

    <!-- Pipeline Visualization -->
    <WhisPipeline
      :pipeline-data="pipelineData"
      :current-step="currentStep"
      @step-click="handleStepClick"
    />

    <!-- Input Section -->
    <section class="input-section">
      <h2 class="section-title">Data Input</h2>
      <div class="input-container">
        <textarea
          v-model="inputData"
          placeholder="Enter your data here or paste JSON/CSV content..."
          class="data-input"
          rows="8"
        />
        <div class="input-actions">
          <button class="btn primary" @click="processData">
            <span class="btn-icon">⚡</span>
            Process Data
          </button>
          <button class="btn secondary" @click="loadSampleData">
            <span class="btn-icon">📋</span>
            Load Sample
          </button>
          <button class="btn secondary" @click="clearData">
            <span class="btn-icon">🗑️</span>
            Clear
          </button>
        </div>
      </div>
    </section>

    <!-- Results Section -->
    <section v-if="results.length > 0" class="results-section">
      <h2 class="section-title">Processing Results</h2>
      <div class="results-container">
        <div
          v-for="(result, index) in results"
          :key="index"
          class="result-card"
        >
          <div class="result-header">
            <h3>{{ result.step }}</h3>
            <span class="result-status" :class="result.status">
              {{ result.status }}
            </span>
          </div>
          <div class="result-content">
            <p><strong>Input:</strong> {{ result.input }}</p>
            <p><strong>Output:</strong> {{ result.output }}</p>
            <p v-if="result.metrics">
              <strong>Metrics:</strong> {{ result.metrics }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Configuration Panel -->
    <section class="config-section">
      <h2 class="section-title">Pipeline Configuration</h2>
      <div class="config-grid">
        <div class="config-card">
          <h3>Data Sanitization</h3>
          <label>
            <input v-model="config.sanitize" type="checkbox" />
            Enable data cleaning
          </label>
          <label>
            <input v-model="config.removeDuplicates" type="checkbox" />
            Remove duplicates
          </label>
        </div>

        <div class="config-card">
          <h3>Data Enhancement</h3>
          <label>
            <input v-model="config.enhance" type="checkbox" />
            Enable enhancement
          </label>
          <label>
            <input v-model="config.validate" type="checkbox" />
            Validate output
          </label>
        </div>

        <div class="config-card">
          <h3>Output Format</h3>
          <select v-model="config.outputFormat" class="format-select">
            <option value="json">JSON</option>
            <option value="csv">CSV</option>
            <option value="xml">XML</option>
          </select>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import WhisPipeline from '../components/WhisPipeline.vue';

export default {
  name: 'Whis',
  components: {
    WhisPipeline,
  },
  data() {
    return {
      inputData: '',
      currentStep: 0,
      results: [],
      config: {
        sanitize: true,
        removeDuplicates: true,
        enhance: true,
        validate: true,
        outputFormat: 'json',
      },
      pipelineData: [
        {
          id: 1,
          name: 'Data Input',
          description: 'Raw data ingestion',
          status: 'pending',
          icon: '📥',
        },
        {
          id: 2,
          name: 'Sanitization',
          description: 'Clean and validate data',
          status: 'pending',
          icon: '🧹',
        },
        {
          id: 3,
          name: 'Smithing',
          description: 'Transform and structure',
          status: 'pending',
          icon: '⚒️',
        },
        {
          id: 4,
          name: 'Enhancement',
          description: 'Add ML enhancements',
          status: 'pending',
          icon: '✨',
        },
        {
          id: 5,
          name: 'Output',
          description: 'Final processed data',
          status: 'pending',
          icon: '📤',
        },
      ],
    };
  },
  methods: {
    async processData() {
      if (!this.inputData.trim()) {
        alert('Please enter some data to process');
        return;
      }

      this.results = [];
      this.currentStep = 0;

      // Simulate pipeline processing
      for (let i = 0; i < this.pipelineData.length; i++) {
        this.currentStep = i;
        this.pipelineData[i].status = 'processing';

        // Simulate processing delay
        await new Promise((resolve) => setTimeout(resolve, 1000));

        // Process step
        const result = await this.processStep(i, this.inputData);
        this.results.push(result);

        this.pipelineData[i].status = 'completed';
      }

      this.currentStep = this.pipelineData.length;
    },

    async processStep(stepIndex, data) {
      switch (stepIndex) {
        case 0: // Data Input
          return {
            step: 'Data Input',
            status: 'success',
            input: 'Raw data',
            output: `${data.length} characters received`,
            metrics: {
              characters: data.length,
              lines: data.split('\n').length,
            },
          };

        case 1: // Sanitization
          return {
            step: 'Data Sanitization',
            status: 'success',
            input: `${data.length} characters`,
            output: `${data.length - 10} characters (cleaned)`,
            metrics: { cleaned: data.length - 10, removed: 10 },
          };

        case 2: // Smithing
          return {
            step: 'Data Smithing',
            status: 'success',
            input: `${data.length - 10} characters`,
            output: 'Structured data object',
            metrics: { structured: true, fields: 5 },
          };

        case 3: // Enhancement
          return {
            step: 'Data Enhancement',
            status: 'success',
            input: 'Structured data',
            output: 'Enhanced with ML features',
            metrics: { enhanced: true, features: 8 },
          };

        case 4: // Output
          return {
            step: 'Data Output',
            status: 'success',
            input: 'Enhanced data',
            output: `Final ${this.config.outputFormat.toUpperCase()} output`,
            metrics: { format: this.config.outputFormat, size: '2.5KB' },
          };

        default:
          return {
            step: 'Unknown Step',
            status: 'error',
            input: 'Unknown',
            output: 'Error occurred',
            metrics: { error: true, message: 'Unknown step' },
          };
      }
    },

    handleStepClick() {
      // Show step details or configuration
    },

    loadSampleData() {
      this.inputData = `{
  "name": "Sample Data",
  "values": [1, 2, 3, 4, 5],
  "metadata": {
    "source": "test",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}`;
    },

    clearData() {
      this.inputData = '';
      this.results = [];
      this.currentStep = 0;
      this.pipelineData.forEach((step) => {
        step.status = 'pending';
      });
    },
  },
};
</script>
<style scoped>
.whis-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 3rem;
  font-weight: bold;
  background: linear-gradient(45deg, #00d4ff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1.2rem;
  color: #888;
  margin: 0;
}

.input-section,
.results-section,
.config-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2rem;
  color: #00d4ff;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #00d4ff;
  padding-bottom: 0.5rem;
}

.input-container {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.data-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #333;
  border-radius: 8px;
  padding: 1rem;
  color: #e0e0e0;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  resize: vertical;
  margin-bottom: 1rem;
}

.data-input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

.input-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn.primary {
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  color: white;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.btn.secondary {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  color: #00d4ff;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.btn-icon {
  font-size: 1.1rem;
}

.results-container {
  display: grid;
  gap: 1.5rem;
}

.result-card {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.result-header h3 {
  margin: 0;
  color: #00d4ff;
}

.result-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.result-status.success {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
  border: 1px solid #00ff00;
}

.result-status.error {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
  border: 1px solid #ff0000;
}

.result-content p {
  margin: 0.5rem 0;
  color: #e0e0e0;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.config-card {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.config-card h3 {
  color: #00d4ff;
  margin-bottom: 1rem;
}

.config-card label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  color: #e0e0e0;
  cursor: pointer;
}

.config-card input[type='checkbox'] {
  width: 18px;
  height: 18px;
  accent-color: #00d4ff;
}

.format-select {
  width: 100%;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #333;
  border-radius: 8px;
  padding: 0.75rem;
  color: #e0e0e0;
  font-size: 1rem;
}

.format-select:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .input-actions {
    flex-direction: column;
  }

  .btn {
    justify-content: center;
  }

  .config-grid {
    grid-template-columns: 1fr;
  }
}
</style>
