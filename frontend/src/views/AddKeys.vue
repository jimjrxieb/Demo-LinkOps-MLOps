<template>
  <div class="add-keys">
    <!-- Header Section -->
    <div class="header-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">🔑 API Key Management</h2>
          <p class="text-gray-600">
            Configure AI API keys to enable enhanced features and real AI
            processing
          </p>
        </div>
        <div class="card-body">
          <div class="demo-notice">
            <div class="notice-icon">🎯</div>
            <div class="notice-content">
              <h4>Demo Mode Active</h4>
              <p>
                Currently running in demo mode with simulated responses. Add API
                keys to enable real AI processing.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- API Keys Form -->
    <div class="keys-section">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Configure API Keys</h3>
        </div>
        <div class="card-body">
          <form class="keys-form" @submit.prevent="saveKeys">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🤖</span>
                  OpenAI API Key
                </label>
                <input
                  v-model="apiKeys.openai"
                  type="password"
                  class="form-input"
                  placeholder="sk-..."
                  :disabled="isDemoMode"
                />
                <p class="form-help">
                  Used for GPT-4 task processing and code generation
                </p>
              </div>

              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🧠</span>
                  Grok API Key
                </label>
                <input
                  v-model="apiKeys.grok"
                  type="password"
                  class="form-input"
                  placeholder="grok_..."
                  :disabled="isDemoMode"
                />
                <p class="form-help">
                  Used for advanced reasoning and complex task analysis
                </p>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">
                  <span class="label-icon">🔍</span>
                  Anthropic API Key
                </label>
                <input
                  v-model="apiKeys.anthropic"
                  type="password"
                  class="form-input"
                  placeholder="sk-ant-..."
                  :disabled="isDemoMode"
                />
                <p class="form-help">
                  Used for Claude-based reasoning and analysis
                </p>
              </div>

              <div class="form-group">
                <label class="form-group">
                  <span class="label-icon">⚡</span>
                  Custom Endpoint
                </label>
                <input
                  v-model="apiKeys.customEndpoint"
                  type="url"
                  class="form-input"
                  placeholder="https://api.example.com/v1"
                  :disabled="isDemoMode"
                />
                <p class="form-help">
                  Custom API endpoint for specialized services
                </p>
              </div>
            </div>

            <div class="form-actions">
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isDemoMode"
              >
                <span class="btn-icon">💾</span>
                Save API Keys
              </button>

              <button
                type="button"
                class="btn btn-secondary"
                :disabled="isDemoMode"
                @click="clearKeys"
              >
                <span class="btn-icon">🗑️</span>
                Clear All Keys
              </button>

              <button
                type="button"
                class="btn btn-success"
                :disabled="isDemoMode || !hasAnyKey"
                @click="testConnection"
              >
                <span class="btn-icon">🧪</span>
                Test Connection
              </button>
            </div>

            <p class="text-sm text-blue-300 mt-2 italic">
              Add your API key to unlock full LLM-powered pipeline experience
              (via Grok or OpenAI).
            </p>
          </form>
        </div>
      </div>
    </div>

    <!-- Status Section -->
    <div class="status-section">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Connection Status</h3>
        </div>
        <div class="card-body">
          <div class="status-grid">
            <div class="status-item">
              <div class="status-icon">🤖</div>
              <div class="status-info">
                <div class="status-name">OpenAI</div>
                <div class="status-value" :class="getStatusClass('openai')">
                  {{ getStatusText('openai') }}
                </div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon">🧠</div>
              <div class="status-info">
                <div class="status-name">Grok</div>
                <div class="status-value" :class="getStatusClass('grok')">
                  {{ getStatusText('grok') }}
                </div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon">🔍</div>
              <div class="status-info">
                <div class="status-name">Anthropic</div>
                <div class="status-value" :class="getStatusClass('anthropic')">
                  {{ getStatusText('anthropic') }}
                </div>
              </div>
            </div>

            <div class="status-item">
              <div class="status-icon">⚡</div>
              <div class="status-info">
                <div class="status-name">Custom</div>
                <div class="status-value" :class="getStatusClass('custom')">
                  {{ getStatusText('custom') }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Instructions Section -->
    <div class="instructions-section">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">📖 Getting Started</h3>
        </div>
        <div class="card-body">
          <div class="instructions-grid">
            <div class="instruction-item">
              <div class="instruction-number">1</div>
              <div class="instruction-content">
                <h4>Get API Keys</h4>
                <p>
                  Sign up for OpenAI, Grok, or Anthropic to get your API keys
                </p>
              </div>
            </div>

            <div class="instruction-item">
              <div class="instruction-number">2</div>
              <div class="instruction-content">
                <h4>Add Keys Securely</h4>
                <p>
                  Enter your API keys above. They're stored locally in your
                  browser
                </p>
              </div>
            </div>

            <div class="instruction-item">
              <div class="instruction-number">3</div>
              <div class="instruction-content">
                <h4>Test Connection</h4>
                <p>Verify your keys work by testing the connection</p>
              </div>
            </div>

            <div class="instruction-item">
              <div class="instruction-number">4</div>
              <div class="instruction-content">
                <h4>Start Using AI</h4>
                <p>
                  Go to the Home page and submit tasks for real AI processing
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const apiKeys = ref({
  openai: '',
  grok: '',
  anthropic: '',
  customEndpoint: '',
});

const isDemoMode = ref(true); // Always demo mode for now
const connectionStatus = ref({
  openai: 'demo',
  grok: 'demo',
  anthropic: 'demo',
  custom: 'demo',
});

const hasAnyKey = computed(() => {
  return Object.values(apiKeys.value).some((key) => key.trim() !== '');
});

const getStatusClass = (service) => {
  const status = connectionStatus.value[service];
  switch (status) {
    case 'connected':
      return 'status-connected';
    case 'error':
      return 'status-error';
    case 'demo':
      return 'status-demo';
    default:
      return 'status-disconnected';
  }
};

const getStatusText = (service) => {
  const status = connectionStatus.value[service];
  switch (status) {
    case 'connected':
      return 'Connected';
    case 'error':
      return 'Error';
    case 'demo':
      return 'Demo Mode';
    default:
      return 'Not Configured';
  }
};

const saveKeys = () => {
  localStorage.setItem('linkops-api-keys', JSON.stringify(apiKeys.value));
  alert('API keys saved successfully!');
};

const clearKeys = () => {
  if (confirm('Are you sure you want to clear all API keys?')) {
    apiKeys.value = {
      openai: '',
      grok: '',
      anthropic: '',
      customEndpoint: '',
    };
    localStorage.removeItem('linkops-api-keys');
    alert('API keys cleared!');
  }
};

const testConnection = async () => {
  alert(
    'Connection testing is available in production mode with valid API keys.'
  );
};

const loadKeys = () => {
  const saved = localStorage.getItem('linkops-api-keys');
  if (saved) {
    try {
      apiKeys.value = { ...apiKeys.value, ...JSON.parse(saved) };
    } catch (error) {
      console.error('Failed to load saved API keys:', error);
    }
  }
};

onMounted(() => {
  loadKeys();
});
</script>

<style scoped>
.add-keys {
  space-y: 6;
}

.header-section {
  margin-bottom: 2rem;
}

.demo-notice {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1px solid #f59e0b;
  border-radius: 12px;
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
  margin: 0;
  line-height: 1.5;
}

.keys-section {
  margin-bottom: 2rem;
}

.keys-form {
  space-y: 2;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.label-icon {
  font-size: 1rem;
}

.form-help {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.btn-icon {
  font-size: 1rem;
}

.status-section {
  margin-bottom: 2rem;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.status-icon {
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.status-info {
  flex: 1;
}

.status-name {
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
}

.status-value {
  font-size: 0.875rem;
  font-weight: 500;
}

.status-connected {
  color: #059669;
}

.status-error {
  color: #dc2626;
}

.status-demo {
  color: #f59e0b;
}

.status-disconnected {
  color: #6b7280;
}

.instructions-section {
  margin-bottom: 2rem;
}

.instructions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.instruction-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.instruction-number {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.instruction-content h4 {
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
  font-size: 0.875rem;
}

.instruction-content p {
  color: #64748b;
  margin: 0;
  font-size: 0.75rem;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .status-grid {
    grid-template-columns: 1fr;
  }

  .instructions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
