<template>
  <div>
    <!-- Header Timer -->
    <div
      v-if="store.isAuthenticated"
      class="session-timer"
    >
      Session: {{ formatTime(store.sessionTimeLeft) }}
    </div>

    <!-- Warning Banner -->
    <div
      v-if="store.showSessionWarning"
      class="session-warning"
    >
      <div class="warning-content">
        <div class="warning-icon">
          ⚠️
        </div>
        <div class="warning-text">
          <h3>Session Expiring Soon</h3>
          <p>
            Your session will expire in {{ formatTime(store.sessionTimeLeft) }}
          </p>
        </div>
        <button
          class="refresh-button"
          :disabled="refreshing"
          @click="refreshSession"
        >
          {{ refreshing ? 'Extending...' : 'Extend Session' }}
        </button>
        <button
          class="dismiss-button"
          @click="dismissWarning"
        >
          Dismiss
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useMainStore } from '@/store/useMainStore';

const store = useMainStore();
const refreshing = ref(false);

const formatTime = (seconds) => {
  if (!seconds || seconds <= 0) return '00:00';
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs
    .toString()
    .padStart(2, '0')}`;
};

const refreshSession = async () => {
  refreshing.value = true;
  try {
    await store.refreshSession();
  } finally {
    refreshing.value = false;
  }
};

const dismissWarning = () => {
  store.showSessionWarning = false;
};
</script>

<style scoped>
.session-timer {
  position: fixed;
  top: 1rem;
  right: 1rem;
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  color: #6c757d;
  border: 1px solid #dee2e6;
  z-index: 1000;
}

.session-warning {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #fff3cd;
  border: 1px solid #ffeeba;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-width: 400px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.warning-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.warning-icon {
  font-size: 24px;
}

.warning-text {
  flex-grow: 1;
}

.warning-text h3 {
  margin: 0;
  font-size: 16px;
  color: #856404;
}

.warning-text p {
  margin: 4px 0 0;
  font-size: 14px;
  color: #666;
}

.refresh-button {
  padding: 8px 16px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.refresh-button:not(:disabled):hover {
  background: #218838;
}

.refresh-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.dismiss-button {
  padding: 8px 16px;
  background: transparent;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-left: 8px;
  transition: all 0.2s;
}

.dismiss-button:hover {
  background: #f8f9fa;
  border-color: #c8c8c8;
}
</style>
