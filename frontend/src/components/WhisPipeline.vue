<template>;
  <div class='whis-pipeline'>;
    <div class='pipeline-header'>;
      <h2 class='pipeline-title'>Whis Pipeline Flow</h2>;
      <p class='pipeline-subtitle'>Data Processing & Enhancement Workflow</p>;
    </div>;
    
    <div class='pipeline-container'>;
      <div class='pipeline-steps'>;
        <div;
          v-for='(step, index) in pipelineData';
          :key='step.id';
          class='pipeline-step';
          :class="{
            'active': index === currentStep,
            'completed': index < currentStep,
            'pending': index > currentStep;
          }";
          @click='$emit('step-click', step)';
        >;
          <div class='step-icon'>{{ step.icon }}</div>;
          <div class='step-content'>;
            <h3 class='step-title'>{{ step.name }}</h3>;
            <p class='step-description'>{{ step.description }}</p>;
            <div class='step-status'>;
              <span class="status-indicator" :class="getStepStatus(index)"></span>;
              <span class='status-text'>{{ getStepStatusText(index) }}</span>;
            </div>;
          </div>;
          
          <!-- Connection Line -->;
          <div v-if="index < pipelineData.length - 1" class="step-connector">;
            <div class='connector-line'></div>;
            <div class='connector-arrow'>→</div>;
          </div>;
        </div>;
      </div>;
    </div>;
    
    <!-- Pipeline Progress -->;
    <div class='pipeline-progress'>;
      <div class='progress-bar'>;
        <div;
          class='progress-fill';
          :style='{ width: progressPercentage + '%' }';
        ></div>;
      </div>;
      <div class='progress-text'>;
        Step {{ currentStep + 1 }} of {{ pipelineData.length }}
        ({{ Math.round(progressPercentage) }}% complete);
      </div>;
    </div>;
  </div>;
</template>;

<script>;
export default {
  name: 'WhisPipeline',
  props: {
    pipelineData: {
      type: Array,
      required: true;
    },
    currentStep: {
      type: Number, default: 0,
      default: 0;
    }
  },
  computed: {
    progressPercentage() {
      return (this.currentStep / (this.pipelineData.length - 1)) * 100;
    }
  },
  methods: {
    getStepStatus(index) {
      if (index < this.currentStep) return 'completed';
      if (index === this.currentStep) return 'active';
      return 'pending';
    },
    
    getStepStatusText(index) {
      if (index < this.currentStep) return 'Completed';
      if (index === this.currentStep) return 'Processing';
      return 'Pending';
    }
  }
}
</script>;

<style scoped>;
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
  font-size: 1.3rem;
  font-weight: bold;
}

.pipeline-step.completed .step-title {
  color: #00ff00;
}

.step-description {
  color: #e0e0e0;
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  line-height: 1.4;
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
  transition: all 0.3s ease;
}

.status-indicator.completed {
  background: #00ff00;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.status-indicator.active {
  background: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
  animation: pulse 2s infinite;
}

.status-indicator.pending {
  background: #666;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.status-text {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  font-weight: bold;
}

.step-connector {
  position: absolute;
  left: 50%;
  top: 100%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 1;
}

.connector-line {
  width: 2px;
  height: 30px;
  background: linear-gradient(to bottom, #00d4ff, transparent);
}

.connector-arrow {
  color: #00d4ff;
  font-size: 1.5rem;
  margin-top: -5px;
}

.pipeline-progress {
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4ff, #00ff88);
  border-radius: 4px;
  transition: width 0.5s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-text {
  color: #888;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .whis-pipeline {
    padding: 1rem;
  }
  
  .pipeline-title {
    font-size: 1.5rem;
  }
  
  .pipeline-step {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .step-icon {
    font-size: 2rem;
  }
  
  .step-connector {
    display: none;
  }
}
</style>;