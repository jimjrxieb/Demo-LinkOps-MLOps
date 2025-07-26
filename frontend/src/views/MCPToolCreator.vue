<template>
  <div class="mcp-container">
    <div class="mcp-card">
      <h2 class="title">
        🛠️ MCP Tool Creator
      </h2>

      <!-- Form -->
      <form
        class="space-y-6"
        @submit.prevent="submitTool"
      >
        <!-- Task Description -->
        <div class="form-group">
          <label class="label">Task Description</label>
          <textarea
            v-model="form.description"
            :class="['form-input', { error: v$.description.$error }]"
            placeholder="e.g., Restart Nginx on staging server"
            rows="4"
          />
          <p
            v-if="v$.description.$error"
            class="error-text"
          >
            {{ v$.description.$errors[0].$message }}
          </p>
        </div>

        <!-- Tool Name -->
        <div class="form-group">
          <label class="label">Tool Name</label>
          <input
            v-model="form.name"
            type="text"
            :class="['form-input', { error: v$.name.$error }]"
            placeholder="e.g., restart_nginx"
          >
          <p
            v-if="v$.name.$error"
            class="error-text"
          >
            {{ v$.name.$errors[0].$message }}
          </p>
        </div>

        <!-- Task Type -->
        <div class="form-group">
          <label class="label">Task Type</label>
          <select
            v-model="form.task_type"
            :class="['form-select', { error: v$.task_type.$error }]"
          >
            <option value="">
              Select task type
            </option>
            <option value="sysadmin">
              System Administration
            </option>
            <option value="monitoring">
              Monitoring
            </option>
            <option value="backup">
              Backup
            </option>
            <option value="deployment">
              Deployment
            </option>
            <option value="maintenance">
              Maintenance
            </option>
          </select>
          <p
            v-if="v$.task_type.$error"
            class="error-text"
          >
            {{ v$.task_type.$errors[0].$message }}
          </p>
        </div>

        <!-- Command -->
        <div class="form-group">
          <label class="label">Command</label>
          <textarea
            v-model="form.command"
            :class="['form-input', { error: v$.command.$error }]"
            placeholder="e.g., sudo systemctl restart nginx"
            rows="3"
          />
          <p
            v-if="v$.command.$error"
            class="error-text"
          >
            {{ v$.command.$errors[0].$message }}
          </p>
        </div>

        <!-- Tags -->
        <div class="form-group">
          <label class="label">Tags</label>
          <div class="tag-input">
            <input
              v-model="tagInput"
              type="text"
              placeholder="Add tag and press Enter"
              class="form-input"
              @keydown.enter.prevent="addTag"
            >
          </div>
          <div
            v-if="form.tags.length"
            class="tag-list"
          >
            <span
              v-for="tag in form.tags"
              :key="tag"
              class="tag"
            >
              {{ tag }}
              <button
                type="button"
                class="tag-remove"
                @click="removeTag(tag)"
              >
                ×
              </button>
            </span>
          </div>
        </div>

        <!-- Auto-Execution -->
        <div class="form-group">
          <label class="checkbox">
            <input
              v-model="form.auto"
              type="checkbox"
              class="form-checkbox"
            >
            <span class="ml-2">Enable Auto-Execution</span>
          </label>
          <p class="text-sm text-teal-200 mt-1">
            When enabled, this tool can be run automatically by the Auto Runner
          </p>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="loading || v$.$invalid"
          class="submit-btn"
        >
          <div
            v-if="loading"
            class="spinner mr-2"
          />
          <span v-if="loading">Creating Tool...</span>
          <span v-else>🚀 Create Tool</span>
        </button>
      </form>

      <!-- Success Response -->
      <div
        v-if="response"
        class="response-box"
      >
        <div class="response-header">
          <h3>✅ Tool Created Successfully</h3>
          <button
            class="close-btn"
            @click="response = null"
          >
            ×
          </button>
        </div>

        <div class="response-details">
          <p><strong>Name:</strong> {{ response.name }}</p>
          <p><strong>Type:</strong> {{ response.task_type }}</p>
          <p><strong>Auto:</strong> {{ response.auto ? 'Yes' : 'No' }}</p>
          <p><strong>Tags:</strong> {{ response.tags.join(', ') || 'None' }}</p>
        </div>

        <div class="response-actions">
          <button
            class="reset-btn"
            @click="resetForm"
          >
            Create Another Tool
          </button>
          <button
            class="run-btn"
            :disabled="isRunning"
            @click="runTool(response.name)"
          >
            <div
              v-if="isRunning"
              class="spinner mr-2"
            />
            {{ isRunning ? 'Running...' : '▶️ Run Now' }}
          </button>
        </div>
      </div>

      <!-- Error Message -->
      <div
        v-if="error"
        class="error-box"
      >
        <div class="error-content">
          <svg
            class="error-icon"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"
            />
          </svg>
          <span>{{ error }}</span>
        </div>
        <button
          class="error-close"
          @click="error = null"
        >
          ×
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useVuelidate } from '@vuelidate/core';
import { required, minLength, helpers } from '@vuelidate/validators';
import axios from 'axios';

// Form state
const form = reactive({
  name: '',
  description: '',
  task_type: '',
  command: '',
  tags: [],
  auto: false,
});

const tagInput = ref('');
const loading = ref(false);
const isRunning = ref(false);
const response = ref(null);
const error = ref(null);

// Validation rules
const namePattern = helpers.regex(/^[a-zA-Z0-9_-]+$/);
const rules = {
  name: {
    required,
    minLength: minLength(3),
    pattern: helpers.withMessage(
      'Only letters, numbers, hyphens, and underscores allowed',
      namePattern
    ),
  },
  description: {
    required,
    minLength: minLength(10),
  },
  task_type: { required },
  command: {
    required,
    minLength: minLength(3),
  },
};

const v$ = useVuelidate(rules, form);

// Methods
const addTag = () => {
  const tag = tagInput.value.trim().toLowerCase();
  if (tag && !form.tags.includes(tag)) {
    form.tags.push(tag);
  }
  tagInput.value = '';
};

const removeTag = (tag) => {
  form.tags = form.tags.filter((t) => t !== tag);
};

const submitTool = async () => {
  error.value = null;

  const isValid = await v$.$validate();
  if (!isValid) return;

  loading.value = true;

  try {
    const res = await axios.post('/mcp-tool', form);
    response.value = res.data;

    // Check auto-runner status if auto-execution is enabled
    if (form.auto) {
      try {
        await axios.get('/auto-runner/status');
      } catch (e) {
        error.value =
          'Warning: Auto-runner may not be active. Tool created but may not auto-execute.';
      }
    }
  } catch (err) {
    error.value =
      err.response?.data?.detail || 'Failed to create tool. Please try again.';
  } finally {
    loading.value = false;
  }
};

const runTool = async (toolName) => {
  isRunning.value = true;
  try {
    const res = await axios.post(`/mcp-tool/execute/${toolName}`);
    if (res.data.status === 'success') {
      alert('Tool executed successfully!');
    } else {
      throw new Error(res.data.result.error_message);
    }
  } catch (err) {
    error.value = `Failed to run tool: ${err.message}`;
  } finally {
    isRunning.value = false;
  }
};

const resetForm = () => {
  // Reset form data
  Object.keys(form).forEach((key) => {
    if (key === 'tags') {
      form[key] = [];
    } else if (key === 'auto') {
      form[key] = false;
    } else {
      form[key] = '';
    }
  });

  // Reset validation
  v$.$reset();

  // Clear states
  response.value = null;
  error.value = null;
  tagInput.value = '';
};
</script>

<style scoped>
.mcp-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem;
  min-height: 100vh;
  background: radial-gradient(circle at center, #1c3f45, #0f2e38);
}

.mcp-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #31a3a3;
  padding: 2rem;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  color: white;
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.title {
  color: #ffffff;
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
}

/* Form Controls */
.form-group {
  margin-bottom: 1.5rem;
}

.label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input,
.form-select {
  width: 100%;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: white;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-select:focus {
  border-color: #31a3a3;
  outline: none;
}

.form-input.error,
.form-select.error {
  border-color: #ff6b6b;
}

.error-text {
  color: #ff6b6b;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* Checkbox */
.checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.form-checkbox {
  width: 1rem;
  height: 1rem;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.2);
  cursor: pointer;
}

.form-checkbox:checked {
  background-color: #31a3a3;
  border-color: #31a3a3;
}

/* Tags */
.tag-input {
  margin-bottom: 0.5rem;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: rgba(49, 163, 163, 0.2);
  border: 1px solid #31a3a3;
  border-radius: 4px;
  font-size: 0.875rem;
}

.tag-remove {
  margin-left: 0.5rem;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.tag-remove:hover {
  opacity: 1;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background: #0a2e3c;
  border-radius: 8px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.submit-btn:not(:disabled):hover {
  background: #094759;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Response Box */
.response-box {
  margin-top: 2rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
}

.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.close-btn {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.5);
  transition: color 0.2s;
}

.close-btn:hover {
  color: white;
}

.response-details {
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
  line-height: 1.6;
}

.response-actions {
  display: flex;
  gap: 1rem;
}

.reset-btn,
.run-btn {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.reset-btn {
  background: rgba(255, 255, 255, 0.1);
}

.run-btn {
  background: #31a3a3;
}

.reset-btn:hover {
  background: rgba(255, 255, 255, 0.15);
}

.run-btn:hover:not(:disabled) {
  background: #3cbcbc;
}

.run-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Error Box */
.error-box {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.error-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #ff6b6b;
}

.error-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.error-close {
  color: rgba(255, 107, 107, 0.7);
  font-size: 1.25rem;
  transition: color 0.2s;
}

.error-close:hover {
  color: #ff6b6b;
}

/* Spinner */
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
</style>
