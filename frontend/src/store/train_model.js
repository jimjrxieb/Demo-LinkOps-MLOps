import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useTrainModelStore = defineStore('trainModel', () => {
  // State
  const isTraining = ref(false);
  const trainingProgress = ref(0);
  const trainingStatus = ref('');
  const trainingResult = ref(null);
  const trainingError = ref(null);
  const modelHistory = ref([]);
  const uploadedFile = ref(null);
  const csvHeaders = ref([]);
  const modelConfig = ref({
    name: '',
    targetColumn: '',
    features: [],
  });

  // Computed properties
  const canTrain = computed(() => {
    return (
      uploadedFile.value &&
      modelConfig.value.name &&
      modelConfig.value.targetColumn &&
      modelConfig.value.features.length > 0
    );
  });

  const hasTrainedModels = computed(() => {
    return modelHistory.value.length > 0;
  });

  const latestModel = computed(() => {
    if (modelHistory.value.length === 0) return null;
    return modelHistory.value[modelHistory.value.length - 1];
  });

  // Actions
  const setUploadedFile = (file) => {
    uploadedFile.value = file;
  };

  const setCsvHeaders = (headers) => {
    csvHeaders.value = headers;
  };

  const updateModelConfig = (config) => {
    modelConfig.value = { ...modelConfig.value, ...config };
  };

  const resetModelConfig = () => {
    modelConfig.value = {
      name: '',
      targetColumn: '',
      features: [],
    };
  };

  const startTraining = () => {
    isTraining.value = true;
    trainingProgress.value = 0;
    trainingStatus.value = 'Preparing data...';
    trainingResult.value = null;
    trainingError.value = null;
  };

  const updateTrainingProgress = (progress, status) => {
    trainingProgress.value = progress;
    trainingStatus.value = status;
  };

  const setTrainingResult = (result) => {
    trainingResult.value = result;
    isTraining.value = false;
    trainingProgress.value = 100;
    trainingStatus.value = 'Training complete!';
  };

  const setTrainingError = (error) => {
    trainingError.value = error;
    isTraining.value = false;
  };

  const resetTraining = () => {
    isTraining.value = false;
    trainingProgress.value = 0;
    trainingStatus.value = '';
    trainingResult.value = null;
    trainingError.value = null;
  };

  const setModelHistory = (history) => {
    modelHistory.value = history;
  };

  const addModelToHistory = (model) => {
    modelHistory.value.push(model);
  };

  const removeModelFromHistory = (modelName) => {
    const index = modelHistory.value.findIndex(
      (model) => model.name === modelName
    );
    if (index !== -1) {
      modelHistory.value.splice(index, 1);
    }
  };

  const updateModelInHistory = (modelName, updates) => {
    const index = modelHistory.value.findIndex(
      (model) => model.name === modelName
    );
    if (index !== -1) {
      modelHistory.value[index] = { ...modelHistory.value[index], ...updates };
    }
  };

  // API Actions
  const uploadCsvFile = async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/upload-csv', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      const result = await response.json();
      return result.path;
    } catch (error) {
      console.error('Upload error:', error);
      throw error;
    }
  };

  const trainModel = async () => {
    if (!canTrain.value) {
      throw new Error('Cannot train: missing required configuration');
    }

    startTraining();

    try {
      // Upload file first
      updateTrainingProgress(20, 'Uploading data...');
      const csvPath = await uploadCsvFile(uploadedFile.value);

      // Train model
      updateTrainingProgress(50, 'Training model...');

      const trainResponse = await fetch('/api/train-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model_name: modelConfig.value.name,
          target_column: modelConfig.value.targetColumn,
          features: modelConfig.value.features,
          csv_path: csvPath,
        }),
      });

      if (!trainResponse.ok) {
        const errorData = await trainResponse.json();
        throw new Error(errorData.detail || 'Training failed');
      }

      const result = await trainResponse.json();
      setTrainingResult(result);

      // Add to history
      addModelToHistory({
        name: modelConfig.value.name,
        target: modelConfig.value.targetColumn,
        features: modelConfig.value.features,
        mae: result.mae,
        r2: result.r2,
        date: new Date().toISOString(),
      });

      return result;
    } catch (error) {
      console.error('Training error:', error);
      setTrainingError(error.message);
      throw error;
    }
  };

  const loadModelHistory = async () => {
    try {
      const response = await fetch('/api/train-model/models');
      if (response.ok) {
        const history = await response.json();
        setModelHistory(history);
        return history;
      } else {
        throw new Error('Failed to load model history');
      }
    } catch (error) {
      console.error('Error loading model history:', error);
      throw error;
    }
  };

  const getModelSummary = async (modelName) => {
    try {
      const response = await fetch(
        `/api/train-model/models/${modelName}/summary`
      );
      if (response.ok) {
        return await response.json();
      } else {
        throw new Error('Failed to load model summary');
      }
    } catch (error) {
      console.error('Error loading model summary:', error);
      throw error;
    }
  };

  const deleteModel = async (modelName) => {
    try {
      const response = await fetch(`/api/train-model/${modelName}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        removeModelFromHistory(modelName);
        return true;
      } else {
        throw new Error('Failed to delete model');
      }
    } catch (error) {
      console.error('Error deleting model:', error);
      throw error;
    }
  };

  const getTrainingStatus = async () => {
    try {
      const response = await fetch('/api/train-model/status');
      if (response.ok) {
        return await response.json();
      } else {
        throw new Error('Failed to get training status');
      }
    } catch (error) {
      console.error('Error getting training status:', error);
      throw error;
    }
  };

  // Utility functions
  const processCsvFile = async (file) => {
    try {
      const text = await file.text();
      const lines = text.split('\n');
      const headers = lines[0]
        .split(',')
        .map((h) => h.trim().replace(/"/g, ''));

      setCsvHeaders(headers);
      setUploadedFile(file);

      // Auto-generate model name if empty
      if (!modelConfig.value.name) {
        updateModelConfig({
          name: `${file.name.replace('.csv', '')}_predictor`,
        });
      }

      // Auto-select features (exclude target if already selected)
      const availableFeatures = headers.filter(
        (h) => h !== modelConfig.value.targetColumn
      );
      updateModelConfig({ features: availableFeatures });

      return headers;
    } catch (error) {
      console.error('Error processing CSV:', error);
      throw new Error('Error reading CSV file. Please check the file format.');
    }
  };

  const clearUploadedFile = () => {
    uploadedFile.value = null;
    csvHeaders.value = [];
    resetModelConfig();
    resetTraining();
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return {
    // State
    isTraining,
    trainingProgress,
    trainingStatus,
    trainingResult,
    trainingError,
    modelHistory,
    uploadedFile,
    csvHeaders,
    modelConfig,

    // Computed
    canTrain,
    hasTrainedModels,
    latestModel,

    // Actions
    setUploadedFile,
    setCsvHeaders,
    updateModelConfig,
    resetModelConfig,
    startTraining,
    updateTrainingProgress,
    setTrainingResult,
    setTrainingError,
    resetTraining,
    setModelHistory,
    addModelToHistory,
    removeModelFromHistory,
    updateModelInHistory,

    // API Actions
    uploadCsvFile,
    trainModel,
    loadModelHistory,
    getModelSummary,
    deleteModel,
    getTrainingStatus,

    // Utility functions
    processCsvFile,
    clearUploadedFile,
    formatFileSize,
    formatDate,
  };
});
