<template>
  <div class="model-predictor">
    <button
      class="predict-btn"
      @click="show = !show"
    >
      {{ show ? '🔽 Hide' : '🔮 Predict' }}
    </button>

    <div
      v-if="show"
      class="predictor-panel"
    >
      <div class="panel-header">
        <h4>🔮 Make Prediction</h4>
        <p class="model-name">
          Model: {{ model }}
        </p>
      </div>

      <div class="input-section">
        <label class="input-label">📊 Input Features (JSON format):</label>
        <textarea
          v-model="input"
          rows="6"
          class="feature-input"
          placeholder="{&quot;feature1&quot;: value1, &quot;feature2&quot;: value2, ...}"
        />

        <div class="input-help">
          <p class="help-text">
            💡 Enter your features as JSON. Example:
          </p>
          <code class="example-code">
            {"bedrooms": 3, "bathrooms": 2, "sqft": 1500, "year_built": 2010}
          </code>
        </div>
      </div>

      <div class="action-section">
        <button
          class="predict-action-btn"
          :disabled="loading || !isValidJson"
          @click="predict"
        >
          <span v-if="!loading">🚀 Make Prediction</span>
          <span v-else>⏳ Predicting...</span>
        </button>

        <button
          v-if="input !== '{}'"
          class="clear-btn"
          @click="clearInput"
        >
          🧹 Clear
        </button>
      </div>

      <!-- Prediction Result -->
      <div
        v-if="result !== null"
        class="result-section"
      >
        <div class="result-header">
          <h5>📈 Prediction Result</h5>
          <span class="result-timestamp">{{
            formatTimestamp(resultTimestamp)
          }}</span>
        </div>

        <div class="prediction-display">
          <div class="prediction-value">
            <span class="value-label">Predicted Value:</span>
            <span class="value">{{ formatPrediction(result) }}</span>
          </div>

          <div
            v-if="result.confidence"
            class="confidence"
          >
            <span class="confidence-label">Confidence:</span>
            <span class="confidence-value">{{ (result.confidence * 100).toFixed(1) }}%</span>
          </div>
        </div>
      </div>

      <!-- Error Display -->
      <div
        v-if="error"
        class="error-section"
      >
        <div class="error-header">
          <span class="error-icon">❌</span>
          <span class="error-title">Prediction Error</span>
        </div>
        <p class="error-message">
          {{ error }}
        </p>
      </div>

      <!-- Validation Error -->
      <div
        v-if="!isValidJson && input !== '{}'"
        class="validation-error"
      >
        <span class="validation-icon">⚠️</span>
        <span class="validation-text">Invalid JSON format</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

const props = defineProps({
  model: {
    type: String,
    required: true,
  },
});

const show = ref(false);
const input = ref('{}');
const result = ref(null);
const resultTimestamp = ref(null);
const loading = ref(false);
const error = ref(null);

// JSON validation
const isValidJson = computed(() => {
  if (!input.value || input.value === '{}') return true;
  try {
    JSON.parse(input.value);
    return true;
  } catch {
    return false;
  }
});

const predict = async () => {
  if (!isValidJson.value) return;

  loading.value = true;
  error.value = null;
  result.value = null;

  try {
    const features = JSON.parse(input.value);

    const response = await axios.post(`/api/models/predict/${props.model}`, {
      features: features,
    });

    result.value = response.data.prediction;
    resultTimestamp.value = new Date();
  } catch (err) {
    console.error('Prediction failed:', err);
    error.value =
      err.response?.data?.detail || err.message || 'Prediction failed';
  } finally {
    loading.value = false;
  }
};

const clearInput = () => {
  input.value = '{}';
  result.value = null;
  error.value = null;
};

const formatPrediction = (prediction) => {
  if (typeof prediction === 'number') {
    return prediction.toFixed(2);
  }
  return prediction;
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return '';
  return timestamp.toLocaleTimeString();
};
</script>

<style scoped>
.model-predictor {
  display: inline-block;
}

.predict-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.predict-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.predictor-panel {
  margin-top: 12px;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  min-width: 400px;
}

.panel-header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.panel-header h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.model-name {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  font-family: monospace;
}

.input-section {
  margin-bottom: 16px;
}

.input-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
  font-size: 14px;
}

.feature-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.4;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.feature-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-help {
  margin-top: 8px;
}

.help-text {
  margin: 0 0 4px 0;
  font-size: 12px;
  color: #6b7280;
}

.example-code {
  display: block;
  padding: 8px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  color: #374151;
}

.action-section {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.predict-action-btn {
  flex: 1;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.predict-action-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
}

.predict-action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.clear-btn {
  background: #6b7280;
  color: white;
  border: none;
  padding: 10px 12px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.clear-btn:hover {
  background: #4b5563;
}

.result-section {
  padding: 16px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #bae6fd;
  border-radius: 6px;
  margin-bottom: 12px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.result-header h5 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #0369a1;
}

.result-timestamp {
  font-size: 12px;
  color: #0891b2;
}

.prediction-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.prediction-value {
  display: flex;
  align-items: center;
  gap: 8px;
}

.value-label {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.value {
  font-size: 18px;
  font-weight: 700;
  color: #059669;
  font-family: monospace;
}

.confidence {
  display: flex;
  align-items: center;
  gap: 4px;
}

.confidence-label {
  font-size: 12px;
  color: #6b7280;
}

.confidence-value {
  font-size: 14px;
  font-weight: 600;
  color: #7c3aed;
}

.error-section {
  padding: 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  margin-bottom: 12px;
}

.error-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.error-icon {
  font-size: 16px;
}

.error-title {
  font-weight: 600;
  color: #dc2626;
  font-size: 14px;
}

.error-message {
  margin: 0;
  font-size: 13px;
  color: #991b1b;
  line-height: 1.4;
}

.validation-error {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: #fffbeb;
  border: 1px solid #fcd34d;
  border-radius: 4px;
  margin-top: 8px;
}

.validation-icon {
  font-size: 14px;
}

.validation-text {
  font-size: 12px;
  color: #92400e;
  font-weight: 500;
}
</style>
