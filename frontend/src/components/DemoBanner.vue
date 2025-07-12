<template>
  <div v-if="isDemoMode" class="demo-banner">
    <div class="banner-content">
      <div class="banner-icon">🚀</div>
      <div class="banner-text">
        <strong>LinkOps Demo Platform</strong>
        <span class="banner-description">
          This is the public LinkOps demo. Agent enhancement, refinement, and Runes are disabled. Only Orbs and fallback answers are shown.
        </span>
      </div>
      <button class="banner-close" @click="dismissBanner">
        <span class="close-icon">×</span>
      </button>
    </div>

    <!-- Animated border -->
    <div class="banner-border" />
  </div>
</template>

<script>
import { useMainStore } from '../store/index.js';

export default {
  name: 'DemoBanner',
  data() {
    return {
      isDismissed: false,
    };
  },
  computed: {
    isDemoMode() {
      const store = useMainStore();
      return store.authRole === 'demo' && !this.isDismissed;
    },
  },
  mounted() {
    // Check if banner was previously dismissed
    const dismissed = localStorage.getItem('demo-banner-dismissed');
    if (dismissed === 'true') {
      this.isDismissed = true;
    }
  },
  methods: {
    dismissBanner() {
      this.isDismissed = true;
      // Store dismissal in localStorage
      localStorage.setItem('demo-banner-dismissed', 'true');
    },
  },
};
</script>

<style scoped>
.demo-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: linear-gradient(
    90deg,
    rgba(0, 150, 255, 0.95),
    rgba(0, 100, 200, 0.95)
  );
  backdrop-filter: blur(15px);
  border-bottom: 3px solid #0096ff;
  z-index: 9999;
  animation: slideDown 0.6s ease-out;
  font-family: 'Orbitron', 'Courier New', monospace;
  box-shadow: 0 4px 20px rgba(0, 150, 255, 0.3);
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.banner-icon {
  font-size: 2rem;
  flex-shrink: 0;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.banner-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.banner-text strong {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

.banner-description {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.95rem;
  line-height: 1.4;
  font-weight: 400;
}

.banner-close {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
  backdrop-filter: blur(5px);
}

.banner-close:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

.close-icon {
  color: #ffffff;
  font-size: 1.8rem;
  font-weight: bold;
  line-height: 1;
}

.banner-border {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #0096ff, #00d4ff, #0096ff);
  animation: shimmer 3s linear infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .banner-content {
    padding: 0.75rem 1rem;
    gap: 1rem;
  }

  .banner-text {
    gap: 0.25rem;
  }

  .banner-text strong {
    font-size: 1rem;
  }

  .banner-description {
    font-size: 0.85rem;
  }

  .banner-close {
    width: 32px;
    height: 32px;
  }

  .close-icon {
    font-size: 1.5rem;
  }

  .banner-icon {
    font-size: 1.5rem;
  }
}
</style>
