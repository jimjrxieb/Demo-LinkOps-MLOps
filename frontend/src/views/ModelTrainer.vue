<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4 text-teal-300">
      🤖 Vendor Suggestion Model
    </h2>

    <!-- Model Creation Animation -->
    <div
      v-if="step === 'animating'"
      class="glass p-6 rounded-xl mb-6"
    >
      <div class="animation-sequence">
        <ul class="animation-steps">
          <li :class="{ active: animationStep >= 1 }">
            <div class="step-content">
              <span class="step-icon">🔍</span>
              <span class="step-text">Scanning past tickets...</span>
              <span
                v-if="animationStep === 1"
                class="step-detail"
              >Analyzing work order history</span>
            </div>
          </li>
          <li :class="{ active: animationStep >= 2 }">
            <div class="step-content">
              <span class="step-icon">📁</span>
              <span class="step-text">Extracting vendor data...</span>
              <span
                v-if="animationStep === 2"
                class="step-detail"
              >Computing performance metrics</span>
            </div>
          </li>
          <li :class="{ active: animationStep >= 3 }">
            <div class="step-content">
              <span class="step-icon">🧠</span>
              <span class="step-text">Building ML model...</span>
              <span
                v-if="animationStep === 3"
                class="step-detail"
              >Training vendor ranking algorithm</span>
            </div>
          </li>
          <li :class="{ active: animationStep >= 4 }">
            <div class="step-content">
              <span class="step-icon">✅</span>
              <span class="step-text">Ranking vendors...</span>
              <span
                v-if="animationStep === 4"
                class="step-detail"
              >Calculating quality-cost-response scores</span>
            </div>
          </li>
          <li :class="{ active: animationStep >= 5 }">
            <div class="step-content">
              <span class="step-icon">📊</span>
              <span class="step-text">Model deployed</span>
              <span
                v-if="animationStep === 5"
                class="step-detail"
              >Ready for vendor suggestions</span>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Model Controls -->
    <div
      v-else-if="step === 'results'"
      class="space-y-6"
    >
      <!-- Parameter Controls -->
      <div class="glass p-6 rounded-xl">
        <h3 class="text-lg font-semibold mb-4 text-white">
          Model Parameters
        </h3>

        <div class="space-y-4">
          <!-- Work Type Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">Work Type</label>
            <select
              v-model="params.workType"
              class="w-full bg-black bg-opacity-50 text-white rounded-lg p-2 border border-gray-700"
            >
              <option value="hvac">
                HVAC
              </option>
              <option value="plumbing">
                Plumbing
              </option>
              <option value="electrical">
                Electrical
              </option>
            </select>
          </div>

          <!-- Importance Sliders -->
          <div
            v-for="(value, key) in params.weights"
            :key="key"
            class="space-y-2"
          >
            <label class="block text-sm font-medium text-gray-300">
              {{ formatLabel(key) }} Importance
            </label>
            <input
              v-model.number="params.weights[key]"
              type="range"
              min="0"
              max="1"
              step="0.1"
              class="w-full"
            >
            <div class="text-sm text-gray-400">
              {{ Math.round(value * 100) }}%
            </div>
          </div>
        </div>

        <!-- Get Suggestion Button -->
        <button
          class="mt-4 w-full bg-teal-600 text-white py-2 px-4 rounded-lg hover:bg-teal-500 transition"
          :disabled="loading"
          @click="getSuggestion"
        >
          {{ loading ? 'Analyzing...' : 'Get Vendor Suggestion' }}
        </button>
      </div>

      <!-- Results Display -->
      <div
        v-if="suggestion"
        class="glass p-6 rounded-xl"
      >
        <h3 class="text-lg font-semibold mb-4 text-white">
          Suggested Vendor
        </h3>

        <!-- Vendor Score -->
        <div class="flex items-center justify-between mb-4">
          <div class="text-2xl font-bold text-teal-400">
            {{ suggestion.vendor }}
          </div>
          <div class="text-xl font-semibold text-white">
            {{ suggestion.score }}% Match
          </div>
        </div>

        <!-- Metrics -->
        <div class="space-y-3">
          <div
            v-for="(score, metric) in suggestion.metrics"
            :key="metric"
            class="relative"
          >
            <div class="flex justify-between text-sm mb-1">
              <span class="text-gray-300">{{ formatLabel(metric) }}</span>
              <span class="text-teal-400">{{ score }}%</span>
            </div>
            <div class="h-2 bg-gray-700 rounded-full">
              <div
                class="h-full bg-teal-500 rounded-full transition-all duration-500"
                :style="{ width: `${score}%` }"
              />
            </div>
          </div>
        </div>

        <!-- Explanation -->
        <div class="mt-6 text-gray-300 text-sm">
          <pre class="whitespace-pre-wrap">{{ suggestion.explanation }}</pre>
        </div>
      </div>
    </div>

    <!-- Initial State -->
    <div
      v-else
      class="text-center py-12"
    >
      <button
        class="bg-teal-600 text-white py-3 px-6 rounded-lg hover:bg-teal-500 transition text-lg"
        @click="startAnimationSequence"
      >
        🚀 Create Vendor Suggestion Model
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

// State
const step = ref('initial'); // 'initial' | 'animating' | 'results'
const animationStep = ref(0);
const loading = ref(false);
const suggestion = ref(null);

// Model parameters
const params = ref({
  workType: 'hvac',
  weights: {
    quality: 0.5,
    response_time: 0.3,
    cost: 0.2,
  },
});

async function startAnimationSequence() {
  step.value = 'animating';
  animationStep.value = 0;

  // Run animation sequence
  for (let i = 1; i <= 5; i++) {
    await new Promise((resolve) => setTimeout(resolve, 1200));
    animationStep.value = i;
  }

  // Show model controls after animation
  await new Promise((resolve) => setTimeout(resolve, 500));
  step.value = 'results';
}

// Get vendor suggestion
const getSuggestion = async () => {
  loading.value = true;
  try {
    const res = await axios.post('/api/suggest-vendor', {
      work_type: params.value.workType,
      parameters: params.value.weights,
    });
    suggestion.value = res.data;
  } catch (err) {
    console.error('Failed to get suggestion:', err);
  } finally {
    loading.value = false;
  }
};

// Utilities
const formatLabel = (key) => {
  return key
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};
</script>

<style scoped>
.glass {
  background: rgba(13, 26, 34, 0.6);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.animation-sequence {
  @apply py-4;
}

.animation-steps {
  @apply space-y-6;
}

.animation-steps li {
  @apply opacity-30 transition-all duration-500;
}

.animation-steps li.active {
  @apply opacity-100;
}

.step-content {
  @apply flex items-start space-x-3;
}

.step-icon {
  @apply text-xl;
}

.step-text {
  @apply text-white font-medium;
}

.step-detail {
  @apply ml-2 text-sm text-teal-400 opacity-75;
}

/* Custom slider styling */
input[type='range'] {
  @apply appearance-none bg-gray-700 h-2 rounded-lg;
}

input[type='range']::-webkit-slider-thumb {
  @apply appearance-none w-4 h-4 rounded-full bg-teal-500 cursor-pointer;
}

input[type='range']::-moz-range-thumb {
  @apply w-4 h-4 rounded-full bg-teal-500 cursor-pointer border-0;
}
</style>
