<template>
  <div class="p-6 animate-slide-in bg-gray-900 text-white min-h-screen">
    <div class="max-w-4xl mx-auto">
      <h2 class="text-3xl font-bold mb-6 text-blue-400">
        Demo RAG: Kubernetes Model Interaction
      </h2>
      <p class="mb-6 text-gray-300 text-lg">
        Ask questions or assign tasks about the Kubernetes ML model. Experience
        intelligent task ranking and execution.
      </p>

      <!-- Query Input Section -->
      <div class="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
        <div class="flex space-x-4 mb-4">
          <input
            v-model="query"
            type="text"
            placeholder="e.g., What is Kubernetes? or Deploy app to cluster"
            class="flex-1 p-3 bg-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-600"
            @keyup.enter="handleQuery"
          >
          <button
            class="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200 animate-pulse-slow"
            :disabled="!query.trim()"
            @click="handleQuery"
          >
            <span v-if="!loading">Submit Query</span>
            <span
              v-else
              class="flex items-center"
            >
              <svg
                class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                />
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Processing...
            </span>
          </button>
        </div>

        <!-- Quick Query Buttons -->
        <div class="flex flex-wrap gap-2">
          <button
            v-for="quickQuery in quickQueries"
            :key="quickQuery"
            class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm transition-colors duration-200"
            @click="
              query = quickQuery;
              handleQuery();
            "
          >
            {{ quickQuery }}
          </button>
        </div>
      </div>

      <!-- Response Section -->
      <div
        v-if="response"
        class="bg-gray-800 rounded-lg p-6 border border-gray-700 animate-slide-in"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-semibold text-green-400">
            Response
          </h3>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-400">Confidence:</span>
            <div class="flex items-center">
              <div class="w-16 bg-gray-700 rounded-full h-2 mr-2">
                <div
                  class="bg-green-500 h-2 rounded-full transition-all duration-500"
                  :style="{ width: response.rank * 100 + '%' }"
                />
              </div>
              <span class="text-sm font-mono">{{ (response.rank * 100).toFixed(1) }}%</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-700 rounded-lg p-4 mb-4">
          <p class="text-gray-200 leading-relaxed">
            {{ response.response }}
          </p>
        </div>

        <div class="flex space-x-4">
          <button
            class="bg-green-600 hover:bg-green-700 px-6 py-2 rounded-lg font-semibold transition-all duration-200 flex items-center"
            @click="executeTask"
          >
            <svg
              class="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            Execute Task
          </button>
          <button
            class="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg font-semibold transition-all duration-200 flex items-center"
            @click="saveToHistory"
          >
            <svg
              class="w-5 h-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
              />
            </svg>
            Save to History
          </button>
        </div>
      </div>

      <!-- Query History -->
      <div
        v-if="queryHistory.length > 0"
        class="mt-8"
      >
        <h3 class="text-xl font-semibold mb-4 text-blue-400">
          Recent Queries
        </h3>
        <div class="space-y-3">
          <div
            v-for="(item, index) in queryHistory.slice(-5)"
            :key="index"
            class="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors duration-200"
          >
            <div class="flex justify-between items-start">
              <div>
                <p class="font-medium text-gray-200">
                  {{ item.query }}
                </p>
                <p class="text-sm text-gray-400 mt-1">
                  {{ item.response.substring(0, 100) }}...
                </p>
              </div>
              <span class="text-xs text-gray-500">{{ item.timestamp }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DemoRAG',
  data() {
    return {
      query: '',
      response: null,
      loading: false,
      queryHistory: [],
      quickQueries: [
        'What is Kubernetes?',
        'How to deploy an app?',
        'Optimize cluster performance',
        'Scale pods automatically',
        'Monitor cluster health',
      ],
      mockResponses: [
        {
          query: 'what is kubernetes',
          response:
            'Kubernetes is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. It provides features like load balancing, service discovery, and automated rollouts/rollbacks.',
          rank: 0.95,
        },
        {
          query: 'deploy app',
          response:
            'To deploy an app on Kubernetes, create a YAML manifest with deployment, service, and ingress configurations. Use kubectl apply -f manifest.yaml to deploy. The system will automatically schedule pods across available nodes.',
          rank: 0.92,
        },
        {
          query: 'optimize cluster',
          response:
            'Cluster optimization involves adjusting resource limits, enabling horizontal pod autoscaling, implementing proper resource requests, and using node affinity for workload distribution. Monitor metrics with Prometheus and Grafana.',
          rank: 0.88,
        },
        {
          query: 'scale pods',
          response:
            'Use HorizontalPodAutoscaler (HPA) to automatically scale pods based on CPU/memory metrics. Set min/max replicas and target utilization. For manual scaling, use kubectl scale deployment <name> --replicas=<number>.',
          rank: 0.9,
        },
        {
          query: 'monitor cluster',
          response:
            'Implement monitoring with Prometheus for metrics collection, Grafana for visualization, and AlertManager for notifications. Monitor node health, pod status, resource usage, and application metrics.',
          rank: 0.87,
        },
      ],
    };
  },
  methods: {
    async handleQuery() {
      if (!this.query.trim()) return;

      this.loading = true;

      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Find matching response or generate default
      const found = this.mockResponses.find((r) =>
        this.query.toLowerCase().includes(r.query.toLowerCase())
      ) || {
        response:
          "I understand you're asking about Kubernetes. While I don't have a specific response for this query, I can help with deployment, scaling, monitoring, and optimization tasks. Try asking about specific Kubernetes operations!",
        rank: 0.75,
      };

      this.response = found;
      this.loading = false;
    },

    executeTask() {
      // Simulate task execution
      this.$toast?.success(
        'Task execution simulated! This would trigger actual Kubernetes operations in production.'
      );
    },

    saveToHistory() {
      if (this.response) {
        this.queryHistory.push({
          query: this.query,
          response: this.response.response,
          timestamp: new Date().toLocaleTimeString(),
          rank: this.response.rank,
        });
        this.$toast?.success('Query saved to history!');
      }
    },
  },
};
</script>

<style scoped>
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.02);
    opacity: 0.9;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes slideIn {
  0% {
    transform: translateY(20px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-pulse-slow {
  animation: pulse 2s infinite;
}

.animate-slide-in {
  animation: slideIn 0.5s ease-out;
}

/* Custom scrollbar for better UX */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #374151;
}

::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
