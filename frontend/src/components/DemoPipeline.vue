<template>
  <div class="p-6 animate-slide-in bg-gray-900 text-white min-h-screen">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-3xl font-bold mb-6 text-blue-400">
        Demo Pipeline: Model Training
      </h2>
      <p class="mb-6 text-gray-300 text-lg">
        Experience a simplified, animated visualization of the Kubernetes ML
        model training pipeline.
      </p>

      <!-- Pipeline Overview -->
      <div class="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div v-for="(stage, index) in stages" :key="index" class="relative">
            <div
              class="p-4 rounded-lg border-2 transition-all duration-500"
              :class="{
                'border-blue-500 bg-blue-900/20': index === stage,
                'border-green-500 bg-green-900/20': index < stage,
                'border-gray-600 bg-gray-700/20': index > stage,
              }"
            >
              <div class="flex items-center mb-2">
                <div
                  class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold mr-3"
                  :class="{
                    'bg-blue-500 text-white': index === stage,
                    'bg-green-500 text-white': index < stage,
                    'bg-gray-600 text-gray-300': index > stage,
                  }"
                >
                  {{ index + 1 }}
                </div>
                <h3 class="font-semibold text-sm">
                  {{ stage.name }}
                </h3>
              </div>
              <p class="text-xs text-gray-400">
                {{ stage.desc }}
              </p>

              <!-- Progress Bar -->
              <div class="mt-3 w-full bg-gray-700 rounded-full h-2">
                <div
                  class="h-2 rounded-full transition-all duration-1000"
                  :class="{
                    'bg-blue-500': index === stage,
                    'bg-green-500': index < stage,
                    'bg-gray-600': index > stage,
                  }"
                  :style="{ width: getStageProgress(index) + '%' }"
                />
              </div>
            </div>

            <!-- Arrow connector -->
            <div
              v-if="index < stages.length - 1"
              class="hidden md:block absolute top-1/2 -right-2 transform -translate-y-1/2"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Current Stage Details -->
      <div class="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-semibold text-blue-400">
            Current Stage: {{ stages[stage].name }}
          </h3>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-400">Progress:</span>
            <span class="text-lg font-mono text-green-400"
              >{{ getStageProgress(stage) }}%</span
            >
          </div>
        </div>

        <div class="bg-gray-700 rounded-lg p-4 mb-4">
          <p class="text-gray-200 leading-relaxed">
            {{ stages[stage].desc }}
          </p>
          <div class="mt-3 text-sm text-gray-400">
            <p><strong>Duration:</strong> {{ stages[stage].duration }}</p>
            <p><strong>Resources:</strong> {{ stages[stage].resources }}</p>
          </div>
        </div>

        <!-- Stage-specific details -->
        <div v-if="stages[stage].details" class="bg-gray-700 rounded-lg p-4">
          <h4 class="font-semibold text-green-400 mb-2">Stage Details:</h4>
          <ul class="text-sm text-gray-300 space-y-1">
            <li
              v-for="detail in stages[stage].details"
              :key="detail"
              class="flex items-center"
            >
              <svg
                class="w-4 h-4 text-green-500 mr-2"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
              {{ detail }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Control Buttons -->
      <div class="flex space-x-4 mb-6">
        <button
          class="bg-gray-600 hover:bg-gray-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center"
          :disabled="stage === 0"
          @click="previousStage"
        >
          <svg
            class="w-5 h-5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
          Previous Stage
        </button>

        <button
          class="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center animate-pulse-slow"
          @click="nextStage"
        >
          <span v-if="stage < stages.length - 1">Next Stage</span>
          <span v-else>Restart Pipeline</span>
          <svg
            class="w-5 h-5 ml-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>

        <button
          class="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center"
          :disabled="autoRunning"
          @click="autoRun"
        >
          <span v-if="!autoRunning">Auto Run</span>
          <span v-else class="flex items-center">
            <svg
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
            Running...
          </span>
        </button>
      </div>

      <!-- Pipeline Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <h4 class="font-semibold text-blue-400 mb-2">Total Progress</h4>
          <div class="text-2xl font-bold text-green-400">
            {{ Math.round((stage / (stages.length - 1)) * 100) }}%
          </div>
        </div>

        <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <h4 class="font-semibold text-blue-400 mb-2">Stages Completed</h4>
          <div class="text-2xl font-bold text-green-400">
            {{ stage }}/{{ stages.length - 1 }}
          </div>
        </div>

        <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <h4 class="font-semibold text-blue-400 mb-2">Estimated Time</h4>
          <div class="text-2xl font-bold text-green-400">
            {{ getEstimatedTime() }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DemoPipeline',
  data() {
    return {
      stage: 0,
      autoRunning: false,
      stages: [
        {
          name: 'Data Intake',
          desc: 'Ingesting Kubernetes logs, metrics, and configuration data from multiple sources.',
          duration: '2-3 minutes',
          resources: 'CPU: 2 cores, Memory: 4GB',
          progress: 25,
          details: [
            'Collecting pod logs and events',
            'Gathering node metrics',
            'Extracting configuration data',
            'Validating data integrity',
          ],
        },
        {
          name: 'Data Sanitization',
          desc: 'Removing sensitive PII and normalizing data using advanced NLP processing.',
          duration: '3-4 minutes',
          resources: 'CPU: 4 cores, Memory: 8GB',
          progress: 50,
          details: [
            'PII detection and removal',
            'Data normalization',
            'Feature extraction',
            'Quality validation',
          ],
        },
        {
          name: 'Model Training',
          desc: 'Training the Kubernetes optimization model using advanced ML algorithms.',
          duration: '5-7 minutes',
          resources: 'CPU: 8 cores, Memory: 16GB, GPU: 1',
          progress: 75,
          details: [
            'Hyperparameter optimization',
            'Cross-validation',
            'Model selection',
            'Performance evaluation',
          ],
        },
        {
          name: 'Model Output',
          desc: 'Generating optimized cluster configurations and deployment recommendations.',
          duration: '1-2 minutes',
          resources: 'CPU: 2 cores, Memory: 4GB',
          progress: 100,
          details: [
            'Configuration generation',
            'Resource optimization',
            'Deployment planning',
            'Documentation creation',
          ],
        },
      ],
    };
  },
  methods: {
    nextStage() {
      if (this.stage < this.stages.length - 1) {
        this.stage++;
      } else {
        this.stage = 0; // Restart
      }
    },

    previousStage() {
      if (this.stage > 0) {
        this.stage--;
      }
    },

    getStageProgress(stageIndex) {
      if (stageIndex < this.stage) {
        return 100; // Completed
      } else if (stageIndex === this.stage) {
        return 75; // In progress
      } else {
        return 0; // Not started
      }
    },

    getEstimatedTime() {
      const remainingStages = this.stages.length - 1 - this.stage;
      const avgTime = 3; // Average minutes per stage
      return `${remainingStages * avgTime} min`;
    },

    async autoRun() {
      this.autoRunning = true;

      for (let i = this.stage; i < this.stages.length; i++) {
        this.stage = i;
        await new Promise((resolve) => setTimeout(resolve, 2000)); // 2 seconds per stage
      }

      this.autoRunning = false;
      this.$toast?.success('Pipeline completed successfully!');
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
</style>
