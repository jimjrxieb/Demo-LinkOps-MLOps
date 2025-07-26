<template>
  <div class="htc-container">
    <div class="upload-card">
      <h2 class="title">
        📁 Document Memory Training
      </h2>

      <!-- Upload Area -->
      <div
        class="drop-area"
        :class="{ 'drag-active': isDragging, uploading: isUploading }"
        @dragenter.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @dragover.prevent
        @drop.prevent="handleDrop"
      >
        <div
          v-if="isUploading"
          class="upload-progress"
        >
          <div class="spinner" />
          <p>Uploading files...</p>
        </div>
        <div v-else>
          <svg
            class="upload-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          <p>
            Drag & drop files or
            <span
              class="browse"
              @click="openFilePicker"
            >browse</span>
          </p>
          <p class="text-sm">
            Supported: PDF, DOCX, TXT
          </p>
        </div>
        <input
          ref="fileInput"
          type="file"
          multiple
          accept=".pdf,.docx,.txt"
          class="hidden"
          @change="handleFileChange"
        >
      </div>

      <!-- File List -->
      <div
        v-if="files.length"
        class="file-list-container"
      >
        <h3 class="text-teal-100 text-sm font-medium mb-2">
          Selected Files
        </h3>
        <ul class="file-list">
          <li
            v-for="file in files"
            :key="file.name"
            class="file-item"
          >
            <span class="file-name">{{ file.name }}</span>
            <span class="file-size">{{ formatFileSize(file.size) }}</span>
            <button
              class="remove-btn"
              @click="removeFile(file)"
            >
              <svg
                class="w-4 h-4"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </li>
        </ul>
      </div>

      <!-- Sync Controls -->
      <div class="sync-controls">
        <button
          :disabled="!files.length || isUploading || isSyncing"
          class="sync-btn"
          @click="uploadAndSync"
        >
          <div
            v-if="isUploading || isSyncing"
            class="spinner mr-2"
          />
          <span v-if="isUploading">Uploading...</span>
          <span v-else-if="isSyncing">Syncing...</span>
          <span v-else>🚀 Upload & Sync</span>
        </button>

        <div class="flex items-center mt-4 justify-between">
          <label class="flex items-center text-teal-100 text-sm">
            <input
              v-model="autoSync"
              type="checkbox"
              class="form-checkbox h-4 w-4 text-teal-500 rounded"
              @change="toggleAutoSync"
            >
            <span class="ml-2">Auto-sync new files</span>
          </label>

          <button
            v-if="uploadedFiles.length"
            class="text-teal-300 text-sm hover:text-teal-100"
            @click="refreshStatus"
          >
            Refresh Status
          </button>
        </div>
      </div>

      <!-- Status Section -->
      <div
        v-if="uploadedFiles.length"
        class="status-section"
      >
        <h3 class="text-teal-100 text-sm font-medium mb-2">
          Uploaded Files
        </h3>
        <ul class="uploaded-list">
          <li
            v-for="file in uploadedFiles"
            :key="file.name"
            class="uploaded-item"
          >
            <span class="file-name">{{ file.name }}</span>
            <div class="flex items-center space-x-2">
              <span class="text-teal-300 text-xs">{{
                formatDate(file.uploaded_at)
              }}</span>
              <button
                class="delete-btn"
                @click="deleteFile(file.name)"
              >
                <svg
                  class="w-4 h-4"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </li>
        </ul>

        <div class="mt-4 text-sm text-teal-200">
          <p>Last sync: {{ lastSync ? formatDate(lastSync) : 'Never' }}</p>
          <p>Total files: {{ uploadedFiles.length }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// State
const fileInput = ref(null);
const files = ref([]);
const isDragging = ref(false);
const isUploading = ref(false);
const isSyncing = ref(false);
const autoSync = ref(false);
const uploadedFiles = ref([]);
const lastSync = ref(null);

// File Input Handler
const openFilePicker = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  const newFiles = Array.from(event.target.files);
  validateAndAddFiles(newFiles);
};

const handleDrop = (event) => {
  isDragging.value = false;
  const newFiles = Array.from(event.dataTransfer.files);
  validateAndAddFiles(newFiles);
};

const validateAndAddFiles = (newFiles) => {
  const allowedTypes = ['.pdf', '.docx', '.txt'];
  const validFiles = newFiles.filter((file) => {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    return allowedTypes.includes(ext);
  });

  if (validFiles.length !== newFiles.length) {
    alert(
      'Some files were skipped. Only PDF, DOCX, and TXT files are supported.'
    );
  }

  files.value = [...files.value, ...validFiles];
};

const removeFile = (file) => {
  files.value = files.value.filter((f) => f !== file);
};

// API Integration
const uploadAndSync = async () => {
  if (!files.value.length) return;

  isUploading.value = true;

  try {
    // Upload each file
    for (const file of files.value) {
      const formData = new FormData();
      formData.append('file', file);
      await axios.post('/htc/upload-docs', formData);
    }

    // Clear selected files
    files.value = [];

    // Trigger sync if not in auto mode
    if (!autoSync.value) {
      isSyncing.value = true;
      await axios.post('/htc/manual-sync');
    }

    // Refresh status
    await refreshStatus();
  } catch (error) {
    alert(
      'Error uploading files: ' +
        (error.response?.data?.detail || error.message)
    );
  } finally {
    isUploading.value = false;
    isSyncing.value = false;
  }
};

const toggleAutoSync = async () => {
  try {
    await axios.post('/htc/toggle-auto-sync', {
      enabled: autoSync.value,
    });
  } catch (error) {
    autoSync.value = !autoSync.value; // Revert on error
    alert('Error toggling auto-sync: ' + error.message);
  }
};

const deleteFile = async (filename) => {
  if (!confirm(`Delete ${filename}?`)) return;

  try {
    await axios.delete(`/htc/delete-file/${filename}`);
    await refreshStatus();
  } catch (error) {
    alert('Error deleting file: ' + error.message);
  }
};

const refreshStatus = async () => {
  try {
    const { data } = await axios.get('/htc/status');
    uploadedFiles.value = data.uploaded_files;
    autoSync.value = data.auto_sync_enabled;
    lastSync.value = data.last_sync;
  } catch (error) {
    console.error('Error fetching status:', error);
  }
};

// Utilities
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
};

const formatDate = (isoDate) => {
  if (!isoDate) return '';
  return new Date(isoDate).toLocaleString();
};

// Initialize
onMounted(refreshStatus);
</script>

<style scoped>
.htc-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem;
  min-height: 100vh;
  background: radial-gradient(circle at center, #1c3f45, #0f2e38);
}

.upload-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #31a3a3;
  padding: 2rem;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  text-align: center;
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.title {
  color: #ffffff;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.drop-area {
  border: 2px dashed #2bc0c0;
  padding: 2rem;
  border-radius: 12px;
  background-color: rgba(0, 255, 255, 0.05);
  color: #d6f9ff;
  cursor: pointer;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.drop-area.drag-active {
  background-color: rgba(0, 255, 255, 0.1);
  border-color: #40f7f7;
  transform: scale(1.02);
}

.upload-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 1rem;
  color: #2bc0c0;
}

.browse {
  color: #40f7f7;
  text-decoration: underline;
  cursor: pointer;
}

.file-list-container {
  margin: 1.5rem 0;
  text-align: left;
}

.file-list {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  overflow: hidden;
}

.file-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #e6ffff;
  font-size: 0.875rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.file-item:last-child {
  border-bottom: none;
}

.file-name {
  flex: 1;
  margin-right: 1rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  color: #2bc0c0;
  margin-right: 1rem;
}

.remove-btn {
  color: #ff6b6b;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.remove-btn:hover {
  opacity: 1;
}

.sync-controls {
  margin-top: 1.5rem;
}

.sync-btn {
  background-color: #0a2e3c;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  width: 100%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sync-btn:not(:disabled):hover {
  background-color: #094759;
  transform: translateY(-1px);
}

.sync-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-section {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: left;
}

.uploaded-list {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  overflow: hidden;
}

.uploaded-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  color: #e6ffff;
  font-size: 0.875rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.uploaded-item:last-child {
  border-bottom: none;
}

.delete-btn {
  color: #ff6b6b;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.delete-btn:hover {
  opacity: 1;
}

.spinner {
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  width: 1rem;
  height: 1rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Form Controls */
.form-checkbox {
  background-color: rgba(0, 0, 0, 0.2);
  border-color: #2bc0c0;
}

.form-checkbox:checked {
  background-color: #2bc0c0;
}

/* Upload Progress */
.upload-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-progress .spinner {
  width: 2rem;
  height: 2rem;
  border-width: 3px;
}
</style>
