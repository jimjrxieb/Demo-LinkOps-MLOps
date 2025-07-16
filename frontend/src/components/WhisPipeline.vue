<template>
  <div class="whis-pipeline">
    <div class="pipeline-header">
      <h2 class="pipeline-title">
        Whis Pipeline Flow
      </h2>
      <p class="pipeline-subtitle">
        Data Processing & Enhancement Workflow
      </p>
    </div>

    <div class="pipeline-container">
      <div class="pipeline-steps">
        <transition-group
          name="step-fade"
          tag="div"
        >
          <div
            v-for="(step, index) in pipelineData"
            :key="step.id"
            class="pipeline-step"
            :class="{
              active: index === currentStep,
              completed: index < currentStep,
              pending: index > currentStep,
            }"
            @click="$emit('step-click', step)"
          >
            <div class="step-icon">
              {{ step.icon }}
            </div>
            <div class="step-content">
              <h3 class="step-title">
                {{ step.name }}
              </h3>
              <p class="step-description">
                {{ step.description }}
              </p>
              <p class="step-tools">
                📦 Tools: {{ step.tools }}
              </p>
            
              <!-- Enhanced Tool Details -->
              <div
                v-if="index === currentStep"
                class="tool-details"
              >
                <div class="tool-title">
                  🔧 Current Process
                </div>
                <div class="tool-description">
                  {{ getToolDescription(index) }}
                </div>
                <div class="tool-tech">
                  {{ getToolTechStack(index) }}
                </div>
              </div>
              <div class="step-status">
                <span
                  class="status-indicator"
                  :class="getStepStatus(index)"
                />
                <span class="status-text">{{ getStepStatusText(index) }}</span>
              </div>
            
              <!-- Approve/Reject buttons for Logic step (index 2) -->
              <div
                v-if="index === 2 && currentStep >= 2"
                class="approval-section mt-3"
              >
                <!-- 3a. Orb Creation -->
                <div
                  v-if="!orbApproved"
                  class="bg-gray-900 p-3 rounded shadow mb-2"
                >
                  <h4 class="text-md text-yellow-300 font-bold mb-1">
                    3a. Orb Creation
                  </h4>
                  <p class="text-white text-sm mb-2">
                    Whis uses LLMs + LangChain to create best practices (Orbs) from sanitized input.
                  </p>
                  <div class="flex gap-2">
                    <button
                      class="btn btn-success text-xs px-3 py-1"
                      @click="orbApproved = true"
                    >
                      ✅ Approve Orb
                    </button>
                    <button
                      class="btn btn-secondary text-xs px-3 py-1"
                      @click="runeApproved = false"
                    >
                      ❌ Reject Orb
                    </button>
                  </div>
                </div>

                <!-- 3b. Rune Creation -->
                <div
                  v-if="orbApproved && !runeApproved"
                  class="bg-gray-900 p-3 rounded shadow mb-2"
                >
                  <h4 class="text-md text-purple-300 font-bold mb-1">
                    3b. Rune Generation
                  </h4>
                  <p class="text-white text-sm mb-2">
                    Whis converts the approved Orb into an executable step-by-step solution path (Rune).
                  </p>
                  <div class="flex gap-2">
                    <button
                      class="btn btn-success text-xs px-3 py-1"
                      @click="runeApproved = true"
                    >
                      ✅ Approve Rune
                    </button>
                    <button
                      class="btn btn-secondary text-xs px-3 py-1"
                      @click="orbApproved = false"
                    >
                      ❌ Reject Rune
                    </button>
                  </div>
                </div>

                <!-- Success messages -->
                <div
                  v-if="orbApproved && !runeApproved"
                  class="text-green-400 text-sm font-bold mt-2"
                >
                  Orb approved. Proceeding to Rune generation...
                </div>
                <div
                  v-if="runeApproved"
                  class="text-green-400 text-sm font-bold mt-2"
                >
                  Rune approved. Task is now complete.
                </div>
              </div>
            </div>

            <!-- Connection Line -->
            <div
              v-if="index < pipelineData.length - 1"
              class="step-connector"
            >
              <div class="connector-line" />
              <div class="connector-arrow">
                →
              </div>
            </div>
          </div>
        </transition-group>
      </div>
    </div>

    <!-- Pipeline Progress -->
    <div class="pipeline-progress">
      <div class="progress-bar">
        <div
          class="progress-fill"
          :style="{ width: progressPercentage + '%' }"
        />
      </div>
    </div>
    <div class="progress-text">
      Step {{ currentStep + 1 }} of {{ pipelineData.length }} ({{
        Math.round(progressPercentage)
      }}% complete)
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Props
const props = defineProps({
  pipelineData: {
    type: Array,
    required: true,
  },
  currentStep: {
    type: Number,
    default: 0,
  },
});

// Emits
const emit = defineEmits(['step-click']);

// State for approve/reject functionality
const orbApproved = ref(false);
const runeApproved = ref(false);

// Computed
const progressPercentage = computed(() => {
  return (props.currentStep / (props.pipelineData.length - 1)) * 100;
});

// Methods
const getStepStatus = (index) => {
  if (index < props.currentStep) return 'completed';
  if (index === props.currentStep) return 'active';
  return 'pending';
};

const getStepStatusText = (index) => {
  if (index < props.currentStep) return 'Completed';
  if (index === props.currentStep) return 'Processing';
  return 'Pending';
};

const getToolDescription = (index) => {
  const descriptions = {
    0: 'Collecting task input from user interface and preparing for processing. Validating input format and extracting key parameters.',
    1: 'Sanitizing input data by removing sensitive information, standardizing format, and ensuring data quality for AI processing.',
    2: 'AI-powered analysis using LangChain and OpenAI to understand task requirements and generate execution strategies.',
    3: 'Orchestrating the complete workflow, managing dependencies, and coordinating between different processing stages.',
    4: 'Executing the final solution, deploying resources, and providing real-time feedback on task completion.'
  };
  return descriptions[index] || 'Processing step...';
};

const getToolTechStack = (index) => {
  const techStacks = {
    0: 'FastAPI, JSON Schema, Vue.js, Axios',
    1: 'Python sanitizer, PII detection, data validation',
    2: 'LangChain, OpenAI GPT-4, prompt engineering',
    3: 'Workflow engine, Redis, PostgreSQL, monitoring',
    4: 'Kubernetes API, Helm, Terraform, CI/CD tools'
  };
  return techStacks[index] || 'Various tools and frameworks';
};
</script>

<style scoped>
.whis-pipeline {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  margin-bottom: 2rem;
}

.pipeline-header {
  text-align: center;
  margin-bottom: 2rem;
}

.pipeline-title {
  font-size: 2rem;
  color: #00d4ff;
  margin-bottom: 0.5rem;
}

.pipeline-subtitle {
  color: #888;
  font-size: 1rem;
  margin: 0;
}

.pipeline-container {
  margin-bottom: 2rem;
}

.pipeline-steps {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.pipeline-step {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.pipeline-step:hover {
  background: rgba(0, 212, 255, 0.1);
  border-color: #00d4ff;
  transform: translateX(5px);
}

.pipeline-step.active {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.pipeline-step.completed {
  background: rgba(0, 255, 0, 0.1);
  border-color: #00ff00;
}

.step-icon {
  font-size: 2.5rem;
  min-width: 60px;
  text-align: center;
  filter: drop-shadow(0 0 15px rgba(0, 212, 255, 0.6));
}

.pipeline-step.completed .step-icon {
  filter: drop-shadow(0 0 15px rgba(0, 255, 0, 0.6));
}

.step-content {
  flex: 1;
}

.step-title {
  color: #00d4ff;
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
}

.step-description {
  color: #e0e0e0;
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.step-tools {
  color: #888;
  margin: 0 0 1rem 0;
  font-size: 0.8rem;
  line-height: 1.4;
  font-style: italic;
}

.step-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #666;
}

.status-indicator.active {
  background: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.6);
}

.status-indicator.completed {
  background: #00ff00;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.6);
}

.status-text {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  font-weight: bold;
}

.step-connector {
  position: absolute;
  right: -2rem;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.connector-line {
  width: 2px;
  height: 40px;
  background: linear-gradient(to bottom, #00d4ff, transparent);
}

.connector-arrow {
  color: #00d4ff;
  font-size: 1.2rem;
  filter: drop-shadow(0 0 5px rgba(0, 212, 255, 0.6));
}

.pipeline-progress {
  margin-top: 2rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4ff, #0099cc);
  border-radius: 4px;
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
}

.progress-text {
  text-align: center;
  color: #00d4ff;
  font-weight: bold;
  font-size: 1rem;
}

.approval-section {
  border-top: 1px solid rgba(0, 212, 255, 0.3);
  padding-top: 1rem;
}

.approval-section .btn {
  font-size: 0.75rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.approval-section .btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* Transition Animations */
.step-fade-enter-active,
.step-fade-leave-active {
  transition: all 0.5s ease;
}

.step-fade-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.step-fade-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.step-fade-move {
  transition: transform 0.5s ease;
}

/* Enhanced Tool Descriptions */
.tool-details {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(0, 212, 255, 0.3);
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.tool-details:hover {
  border-color: #00d4ff;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
}

.tool-title {
  color: #00d4ff;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.tool-description {
  color: #e0e0e0;
  font-size: 0.8rem;
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.tool-tech {
  color: #888;
  font-size: 0.75rem;
  font-style: italic;
}

/* Live Pipeline Animation */
.pipeline-step.processing {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.6);
  }
  100% {
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .whis-pipeline {
    padding: 1.5rem;
  }

  .pipeline-step {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .step-connector {
    display: none;
  }

  .pipeline-title {
    font-size: 1.5rem;
  }
}
</style>
