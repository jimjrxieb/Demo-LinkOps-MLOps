<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">
              ML Model Creator
            </h1>
            <p class="mt-1 text-sm text-gray-500">
              Create machine learning models from your data
            </p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              @click="resetForm"
            >
              Reset
            </button>
            <button
              :disabled="!canGenerate"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="generateModel"
            >
              Generate Model
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Configuration Panel -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-6">
            Model Configuration
          </h2>

          <!-- File Upload -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Dataset File
            </label>
            <div
              class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-gray-400 transition-colors"
            >
              <div class="space-y-1 text-center">
                <svg
                  class="mx-auto h-12 w-12 text-gray-400"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                  aria-hidden="true"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
                <div class="flex text-sm text-gray-600">
                  <label
                    for="file-upload"
                    class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
                  >
                    <span>Upload a file</span>
                    <input
                      id="file-upload"
                      name="file-upload"
                      type="file"
                      class="sr-only"
                      accept=".csv,.json,.xlsx,.xls"
                      @change="handleFile"
                    >
                  </label>
                  <p class="pl-1">
                    or drag and drop
                  </p>
                </div>
                <p class="text-xs text-gray-500">
                  CSV, JSON, Excel files up to 10MB
                </p>
              </div>
            </div>
            <div
              v-if="selectedFile"
              class="mt-2 text-sm text-gray-600"
            >
              Selected: {{ selectedFile.name }} ({{
                formatFileSize(selectedFile.size)
              }})
            </div>
          </div>

          <!-- Model Type -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Model Type
            </label>
            <select
              v-model="modelType"
              class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="classifier">
                Classification
              </option>
              <option value="regression">
                Regression
              </option>
              <option value="clustering">
                Clustering
              </option>
              <option value="time_series">
                Time Series
              </option>
            </select>
          </div>

          <!-- Target Column -->
          <div
            v-if="modelType !== 'clustering'"
            class="mb-6"
          >
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Target Column
            </label>
            <input
              v-model="targetColumn"
              type="text"
              placeholder="Enter target column name"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
          </div>

          <!-- Algorithm Selection -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Algorithm
            </label>
            <select
              v-model="algorithm"
              class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option
                v-if="modelType === 'classifier'"
                value="random_forest"
              >
                Random Forest
              </option>
              <option
                v-if="modelType === 'classifier'"
                value="svm"
              >
                Support Vector Machine
              </option>
              <option
                v-if="modelType === 'classifier'"
                value="neural_network"
              >
                Neural Network
              </option>
              <option
                v-if="modelType === 'regression'"
                value="linear_regression"
              >
                Linear Regression
              </option>
              <option
                v-if="modelType === 'regression'"
                value="random_forest"
              >
                Random Forest
              </option>
              <option
                v-if="modelType === 'regression'"
                value="neural_network"
              >
                Neural Network
              </option>
              <option
                v-if="modelType === 'clustering'"
                value="kmeans"
              >
                K-Means
              </option>
              <option
                v-if="modelType === 'clustering'"
                value="dbscan"
              >
                DBSCAN
              </option>
              <option
                v-if="modelType === 'time_series'"
                value="lstm"
              >
                LSTM
              </option>
              <option
                v-if="modelType === 'time_series'"
                value="arima"
              >
                ARIMA
              </option>
            </select>
          </div>

          <!-- Advanced Options -->
          <div class="mb-6">
            <button
              class="text-sm text-blue-600 hover:text-blue-500 focus:outline-none"
              @click="showAdvanced = !showAdvanced"
            >
              {{ showAdvanced ? 'Hide' : 'Show' }} Advanced Options
            </button>

            <div
              v-if="showAdvanced"
              class="mt-4 space-y-4"
            >
              <!-- Test Size -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Test Size (%)
                </label>
                <input
                  v-model.number="testSize"
                  type="number"
                  min="10"
                  max="50"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
              </div>

              <!-- Random State -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Random State
                </label>
                <input
                  v-model.number="randomState"
                  type="number"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                >
              </div>

              <!-- Feature Selection -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Feature Selection
                </label>
                <select
                  v-model="featureSelection"
                  class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  <option value="auto">
                    Automatic
                  </option>
                  <option value="manual">
                    Manual Selection
                  </option>
                  <option value="correlation">
                    Correlation-based
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Preview & Results Panel -->
        <div class="space-y-6">
          <!-- Data Preview -->
          <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              Data Preview
            </h3>
            <div
              v-if="dataPreview.length > 0"
              class="overflow-x-auto"
            >
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th
                      v-for="column in dataColumns"
                      :key="column"
                      class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {{ column }}
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr
                    v-for="(row, index) in dataPreview"
                    :key="index"
                  >
                    <td
                      v-for="column in dataColumns"
                      :key="column"
                      class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                    >
                      {{ row[column] }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div
              v-else
              class="text-center py-8 text-gray-500"
            >
              Upload a file to see data preview
            </div>
          </div>

          <!-- Generation Results -->
          <div
            v-if="generationResult"
            class="bg-white rounded-lg shadow p-6"
          >
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              Generation Result
            </h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-700">Status:</span>
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                >
                  Success
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-700">Model Path:</span>
                <span class="text-sm text-gray-900">{{
                  generationResult.path
                }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-gray-700">Generated At:</span>
                <span class="text-sm text-gray-900">{{
                  formatDate(generationResult.timestamp)
                }}</span>
              </div>
              <div class="mt-4">
                <button
                  class="w-full px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  @click="downloadModel"
                >
                  Download Model
                </button>
              </div>
            </div>
          </div>

          <!-- Error Display -->
          <div
            v-if="error"
            class="bg-red-50 border border-red-200 rounded-lg p-4"
          >
            <div class="flex">
              <div class="flex-shrink-0">
                <svg
                  class="h-5 w-5 text-red-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Error
                </h3>
                <div class="mt-2 text-sm text-red-700">
                  {{ error }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div
      v-if="isLoading"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
      >
        <div class="mt-3 text-center">
          <div
            class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100"
          >
            <svg
              class="animate-spin h-6 w-6 text-blue-600"
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
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900 mt-4">
            Generating Model
          </h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              Please wait while we generate your machine learning model...
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// Reactive data
const selectedFile = ref(null);
const modelType = ref('classifier');
const targetColumn = ref('');
const algorithm = ref('random_forest');
const testSize = ref(20);
const randomState = ref(42);
const featureSelection = ref('auto');
const showAdvanced = ref(false);
const dataPreview = ref([]);
const dataColumns = ref([]);
const generationResult = ref(null);
const error = ref(null);
const isLoading = ref(false);

// Computed properties
const canGenerate = computed(() => {
  return (
    selectedFile.value &&
    (modelType.value === 'clustering' || targetColumn.value.trim()) &&
    algorithm.value
  );
});

// Methods
function handleFile(event) {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    error.value = null;
    generationResult.value = null;
    previewData(file);
  }
}

async function previewData(file) {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
      'http://localhost:8002/preview',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    dataPreview.value = response.data.preview;
    dataColumns.value = response.data.columns;
  } catch (err) {
    console.error('Error previewing data:', err);
    error.value = 'Failed to preview data. Please check your file format.';
  }
}

async function generateModel() {
  if (!canGenerate.value) return;

  isLoading.value = true;
  error.value = null;

  try {
    const formData = new FormData();
    formData.append('file', selectedFile.value);
    formData.append('model_type', modelType.value);
    formData.append('algorithm', algorithm.value);
    formData.append('test_size', testSize.value);
    formData.append('random_state', randomState.value);
    formData.append('feature_selection', featureSelection.value);

    if (targetColumn.value) {
      formData.append('target_column', targetColumn.value);
    }

    const response = await axios.post(
      'http://localhost:8002/generate-model',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    generationResult.value = response.data;
  } catch (err) {
    console.error('Error generating model:', err);
    error.value =
      err.response?.data?.detail ||
      'Failed to generate model. Please try again.';
  } finally {
    isLoading.value = false;
  }
}

function resetForm() {
  selectedFile.value = null;
  modelType.value = 'classifier';
  targetColumn.value = '';
  algorithm.value = 'random_forest';
  testSize.value = 20;
  randomState.value = 42;
  featureSelection.value = 'auto';
  showAdvanced.value = false;
  dataPreview.value = [];
  dataColumns.value = [];
  generationResult.value = null;
  error.value = null;
}

function downloadModel() {
  if (generationResult.value?.path) {
    // Create a download link
    const link = document.createElement('a');
    link.href = `http://localhost:8002/download/${generationResult.value.path}`;
    link.download = `model_${Date.now()}.py`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleString();
}

// Lifecycle
onMounted(() => {
  // Initialize with default values
});
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
