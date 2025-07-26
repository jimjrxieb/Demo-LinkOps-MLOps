<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">
      🚀 Auto Tool Runner Status
    </h1>

    <!-- Status Overview -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <div class="flex items-center">
          <div
            class="w-3 h-3 rounded-full mr-2"
            :class="runnerStatus === 'running' ? 'bg-green-500' : 'bg-red-500'"
          />
          <h3 class="font-semibold">
            Runner Status
          </h3>
        </div>
        <p
          class="text-lg font-bold mt-2"
          :class="
            runnerStatus === 'running' ? 'text-green-600' : 'text-red-600'
          "
        >
          {{ runnerStatus === 'running' ? '🟢 Running' : '🔴 Stopped' }}
        </p>
      </div>

      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <h3 class="font-semibold">
          Auto-Enabled Tools
        </h3>
        <p class="text-2xl font-bold text-blue-600 mt-2">
          {{ autoToolsCount }}
        </p>
        <p class="text-sm text-gray-600">
          tools configured
        </p>
      </div>

      <div class="bg-white p-4 rounded-lg shadow-sm border">
        <h3 class="font-semibold">
          Last Execution
        </h3>
        <p class="text-lg font-bold mt-2 text-gray-800">
          {{ lastExecutionTime || 'Never' }}
        </p>
        <p class="text-sm text-gray-600">
          {{ lastExecutionTool || '' }}
        </p>
      </div>
    </div>

    <!-- Control Buttons -->
    <div class="flex gap-4 mb-6">
      <button
        class="btn btn-secondary"
        :disabled="loading"
        @click="checkRunnerStatus"
      >
        🔄 Refresh Status
      </button>
      <button
        class="btn btn-success"
        :disabled="loading || runnerStatus === 'running'"
        @click="startRunner"
      >
        ▶️ Start Runner
      </button>
      <button
        class="btn btn-danger"
        :disabled="loading || runnerStatus === 'stopped'"
        @click="stopRunner"
      >
        ⏹️ Stop Runner
      </button>
    </div>

    <!-- Auto-Enabled Tools List -->
    <div class="bg-white p-4 rounded-lg shadow-sm border mb-6">
      <h2 class="text-lg font-semibold mb-4">
        🔧 Auto-Enabled Tools
      </h2>
      <div
        v-if="autoTools.length === 0"
        class="text-gray-500 text-center py-4"
      >
        No auto-enabled tools found. Create tools with "Auto Execute" enabled in
        the MCP Tool Creator.
      </div>
      <div
        v-else
        class="grid gap-3"
      >
        <div
          v-for="tool in autoTools"
          :key="tool.name"
          class="flex items-center justify-between p-3 bg-gray-50 rounded"
        >
          <div>
            <h4 class="font-medium">
              {{ tool.name }}
            </h4>
            <p class="text-sm text-gray-600">
              {{ tool.description }}
            </p>
            <p class="text-xs text-gray-500 font-mono">
              {{ tool.command }}
            </p>
          </div>
          <span
            class="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-medium"
          >🚀 Auto</span>
        </div>
      </div>
    </div>

    <!-- Recent Executions -->
    <div class="bg-white p-4 rounded-lg shadow-sm border">
      <h2 class="text-lg font-semibold mb-4">
        📋 Recent Executions
      </h2>
      <div
        v-if="recentExecutions.length === 0"
        class="text-gray-500 text-center py-4"
      >
        No recent executions found.
      </div>
      <div
        v-else
        class="space-y-3"
      >
        <div
          v-for="execution in recentExecutions"
          :key="execution.id"
          class="flex items-center justify-between p-3 border rounded"
        >
          <div class="flex-1">
            <div class="flex items-center gap-2">
              <h4 class="font-medium">
                {{ execution.tool_name || 'Unknown Tool' }}
              </h4>
              <span
                class="px-2 py-1 rounded text-xs font-medium"
                :class="
                  execution.success
                    ? 'bg-green-100 text-green-700'
                    : 'bg-red-100 text-red-700'
                "
              >
                {{ execution.success ? '✅ Success' : '❌ Failed' }}
              </span>
            </div>
            <p class="text-sm text-gray-600">
              {{ formatTimestamp(execution.timestamp) }}
            </p>
            <p class="text-xs text-gray-500">
              Duration: {{ execution.duration_ms }}ms
            </p>
          </div>
          <div class="text-right">
            <p class="text-sm font-mono text-gray-600">
              {{ execution.returncode }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div
      v-if="loading"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg">
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"
        />
        <p class="mt-2 text-center">
          Loading...
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const loading = ref(false);
const runnerStatus = ref('unknown');
const autoToolsCount = ref(0);
const lastExecutionTime = ref(null);
const lastExecutionTool = ref(null);
const autoTools = ref([]);
const recentExecutions = ref([]);

const checkRunnerStatus = async () => {
  loading.value = true;
  try {
    // Check if auto runner is running (this would need a backend endpoint)
    const response = await axios.get('/api/auto-runner/status');
    runnerStatus.value = response.data.status;
  } catch (error) {
    console.error('Error checking runner status:', error);
    runnerStatus.value = 'unknown';
  } finally {
    loading.value = false;
  }
};

const startRunner = async () => {
  loading.value = true;
  try {
    await axios.post('/api/auto-runner/start');
    await checkRunnerStatus();
  } catch (error) {
    console.error('Error starting runner:', error);
  } finally {
    loading.value = false;
  }
};

const stopRunner = async () => {
  loading.value = true;
  try {
    await axios.post('/api/auto-runner/stop');
    await checkRunnerStatus();
  } catch (error) {
    console.error('Error stopping runner:', error);
  } finally {
    loading.value = false;
  }
};

const loadAutoTools = async () => {
  try {
    const response = await axios.get('/api/mcp-tool/list');
    autoTools.value = response.data.filter((tool) => tool.auto);
    autoToolsCount.value = autoTools.value.length;
  } catch (error) {
    console.error('Error loading auto tools:', error);
  }
};

const loadRecentExecutions = async () => {
  try {
    const response = await axios.get('/api/auto-runner/executions?limit=10');
    recentExecutions.value = response.data;

    if (recentExecutions.value.length > 0) {
      const last = recentExecutions.value[0];
      lastExecutionTime.value = formatTimestamp(last.timestamp);
      lastExecutionTool.value = last.tool_name;
    }
  } catch (error) {
    console.error('Error loading recent executions:', error);
  }
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'Unknown';
  const date = new Date(timestamp);
  return date.toLocaleString();
};

const refreshData = async () => {
  await Promise.all([
    checkRunnerStatus(),
    loadAutoTools(),
    loadRecentExecutions(),
  ]);
};

onMounted(() => {
  refreshData();

  // Refresh data every 30 seconds
  setInterval(refreshData, 30000);
});
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded font-medium transition-colors;
}

.btn-secondary {
  @apply bg-gray-500 text-white hover:bg-gray-600;
}

.btn-success {
  @apply bg-green-600 text-white hover:bg-green-700;
}

.btn-danger {
  @apply bg-red-600 text-white hover:bg-red-700;
}

.btn:disabled {
  @apply opacity-50 cursor-not-allowed;
}
</style>
