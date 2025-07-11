<template>
  <div v-if="isDemoMode" class="demo-banner">
    <div class="banner-content">
      <div class="banner-icon">🎭</div>
      <div class="banner-text">
        <strong>Demo Mode Active</strong>
        <span class="banner-description">
          You're viewing simulated data. No real changes will be made to the
          system.
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
    rgba(255, 170, 0, 0.9),
    rgba(255, 140, 0, 0.9)
  );
  backdrop-filter: blur(10px);
  border-bottom: 2px solid #ffaa00;
  z-index: 9999;
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
  }
  to {
    transform: translateY(0);
  }
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.banner-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.banner-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.banner-text strong {
  color: #000;
  font-size: 1rem;
  font-weight: bold;
}

.banner-description {
  color: rgba(0, 0, 0, 0.8);
  font-size: 0.9rem;
}

.banner-close {
  background: rgba(0, 0, 0, 0.2);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.banner-close:hover {
  background: rgba(0, 0, 0, 0.3);
  transform: scale(1.1);
}

.close-icon {
  color: #000;
  font-size: 1.5rem;
  font-weight: bold;
  line-height: 1;
}

.banner-border {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #ffaa00, #ff8000, #ffaa00);
  animation: shimmer 2s linear infinite;
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
    gap: 0.75rem;
  }

  .banner-text {
    gap: 0.125rem;
  }

  .banner-text strong {
    font-size: 0.9rem;
  }

  .banner-description {
    font-size: 0.8rem;
  }

  .banner-close {
    width: 28px;
    height: 28px;
  }

  .close-icon {
    font-size: 1.2rem;
  }
}
</style>
