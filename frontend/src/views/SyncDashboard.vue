<!-- DEMO-LinkOps/frontend/src/views/SyncDashboard.vue -->
<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4 text-teal-300">
      🔁 Sync Status Dashboard
    </h2>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Sync Status Card -->
      <div :class="['status-card', status.active ? 'pulse' : '']">
        <div class="status-header">
          🌀 Sync Engine
        </div>
        <div class="status-details">
          <p class="status-text">
            Status:
            <span :class="status.active ? 'text-green-400' : 'text-gray-400'">
              {{ status.active ? 'Syncing...' : 'Idle' }}
            </span>
          </p>
          <p class="text-sm text-gray-300">
            Watch Folder:
            <strong class="text-white">{{
              status.watch_folder || 'Loading...'
            }}</strong>
          </p>
          <p class="last-sync">
            Last Sync: <strong>{{ formatDate(status.last_sync) }}</strong>
          </p>
          <button
            class="mt-3 px-4 py-2 bg-black text-white rounded hover:bg-teal-600"
            :disabled="syncing"
            @click="triggerSync"
          >
            🔄 {{ syncing ? 'Syncing...' : 'Manual Sync' }}
          </button>
        </div>
      </div>

      <!-- Logs -->
      <div class="glass p-4 rounded-xl shadow">
        <h3 class="text-lg font-semibold mb-2 text-white">
          📜 Last Sync Logs
        </h3>
        <ul class="text-sm text-gray-200 space-y-1 max-h-48 overflow-y-auto">
          <li
            v-for="(log, idx) in logs"
            :key="idx"
          >
            <span class="text-teal-400">•</span> {{ log }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Redactions Chart -->
    <div class="mt-8 glass p-4 rounded-xl shadow">
      <h3 class="text-lg font-semibold mb-4 text-teal-300">
        📈 Redactions Over Time
      </h3>
      <Line
        v-if="chartData.labels.length"
        :data="chartData"
        :options="chartOptions"
        class="bg-black bg-opacity-40 rounded-lg p-4"
      />
      <div
        v-else
        class="text-center text-gray-400 py-8"
      >
        Loading chart data...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
);

const status = ref({});
const logs = ref([]);
const syncing = ref(false);

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Redacted Entries',
      data: [],
      fill: false,
      borderColor: 'rgba(45, 212, 191, 1)',
      backgroundColor: 'rgba(45, 212, 191, 0.6)',
      tension: 0.3,
      pointRadius: 4,
      pointHoverRadius: 6,
    },
  ],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(13, 26, 34, 0.9)',
      titleColor: '#fff',
      bodyColor: '#fff',
      padding: 12,
      borderColor: 'rgba(45, 212, 191, 0.3)',
      borderWidth: 1,
      callbacks: {
        label: (ctx) => `${ctx.parsed.y} entries redacted`,
      },
    },
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(255, 255, 255, 0.1)',
      },
      ticks: {
        color: '#aaa',
        maxRotation: 45,
        minRotation: 45,
      },
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(255, 255, 255, 0.1)',
      },
      ticks: {
        stepSize: 5,
        color: '#aaa',
      },
    },
  },
};

const fetchStatus = async () => {
  try {
    const res = await axios.get('/sync-engine/status');
    status.value = res.data.status;
    logs.value = res.data.logs || [];
  } catch (err) {
    console.error('Failed to fetch sync status', err);
  }
};

const fetchRedactionHistory = async () => {
  try {
    const res = await axios.get('/sync-engine/history');
    chartData.value.labels = res.data.map((item) =>
      new Date(item.timestamp).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      })
    );
    chartData.value.datasets[0].data = res.data.map(
      (item) => item.redacted_count
    );
  } catch (err) {
    console.error('Failed to fetch redaction history', err);
  }
};

const triggerSync = async () => {
  syncing.value = true;
  try {
    await axios.post('/sync-engine/manual-sync');
    await Promise.all([fetchStatus(), fetchRedactionHistory()]);
  } catch (err) {
    console.error('Manual sync failed', err);
  } finally {
    syncing.value = false;
  }
};

const formatDate = (iso) => {
  if (!iso) return '—';
  return new Date(iso).toLocaleString();
};

onMounted(async () => {
  await Promise.all([fetchStatus(), fetchRedactionHistory()]);
  // Refresh data every 10 seconds
  setInterval(async () => {
    await Promise.all([fetchStatus(), fetchRedactionHistory()]);
  }, 10000);
});
</script>

<style scoped>
.status-card {
  @apply p-6 rounded-xl shadow transition-all duration-300;
  background: rgba(0, 128, 128, 0.15);
  border: 1px solid rgba(0, 247, 255, 0.2);
  backdrop-filter: blur(8px);
}

.status-card.pulse {
  animation: pulse 1.5s infinite ease-in-out;
  box-shadow: 0 0 12px rgba(0, 247, 255, 0.33);
  border-color: rgba(0, 247, 255, 0.33);
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

.status-header {
  @apply text-xl font-semibold text-teal-300 mb-3;
}

.status-details {
  @apply space-y-2;
}

.status-text {
  @apply text-white;
}

.last-sync {
  @apply text-sm text-gray-400;
}

.glass {
  background: rgba(13, 26, 34, 0.6);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
