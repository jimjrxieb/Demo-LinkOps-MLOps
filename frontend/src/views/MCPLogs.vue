<!-- MCPLogs.vue -->
<template>
  <div class="p-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">
        🗒️ MCP Execution Logs
      </h1>
      <p class="text-gray-600">
        Monitor and analyze MCP tool execution history with comprehensive
        logging
      </p>
    </div>

    <!-- Controls and Filters -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-700">
        📊 Log Filters & Controls
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
        <!-- Search -->
        <div>
          <label class="block font-semibold mb-2 text-gray-700">🔍 Search:</label>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search tool names, commands..."
            class="border border-gray-300 px-4 py-2 rounded-lg w-full focus:ring-2 focus:ring-blue-500"
            @input="filterLogs"
          >
        </div>

        <!-- Status Filter -->
        <div>
          <label class="block font-semibold mb-2 text-gray-700">📊 Status:</label>
          <select
            v-model="statusFilter"
            class="border border-gray-300 px-4 py-2 rounded-lg w-full focus:ring-2 focus:ring-blue-500"
            @change="filterLogs"
          >
            <option value="">
              All Status
            </option>
            <option value="success">
              ✅ Success
            </option>
            <option value="failure">
              ❌ Failure
            </option>
          </select>
        </div>

        <!-- Tool Filter -->
        <div>
          <label class="block font-semibold mb-2 text-gray-700">🛠️ Tool:</label>
          <select
            v-model="toolFilter"
            class="border border-gray-300 px-4 py-2 rounded-lg w-full focus:ring-2 focus:ring-blue-500"
            @change="filterLogs"
          >
            <option value="">
              All Tools
            </option>
            <option
              v-for="tool in uniqueTools"
              :key="tool"
              :value="tool"
            >
              {{ tool }}
            </option>
          </select>
        </div>

        <!-- Limit -->
        <div>
          <label class="block font-semibold mb-2 text-gray-700">📋 Show:</label>
          <select
            v-model="limitFilter"
            class="border border-gray-300 px-4 py-2 rounded-lg w-full focus:ring-2 focus:ring-blue-500"
            @change="fetchLogs"
          >
            <option value="25">
              Last 25
            </option>
            <option value="50">
              Last 50
            </option>
            <option value="100">
              Last 100
            </option>
            <option value="200">
              Last 200
            </option>
          </select>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4">
        <button
          :disabled="loading"
          class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg font-semibold transition-colors duration-200 flex items-center gap-2"
          @click="refreshLogs"
        >
          <span
            v-if="loading"
            class="animate-spin"
          >⏳</span>
          <span v-else>🔄</span>
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>

        <button
          class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors duration-200"
          @click="clearFilters"
        >
          🧹 Clear Filters
        </button>

        <button
          :disabled="filteredLogs.length === 0"
          class="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg font-semibold transition-colors duration-200"
          @click="exportLogs"
        >
          📄 Export CSV
        </button>
      </div>
    </div>

    <!-- Statistics -->
    <div
      v-if="logs.length > 0"
      class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6"
    >
      <div class="bg-white rounded-lg shadow-md p-4">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-2xl">📊</span>
          <h3 class="font-semibold text-gray-700">
            Total Executions
          </h3>
        </div>
        <div class="text-2xl font-bold text-blue-600">
          {{ logs.length }}
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-4">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-2xl">✅</span>
          <h3 class="font-semibold text-gray-700">
            Successful
          </h3>
        </div>
        <div class="text-2xl font-bold text-green-600">
          {{ successCount }}
        </div>
        <div class="text-sm text-gray-500">
          {{ successRate }}%
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-4">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-2xl">❌</span>
          <h3 class="font-semibold text-gray-700">
            Failed
          </h3>
        </div>
        <div class="text-2xl font-bold text-red-600">
          {{ failureCount }}
        </div>
        <div class="text-sm text-gray-500">
          {{ failureRate }}%
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-4">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-2xl">⏱️</span>
          <h3 class="font-semibold text-gray-700">
            Avg Time
          </h3>
        </div>
        <div class="text-2xl font-bold text-purple-600">
          {{ averageExecutionTime }}s
        </div>
      </div>
    </div>

    <!-- Logs Table -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-xl font-semibold text-gray-700">
          📋 Execution History
          <span
            v-if="filteredLogs.length !== logs.length"
            class="text-sm text-gray-500"
          >
            ({{ filteredLogs.length }} of {{ logs.length }})
          </span>
        </h2>
      </div>

      <!-- Loading State -->
      <div
        v-if="loading"
        class="p-8 text-center"
      >
        <div class="animate-spin text-4xl mb-4">
          ⏳
        </div>
        <div class="text-gray-600">
          Loading execution logs...
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="logs.length === 0"
        class="p-8 text-center"
      >
        <div class="text-4xl mb-4">
          📋
        </div>
        <div class="text-gray-600 mb-4">
          No execution logs found
        </div>
        <div class="text-sm text-gray-500">
          Logs will appear here after tools are executed
        </div>
      </div>

      <!-- Filtered Empty State -->
      <div
        v-else-if="filteredLogs.length === 0"
        class="p-8 text-center"
      >
        <div class="text-4xl mb-4">
          🔍
        </div>
        <div class="text-gray-600 mb-4">
          No logs match your filters
        </div>
        <button
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          @click="clearFilters"
        >
          Clear Filters
        </button>
      </div>

      <!-- Logs Table -->
      <div
        v-else
        class="overflow-x-auto"
      >
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Status
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Tool Name
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Command
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Return Code
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Execution Time
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Timestamp
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="log in filteredLogs"
              :key="log.timestamp"
              class="hover:bg-gray-50 transition-colors duration-200"
            >
              <!-- Status -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <span class="text-2xl">{{ log.success ? '✅' : '❌' }}</span>
                  <div class="ml-2">
                    <div
                      class="text-sm font-medium"
                      :class="log.success ? 'text-green-800' : 'text-red-800'"
                    >
                      {{ log.success ? 'Success' : 'Failed' }}
                    </div>
                    <div
                      v-if="log.security_check_passed !== undefined"
                      class="text-xs"
                      :class="
                        log.security_check_passed
                          ? 'text-green-600'
                          : 'text-red-600'
                      "
                    >
                      {{
                        log.security_check_passed ? '🔒 Secure' : '⚠️ Security'
                      }}
                    </div>
                  </div>
                </div>
              </td>

              <!-- Tool Name -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">
                  {{ log.tool_name }}
                </div>
              </td>

              <!-- Command -->
              <td class="px-6 py-4">
                <div
                  class="text-sm text-gray-900 font-mono max-w-xs truncate"
                  :title="log.command"
                >
                  {{ log.command }}
                </div>
              </td>

              <!-- Return Code -->
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="
                    log.returncode === 0
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  "
                >
                  {{ log.returncode }}
                </span>
              </td>

              <!-- Execution Time -->
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ log.execution_time?.toFixed(2) || 'N/A' }}s
              </td>

              <!-- Timestamp -->
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatTimestamp(log.timestamp) }}
              </td>

              <!-- Actions -->
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  class="text-blue-600 hover:text-blue-900 mr-3"
                  @click="showLogDetails(log)"
                >
                  👁️ View
                </button>
                <button
                  class="text-green-600 hover:text-green-900"
                  @click="copyLogData(log)"
                >
                  📋 Copy
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Log Details Modal -->
    <div
      v-if="selectedLog"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    >
      <div
        class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col"
      >
        <!-- Modal Header -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900">
              {{ selectedLog.success ? '✅' : '❌' }} Execution Details -
              {{ selectedLog.tool_name }}
            </h3>
            <button
              class="text-gray-400 hover:text-gray-600 text-2xl"
              @click="selectedLog = null"
            >
              ✕
            </button>
          </div>
        </div>

        <!-- Modal Content -->
        <div class="p-6 overflow-y-auto flex-1">
          <!-- Basic Info -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div class="bg-gray-50 p-4 rounded-lg">
              <h4 class="font-semibold mb-2">
                📊 Execution Info
              </h4>
              <div class="space-y-2 text-sm">
                <div><strong>Tool:</strong> {{ selectedLog.tool_name }}</div>
                <div>
                  <strong>Status:</strong>
                  {{ selectedLog.success ? 'Success' : 'Failed' }}
                </div>
                <div>
                  <strong>Return Code:</strong> {{ selectedLog.returncode }}
                </div>
                <div>
                  <strong>Execution Time:</strong>
                  {{ selectedLog.execution_time?.toFixed(2) || 'N/A' }}s
                </div>
                <div>
                  <strong>Timestamp:</strong>
                  {{ formatTimestamp(selectedLog.timestamp) }}
                </div>
                <div v-if="selectedLog.security_check_passed !== undefined">
                  <strong>Security Check:</strong>
                  {{
                    selectedLog.security_check_passed
                      ? '✅ Passed'
                      : '❌ Failed'
                  }}
                </div>
              </div>
            </div>

            <div class="bg-gray-50 p-4 rounded-lg">
              <h4 class="font-semibold mb-2">
                🔧 Command
              </h4>
              <div
                class="bg-gray-900 text-green-300 p-3 rounded font-mono text-sm break-all"
              >
                {{ selectedLog.command }}
              </div>
            </div>
          </div>

          <!-- Output -->
          <div
            v-if="selectedLog.stdout"
            class="mb-6"
          >
            <h4 class="font-semibold mb-2">
              📤 Standard Output
            </h4>
            <div
              class="bg-gray-900 text-green-300 p-4 rounded-lg font-mono text-sm whitespace-pre-wrap max-h-64 overflow-y-auto"
            >
              {{ selectedLog.stdout }}
            </div>
          </div>

          <!-- Error Output -->
          <div
            v-if="selectedLog.stderr || selectedLog.error_message"
            class="mb-6"
          >
            <h4 class="font-semibold mb-2">
              ⚠️ Error Output
            </h4>
            <div
              class="bg-red-900 text-red-200 p-4 rounded-lg font-mono text-sm whitespace-pre-wrap max-h-64 overflow-y-auto"
            >
              {{ selectedLog.stderr || selectedLog.error_message }}
            </div>
          </div>

          <!-- Log File -->
          <div
            v-if="selectedLog.log_file"
            class="mb-6"
          >
            <h4 class="font-semibold mb-2">
              📁 Log File
            </h4>
            <div class="bg-blue-50 p-3 rounded-lg">
              <code class="text-sm">{{ selectedLog.log_file }}</code>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="p-6 border-t border-gray-200">
          <div class="flex justify-end gap-4">
            <button
              class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
              @click="copyLogData(selectedLog)"
            >
              📋 Copy Data
            </button>
            <button
              class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
              @click="selectedLog = null"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// Reactive data
const logs = ref([]);
const filteredLogs = ref([]);
const loading = ref(false);
const selectedLog = ref(null);

// Filters
const searchQuery = ref('');
const statusFilter = ref('');
const toolFilter = ref('');
const limitFilter = ref('50');

// Computed properties
const uniqueTools = computed(() => {
  const tools = [...new Set(logs.value.map((log) => log.tool_name))];
  return tools.sort();
});

const successCount = computed(() => {
  return logs.value.filter((log) => log.success).length;
});

const failureCount = computed(() => {
  return logs.value.filter((log) => !log.success).length;
});

const successRate = computed(() => {
  if (logs.value.length === 0) return 0;
  return Math.round((successCount.value / logs.value.length) * 100);
});

const failureRate = computed(() => {
  if (logs.value.length === 0) return 0;
  return Math.round((failureCount.value / logs.value.length) * 100);
});

const averageExecutionTime = computed(() => {
  if (logs.value.length === 0) return 0;
  const times = logs.value
    .filter((log) => log.execution_time != null)
    .map((log) => log.execution_time);
  if (times.length === 0) return 0;
  const avg = times.reduce((sum, time) => sum + time, 0) / times.length;
  return avg.toFixed(2);
});

// Methods
const fetchLogs = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
      `/api/mcp-tool/executions?limit=${limitFilter.value}`
    );
    logs.value = res.data.executions || [];
    filterLogs();
    console.log('✅ Fetched logs:', logs.value.length);
  } catch (err) {
    console.error('❌ Failed to fetch logs:', err);
    alert(
      'Failed to load execution logs. Please check your connection and try again.'
    );
  } finally {
    loading.value = false;
  }
};

const filterLogs = () => {
  let filtered = [...logs.value];

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (log) =>
        log.tool_name.toLowerCase().includes(query) ||
        log.command.toLowerCase().includes(query) ||
        (log.stdout && log.stdout.toLowerCase().includes(query)) ||
        (log.stderr && log.stderr.toLowerCase().includes(query))
    );
  }

  // Status filter
  if (statusFilter.value) {
    if (statusFilter.value === 'success') {
      filtered = filtered.filter((log) => log.success);
    } else if (statusFilter.value === 'failure') {
      filtered = filtered.filter((log) => !log.success);
    }
  }

  // Tool filter
  if (toolFilter.value) {
    filtered = filtered.filter((log) => log.tool_name === toolFilter.value);
  }

  filteredLogs.value = filtered;
};

const refreshLogs = async () => {
  await fetchLogs();
};

const clearFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  toolFilter.value = '';
  filterLogs();
};

const showLogDetails = (log) => {
  selectedLog.value = log;
};

const copyLogData = async (log) => {
  try {
    const logData = JSON.stringify(log, null, 2);
    await navigator.clipboard.writeText(logData);
    alert('Log data copied to clipboard!');
  } catch (err) {
    console.error('Failed to copy:', err);
    alert('Failed to copy log data');
  }
};

const exportLogs = () => {
  const headers = [
    'timestamp',
    'tool_name',
    'command',
    'success',
    'returncode',
    'execution_time',
    'stdout',
    'stderr',
  ];
  const csvContent = [
    headers.join(','),
    ...filteredLogs.value.map((log) =>
      headers
        .map((header) => {
          const value = log[header] || '';
          // Escape commas and quotes in CSV
          return `"${String(value).replace(/"/g, '""')}"`;
        })
        .join(',')
    ),
  ].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `mcp-execution-logs-${
    new Date().toISOString().split('T')[0]
  }.csv`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'Unknown';
  try {
    return new Date(timestamp).toLocaleString();
  } catch {
    return timestamp;
  }
};

// Lifecycle
onMounted(async () => {
  await fetchLogs();
});
</script>

<style scoped>
/* Custom scrollbar for modal content */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
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

/* Table hover effects */
tbody tr:hover {
  background-color: #f9fafb;
}

/* Modal backdrop blur */
.fixed.inset-0 {
  backdrop-filter: blur(4px);
}
</style>
