<template>
  <div class="pipeline-container">
    <div class="pipeline-header">
      <h2>🧠 Whis Learning Pipeline (Simulated)</h2>
      <p class="pipeline-subtitle">
        This task was not found in the Orb Library. Here's how Whis would learn it:
      </p>
    </div>

    <div class="pipeline-steps">
      <div 
        v-for="(step, index) in steps" 
        :key="index" 
        class="pipeline-step"
        :class="{ 'active': currentStep >= index }"
      >
        <div class="step-header">
          <div class="step-number">{{ index + 1 }}</div>
          <h3>{{ step.title }}</h3>
        </div>
        <p class="step-description">{{ step.description }}</p>
        <div class="step-status">
          <span v-if="currentStep >= index" class="status-completed">✅ Completed</span>
          <span v-else class="status-pending">⏳ Pending</span>
        </div>
        <div v-if="step.tools" class="step-tools">
          <strong>Tools:</strong> {{ step.tools }}
        </div>
      </div>
    </div>

    <div class="pipeline-footer">
      <div class="final-note">
        <h4>🎯 Learning Outcome</h4>
        <p>✅ Task learned and a new Orb + Rune would be created in full system.</p>
        <p>📌 Note: In demo mode, actual learning is disabled.</p>
      </div>
      
      <div class="demo-info">
        <h4>🔍 Demo Mode Information</h4>
        <ul>
          <li>This is a simulation of the Whis MLOps pipeline</li>
          <li>In production, Whis would create new Orbs and Runes</li>
          <li>Each step uses specialized AI models and tools</li>
          <li>The pipeline ensures quality and consistency</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentStep = ref(-1)

const steps = [
  {
    title: "Task Received in whis_data_input",
    description: "Tasks are input from text, Q&A, images, or YouTube transcripts. The system captures and normalizes the input for processing.",
    tools: "Text processing, Image analysis, YouTube API"
  },
  {
    title: "Sanitization in whis_sanitize", 
    description: "Whis removes sensitive data, structures input, and engineers it into clean ML-ready format. This ensures data quality and security.",
    tools: "Data cleaning, PII detection, Structure validation"
  },
  {
    title: "Smithing in whis_smithing",
    description: "Whis analyzes the cleaned input, applies AI reasoning to generate Orbs and Runes. This is where the core learning happens.",
    tools: "AI reasoning, Pattern recognition, Orb generation"
  },
  {
    title: "Enhancement in whis_enhance",
    description: "After human approval, new Orbs/Runes are stored under categories like CI, CD, Security, and GitOps philosophy.",
    tools: "Category classification, Metadata enrichment, Storage"
  }
]

// Simulate pipeline progression
onMounted(() => {
  let step = 0
  const interval = setInterval(() => {
    currentStep.value = step
    step++
    if (step >= steps.length) {
      clearInterval(interval)
    }
  }, 800) // 800ms between steps
})
</script>

<style scoped>
.pipeline-container {
  padding: 2rem;
  background: linear-gradient(135deg, #101820 0%, #1e2b35 100%);
  border-radius: 12px;
  color: #f8f8f8;
  border: 1px solid #2c3e50;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.pipeline-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #00bcd4;
}

.pipeline-header h2 {
  color: #00bcd4;
  margin-bottom: 0.5rem;
  font-size: 1.8rem;
}

.pipeline-subtitle {
  color: #bdc3c7;
  font-size: 1.1rem;
  margin: 0;
}

.pipeline-steps {
  margin-bottom: 2rem;
}

.pipeline-step {
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  border-left: 4px solid #34495e;
  background: rgba(30, 43, 53, 0.6);
  border-radius: 0 8px 8px 0;
  transition: all 0.3s ease;
  opacity: 0.6;
}

.pipeline-step.active {
  border-left-color: #00bcd4;
  background: rgba(30, 43, 53, 0.9);
  opacity: 1;
  box-shadow: 0 4px 16px rgba(0, 188, 212, 0.2);
}

.step-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.step-number {
  background: #00bcd4;
  color: #101820;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 1rem;
  font-size: 1.1rem;
}

.pipeline-step.active .step-number {
  background: #00e676;
  animation: pulse 2s infinite;
}

.step-header h3 {
  margin: 0;
  color: #00bcd4;
  font-size: 1.3rem;
}

.pipeline-step.active .step-header h3 {
  color: #00e676;
}

.step-description {
  color: #ecf0f1;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.step-status {
  margin-bottom: 0.5rem;
}

.status-completed {
  color: #00e676;
  font-weight: bold;
  font-size: 1.1rem;
}

.status-pending {
  color: #f39c12;
  font-weight: bold;
  font-size: 1.1rem;
}

.step-tools {
  background: rgba(52, 73, 94, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #bdc3c7;
}

.pipeline-footer {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.final-note, .demo-info {
  background: rgba(40, 56, 69, 0.8);
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #ff9800;
}

.final-note h4, .demo-info h4 {
  color: #ff9800;
  margin-top: 0;
  margin-bottom: 1rem;
}

.final-note p, .demo-info p {
  margin-bottom: 0.5rem;
  color: #ecf0f1;
}

.demo-info ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #bdc3c7;
}

.demo-info li {
  margin-bottom: 0.5rem;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .pipeline-container {
    padding: 1rem;
  }
  
  .pipeline-footer {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .step-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .step-number {
    margin-bottom: 0.5rem;
    margin-right: 0;
  }
}
</style> 