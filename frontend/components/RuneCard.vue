<template>;
  <div class="rune-card" @click="$emit('click', rune)">;
    <div class="rune-header">;
      <div class="rune-icon">{{ getRuneIcon(rune.type) }}</div>;
      <div class="rune-cost">{{ rune.cost }} ⚡</div>;
    </div>;
    
    <div class="rune-content">;
      <h3 class="rune-name">{{ rune.name }}</h3>;
      <p class="rune-description">{{ rune.description }}</p>;
      
      <div class="rune-type">;
        <span class="type-badge" :class="rune.type">{{ rune.type }}</span>;
      </div>;
    </div>;
    
    <div class="rune-footer">;
      <button class="activate-btn" @click.stop="activateRune">;
        <span class="btn-icon">⚡</span>;
        Activate;
      </button>;
    </div>;
  </div>;
</template>;

<script>;
export default {
  name: 'RuneCard',
  props: {
    rune: {
      type: Object,
      required: true;
    }
  },
  methods: {
    getRuneIcon(type) {
      const icons = {
        'data-processing': '🔄',
        'security': '🛡️',
        'optimization': '⚡',
        'analysis': '🔍',
        'enhancement': '✨',
        'default': '🔮';
      }
      return icons[type] || icons.default;
    },
    activateRune() {
      this.$emit('activate', this.rune);
    }
  }
}
</script>;

<style scoped>;
.rune-card {
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

.rune-card::before {
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

.rune-card:hover::before {
  transform: scaleX(1);
}

.rune-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 212, 255, 0.3);
}

.rune-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.rune-icon {
  font-size: 2.5rem;
  filter: drop-shadow(0 0 15px rgba(0, 212, 255, 0.6));
}

.rune-cost {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
  border: 1px solid #ffaa00;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.rune-content {
  margin-bottom: 1.5rem;
}

.rune-name {
  font-size: 1.3rem;
  color: #00d4ff;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.rune-description {
  color: #e0e0e0;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.rune-type {
  margin-top: 1rem;
}

.type-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
}

.type-badge.data-processing {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
  border: 1px solid #00d4ff;
}

.type-badge.security {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
  border: 1px solid #ff0000;
}

.type-badge.optimization {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
  border: 1px solid #00ff00;
}

.type-badge.analysis {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
  border: 1px solid #ffaa00;
}

.type-badge.enhancement {
  background: rgba(255, 0, 255, 0.2);
  color: #ff00ff;
  border: 1px solid #ff00ff;
}

.rune-footer {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 212, 255, 0.2);
}

.activate-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.activate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.btn-icon {
  font-size: 1.1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .rune-card {
    padding: 1rem;
  }
  
  .rune-name {
    font-size: 1.1rem;
  }
  
  .rune-description {
    font-size: 0.8rem;
  }
  
  .rune-icon {
    font-size: 2rem;
  }
}
</style>;