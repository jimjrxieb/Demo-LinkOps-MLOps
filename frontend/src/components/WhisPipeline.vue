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

    <!-- Flowchart Container -->
    <div class="flowchart-container">
      <!-- Step 1: Input Processing -->
      <div class="flowchart-step input-step" :class="{ active: currentStep === 0 }">
        <div class="step-icon">📥</div>
        <div class="step-content">
          <h3 class="step-title">1. Input Processing</h3>
          <p class="step-description">Task input received and validated</p>
          <div class="step-status active">Active</div>
        </div>
      </div>

      <!-- Arrow Down -->
      <div class="flow-arrow vertical"></div>

      <!-- Step 2: Orb Library Search -->
      <div class="flowchart-step search-step" :class="{ active: currentStep === 1 }">
        <div class="step-icon">🔍</div>
        <div class="step-content">
          <h3 class="step-title">2. Orb Library Search</h3>
          <p class="step-description">Search existing solution patterns</p>
          <div class="step-status" :class="currentStep >= 1 ? 'active' : 'pending'">
            {{ currentStep >= 1 ? 'Searching...' : 'Pending' }}
          </div>
        </div>
      </div>

      <!-- Decision Diamond -->
      <div class="flow-arrow vertical"></div>
      <div class="decision-diamond" :class="{ active: currentStep === 2 }">
        <div class="diamond-content">
          <div class="diamond-text">
            <strong>Confidence ≥ 70%?</strong>
          </div>
        </div>
      </div>

      <!-- Split Flow -->
      <div class="split-container">
        <!-- Left Path: High Confidence -->
        <div class="flow-path left-path">
          <div class="flow-arrow horizontal-right"></div>
          <div class="flowchart-step solution-step high-confidence">
            <div class="step-icon">✅</div>
            <div class="step-content">
              <h3 class="step-title">Use Existing Orb</h3>
              <p class="step-description">Execute matched solution</p>
              <div class="confidence-badge high">High Confidence</div>
            </div>
          </div>
        </div>

        <!-- Right Path: Low Confidence - Whis Pipeline -->
        <div class="flow-path right-path">
          <div class="flow-arrow horizontal-left"></div>
          <div class="whis-section">
            <!-- 3. Sanitization with TensorFlow -->
            <div class="flowchart-step sanitize-step" :class="{ active: currentStep === 3 }">
              <div class="step-icon">🧹</div>
              <div class="step-content">
                <h3 class="step-title">3. Sanitization</h3>
                <p class="step-description">TensorFlow USE embeddings generation</p>
                <div class="tensorflow-info">
                  <div class="tf-badge">TensorFlow v2.15+</div>
                  <div class="embedding-details">
                    <span>• Universal Sentence Encoder</span>
                    <span>• 512-dimensional embeddings</span>
                    <span>• Semantic similarity matching</span>
                  </div>
                </div>
                <div class="step-status" :class="currentStep >= 3 ? 'processing' : 'pending'">
                  {{ currentStep >= 3 ? 'Processing' : 'Pending' }}
                </div>
              </div>
            </div>

            <div class="flow-arrow vertical small"></div>

            <!-- 4. Smithing with ML -->
            <div class="flowchart-step smithing-step" :class="{ active: currentStep === 4 }">
              <div class="step-icon">⚒️</div>
              <div class="step-content">
                <h3 class="step-title">4. Smithing</h3>
                <p class="step-description">AI processing and solution crafting</p>
                <div class="ml-details">
                  <div class="ml-components">
                    <span>• LangChain orchestration</span>
                    <span>• OpenAI GPT-4 integration</span>
                    <span>• Custom ML classifiers</span>
                  </div>
                </div>
                <div class="step-status" :class="currentStep >= 4 ? 'processing' : 'pending'">
                  {{ currentStep >= 4 ? 'Smithing Process Includes:' : 'Pending' }}
                </div>
                <div v-if="currentStep >= 4" class="smithing-process">
                  <ul>
                    <li>Analyze the task requirements</li>
                    <li>Identify key components and dependencies</li>
                    <li>Follow industry best practices</li>
                    <li>Implement with proper error handling</li>
                    <li>Test and validate the solution</li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="flow-arrow vertical small"></div>

            <!-- 5. Evaluation -->
            <div class="flowchart-step evaluation-step" :class="{ active: currentStep === 5 }">
              <div class="step-icon">📊</div>
              <div class="step-content">
                <h3 class="step-title">5. Evaluation</h3>
                <p class="step-description">Quality assessment and scoring</p>
                <div class="step-status" :class="currentStep >= 5 ? 'processing' : 'pending'">
                  {{ currentStep >= 5 ? 'Evaluating' : 'Pending' }}
                </div>
              </div>
            </div>

            <!-- Approval Decision -->
            <div v-if="currentStep >= 5" class="approval-section">
              <div class="flow-arrow vertical small"></div>
              <div class="approval-diamond">
                <div class="diamond-content">
                  <div class="diamond-text">
                    <strong>Approve Solution?</strong>
                  </div>
                </div>
              </div>
              
              <div class="approval-buttons">
                <button class="approve-btn" @click="approveSolution">
                  ✅ Approve & Save to Orb Library
                </button>
                <button class="reject-btn" @click="rejectSolution">
                  ❌ Reject - Request API Key Input
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress Indicator -->
      <div class="progress-section">
        <div class="progress-bar-container">
          <div class="progress-title">Step {{ Math.min(currentStep + 1, 5) }} of 5 ({{ Math.round(progressPercentage) }}% complete)</div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
          </div>
        </div>
      </div>
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
const emit = defineEmits(['step-click', 'approve-solution', 'reject-solution']);

// State for approve/reject functionality
const orbApproved = ref(false);
const runeApproved = ref(false);

// Computed
const progressPercentage = computed(() => {
  return (props.currentStep / 4) * 100; // 5 steps total (0-4)
});

// Methods
const approveSolution = () => {
  emit('approve-solution');
};

const rejectSolution = () => {
  emit('reject-solution');
};
</script>

<style scoped>
.whis-pipeline {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border-radius: 16px;
  padding: 2rem;
  margin: 2rem 0;
  border: 1px solid #334155;
}

.pipeline-header {
  text-align: center;
  margin-bottom: 2rem;
}

.pipeline-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f8fafc;
  margin-bottom: 0.5rem;
}

.pipeline-subtitle {
  color: #94a3b8;
  font-size: 0.875rem;
}

.flowchart-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 800px;
}

.flowchart-step {
  background: rgba(30, 41, 59, 0.8);
  border: 2px solid #475569;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 0.5rem;
  min-width: 280px;
  max-width: 320px;
  transition: all 0.3s ease;
  position: relative;
  backdrop-filter: blur(10px);
}

.flowchart-step.active {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

.step-icon {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 0.75rem;
}

.step-content {
  text-align: center;
}

.step-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f8fafc;
  margin-bottom: 0.5rem;
}

.step-description {
  color: #cbd5e1;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.step-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.step-status.active {
  background: #dcfce7;
  color: #166534;
}

.step-status.processing {
  background: #fef3c7;
  color: #92400e;
}

.step-status.pending {
  background: #e5e7eb;
  color: #374151;
}

.flow-arrow {
  position: relative;
  background: #64748b;
}

.flow-arrow.vertical {
  width: 2px;
  height: 40px;
  margin: 0.5rem 0;
}

.flow-arrow.vertical.small {
  height: 20px;
}

.flow-arrow.horizontal-right {
  width: 100px;
  height: 2px;
  margin: 1rem 0;
}

.flow-arrow.horizontal-left {
  width: 100px;
  height: 2px;
  margin: 1rem 0;
}

.flow-arrow::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
}

.flow-arrow.vertical::after {
  bottom: -6px;
  left: -3px;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 8px solid #64748b;
}

.flow-arrow.horizontal-right::after {
  right: -6px;
  top: -3px;
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
  border-left: 8px solid #64748b;
}

.flow-arrow.horizontal-left::after {
  left: -6px;
  top: -3px;
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
  border-right: 8px solid #64748b;
}

.decision-diamond {
  width: 150px;
  height: 150px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  transform: rotate(45deg);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1rem 0;
  border: 2px solid #d97706;
  transition: all 0.3s ease;
}

.decision-diamond.active {
  box-shadow: 0 0 20px rgba(251, 191, 36, 0.5);
}

.diamond-content {
  transform: rotate(-45deg);
  text-align: center;
  padding: 0.5rem;
}

.diamond-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: #92400e;
  line-height: 1.2;
}

.split-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1000px;
  margin: 2rem 0;
}

.flow-path {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.left-path {
  margin-right: 2rem;
}

.right-path {
  margin-left: 2rem;
}

.solution-step.high-confidence {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.confidence-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.confidence-badge.high {
  background: #dcfce7;
  color: #166534;
}

.whis-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tensorflow-info {
  margin-top: 0.75rem;
  text-align: left;
}

.tf-badge {
  background: linear-gradient(135deg, #ff6600, #ff8533);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-block;
  margin-bottom: 0.5rem;
}

.embedding-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.embedding-details span {
  font-size: 0.75rem;
  color: #94a3b8;
}

.ml-details {
  margin-top: 0.75rem;
}

.ml-components {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.ml-components span {
  font-size: 0.75rem;
  color: #94a3b8;
}

.smithing-process {
  margin-top: 0.75rem;
  text-align: left;
}

.smithing-process ul {
  margin: 0;
  padding-left: 1rem;
  font-size: 0.75rem;
  color: #cbd5e1;
}

.smithing-process li {
  margin-bottom: 0.25rem;
}

.approval-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
}

.approval-diamond {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  transform: rotate(45deg);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1rem 0;
  border: 2px solid #6d28d9;
}

.approval-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.approve-btn, .reject-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.approve-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.approve-btn:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-2px);
}

.reject-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.reject-btn:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-2px);
}

.progress-section {
  width: 100%;
  max-width: 600px;
  margin-top: 2rem;
}

.progress-bar-container {
  text-align: center;
}

.progress-title {
  color: #cbd5e1;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(100, 116, 139, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #1d4ed8);
  border-radius: 4px;
  transition: width 0.5s ease;
}

@media (max-width: 768px) {
  .split-container {
    flex-direction: column;
    align-items: center;
  }
  
  .left-path, .right-path {
    margin: 1rem 0;
  }
  
  .flowchart-step {
    min-width: 250px;
    max-width: 280px;
  }
  
  .approval-buttons {
    flex-direction: column;
    width: 100%;
  }
  
  .approve-btn, .reject-btn {
    width: 100%;
  }
}
</style>
