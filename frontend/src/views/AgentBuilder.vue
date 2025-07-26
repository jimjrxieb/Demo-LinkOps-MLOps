<template>
  <div class="p-6 max-w-6xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-primary mb-2">
        🤖 Agent Builder
      </h1>
      <p class="text-gray-600">
        Create AI agents and tools from natural language - fully offline,
        powered by local LLM
      </p>
    </div>

    <!-- Main Content -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Left Panel: Tool Generation -->
      <div class="space-y-6">
        <!-- Task Input -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-xl mb-4">
              📝 Describe Your Task
            </h2>

            <div class="form-control">
              <label class="label">
                <span class="label-text">Task Description</span>
              </label>
              <textarea
                v-model="taskDescription"
                placeholder="e.g., create a Kubernetes pod with nginx, write a bash script to backup files, create a Python API endpoint..."
                class="textarea textarea-bordered h-32"
                :disabled="generating"
              />
            </div>

            <div class="form-control">
              <label class="label">
                <span class="label-text">Category (Optional)</span>
              </label>
              <select
                v-model="selectedCategory"
                class="select select-bordered"
              >
                <option value="">
                  Auto-detect
                </option>
                <option value="kubernetes">
                  Kubernetes
                </option>
                <option value="docker">
                  Docker
                </option>
                <option value="bash">
                  Bash Script
                </option>
                <option value="python">
                  Python Script
                </option>
                <option value="terraform">
                  Terraform
                </option>
                <option value="general">
                  General
                </option>
              </select>
            </div>

            <div class="card-actions justify-end mt-4">
              <button
                :disabled="!canGenerate || generating"
                class="btn btn-primary"
                @click="generateTool"
              >
                <span
                  v-if="generating"
                  class="loading loading-spinner loading-sm"
                />
                {{ generating ? 'Generating...' : 'Generate Tool' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Generated Tool Preview -->
        <div
          v-if="generatedTool"
          class="card bg-base-100 shadow-xl"
        >
          <div class="card-body">
            <h2 class="card-title text-xl mb-4">
              🛠️ Generated Tool
            </h2>

            <div class="stats stats-vertical lg:stats-horizontal shadow mb-4">
              <div class="stat">
                <div class="stat-title">
                  Category
                </div>
                <div class="stat-value text-primary text-lg">
                  {{ generatedTool.category }}
                </div>
              </div>
              <div class="stat">
                <div class="stat-title">
                  Complexity
                </div>
                <div class="stat-value text-secondary">
                  {{ generatedTool.estimated_complexity }}
                </div>
              </div>
            </div>

            <!-- Tool Code -->
            <div class="form-control">
              <label class="label">
                <span class="label-text">Generated Code</span>
              </label>
              <div class="mockup-code bg-base-300">
                <pre
                  data-prefix="$"
                ><code>{{ generatedTool.tool_code }}</code></pre>
              </div>
            </div>

            <!-- Usage Suggestions -->
            <div class="mt-4">
              <h3 class="font-semibold mb-2">
                💡 Usage Suggestions
              </h3>
              <div class="space-y-2">
                <div
                  v-for="suggestion in generatedTool.suggested_usage"
                  :key="suggestion"
                  class="p-2 bg-base-200 rounded text-sm"
                >
                  {{ suggestion }}
                </div>
              </div>
            </div>

            <div class="card-actions justify-end mt-4">
              <button
                class="btn btn-success"
                @click="saveTool"
              >
                💾 Save Tool
              </button>
              <button
                class="btn btn-outline"
                @click="copyToClipboard"
              >
                📋 Copy Code
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel: Tool Management -->
      <div class="space-y-6">
        <!-- Tool Categories -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-xl mb-4">
              📂 Tool Categories
            </h2>

            <div class="grid grid-cols-2 gap-4">
              <div
                v-for="(info, category) in categories"
                :key="category"
                class="p-4 bg-base-200 rounded-lg cursor-pointer hover:bg-base-300"
                @click="selectCategory(category)"
              >
                <div class="flex justify-between items-center">
                  <div>
                    <span class="font-medium capitalize">{{ category }}</span>
                    <span class="badge badge-primary ml-2">{{
                      info.file_extension
                    }}</span>
                  </div>
                </div>
                <p class="text-sm text-gray-600 mt-1">
                  {{ info.description }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tool Library -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-xl mb-4">
              🗂️ Tool Library
            </h2>

            <div class="flex justify-between items-center mb-4">
              <button
                class="btn btn-outline"
                @click="loadTools"
              >
                <span
                  v-if="loadingTools"
                  class="loading loading-spinner loading-sm"
                />
                {{ loadingTools ? 'Loading...' : 'Refresh Tools' }}
              </button>
              <span class="text-sm text-gray-500">{{ tools.length }} generated tools</span>
            </div>

            <div
              v-if="tools.length > 0"
              class="space-y-2 max-h-96 overflow-y-auto"
            >
              <div
                v-for="tool in tools"
                :key="tool.tool_id"
                class="p-3 bg-base-200 rounded-lg cursor-pointer hover:bg-base-300"
                @click="viewTool(tool)"
              >
                <div class="flex justify-between items-center">
                  <div>
                    <span class="font-medium">{{ tool.filename }}</span>
                    <span
                      class="badge ml-2"
                      :class="getCategoryBadgeClass(tool.category)"
                    >
                      {{ tool.category }}
                    </span>
                  </div>
                  <div class="flex gap-2">
                    <span class="badge badge-outline">{{
                      tool.complexity
                    }}</span>
                    <button
                      class="btn btn-sm btn-error"
                      @click.stop="deleteTool(tool.tool_id)"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                <div class="text-sm text-gray-500 mt-1">
                  {{ tool.lines_of_code }} lines •
                  {{ formatFileSize(tool.file_size) }}
                </div>
              </div>
            </div>

            <div
              v-else
              class="text-center py-8 text-gray-500"
            >
              <div class="text-4xl mb-4">
                🛠️
              </div>
              <p>
                No tools generated yet. Describe a task to create your first
                tool!
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tool Viewer Modal -->
    <div
      v-if="showToolModal"
      class="modal modal-open"
    >
      <div class="modal-box max-w-4xl">
        <h3 class="font-bold text-lg mb-4">
          🔍 Tool Details
        </h3>

        <div
          v-if="selectedTool"
          class="mb-4"
        >
          <div class="stats stats-horizontal shadow">
            <div class="stat">
              <div class="stat-title">
                Tool ID
              </div>
              <div class="stat-value text-primary text-lg">
                {{ selectedTool.tool_id }}
              </div>
            </div>
            <div class="stat">
              <div class="stat-title">
                Category
              </div>
              <div class="stat-value text-secondary">
                {{ selectedTool.category }}
              </div>
            </div>
            <div class="stat">
              <div class="stat-title">
                Complexity
              </div>
              <div class="stat-value">
                {{ selectedTool.complexity }}
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="selectedTool"
          class="mb-4"
        >
          <h4 class="font-semibold mb-2">
            Code Content
          </h4>
          <div class="mockup-code bg-base-300 max-h-96 overflow-y-auto">
            <pre data-prefix="$"><code>{{ selectedTool.content }}</code></pre>
          </div>
        </div>

        <div class="modal-action">
          <button
            class="btn btn-outline"
            @click="copySelectedTool"
          >
            Copy Code
          </button>
          <button
            class="btn"
            @click="closeToolModal"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Success Toast -->
    <div
      v-if="showToast"
      class="toast toast-top toast-end"
    >
      <div class="alert alert-success">
        <span>{{ toastMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// Reactive data
const taskDescription = ref('');
const selectedCategory = ref('');
const generating = ref(false);
const generatedTool = ref(null);
const tools = ref([]);
const loadingTools = ref(false);
const categories = ref({});
const showToolModal = ref(false);
const selectedTool = ref(null);
const showToast = ref(false);
const toastMessage = ref('');

// Computed properties
const canGenerate = computed(() => {
  return taskDescription.value.trim().length > 0 && !generating.value;
});

// Methods
async function generateTool() {
  if (!canGenerate.value) return;

  generating.value = true;
  try {
    const formData = new FormData();
    formData.append('task', taskDescription.value);
    if (selectedCategory.value) {
      formData.append('category', selectedCategory.value);
    }

    const response = await fetch(
      'http://localhost:9000/agent-builder/agent/create',
      {
        method: 'POST',
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    generatedTool.value = await response.json();

    // Refresh tools list
    await loadTools();

    showToastMessage('Tool generated successfully!');
  } catch (error) {
    console.error('Tool generation failed:', error);
    alert('Failed to generate tool: ' + error.message);
  } finally {
    generating.value = false;
  }
}

async function loadTools() {
  loadingTools.value = true;
  try {
    const response = await fetch(
      'http://localhost:9000/agent-builder/agent/list'
    );
    if (response.ok) {
      const data = await response.json();
      tools.value = data.tools || [];
    }
  } catch (error) {
    console.error('Failed to load tools:', error);
  } finally {
    loadingTools.value = false;
  }
}

async function loadCategories() {
  try {
    const response = await fetch(
      'http://localhost:9000/agent-builder/categories'
    );
    if (response.ok) {
      const data = await response.json();
      categories.value = data.categories || {};
    }
  } catch (error) {
    console.error('Failed to load categories:', error);
  }
}

async function deleteTool(toolId) {
  if (!confirm('Are you sure you want to delete this tool?')) return;

  try {
    const response = await fetch(
      `http://localhost:9000/agent-builder/agent/${toolId}`,
      {
        method: 'DELETE',
      }
    );

    if (response.ok) {
      await loadTools();
      showToastMessage('Tool deleted successfully!');
    } else {
      throw new Error('Failed to delete tool');
    }
  } catch (error) {
    console.error('Failed to delete tool:', error);
    alert('Failed to delete tool: ' + error.message);
  }
}

async function viewTool(tool) {
  try {
    const response = await fetch(
      `http://localhost:9000/agent-builder/agent/${tool.tool_id}`
    );
    if (response.ok) {
      selectedTool.value = await response.json();
      showToolModal.value = true;
    }
  } catch (error) {
    console.error('Failed to get tool details:', error);
    alert('Failed to get tool details');
  }
}

function selectCategory(category) {
  selectedCategory.value = category;
}

function saveTool() {
  // Tool is automatically saved by the backend
  showToastMessage('Tool saved successfully!');
}

function copyToClipboard() {
  if (generatedTool.value) {
    navigator.clipboard.writeText(generatedTool.value.tool_code);
    showToastMessage('Code copied to clipboard!');
  }
}

function copySelectedTool() {
  if (selectedTool.value) {
    navigator.clipboard.writeText(selectedTool.value.content);
    showToastMessage('Code copied to clipboard!');
  }
}

function closeToolModal() {
  showToolModal.value = false;
  selectedTool.value = null;
}

function getCategoryBadgeClass(category) {
  const classes = {
    kubernetes: 'badge-primary',
    docker: 'badge-secondary',
    bash: 'badge-accent',
    python: 'badge-info',
    terraform: 'badge-warning',
    general: 'badge-neutral',
  };
  return classes[category] || 'badge-neutral';
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

function showToastMessage(message) {
  toastMessage.value = message;
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 3000);
}

// Load data on mount
onMounted(() => {
  loadTools();
  loadCategories();
});
</script>

<style scoped>
.modal {
  z-index: 1000;
}

.toast {
  z-index: 1001;
}
</style>
