<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">📂 HTC / Memory Upload</h1>

    <!-- Upload Area -->
    <div
      class="border-dashed border-4 border-blue-400 rounded-md p-8 text-center cursor-pointer bg-blue-50 hover:bg-blue-100 transition-colors"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      :class="{ 'border-green-500 bg-green-50': isDragOver }"
    >
      <div class="text-4xl mb-4">📄</div>
      <p class="text-lg font-semibold mb-2">Drag and drop documents here</p>
      <p class="text-sm text-gray-500 mb-4">.pdf, .docx, .txt supported</p>
      <p class="text-xs text-gray-400">Files will be processed and embedded into memory</p>
    </div>

    <!-- Controls -->
    <div class="mt-6 flex gap-4 items-center">
      <button 
        class="btn btn-primary" 
        @click="manualSync"
        :disabled="isSyncing"
      >
        <span v-if="!isSyncing">🔁 Manual Sync</span>
        <span v-else>🔄 Syncing...</span>
      </button>
      
      <label class="flex items-center gap-2 cursor-pointer">
        <input 
          type="checkbox" 
          v-model="autoSyncEnabled"
          @change="toggleAutoSync"
          class="w-4 h-4"
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
    <div class="mt-6" v-if="uploadedFiles.length > 0">
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
              <p class="font-medium">{{ file.name }}</p>
              <p class="text-sm text-gray-500">{{ formatFileSize(file.size) }}</p>
            </div>
          </div>
          <button 
            @click="deleteFile(file.name)"
            class="text-red-600 hover:text-red-800 transition-colors"
            title="Delete file"
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
          <span class="ml-2" :class="autoSyncEnabled ? 'text-green-600' : 'text-gray-600'">
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
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const status = ref("");
const isDragOver = ref(false);
const isSyncing = ref(false);
const autoSyncEnabled = ref(false);
const uploadedFiles = ref([]);
const lastSync = ref(null);

const statusClass = computed(() => {
  if (status.value.includes('✅')) return 'bg-green-50 text-green-800 border border-green-200';
  if (status.value.includes('🔄')) return 'bg-blue-50 text-blue-800 border border-blue-200';
  if (status.value.includes('❌')) return 'bg-red-50 text-red-800 border border-red-200';
  return 'bg-gray-50 text-gray-800 border border-gray-200';
});

const statusIcon = computed(() => {
  if (status.value.includes('✅')) return '✅';
  if (status.value.includes('🔄')) return '🔄';
  if (status.value.includes('❌')) return '❌';
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
    status.value = '❌ Invalid file type. Please upload .pdf, .docx, or .txt files.';
    return;
  }
  
  try {
    status.value = '🔄 Uploading...';
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("/api/htc/upload-docs", formData);
    status.value = res.data.message;
    
    // Add to uploaded files list
    uploadedFiles.value.push({
      name: file.name,
      size: file.size,
      type: file.type
    });
    
    // Auto sync if enabled
    if (autoSyncEnabled.value) {
      await manualSync();
    }
    
  } catch (error) {
    console.error('Upload error:', error);
    status.value = '❌ Upload failed: ' + (error.response?.data?.detail || error.message);
  }
};

const manualSync = async () => {
  try {
    isSyncing.value = true;
    status.value = "🔄 Syncing documents and updating memory...";
    
    const res = await axios.post("/api/htc/manual-sync");
    status.value = res.data.message;
    lastSync.value = new Date().toLocaleString();
    
  } catch (error) {
    console.error('Sync error:', error);
    status.value = '❌ Sync failed: ' + (error.response?.data?.detail || error.message);
  } finally {
    isSyncing.value = false;
  }
};

const toggleAutoSync = async () => {
  try {
    const res = await axios.post("/api/htc/toggle-auto-sync", {
      enabled: autoSyncEnabled.value
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
    uploadedFiles.value = uploadedFiles.value.filter(f => f.name !== filename);
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
    const res = await axios.get("/api/htc/status");
    uploadedFiles.value = res.data.uploaded_files || [];
    autoSyncEnabled.value = res.data.auto_sync_enabled || false;
    lastSync.value = res.data.last_sync;
  } catch (error) {
    console.error('Failed to load system status:', error);
  }
};

onMounted(() => {
  loadSystemStatus();
});
</script>

<style scoped>
.btn {
  @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed;
}
</style> 