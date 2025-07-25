<template>
  <div class="p-6 animate-slide-in bg-gray-900 text-white min-h-screen">
    <div class="max-w-4xl mx-auto">
      <h2 class="text-3xl font-bold mb-6 text-blue-400">
        ML-Creator: Build Your ML Model
      </h2>
      <p class="mb-6 text-gray-300 text-lg">
        Easily create machine learning models without coding expertise. Perfect
        for non-data scientists.
      </p>

      <!-- Model Configuration Form -->
      <div class="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
        <h3 class="text-xl font-semibold mb-4 text-green-400">
          Model Configuration
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Model Type Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2"
              >Model Type:</label
            >
            <select
              v-model="modelConfig.modelType"
              class="w-full p-3 bg-gray-700 rounded-lg text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="LogisticRegression">Logistic Regression</option>
              <option value="RandomForestClassifier">Random Forest</option>
              <option value="SVC">Support Vector Machine</option>
              <option value="NeuralNetwork">Neural Network</option>
              <option value="XGBoost">XGBoost</option>
            </select>
          </div>

          <!-- Dataset Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2"
              >Dataset:</label
            >
            <select
              v-model="modelConfig.dataset"
              class="w-full p-3 bg-gray-700 rounded-lg text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="kubernetes_logs">Kubernetes Logs</option>
              <option value="network_traffic">Network Traffic</option>
              <option value="application_metrics">Application Metrics</option>
              <option value="system_performance">System Performance</option>
              <option value="security_events">Security Events</option>
            </select>
          </div>
        </div>

        <!-- Features Selection -->
        <div class="mt-6">
          <label class="block text-sm font-medium text-gray-300 mb-2"
            >Features:</label
          >
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <label
              v-for="feature in availableFeatures"
              :key="feature.value"
              class="flex items-center p-3 bg-gray-700 rounded-lg border border-gray-600 hover:border-blue-500 cursor-pointer transition-colors duration-200"
            >
              <input
                v-model="modelConfig.features"
                type="checkbox"
                :value="feature.value"
                class="mr-3 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
              />
              <span class="text-sm">{{ feature.label }}</span>
            </label>
          </div>
        </div>

        <!-- Model Parameters -->
        <div class="mt-6">
          <label class="block text-sm font-medium text-gray-300 mb-2"
            >Model Parameters:</label
          >
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-xs text-gray-400 mb-1"
                >Learning Rate</label
              >
              <input
                v-model.number="modelConfig.learningRate"
                type="range"
                min="0.001"
                max="0.1"
                step="0.001"
                class="w-full"
              />
              <span class="text-xs text-gray-400">{{
                modelConfig.learningRate
              }}</span>
            </div>

            <div>
              <label class="block text-xs text-gray-400 mb-1">Epochs</label>
              <input
                v-model.number="modelConfig.epochs"
                type="range"
                min="10"
                max="200"
                step="10"
                class="w-full"
              />
              <span class="text-xs text-gray-400">{{
                modelConfig.epochs
              }}</span>
            </div>

            <div>
              <label class="block text-xs text-gray-400 mb-1">Test Split</label>
              <input
                v-model.number="modelConfig.testSplit"
                type="range"
                min="0.1"
                max="0.5"
                step="0.05"
                class="w-full"
              />
              <span class="text-xs text-gray-400"
                >{{ (modelConfig.testSplit * 100).toFixed(0) }}%</span
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Model Preview -->
      <div class="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">Model Preview</h3>
        <div class="bg-gray-700 rounded-lg p-4 font-mono text-sm">
          <pre class="text-green-400">{{ generateModelCode() }}</pre>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-4 mb-6">
        <button
          class="bg-green-600 hover:bg-green-700 px-8 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center"
          :class="{ 'animate-pulse-slow': creating }"
          :disabled="creating || !isValidConfig"
          @click="createModel"
        >
          <svg
            v-if="!creating"
            class="w-5 h-5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          <svg
            v-else
            class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            />
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          {{ creating ? 'Creating Model...' : 'Create Model' }}
        </button>

        <button
          class="bg-gray-600 hover:bg-gray-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200"
          @click="resetForm"
        >
          Reset
        </button>

        <button
          class="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200"
          @click="saveTemplate"
        >
          Save Template
        </button>
      </div>

      <!-- Model Status -->
      <div
        v-if="modelStatus"
        class="bg-gray-800 rounded-lg p-6 border border-gray-700 animate-slide-in"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-semibold text-green-400">Model Status</h3>
          <span class="text-sm text-gray-400">{{ modelStatus.timestamp }}</span>
        </div>

        <div class="bg-gray-700 rounded-lg p-4 mb-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-400">Model Name:</p>
              <p class="font-semibold text-white">
                {{ modelStatus.modelName }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-400">Status:</p>
              <p class="font-semibold text-green-400">
                {{ modelStatus.status }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-400">Accuracy:</p>
              <p class="font-semibold text-blue-400">
                {{ modelStatus.accuracy }}%
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-400">Training Time:</p>
              <p class="font-semibold text-yellow-400">
                {{ modelStatus.trainingTime }}
              </p>
            </div>
          </div>
        </div>

        <div class="flex space-x-4">
          <button
            class="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg font-semibold transition-all duration-200"
            @click="deployModel"
          >
            Deploy Model
          </button>
          <button
            class="bg-indigo-600 hover:bg-indigo-700 px-6 py-2 rounded-lg font-semibold transition-all duration-200"
            @click="downloadModel"
          >
            Download Model
          </button>
        </div>
      </div>

      <!-- Recent Models -->
      <div v-if="recentModels.length > 0" class="mt-8">
        <h3 class="text-xl font-semibold mb-4 text-blue-400">Recent Models</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="model in recentModels"
            :key="model.id"
            class="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors duration-200"
          >
            <div class="flex justify-between items-start mb-2">
              <h4 class="font-semibold text-white">
                {{ model.name }}
              </h4>
              <span class="text-xs text-gray-400">{{ model.date }}</span>
            </div>
            <p class="text-sm text-gray-400 mb-2">
              {{ model.type }} - {{ model.dataset }}
            </p>
            <div class="flex items-center justify-between">
              <span class="text-sm text-green-400"
                >Accuracy: {{ model.accuracy }}%</span
              >
              <button
                class="text-blue-400 hover:text-blue-300 text-sm"
                @click="loadModel(model)"
              >
                Load
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MLCreator',
  data() {
    return {
      creating: false,
      modelConfig: {
        modelType: 'RandomForestClassifier',
        dataset: 'kubernetes_logs',
        features: ['cpu_usage', 'memory_usage'],
        learningRate: 0.01,
        epochs: 100,
        testSplit: 0.2,
      },
      modelStatus: null,
      recentModels: [
        {
          id: 1,
          name: 'k8s_anomaly_detector',
          type: 'Random Forest',
          dataset: 'Kubernetes Logs',
          accuracy: 94.2,
          date: '2024-01-15',
        },
        {
          id: 2,
          name: 'network_classifier',
          type: 'Neural Network',
          dataset: 'Network Traffic',
          accuracy: 89.7,
          date: '2024-01-14',
        },
      ],
      availableFeatures: [
        { value: 'cpu_usage', label: 'CPU Usage' },
        { value: 'memory_usage', label: 'Memory Usage' },
        { value: 'network_traffic', label: 'Network Traffic' },
        { value: 'disk_io', label: 'Disk I/O' },
        { value: 'error_rate', label: 'Error Rate' },
        { value: 'response_time', label: 'Response Time' },
        { value: 'pod_count', label: 'Pod Count' },
        { value: 'node_status', label: 'Node Status' },
      ],
    };
  },
  computed: {
    isValidConfig() {
      return (
        this.modelConfig.features.length > 0 &&
        this.modelConfig.modelType &&
        this.modelConfig.dataset
      );
    },
  },
  methods: {
    generateModelCode() {
      return `from sklearn.${
        this.modelConfig.modelType.includes('RandomForest')
          ? 'ensemble'
          : 'linear_model'
      } import ${this.modelConfig.modelType}
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# Load dataset
df = pd.read_csv('${this.modelConfig.dataset}.csv')

# Prepare features
X = df[${JSON.stringify(this.modelConfig.features)}]
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=${this.modelConfig.testSplit}, random_state=42
)

# Train model
model = ${this.modelConfig.modelType}()
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model accuracy: {accuracy:.2%}")`;
    },

    async createModel() {
      if (!this.isValidConfig) return;

      this.creating = true;

      // Simulate API call to ml-creator/api/model_generator.py
      await new Promise((resolve) => setTimeout(resolve, 3000));

      this.modelStatus = {
        modelName: `${
          this.modelConfig.dataset
        }_${this.modelConfig.modelType.toLowerCase()}`,
        status: 'Training Completed',
        accuracy: (85 + Math.random() * 10).toFixed(1),
        trainingTime: '2m 34s',
        timestamp: new Date().toLocaleString(),
      };

      this.creating = false;
      this.$toast?.success('Model created successfully!');
    },

    resetForm() {
      this.modelConfig = {
        modelType: 'RandomForestClassifier',
        dataset: 'kubernetes_logs',
        features: ['cpu_usage', 'memory_usage'],
        learningRate: 0.01,
        epochs: 100,
        testSplit: 0.2,
      };
      this.modelStatus = null;
    },

    saveTemplate() {
      const template = {
        name: `${this.modelConfig.dataset}_template`,
        config: { ...this.modelConfig },
        timestamp: new Date().toISOString(),
      };

      // Simulate saving template
      this.$toast?.success('Template saved successfully!');
    },

    deployModel() {
      this.$toast?.success('Model deployment simulated!');
    },

    downloadModel() {
      this.$toast?.success('Model download simulated!');
    },

    loadModel(model) {
      // Simulate loading a previous model
      this.modelConfig.modelType = model.type;
      this.modelConfig.dataset = model.dataset;
      this.$toast?.success(`Loaded model: ${model.name}`);
    },
  },
};
</script>

<style scoped>
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.02);
    opacity: 0.9;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes slideIn {
  0% {
    transform: translateY(20px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-pulse-slow {
  animation: pulse 2s infinite;
}

.animate-slide-in {
  animation: slideIn 0.5s ease-out;
}

/* Custom range slider styling */
input[type='range'] {
  -webkit-appearance: none;
  appearance: none;
  background: #374151;
  border-radius: 5px;
  height: 6px;
}

input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  background: #3b82f6;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  cursor: pointer;
}

input[type='range']::-moz-range-thumb {
  background: #3b82f6;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  cursor: pointer;
  border: none;
}
</style>
