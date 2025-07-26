<template>
  <div
    class="p-8 min-h-screen bg-gradient-to-br from-teal-900 to-teal-700 text-white"
  >
    <div
      class="backdrop-blur-md bg-white/10 p-6 rounded-2xl shadow-xl max-w-6xl mx-auto"
    >
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold">
          MCP Tool History
        </h1>
        <div class="flex gap-4">
          <button
            class="bg-black/30 hover:bg-black/40 px-4 py-2 rounded-lg transition flex items-center gap-2"
            @click="refreshData"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                clip-rule="evenodd"
              />
            </svg>
            Refresh
          </button>
        </div>
      </div>

      <!-- Stats Overview -->
      <div
        v-if="stats"
        class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8"
      >
        <div class="bg-black/20 rounded-xl p-4">
          <h3 class="text-sm text-teal-300 mb-1">
            Total Executions
          </h3>
          <p class="text-2xl font-bold">
            {{ stats.total_executions }}
          </p>
        </div>
        <div class="bg-black/20 rounded-xl p-4">
          <h3 class="text-sm text-teal-300 mb-1">
            Success Rate
          </h3>
          <p class="text-2xl font-bold">
            {{ stats.success_rate }}%
          </p>
        </div>
        <div class="bg-black/20 rounded-xl p-4">
          <h3 class="text-sm text-teal-300 mb-1">
            Avg. Duration
          </h3>
          <p class="text-2xl font-bold">
            {{ (stats.average_execution_time_ms / 1000).toFixed(2) }}s
          </p>
        </div>
        <div class="bg-black/20 rounded-xl p-4">
          <h3 class="text-sm text-teal-300 mb-1">
            Active Tools
          </h3>
          <p class="text-2xl font-bold">
            {{ tools.length }}
          </p>
        </div>
      </div>

      <!-- Loading State -->
      <div
        v-if="loading"
        class="flex items-center justify-center py-12"
      >
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-300"
        />
      </div>

      <!-- Tools List -->
      <div
        v-else-if="tools.length > 0"
        class="space-y-4"
      >
        <div
          v-for="tool in tools"
          :key="tool.name"
          class="tool-card"
        >
          <!-- Tool Header -->
          <div class="flex justify-between items-start mb-4">
            <div>
              <h2 class="text-xl font-semibold flex items-center gap-2">
                {{ tool.name }}
                <span
                  v-if="tool.auto"
                  class="bg-teal-500/20 text-teal-300 text-xs px-2 py-1 rounded"
                >Auto</span>
              </h2>
              <p class="text-sm text-teal-200 mt-1">
                {{ tool.description || 'No description provided.' }}
              </p>
              <div class="flex gap-2 mt-2">
                <span
                  v-for="tag in tool.tags"
                  :key="tag"
                  class="bg-black/20 text-xs px-2 py-1 rounded"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <div class="flex gap-2">
              <button
                :disabled="runningTools[tool.name]"
                class="run-button"
                @click="runTool(tool.name)"
              >
                <div
                  v-if="runningTools[tool.name]"
                  class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"
                />
                <span v-else>Run Now</span>
              </button>
            </div>
          </div>

          <!-- Tool Performance -->
          <div
            v-if="toolStats[tool.name]"
            class="grid grid-cols-3 gap-4 mb-4"
          >
            <div class="bg-black/10 rounded p-3">
              <div class="text-sm text-teal-300">
                Success Rate
              </div>
              <div class="text-lg font-semibold">
                {{ toolStats[tool.name].success_rate }}%
              </div>
            </div>
            <div class="bg-black/10 rounded p-3">
              <div class="text-sm text-teal-300">
                Total Runs
              </div>
              <div class="text-lg font-semibold">
                {{ toolStats[tool.name].total_executions }}
              </div>
            </div>
            <div class="bg-black/10 rounded p-3">
              <div class="text-sm text-teal-300">
                Avg. Duration
              </div>
              <div class="text-lg font-semibold">
                {{
                  (toolStats[tool.name].average_duration_ms / 1000).toFixed(2)
                }}s
              </div>
            </div>
          </div>

          <!-- Recent Executions -->
          <div
            v-if="toolStats[tool.name]?.recent_executions?.length"
            class="mt-4"
          >
            <h3 class="text-sm font-medium text-teal-300 mb-2">
              Recent Executions
            </h3>
            <div class="space-y-2">
              <div
                v-for="execution in toolStats[
                  tool.name
                ].recent_executions.slice(0, 3)"
                :key="execution.id"
                class="bg-black/10 rounded p-3 text-sm"
              >
                <div class="flex justify-between items-center mb-2">
                  <div class="flex items-center gap-2">
                    <span
                      :class="
                        execution.success
                          ? 'bg-green-500/20 text-green-300'
                          : 'bg-red-500/20 text-red-300'
                      "
                      class="px-2 py-0.5 rounded text-xs"
                    >
                      {{ execution.success ? 'Success' : 'Failed' }}
                    </span>
                    <span class="text-teal-300">{{
                      new Date(execution.timestamp).toLocaleString()
                    }}</span>
                  </div>
                  <span class="text-teal-300">{{ (execution.duration_ms / 1000).toFixed(2) }}s</span>
                </div>
                <div class="font-mono text-xs bg-black/20 p-2 rounded">
                  {{ execution.command }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-else
        class="text-center py-12"
      >
        <svg
          class="w-16 h-16 text-teal-300/50 mx-auto mb-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
          />
        </svg>
        <p class="text-teal-300/70">
          No tools found. Create your first tool in the MCP Tool Creator.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// State
const tools = ref([]);
const toolStats = ref({});
const stats = ref(null);
const loading = ref(true);
const runningTools = ref({});

// Methods
const fetchTools = async () => {
  try {
    const res = await axios.get('/mcp-tool/list');
    tools.value = res.data || [];

    // Fetch stats for each tool
    for (const tool of tools.value) {
      await fetchToolStats(tool.name);
    }
  } catch (err) {
    console.error('Failed to fetch tools:', err);
  }
};

const fetchToolStats = async (toolName) => {
  try {
    const res = await axios.get(`/mcp-tool/executions/${toolName}`);
    toolStats.value[toolName] = res.data;
  } catch (err) {
    console.error(`Failed to fetch stats for ${toolName}:`, err);
  }
};

const fetchGlobalStats = async () => {
  try {
    const res = await axios.get('/mcp-tool/status');
    stats.value = res.data;
  } catch (err) {
    console.error('Failed to fetch global stats:', err);
  }
};

const runTool = async (toolName) => {
  runningTools.value[toolName] = true;

  try {
    const res = await axios.post(`/mcp-tool/execute/${toolName}`);
    if (res.data.status === 'success') {
      // Refresh tool stats
      await fetchToolStats(toolName);
      await fetchGlobalStats();
    } else {
      throw new Error(res.data.result.error_message);
    }
  } catch (err) {
    console.error(`Failed to run ${toolName}:`, err);
    alert(`Failed to run tool: ${err.message}`);
  } finally {
    runningTools.value[toolName] = false;
  }
};

const refreshData = async () => {
  loading.value = true;
  await Promise.all([fetchTools(), fetchGlobalStats()]);
  loading.value = false;
};

// Initialize
onMounted(async () => {
  await refreshData();

  // Auto-refresh every 30 seconds
  setInterval(refreshData, 30000);
});
</script>

<style scoped>
.tool-card {
  @apply bg-white/10 border border-white/20 rounded-xl p-6 transition duration-300;
}

.tool-card:hover {
  @apply bg-white/15;
  transform: translateY(-1px);
}

.run-button {
  @apply bg-black text-white px-4 py-2 rounded flex items-center gap-2 transition;
}

.run-button:not(:disabled):hover {
  @apply bg-teal-700;
}

.run-button:disabled {
  @apply opacity-50 cursor-not-allowed;
}
</style>
