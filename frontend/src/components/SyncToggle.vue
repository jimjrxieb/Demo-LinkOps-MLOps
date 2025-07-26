<template>
  <div class="sync-toggle">
    <div class="toggle-container">
      <div class="toggle-header">
        <h3 class="toggle-title">
          🔄 Auto-Sync
        </h3>
        <div
          class="status-indicator"
          :class="statusClass"
        >
          <span class="status-dot" />
          <span class="status-text">{{ statusText }}</span>
        </div>
      </div>

      <div class="toggle-controls">
        <label class="toggle-switch">
          <input
            v-model="enabled"
            type="checkbox"
            :disabled="loading"
            class="toggle-input"
            @change="toggleSync"
          >
          <span class="toggle-slider" />
        </label>

        <div class="toggle-labels">
          <span class="toggle-label">{{
            enabled ? 'Enabled' : 'Disabled'
          }}</span>
          <span class="toggle-description">
            {{
              enabled
                ? 'Automatically process new files'
                : 'Manual processing only'
            }}
          </span>
        </div>
      </div>

      <div
        v-if="enabled"
        class="sync-info"
      >
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">📁 Watch Directory:</span>
            <span class="info-value">{{ config.watch_directory }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">📄 Supported Files:</span>
            <span class="info-value">{{
              config.supported_extensions.join(', ')
            }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">📊 Today Processed:</span>
            <span class="info-value">{{ stats.today_processed || 0 }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">❌ Today Failed:</span>
            <span class="info-value">{{ stats.today_failed || 0 }}</span>
          </div>
        </div>
      </div>

      <div
        v-if="error"
        class="error-message"
      >
        <span class="error-icon">⚠️</span>
        <span class="error-text">{{ error }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const enabled = ref(false);
const loading = ref(false);
const error = ref(null);
const config = ref({});
const stats = ref({});

// Polling interval for stats updates
let statsInterval = null;

const statusClass = computed(() => {
  if (loading.value) return 'status-loading';
  if (error.value) return 'status-error';
  return enabled.value ? 'status-active' : 'status-inactive';
});

const statusText = computed(() => {
  if (loading.value) return 'Loading...';
  if (error.value) return 'Error';
  return enabled.value ? 'Active' : 'Inactive';
});

const fetchSetting = async () => {
  try {
    loading.value = true;
    error.value = null;

    const response = await axios.get('/api/sync/setting');
    enabled.value = response.data.enabled;
    config.value = response.data.config || {};
  } catch (err) {
    console.error('Failed to fetch sync setting:', err);
    error.value = 'Failed to load sync settings';
  } finally {
    loading.value = false;
  }
};

const fetchStats = async () => {
  try {
    const response = await axios.get('/api/sync/stats');
    stats.value = response.data;
  } catch (err) {
    console.error('Failed to fetch sync stats:', err);
  }
};

const toggleSync = async () => {
  try {
    loading.value = true;
    error.value = null;

    await axios.post('/api/sync/setting', {
      enabled: enabled.value,
    });

    // Refresh stats after toggle
    await fetchStats();
  } catch (err) {
    console.error('Failed to update sync setting:', err);
    error.value = 'Failed to update sync settings';
    // Revert the toggle
    enabled.value = !enabled.value;
  } finally {
    loading.value = false;
  }
};

const startStatsPolling = () => {
  // Fetch stats immediately
  fetchStats();

  // Then poll every 30 seconds
  statsInterval = setInterval(fetchStats, 30000);
};

const stopStatsPolling = () => {
  if (statsInterval) {
    clearInterval(statsInterval);
    statsInterval = null;
  }
};

onMounted(() => {
  fetchSetting();
  startStatsPolling();
});

onUnmounted(() => {
  stopStatsPolling();
});
</script>

<style scoped>
.sync-toggle {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.toggle-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.toggle-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-active {
  background: #dcfce7;
  color: #166534;
}

.status-active .status-dot {
  background: #22c55e;
}

.status-inactive {
  background: #f3f4f6;
  color: #6b7280;
}

.status-inactive .status-dot {
  background: #9ca3af;
}

.status-loading {
  background: #dbeafe;
  color: #1e40af;
}

.status-loading .status-dot {
  background: #3b82f6;
  animation: pulse 2s infinite;
}

.status-error {
  background: #fef2f2;
  color: #dc2626;
}

.status-error .status-dot {
  background: #ef4444;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.toggle-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.toggle-input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 34px;
}

.toggle-slider:before {
  position: absolute;
  content: '';
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.toggle-input:checked + .toggle-slider {
  background-color: #3b82f6;
}

.toggle-input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

.toggle-input:disabled + .toggle-slider {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-labels {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.toggle-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.toggle-description {
  font-size: 0.75rem;
  color: #6b7280;
}

.sync-info {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 1rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
  border: 1px solid #f3f4f6;
}

.info-label {
  font-size: 0.875rem;
  color: #374151;
  font-weight: 500;
}

.info-value {
  font-size: 0.875rem;
  color: #6b7280;
  font-family: monospace;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 0.875rem;
}

.error-icon {
  font-size: 1rem;
}

.error-text {
  font-weight: 500;
}

@media (max-width: 640px) {
  .toggle-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .info-value {
    max-width: none;
  }
}
</style>
