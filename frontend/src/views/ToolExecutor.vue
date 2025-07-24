<template>
  <div class="tool-executor">
    <!-- Header -->
    <div class="header">
      <h1 class="title">🔧 MCP Tool Executor</h1>
      <p class="subtitle">Execute saved MCP tools and view their output</p>
    </div>

    <!-- Main Content -->
    <div class="content">
      <!-- Tool Selection -->
      <div class="tool-selection">
        <h2 class="section-title">Select Tool</h2>
        <div class="tool-selector">
          <select 
            v-model="selectedTool" 
            class="tool-select"
            @change="onToolSelect"
          >
            <option value="" disabled>Choose a saved tool...</option>
            <option 
              v-for="tool in tools" 
              :key="tool.name" 
              :value="tool"
            >
              {{ tool.name }} - {{ tool.description }}
            </option>
          </select>
          
          <button 
            @click="refreshTools" 
            class="refresh-btn"
            :disabled="loading"
          >
            🔄 Refresh
          </button>
        </div>

        <!-- Tool Info -->
        <div v-if="selectedTool" class="tool-info">
          <h3>Tool Details</h3>
          <div class="info-grid">
            <div class="info-item">
              <strong>Name:</strong> {{ selectedTool.name }}
            </div>
            <div class="info-item">
              <strong>Type:</strong> {{ selectedTool.task_type }}
            </div>
            <div class="info-item">
              <strong>Tags:</strong> 
              <span v-for="tag in selectedTool.tags" :key="tag" class="tag">
                {{ tag }}
              </span>
            </div>
            <div class="info-item full-width">
              <strong>Description:</strong> {{ selectedTool.description }}
            </div>
            <div class="info-item full-width">
              <strong>Command:</strong>
              <code class="command">{{ selectedTool.command }}</code>
            </div>
          </div>
        </div>
      </div>

      <!-- Execution Controls -->
      <div class="execution-controls">
        <h2 class="section-title">Execution</h2>
        <div class="controls">
          <div class="timeout-control">
            <label for="timeout">Timeout (seconds):</label>
            <input 
              id="timeout"
              v-model.number="timeout" 
              type="number" 
              min="5" 
              max="300" 
              class="timeout-input"
            />
          </div>
          
          <button 
            @click="runTool" 
            class="run-btn"
            :disabled="!selectedTool || executing"
          >
            {{ executing ? '🔄 Running...' : '▶️ Run Tool' }}
          </button>
        </div>
      </div>

      <!-- Results -->
      <div v-if="executionResult" class="results">
        <h2 class="section-title">Execution Results</h2>
        
        <!-- Status -->
        <div class="status-bar" :class="{ success: executionResult.success, error: !executionResult.success }">
          <span class="status-icon">
            {{ executionResult.success ? '✅' : '❌' }}
          </span>
          <span class="status-text">
            {{ executionResult.success ? 'Success' : 'Failed' }}
          </span>
          <span class="execution-time">
            ({{ executionResult.execution_time }}s)
          </span>
          <span class="return-code">
            Return code: {{ executionResult.returncode }}
          </span>
        </div>

        <!-- Output -->
        <div class="output-section">
          <div class="output-tabs">
            <button 
              @click="activeTab = 'stdout'" 
              class="tab-btn"
              :class="{ active: activeTab === 'stdout' }"
            >
              Standard Output
            </button>
            <button 
              @click="activeTab = 'stderr'" 
              class="tab-btn"
              :class="{ active: activeTab === 'stderr' }"
            >
              Error Output
            </button>
            <button 
              @click="activeTab = 'details'" 
              class="tab-btn"
              :class="{ active: activeTab === 'details' }"
            >
              Details
            </button>
          </div>

          <div class="output-content">
            <!-- Standard Output -->
            <div v-if="activeTab === 'stdout'" class="output-panel">
              <pre class="output-text">{{ executionResult.stdout || '(No output)' }}</pre>
            </div>

            <!-- Error Output -->
            <div v-if="activeTab === 'stderr'" class="output-panel">
              <pre class="output-text error">{{ executionResult.stderr || '(No errors)' }}</pre>
            </div>

            <!-- Details -->
            <div v-if="activeTab === 'details'" class="output-panel">
              <div class="details-grid">
                <div class="detail-item">
                  <strong>Command:</strong>
                  <code>{{ executionResult.command }}</code>
                </div>
                <div class="detail-item">
                  <strong>Execution Time:</strong>
                  {{ executionResult.execution_time }} seconds
                </div>
                <div class="detail-item">
                  <strong>Return Code:</strong>
                  {{ executionResult.returncode }}
                </div>
                <div class="detail-item">
                  <strong>Timestamp:</strong>
                  {{ formatTimestamp(executionResult.timestamp) }}
                </div>
                <div class="detail-item">
                  <strong>Tool Name:</strong>
                  {{ executionResult.tool_name || 'Custom command' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics -->
      <div class="statistics">
        <h2 class="section-title">Execution Statistics</h2>
        <div v-if="stats" class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">{{ stats.total_executions }}</div>
            <div class="stat-label">Total Executions</div>
          </div>
          <div class="stat-card">
            <div class="stat-number success">{{ stats.successful_executions }}</div>
            <div class="stat-label">Successful</div>
          </div>
          <div class="stat-card">
            <div class="stat-number error">{{ stats.failed_executions }}</div>
            <div class="stat-label">Failed</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.success_rate }}%</div>
            <div class="stat-label">Success Rate</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.average_execution_time }}s</div>
            <div class="stat-label">Avg Time</div>
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
const tools = ref([])
const selectedTool = ref('')
const timeout = ref(30)
const executing = ref(false)
const executionResult = ref(null)
const activeTab = ref('stdout')
const stats = ref(null)
const loading = ref(false)

// Load tools on mount
onMounted(async () => {
  await loadTools()
  await loadStats()
})

// Methods
const loadTools = async () => {
  try {
    loading.value = true
    const response = await axios.get('/mcp-tool/mcp-tool/list')
    tools.value = response.data
  } catch (error) {
    console.error('Failed to load tools:', error)
    tools.value = []
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await axios.get('/executor/tool-stats')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load stats:', error)
    stats.value = null
  }
}

const refreshTools = async () => {
  await loadTools()
  await loadStats()
}

const onToolSelect = () => {
  // Clear previous results when selecting a new tool
  executionResult.value = null
  activeTab.value = 'stdout'
}

const runTool = async () => {
  if (!selectedTool.value) return

  try {
    executing.value = true
    executionResult.value = null

    const response = await axios.post('/executor/execute-saved-tool/' + selectedTool.value.name, {
      timeout: timeout.value
    })

    executionResult.value = response.data
    activeTab.value = 'stdout'

    // Refresh stats after execution
    await loadStats()

  } catch (error) {
    console.error('Tool execution failed:', error)
    executionResult.value = {
      success: false,
      stdout: '',
      stderr: error.response?.data?.detail || error.message,
      returncode: -1,
      execution_time: 0,
      command: selectedTool.value?.command || '',
      timestamp: new Date().toISOString()
    }
  } finally {
    executing.value = false
  }
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'Unknown'
  return new Date(timestamp).toLocaleString()
}
</script>

<style scoped>
.tool-executor {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.1rem;
  color: #64748b;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

.tool-selection {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.tool-selector {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.tool-select {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
}

.tool-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.refresh-btn {
  padding: 0.75rem 1rem;
  background: #64748b;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.refresh-btn:hover:not(:disabled) {
  background: #475569;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tool-info {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.tag {
  display: inline-block;
  background: #3b82f6;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  margin-right: 0.5rem;
  margin-bottom: 0.25rem;
}

.command {
  background: #1e293b;
  color: #e2e8f0;
  padding: 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  word-break: break-all;
}

.execution-controls {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.controls {
  display: flex;
  gap: 1rem;
  align-items: end;
}

.timeout-control {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.timeout-control label {
  font-weight: 500;
  color: #374151;
}

.timeout-input {
  padding: 0.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  width: 100px;
}

.run-btn {
  padding: 0.75rem 2rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
}

.run-btn:hover:not(:disabled) {
  background: #059669;
}

.run-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.results {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.status-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-weight: 500;
}

.status-bar.success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.status-bar.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.status-icon {
  font-size: 1.25rem;
}

.execution-time {
  color: #6b7280;
  font-weight: normal;
}

.return-code {
  margin-left: auto;
  font-weight: normal;
}

.output-section {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.output-tabs {
  display: flex;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 500;
  color: #64748b;
  border-bottom: 2px solid transparent;
}

.tab-btn:hover {
  background: #f1f5f9;
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
  background: white;
}

.output-content {
  background: white;
}

.output-panel {
  padding: 1rem;
  min-height: 200px;
}

.output-text {
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}

.output-text.error {
  color: #dc2626;
}

.details-grid {
  display: grid;
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item code {
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}

.statistics {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  text-align: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.stat-number.success {
  color: #10b981;
}

.stat-number.error {
  color: #dc2626;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

@media (max-width: 768px) {
  .tool-executor {
    padding: 1rem;
  }
  
  .tool-selector {
    flex-direction: column;
  }
  
  .controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style> 