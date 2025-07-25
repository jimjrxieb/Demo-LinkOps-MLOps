<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">🏋️ HTC Trainer & Memory Upload</h1>

    <!-- Tab Navigation -->
    <div class="mb-6">
      <div class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8">
          <button
            @click="activeTab = 'upload'"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm',
              activeTab === 'upload'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            ]"
          >
            📄 Document Upload
          </button>
          <button
            @click="activeTab = 'retrain'"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm',
              activeTab === 'retrain'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            ]"
          >
            🏋️ Model Retraining
          </button>
          <button
            @click="activeTab = 'history'"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm',
              activeTab === 'history'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            ]"
          >
            📊 Training History
          </button>
        </nav>
      </div>
    </div>

    <!-- Document Upload Tab -->
    <div v-if="activeTab === 'upload'">
      <!-- Upload Area -->
      <div
        class="border-dashed border-4 border-blue-400 rounded-md p-8 text-center cursor-pointer bg-blue-50 hover:bg-blue-100 transition-colors"
        :class="{ 'border-green-500 bg-green-50': isDragOver }"
        @drop.prevent="handleDrop"
        @dragover.prevent="isDragOver = true"
        @dragleave.prevent="isDragOver = false"
      >
        <div class="text-4xl mb-4">📄</div>
        <p class="text-lg font-semibold mb-2">Drag and drop documents here</p>
        <p class="text-sm text-gray-500 mb-4">.pdf, .docx, .txt supported</p>
        <p class="text-xs text-gray-400">
          Files will be processed and embedded into memory
        </p>
      </div>

      <!-- Controls -->
      <div class="mt-6 flex gap-4 items-center">
        <button
          class="btn btn-primary"
          :disabled="isSyncing"
          @click="manualSync"
        >
          <span v-if="!isSyncing">🔁 Manual Sync</span>
          <span v-else>🔄 Syncing...</span>
        </button>

        <label class="flex items-center gap-2 cursor-pointer">
          <input
            v-model="autoSyncEnabled"
            type="checkbox"
            class="w-4 h-4"
            @change="toggleAutoSync"
          />
          <span class="text-sm">Auto Sync Mode</span>
        </label>
      </div>

      <!-- Status Display -->
      <div class="mt-6">
        <div v-if="status" class="p-4 rounded-lg" :class="statusClass">
          <div class="flex items-center gap-2">
            <span class="text-lg">{{ statusIcon }}</span>
            <span>{{ status }}</span>
          </div>
        </div>
      </div>

      <!-- File List -->
      <div v-if="uploadedFiles.length > 0" class="mt-6">
        <h3 class="text-lg font-semibold mb-3">📁 Uploaded Files</h3>
        <div class="space-y-2">
          <div
            v-for="file in uploadedFiles"
            :key="file.name"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center gap-3">
              <span class="text-lg">📄</span>
              <div>
                <p class="font-medium">
                  {{ file.name }}
                </p>
                <p class="text-sm text-gray-500">
                  {{ formatFileSize(file.size) }}
                </p>
              </div>
            </div>
            <button
              class="text-red-600 hover:text-red-800 transition-colors"
              title="Delete file"
              @click="deleteFile(file.name)"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>

      <!-- System Info -->
      <div class="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 class="text-lg font-semibold mb-2">📊 System Info</h3>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="font-medium">Files Uploaded:</span>
            <span class="ml-2">{{ uploadedFiles.length }}</span>
          </div>
          <div>
            <span class="font-medium">Auto Sync:</span>
            <span
              class="ml-2"
              :class="autoSyncEnabled ? 'text-green-600' : 'text-gray-600'"
            >
              {{ autoSyncEnabled ? 'Enabled' : 'Disabled' }}
            </span>
          </div>
          <div>
            <span class="font-medium">Last Sync:</span>
            <span class="ml-2">{{ lastSync || 'Never' }}</span>
          </div>
          <div>
            <span class="font-medium">Memory Status:</span>
            <span class="ml-2 text-green-600">✅ Ready</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Model Retraining Tab -->
    <div v-if="activeTab === 'retrain'">
      <!-- Retrain Upload Area -->
      <div
        class="border-2 border-dashed border-purple-400 rounded-lg p-8 text-center mb-6 bg-purple-50 hover:bg-purple-100 transition-colors"
        :class="{ 'border-green-500 bg-green-50': isRetrainDragOver }"
        @dragover.prevent="isRetrainDragOver = true"
        @dragleave.prevent="isRetrainDragOver = false"
        @drop.prevent="onRetrainDrop"
      >
        <div class="text-4xl mb-4">🏋️</div>
        <p class="text-lg font-semibold mb-2">
          Drag & drop feedback files here
        </p>
        <p class="text-sm text-gray-600 mb-2">
          Upload training data to improve model performance
        </p>
        <p class="text-xs text-gray-500">(PDF, CSV, TXT, JSON…)</p>
      </div>

      <!-- Selected Files List -->
      <div v-if="retrainFiles.length" class="mb-6">
        <h2 class="text-lg font-semibold mb-3">📁 Files to Retrain:</h2>
        <div class="space-y-2">
          <div
            v-for="file in retrainFiles"
            :key="file.name"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center gap-3">
              <span class="text-lg">📄</span>
              <div>
                <p class="font-medium">{{ file.name }}</p>
                <p class="text-sm text-gray-500">
                  {{ formatFileSize(file.size) }}
                </p>
              </div>
            </div>
            <button
              class="text-red-600 hover:text-red-800 transition-colors"
              title="Remove file"
              @click="removeRetrainFile(file)"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>

      <!-- Retrain Controls -->
      <div class="mb-6">
        <button
          class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
          :disabled="retrainFiles.length === 0 || isRetraining"
          @click="submitRetrain"
        >
          <span v-if="!isRetraining">🏋️ Start Retrain</span>
          <span v-else>⏳ Retraining…</span>
        </button>

        <button
          v-if="retrainFiles.length > 0"
          class="ml-4 bg-gray-500 hover:bg-gray-600 text-white px-4 py-3 rounded-lg transition-colors"
          @click="clearRetrainFiles"
        >
          🧹 Clear Files
        </button>
      </div>

      <!-- Retrain Status -->
      <div v-if="retrainStatus" class="mb-6">
        <div class="p-4 rounded-lg" :class="retrainStatusClass">
          <div class="flex items-center gap-2">
            <span class="text-lg">{{ retrainStatusIcon }}</span>
            <span>{{ retrainStatus }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Training History Tab -->
    <div v-if="activeTab === 'history'">
      <div class="mb-6">
        <h2 class="text-xl font-semibold mb-4">📊 Retrain History</h2>
        <div class="flex gap-4 mb-4">
          <button
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
            @click="fetchRetrainHistory"
          >
            🔄 Refresh
          </button>
          <button
            v-if="retrainHistory.length > 0"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition-colors"
            @click="exportHistory"
          >
            📄 Export CSV
          </button>
        </div>
      </div>

      <div v-if="retrainHistory.length" class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Job ID
              </th>
              <th
                class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Timestamp
              </th>
              <th
                class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Status
              </th>
              <th
                class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Details
              </th>
              <th
                class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr
              v-for="job in retrainHistory"
              :key="job.job_id"
              class="hover:bg-gray-50"
            >
              <td class="px-4 py-3 text-sm font-mono text-gray-900">
                {{ job.job_id.slice(0, 8) }}...
              </td>
              <td class="px-4 py-3 text-sm text-gray-900">
                {{ formatDate(job.timestamp) }}
              </td>
              <td class="px-4 py-3">
                <span
                  class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                  :class="getStatusClass(job.status)"
                >
                  {{ job.status }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-900 max-w-xs">
                {{ truncate(job.details, 100) }}
              </td>
              <td class="px-4 py-3 text-sm">
                <button
                  class="text-blue-600 hover:text-blue-800 transition-colors"
                  @click="viewJobDetails(job)"
                >
                  👁️ View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="text-center py-8">
        <div class="text-4xl mb-4">📊</div>
        <p class="text-gray-500">No retrain jobs found.</p>
        <p class="text-sm text-gray-400 mt-2">
          Start a retrain job to see history here.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// Tab management
const activeTab = ref('upload');

// Document upload state
const status = ref('');
const isDragOver = ref(false);
const isSyncing = ref(false);
const autoSyncEnabled = ref(false);
const uploadedFiles = ref([]);
const lastSync = ref(null);

// Retrain state
const isRetrainDragOver = ref(false);
const retrainFiles = ref([]);
const isRetraining = ref(false);
const retrainStatus = ref('');
const retrainHistory = ref([]);

const statusClass = computed(() => {
  if (status.value.includes('✅'))
    return 'bg-green-50 text-green-800 border border-green-200';
  if (status.value.includes('🔄'))
    return 'bg-blue-50 text-blue-800 border border-blue-200';
  if (status.value.includes('❌'))
    return 'bg-red-50 text-red-800 border border-red-200';
  return 'bg-gray-50 text-gray-800 border border-gray-200';
});

const statusIcon = computed(() => {
  if (status.value.includes('✅')) return '✅';
  if (status.value.includes('🔄')) return '🔄';
  if (status.value.includes('❌')) return '❌';
  return 'ℹ️';
});

// Retrain computed properties
const retrainStatusClass = computed(() => {
  if (retrainStatus.value.includes('✅'))
    return 'bg-green-50 text-green-800 border border-green-200';
  if (retrainStatus.value.includes('🔄'))
    return 'bg-blue-50 text-blue-800 border border-blue-200';
  if (retrainStatus.value.includes('❌'))
    return 'bg-red-50 text-red-800 border border-red-200';
  return 'bg-gray-50 text-gray-800 border border-gray-200';
});

const retrainStatusIcon = computed(() => {
  if (retrainStatus.value.includes('✅')) return '✅';
  if (retrainStatus.value.includes('🔄')) return '🔄';
  if (retrainStatus.value.includes('❌')) return '❌';
  return 'ℹ️';
});

const handleDrop = async (event) => {
  isDragOver.value = false;
  const file = event.dataTransfer.files[0];

  if (!file) return;

  // Validate file type
  const allowedTypes = ['.pdf', '.docx', '.txt'];
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

  if (!allowedTypes.includes(fileExtension)) {
    status.value =
      '❌ Invalid file type. Please upload .pdf, .docx, or .txt files.';
    return;
  }

  try {
    status.value = '🔄 Uploading...';
    const formData = new FormData();
    formData.append('file', file);

    const res = await axios.post('/api/htc/upload-docs', formData);
    status.value = res.data.message;

    // Add to uploaded files list
    uploadedFiles.value.push({
      name: file.name,
      size: file.size,
      type: file.type,
    });

    // Auto sync if enabled
    if (autoSyncEnabled.value) {
      await manualSync();
    }
  } catch (error) {
    console.error('Upload error:', error);
    status.value =
      '❌ Upload failed: ' + (error.response?.data?.detail || error.message);
  }
};

const manualSync = async () => {
  try {
    isSyncing.value = true;
    status.value = '🔄 Syncing documents and updating memory...';

    const res = await axios.post('/api/htc/manual-sync');
    status.value = res.data.message;
    lastSync.value = new Date().toLocaleString();
  } catch (error) {
    console.error('Sync error:', error);
    status.value =
      '❌ Sync failed: ' + (error.response?.data?.detail || error.message);
  } finally {
    isSyncing.value = false;
  }
};

const toggleAutoSync = async () => {
  try {
    const res = await axios.post('/api/htc/toggle-auto-sync', {
      enabled: autoSyncEnabled.value,
    });
    status.value = res.data.message;
  } catch (error) {
    console.error('Auto sync toggle error:', error);
    status.value = '❌ Failed to toggle auto sync';
  }
};

const deleteFile = async (filename) => {
  try {
    await axios.delete(`/api/htc/delete-file/${filename}`);
    uploadedFiles.value = uploadedFiles.value.filter(
      (f) => f.name !== filename
    );
    status.value = `✅ Deleted ${filename}`;
  } catch (error) {
    console.error('Delete error:', error);
    status.value = '❌ Failed to delete file';
  }
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const loadSystemStatus = async () => {
  try {
    const res = await axios.get('/api/htc/status');
    uploadedFiles.value = res.data.uploaded_files || [];
    autoSyncEnabled.value = res.data.auto_sync_enabled || false;
    lastSync.value = res.data.last_sync;
  } catch (error) {
    console.error('Failed to load system status:', error);
  }
};

// Retrain methods
const onRetrainDrop = (event) => {
  isRetrainDragOver.value = false;
  const droppedFiles = Array.from(event.dataTransfer.files);
  retrainFiles.value = retrainFiles.value.concat(droppedFiles);
};

const removeRetrainFile = (file) => {
  retrainFiles.value = retrainFiles.value.filter((f) => f !== file);
};

const clearRetrainFiles = () => {
  retrainFiles.value = [];
};

const submitRetrain = async () => {
  if (retrainFiles.value.length === 0) return;

  isRetraining.value = true;
  retrainStatus.value = '🔄 Starting retrain job...';

  try {
    const form = new FormData();
    retrainFiles.value.forEach((file) => {
      form.append('files', file);
    });

    const res = await axios.post('/api/htc/retrain', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    retrainStatus.value = `✅ Retrain job started! Job ID: ${res.data.job_id}`;
    retrainFiles.value = [];

    // Refresh history
    await fetchRetrainHistory();
  } catch (error) {
    console.error('Retrain request failed:', error);
    retrainStatus.value = `❌ Retrain failed: ${
      error.response?.data?.detail || error.message
    }`;
  } finally {
    isRetraining.value = false;
  }
};

const fetchRetrainHistory = async () => {
  try {
    const res = await axios.get('/api/htc/history?limit=50');
    retrainHistory.value = res.data;
  } catch (error) {
    console.error('Failed to fetch retrain history:', error);
  }
};

const getStatusClass = (status) => {
  switch (status.toLowerCase()) {
    case 'completed':
      return 'bg-green-100 text-green-800';
    case 'failed':
      return 'bg-red-100 text-red-800';
    case 'queued':
      return 'bg-yellow-100 text-yellow-800';
    case 'running':
      return 'bg-blue-100 text-blue-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString();
};

const truncate = (text, maxLength = 50) => {
  if (!text) return '';
  return text.length > maxLength ? text.slice(0, maxLength) + '…' : text;
};

const viewJobDetails = (job) => {
  // TODO: Implement job details modal
  alert(
    `Job Details:\nID: ${job.job_id}\nStatus: ${job.status}\nDetails: ${job.details}`
  );
};

const exportHistory = () => {
  if (retrainHistory.value.length === 0) return;

  const csvContent = [
    ['Job ID', 'Timestamp', 'Status', 'Details'],
    ...retrainHistory.value.map((job) => [
      job.job_id,
      job.timestamp,
      job.status,
      job.details,
    ]),
  ]
    .map((row) => row.map((cell) => `"${cell}"`).join(','))
    .join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `htc-retrain-history-${
    new Date().toISOString().split('T')[0]
  }.csv`;
  a.click();
  window.URL.revokeObjectURL(url);
};

onMounted(() => {
  loadSystemStatus();
  fetchRetrainHistory();
});
</script>

<style scoped>
.btn {
  @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed;
}
</style>
