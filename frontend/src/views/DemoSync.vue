<template>
  <div class="demo-sync-container">
    <div class="max-w-4xl mx-auto p-6">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">🔄 Demo Sync</h1>
        <p class="text-gray-600">
          Load demo data for ZRS Property Management demonstration
        </p>
      </div>

      <!-- Status Card -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">📊 Demo Data Status</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 rounded-full" :class="statusColor"></div>
            <span class="text-sm font-medium">{{ statusText }}</span>
          </div>
          <div class="text-sm text-gray-600">
            File: demo_data/delinquency.csv
          </div>
        </div>
      </div>

      <!-- Sync Controls -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">⚡ Sync Controls</h2>

        <div class="space-y-4">
          <!-- Sync Button -->
          <div class="flex items-center space-x-4">
            <button
              @click="syncDemoData"
              :disabled="loading"
              class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <span v-if="loading" class="flex items-center space-x-2">
                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                    fill="none"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                <span>Syncing...</span>
              </span>
              <span v-else>🔄 Sync Demo Data</span>
            </button>

            <button
              @click="clearDemoData"
              :disabled="loading"
              class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              🗑️ Clear Data
            </button>
          </div>

          <!-- Status Message -->
          <div v-if="message" class="p-4 rounded-lg" :class="messageClass">
            <div class="flex items-center space-x-2">
              <span v-if="messageType === 'success'" class="text-green-600"
                >✅</span
              >
              <span v-else-if="messageType === 'error'" class="text-red-600"
                >❌</span
              >
              <span v-else class="text-blue-600">ℹ️</span>
              <span>{{ message }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Demo Data Preview -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">📋 Demo Data Preview</h2>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Name
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Amount Due
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Property Address
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Due Date
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(row, index) in demoData" :key="index">
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                >
                  {{ row.name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${{ row.amount_due }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ row.property_address }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ row.due_date }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    :class="
                      row.status === 'overdue'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-yellow-100 text-yellow-800'
                    "
                  >
                    {{ row.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Instructions -->
      <div class="bg-blue-50 rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-blue-900">📖 How to Use</h2>
        <div class="space-y-3 text-blue-800">
          <div class="flex items-start space-x-3">
            <span class="text-blue-600 font-bold">1.</span>
            <p>
              Click <strong>"Sync Demo Data"</strong> to load the delinquency
              data into the RAG index
            </p>
          </div>
          <div class="flex items-start space-x-3">
            <span class="text-blue-600 font-bold">2.</span>
            <p>
              Go to the <strong>RAG Search</strong> tab to query the loaded data
            </p>
          </div>
          <div class="flex items-start space-x-3">
            <span class="text-blue-600 font-bold">3.</span>
            <p>
              Try queries like: "Who has overdue payments?" or "What's the total
              amount due?"
            </p>
          </div>
          <div class="flex items-start space-x-3">
            <span class="text-blue-600 font-bold">4.</span>
            <p>
              Use <strong>"Clear Data"</strong> to reset the demo and see the
              fallback message
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// Reactive state
const loading = ref(false);
const message = ref('');
const messageType = ref('info');
const demoStatus = ref('unknown');

// Demo data for preview
const demoData = ref([
  {
    name: 'IronMan',
    amount_due: '2,500',
    property_address: '10880 Malibu Point',
    due_date: '2024-01-15',
    status: 'overdue',
  },
  {
    name: 'BlackWidow',
    amount_due: '1,500',
    property_address: '123 Red Room Blvd',
    due_date: '2024-01-20',
    status: 'overdue',
  },
  {
    name: 'Hulk',
    amount_due: '3,000',
    property_address: '742 Evergreen Terrace',
    due_date: '2024-01-10',
    status: 'overdue',
  },
  {
    name: 'Thor',
    amount_due: '2,000',
    property_address: '1 Asgard Palace',
    due_date: '2024-01-25',
    status: 'overdue',
  },
  {
    name: 'Hawkeye',
    amount_due: '1,000',
    property_address: '456 Archer Lane',
    due_date: '2024-01-30',
    status: 'overdue',
  },
  {
    name: 'CaptainAmerica',
    amount_due: '1,800',
    property_address: '789 Brooklyn Heights',
    due_date: '2024-02-01',
    status: 'pending',
  },
  {
    name: 'SpiderMan',
    amount_due: '1,200',
    property_address: '321 Queens Blvd',
    due_date: '2024-02-05',
    status: 'pending',
  },
  {
    name: 'BlackPanther',
    amount_due: '3,500',
    property_address: '1 Wakanda Way',
    due_date: '2024-02-10',
    status: 'pending',
  },
  {
    name: 'ScarletWitch',
    amount_due: '2,200',
    property_address: '555 Westview Ave',
    due_date: '2024-02-15',
    status: 'pending',
  },
  {
    name: 'Vision',
    amount_due: '2,800',
    property_address: '777 Mind Stone Dr',
    due_date: '2024-02-20',
    status: 'pending',
  },
]);

// Computed properties
const statusColor = computed(() => {
  switch (demoStatus.value) {
    case 'loaded':
      return 'bg-green-500';
    case 'not_loaded':
      return 'bg-yellow-500';
    case 'error':
      return 'bg-red-500';
    default:
      return 'bg-gray-500';
  }
});

const statusText = computed(() => {
  switch (demoStatus.value) {
    case 'loaded':
      return 'Demo data loaded';
    case 'not_loaded':
      return 'Demo data not loaded';
    case 'error':
      return 'Error checking status';
    default:
      return 'Checking status...';
  }
});

const messageClass = computed(() => {
  switch (messageType.value) {
    case 'success':
      return 'bg-green-50 border border-green-200';
    case 'error':
      return 'bg-red-50 border border-red-200';
    default:
      return 'bg-blue-50 border border-blue-200';
  }
});

// Methods
const showMessage = (text, type = 'info') => {
  message.value = text;
  messageType.value = type;
  setTimeout(() => {
    message.value = '';
  }, 5000);
};

const checkStatus = async () => {
  try {
    const response = await axios.get('/api/demo/status');
    demoStatus.value = response.data.status;
  } catch (error) {
    console.error('Error checking demo status:', error);
    demoStatus.value = 'error';
  }
};

const syncDemoData = async () => {
  loading.value = true;
  message.value = '';

  try {
    // Simulate 3-second animation delay
    await new Promise((resolve) => setTimeout(resolve, 3000));

    const response = await axios.post('/api/demo/sync');
    showMessage(response.data.message || 'Sync complete', 'success');
    demoStatus.value = 'loaded';

    // Mark demo sync completion for chat UI
    if (response.data.status === 'Sync complete') {
      localStorage.setItem('demoSynced', 'true');
    }
  } catch (error) {
    console.error('Sync failed:', error);
    const errorMessage = error.response?.data?.detail || 'Sync failed';
    showMessage(errorMessage, 'error');
  } finally {
    loading.value = false;
  }
};

const clearDemoData = async () => {
  loading.value = true;
  message.value = '';

  try {
    const response = await axios.delete('/api/demo/clear');
    showMessage(response.data.message || 'Data cleared', 'success');
    demoStatus.value = 'not_loaded';

    // Clear demo sync flag for chat UI
    localStorage.removeItem('demoSynced');
  } catch (error) {
    console.error('Clear failed:', error);
    const errorMessage = error.response?.data?.detail || 'Clear failed';
    showMessage(errorMessage, 'error');
  } finally {
    loading.value = false;
  }
};

// Lifecycle
onMounted(() => {
  checkStatus();
});
</script>

<style scoped>
.demo-sync-container {
  min-height: 100vh;
  background-color: #f9fafb;
}
</style>
