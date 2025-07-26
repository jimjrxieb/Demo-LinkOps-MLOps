<!-- MCPExecution.vue -->
<template>
  <div class="p-6 max-w-6xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">
        🛠️ MCP Tool Execution
      </h1>
      <p class="text-gray-600">
        Execute MCP tools with real-time monitoring and comprehensive logging
      </p>
    </div>

    <!-- Tool Selection Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-700">
        📋 Tool Selection
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label
            for="tool"
            class="block font-semibold mb-2 text-gray-700"
          >Select Tool:</label>
          <select
            v-model="selectedTool"
            class="border border-gray-300 px-4 py-3 rounded-lg w-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            :disabled="loading"
          >
            <option
              disabled
              value=""
            >
              -- Select a Tool --
            </option>
            <option
              v-for="tool in tools"
              :key="tool.name"
              :value="tool.name"
            >
              {{ tool.name }} - {{ tool.description || 'No description' }}
            </option>
          </select>
        </div>

        <div
          v-if="selectedToolInfo"
          class="bg-blue-50 p-4 rounded-lg"
        >
          <h3 class="font-semibold text-blue-800 mb-2">
            Tool Details:
          </h3>
          <div class="text-sm text-blue-700">
            <p><strong>Type:</strong> {{ selectedToolInfo.task_type }}</p>
            <p>
              <strong>Auto:</strong>
              {{ selectedToolInfo.auto ? '✅ Enabled' : '❌ Disabled' }}
            </p>
            <p>
              <strong>Tags:</strong>
              {{ selectedToolInfo.tags.join(', ') || 'None' }}
            </p>
          </div>
        </div>
      </div>

      <div class="mt-4">
        <button
          :disabled="!selectedTool || loading"
          class="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-8 py-3 rounded-lg font-semibold transition-colors duration-200 flex items-center gap-2"
          @click="runTool"
        >
          <span
            v-if="loading"
            class="animate-spin"
          >⏳</span>
          <span v-else>🚀</span>
          {{ loading ? 'Running...' : 'Run Tool' }}
        </button>
      </div>
    </div>

    <!-- Execution Results -->
    <div
      v-if="result"
      class="bg-white rounded-lg shadow-md p-6 mb-6"
    >
      <h2 class="text-xl font-semibold mb-4 text-gray-700">
        📊 Execution Results
      </h2>

      <!-- Status Header -->
      <div
        class="mb-4 p-4 rounded-lg"
        :class="
          result.success
            ? 'bg-green-50 border border-green-200'
            : 'bg-red-50 border border-red-200'
        "
      >
        <div class="flex items-center gap-2">
          <span class="text-2xl">{{ result.success ? '✅' : '❌' }}</span>
          <div>
            <h3
              class="font-semibold"
              :class="result.success ? 'text-green-800' : 'text-red-800'"
            >
              {{ result.success ? 'Execution Successful' : 'Execution Failed' }}
            </h3>
            <p
              class="text-sm"
              :class="result.success ? 'text-green-600' : 'text-red-600'"
            >
              {{
                result.success
                  ? 'Tool executed successfully'
                  : result.error_message || 'Tool execution failed'
              }}
            </p>
          </div>
        </div>
      </div>

      <!-- Execution Details -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div class="bg-gray-50 p-3 rounded">
          <div class="text-sm text-gray-600">
            Command
          </div>
          <div class="font-mono text-sm break-all">
            {{ result.command }}
          </div>
        </div>
        <div class="bg-gray-50 p-3 rounded">
          <div class="text-sm text-gray-600">
            Return Code
          </div>
          <div
            class="font-semibold"
            :class="result.returncode === 0 ? 'text-green-600' : 'text-red-600'"
          >
            {{ result.returncode }}
          </div>
        </div>
        <div class="bg-gray-50 p-3 rounded">
          <div class="text-sm text-gray-600">
            Execution Time
          </div>
          <div class="font-semibold">
            {{ result.execution_time?.toFixed(2) || 'N/A' }}s
          </div>
        </div>
      </div>

      <!-- Output Section -->
      <div
        v-if="result.stdout"
        class="mb-4"
      >
        <h4 class="font-semibold mb-2 text-gray-700">
          📤 Standard Output:
        </h4>
        <div
          class="bg-gray-900 text-green-300 p-4 rounded-lg font-mono text-sm whitespace-pre-wrap max-h-96 overflow-y-auto"
        >
          {{ result.stdout }}
        </div>
      </div>

      <!-- Error Section -->
      <div
        v-if="result.stderr || result.error_message"
        class="mb-4"
      >
        <h4 class="font-semibold mb-2 text-gray-700">
          ⚠️ Error Output:
        </h4>
        <div
          class="bg-red-900 text-red-200 p-4 rounded-lg font-mono text-sm whitespace-pre-wrap max-h-96 overflow-y-auto"
        >
          {{ result.stderr || result.error_message }}
        </div>
      </div>

      <!-- Security Check -->
      <div
        v-if="result.security_check_passed !== undefined"
        class="mt-4 p-3 rounded-lg"
        :class="
          result.security_check_passed
            ? 'bg-green-50 border border-green-200'
            : 'bg-red-50 border border-red-200'
        "
      >
        <div class="flex items-center gap-2">
          <span>{{ result.security_check_passed ? '✅' : '❌' }}</span>
          <span
            class="font-semibold"
            :class="
              result.security_check_passed ? 'text-green-800' : 'text-red-800'
            "
          >
            Security Check:
            {{ result.security_check_passed ? 'Passed' : 'Failed' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Recent Executions -->
    <div
      v-if="recentExecutions.length > 0"
      class="bg-white rounded-lg shadow-md p-6"
    >
      <h2 class="text-xl font-semibold mb-4 text-gray-700">
        📋 Recent Executions
      </h2>

      <div class="space-y-3">
        <div
          v-for="execution in recentExecutions"
          :key="execution.timestamp"
          class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors duration-200"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-xl">{{ execution.success ? '✅' : '❌' }}</span>
              <div>
                <div class="font-semibold text-gray-800">
                  {{ execution.tool_name }}
                </div>
                <div class="text-sm text-gray-600">
                  {{ formatTimestamp(execution.timestamp) }}
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-sm text-gray-600">
                Return Code: {{ execution.returncode }}
              </div>
              <div class="text-sm text-gray-600">
                {{ execution.execution_time?.toFixed(2) || 'N/A' }}s
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div
      v-if="loading"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 flex items-center gap-4">
        <div class="animate-spin text-2xl">
          ⏳
        </div>
        <div>
          <div class="font-semibold">
            Executing Tool...
          </div>
          <div class="text-sm text-gray-600">
            {{ selectedTool }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const selectedTool = ref('');
const tools = ref([]);
const result = ref(null);
const loading = ref(false);
const recentExecutions = ref([]);

// Computed property for selected tool info
const selectedToolInfo = computed(() => {
  return tools.value.find((tool) => tool.name === selectedTool.value);
});

const fetchTools = async () => {
  try {
    const res = await axios.get('/api/mcp-tool/list');
    tools.value = res.data;
    console.log('✅ Fetched tools:', tools.value.length);
  } catch (err) {
    console.error('❌ Failed to fetch tools:', err);
    // Show user-friendly error
    alert('Failed to load tools. Please check your connection and try again.');
  }
};

const fetchRecentExecutions = async () => {
  try {
    const res = await axios.get('/api/mcp-tool/executions?limit=5');
    recentExecutions.value = res.data.executions || [];
  } catch (err) {
    console.error('❌ Failed to fetch recent executions:', err);
  }
};

const runTool = async () => {
  if (!selectedTool.value) return;

  loading.value = true;
  result.value = null;

  try {
    console.log('🚀 Executing tool:', selectedTool.value);
    const res = await axios.post(`/api/mcp-tool/execute/${selectedTool.value}`);
    result.value = res.data.result;
    console.log('✅ Tool execution completed:', result.value);

    // Refresh recent executions
    await fetchRecentExecutions();
  } catch (err) {
    console.error('❌ Tool execution failed:', err);
    result.value = {
      success: false,
      output: '',
      stderr: '',
      error_message: err.response?.data?.detail || 'Unknown error occurred',
      returncode: -1,
      command: '',
      execution_time: 0,
      security_check_passed: false,
    };
  } finally {
    loading.value = false;
  }
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'Unknown';
  try {
    return new Date(timestamp).toLocaleString();
  } catch {
    return timestamp;
  }
};

onMounted(async () => {
  await Promise.all([fetchTools(), fetchRecentExecutions()]);
});
</script>

<style scoped>
/* Custom scrollbar for output areas */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #374151;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* Animation for loading spinner */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
