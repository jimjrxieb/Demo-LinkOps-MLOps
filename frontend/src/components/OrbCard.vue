<template>
  ;
  <div
    class="orb-card"
    @click="$emit('click', orb)"
  >
    ;
    <div class="orb-header">
      ;
      <div class="orb-icon">
        {{ orb.icon || '🔮' }}
      </div>;
      <div
        class="orb-priority"
        :class="orb.priority"
      >
        {{ orb.priority }}
      </div>;
    </div>;
    
    <div class="orb-content">
      ;
      <h3 class="orb-title">
        {{ orb.title }}
      </h3>;
      <p class="orb-description">
        {{ orb.description }}
      </p>;
      
      <div class="orb-metrics">
        ;
        <div class="metric">
          ;
          <span class="metric-label">Score</span>;
          <div class="score-bar">
            ;
            <div
              class="score-fill"
              :style="{ width: orb.score + '%' }"
            />;
          </div>;
          <span class="metric-value">{{ orb.score }}/100</span>;
        </div>;
      </div>;
    </div>;
    
    <div class="orb-footer">
      ;
      <span
        class="orb-status"
        :class="orb.status"
      >{{ orb.status }}</span>;
      <div class="orb-actions">
        ;
        <button
          class="action-btn"
          @click.stop="viewDetails"
        >
          ;
          <span class="btn-icon">👁️</span>;
        </button>;
        <button
          class="action-btn"
          @click.stop="editOrb"
        >
          ;
          <span class="btn-icon">✏️</span>;
        </button>;
      </div>;
    </div>;
  </div>;
</template>;
<script>
export default {
  name: 'OrbCard',
  props: {
    orb: {
      type: Object,
      required: true
    }
  },
  computed: {
    statusClass() {
      switch (this.orb.status) {
        case 'active': return 'orb-active'
        case 'pending': return 'orb-pending'
        case 'completed': return 'orb-completed'
        default: return ''
      }
    }
  },
  methods: {
    viewDetails() {
      this.$emit('view-details', this.orb);
    },
    editOrb() {
      this.$emit('edit-orb', this.orb);
    }
  }
}
</script>;
<style scoped>;
.orb-card {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.orb-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #00d4ff, #ff00ff);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.orb-card:hover::before {
  transform: scaleX(1);
}

.orb-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 212, 255, 0.3);
}

.orb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.orb-icon {
  font-size: 2rem;
  filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.5));
}

.orb-priority {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
}

.orb-priority.critical {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
  border: 1px solid #ff0000;
}

.orb-priority.high {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
  border: 1px solid #ffaa00;
}

.orb-priority.medium {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
  border: 1px solid #00d4ff;
}

.orb-priority.low {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
  border: 1px solid #00ff00;
}

.orb-content {
  margin-bottom: 1.5rem;
}

.orb-title {
  font-size: 1.2rem;
  color: #00d4ff;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.orb-description {
  color: #e0e0e0;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.orb-metrics {
  margin-top: 1rem;
}

.metric {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.metric-label {
  font-size: 0.8rem;
  color: #888;
  min-width: 50px;
}

.score-bar {
  flex: 1;
  height: 6px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 3px;
  overflow: hidden;
  position: relative;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #00d4ff, #00ff88);
  border-radius: 3px;
  transition: width 0.5s ease;
  position: relative;
}

.score-fill::after {
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

.metric-value {
  font-size: 0.8rem;
  color: #00d4ff;
  font-weight: bold;
  min-width: 50px;
  text-align: right;
}

.orb-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 212, 255, 0.2);
}

.orb-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
}

.orb-status.active {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
  border: 1px solid #00ff00;
}

.orb-status.pending {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
  border: 1px solid #ffaa00;
}

.orb-status.completed {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
  border: 1px solid #00d4ff;
}

.orb-status.failed {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
  border: 1px solid #ff0000;
}

.orb-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 6px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: rgba(0, 212, 255, 0.2);
  transform: scale(1.1);
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

.btn-icon {
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .orb-card {
    padding: 1rem;
  }
  
  .orb-title {
    font-size: 1.1rem;
  }
  
  .orb-description {
    font-size: 0.8rem;
  }
  
  .orb-actions {
    gap: 0.25rem;
  }
  
  .action-btn {
    padding: 0.4rem;
  }
}
</style>;
