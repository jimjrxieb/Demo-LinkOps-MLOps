<template>
  <div
    class="border-2 border-dashed border-gray-400 rounded-lg p-8 text-center cursor-pointer transition-all duration-200 hover:bg-gray-50 hover:border-blue-400"
    @dragover.prevent
    @dragenter.prevent
    @dragleave.prevent
    @drop.prevent="handleDrop"
    :class="{ 'border-blue-500 bg-blue-50': isDragOver }"
  >
    <div class="flex flex-col items-center space-y-4">
      <!-- Upload Icon -->
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
        </svg>
      </div>
      
      <!-- Text Content -->
      <div class="space-y-2">
        <p class="text-lg font-medium text-gray-700">
          {{ isDragOver ? 'Drop your files here' : 'Drag and drop your documents here' }}
        </p>
        <p class="text-sm text-gray-500">
          Supports PDF, TXT, CSV, DOCX files (max 10MB)
        </p>
      </div>

      <!-- Browse Button -->
      <button 
        class="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        @click="openFileDialog"
      >
        Browse Files
      </button>
    </div>

    <!-- Hidden File Input -->
    <input
      type="file"
      ref="fileInput"
      class="hidden"
      @change="handleFileSelect"
      accept=".pdf,.txt,.csv,.docx"
      multiple
    />

    <!-- Upload Progress -->
    <div v-if="uploading" class="mt-4">
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-blue-600 h-2 rounded-full transition-all duration-300"
          :style="{ width: uploadProgress + '%' }"
        ></div>
      </div>
      <p class="text-sm text-gray-600 mt-2">Uploading... {{ uploadProgress }}%</p>
    </div>

    <!-- Upload Status -->
    <div v-if="uploadStatus" class="mt-4 p-3 rounded-lg" :class="uploadStatusClass">
      <p class="text-sm font-medium">{{ uploadStatus }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const fileInput = ref(null)
const isDragOver = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref('')
const uploadStatusClass = ref('')

const emit = defineEmits(['file-uploaded', 'upload-error'])

const openFileDialog = () => {
  fileInput.value.click()
}

const uploadFile = async (file) => {
  if (!file) return

  // Validate file size (10MB limit)
  if (file.size > 10 * 1024 * 1024) {
    uploadStatus.value = 'File too large. Maximum size is 10MB.'
    uploadStatusClass.value = 'bg-red-100 text-red-700'
    emit('upload-error', 'File too large')
    return
  }

  // Validate file type
  const allowedTypes = ['.pdf', '.txt', '.csv', '.docx']
  const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
  if (!allowedTypes.includes(fileExtension)) {
    uploadStatus.value = 'Invalid file type. Please upload PDF, TXT, CSV, or DOCX files.'
    uploadStatusClass.value = 'bg-red-100 text-red-700'
    emit('upload-error', 'Invalid file type')
    return
  }

  uploading.value = true
  uploadProgress.value = 0
  uploadStatus.value = 'Starting upload...'
  uploadStatusClass.value = 'bg-blue-100 text-blue-700'

  const formData = new FormData()
  formData.append('file', file)

  try {
    // Simulate upload progress
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += Math.random() * 10
      }
    }, 100)

    const response = await axios.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      }
    })

    clearInterval(progressInterval)
    uploadProgress.value = 100
    
    uploadStatus.value = `File "${file.name}" uploaded successfully!`
    uploadStatusClass.value = 'bg-green-100 text-green-700'
    
    emit('file-uploaded', {
      filename: file.name,
      response: response.data
    })

    // Clear status after 3 seconds
    setTimeout(() => {
      uploadStatus.value = ''
      uploadStatusClass.value = ''
    }, 3000)

  } catch (error) {
    console.error('Upload failed:', error)
    uploadStatus.value = `Upload failed: ${error.response?.data?.message || error.message}`
    uploadStatusClass.value = 'bg-red-100 text-red-700'
    emit('upload-error', error)
  } finally {
    uploading.value = false
    uploadProgress.value = 0
  }
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  files.forEach(file => uploadFile(file))
  // Reset input
  event.target.value = ''
}

const handleDrop = (event) => {
  isDragOver.value = false
  const files = Array.from(event.dataTransfer.files)
  files.forEach(file => uploadFile(file))
}

// Drag and drop visual feedback
const handleDragEnter = () => {
  isDragOver.value = true
}

const handleDragLeave = () => {
  isDragOver.value = false
}
</script>

<style scoped>
.border-dashed {
  border-style: dashed;
}
</style> 