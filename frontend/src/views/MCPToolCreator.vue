<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">🧠 MCP Tool Creator</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
      <div>
        <label class="block font-semibold mb-1">Name:</label>
        <input v-model="form.name" placeholder="Tool Name" class="input" />
      </div>

      <div>
        <label class="block font-semibold mb-1">Task Type:</label>
        <input
          v-model="form.task_type"
          placeholder="command, script, etc."
          class="input"
        />
      </div>
    </div>

    <div class="mb-4">
      <label class="block font-semibold mb-1">Description:</label>
      <textarea
        v-model="form.description"
        placeholder="What does this tool do?"
        class="input"
        rows="2"
      />
    </div>

    <div class="mb-4">
      <label class="block font-semibold mb-1">Command (to execute):</label>
      <textarea
        v-model="form.command"
        placeholder="Command or script to run"
        class="input"
        rows="3"
      />
    </div>

    <div class="mb-4">
      <label class="block font-semibold mb-1">Tags:</label>
      <input
        v-model="tagsInput"
        placeholder="Add tag and press Enter"
        class="input"
        @keyup.enter="addTag"
      />
      <div class="mt-2 flex gap-2 flex-wrap">
        <span
          v-for="(tag, index) in form.tags"
          :key="index"
          class="bg-blue-100 text-blue-700 px-2 py-1 rounded text-sm flex items-center"
        >
          {{ tag }}
          <button
            class="ml-1 text-red-500 hover:text-red-700"
            @click="removeTag(index)"
          >
            ×
          </button>
        </span>
      </div>
    </div>

    <div class="mb-6">
      <label class="inline-flex items-center cursor-pointer">
        <input
          v-model="form.auto"
          type="checkbox"
          class="mr-2 w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
        />
        <span class="font-semibold">🚀 Auto Execute</span>
        <span class="ml-2 text-sm text-gray-600"
          >(Run automatically every 5 minutes)</span
        >
      </label>
    </div>

    <button class="btn btn-primary" @click="submit">💾 Save MCP Tool</button>

    <hr class="my-8" />

    <h2 class="text-xl font-bold mb-4">📚 Saved Tools</h2>
    <div class="grid gap-4">
      <div
        v-for="tool in tools"
        :key="tool.name"
        class="border p-4 rounded-lg bg-white shadow-sm"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <h3 class="font-semibold text-lg">
                {{ tool.name }}
              </h3>
              <span
                v-if="tool.auto"
                class="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-medium"
                >🚀 Auto</span
              >
            </div>
            <p class="text-gray-600 mb-2">
              {{ tool.description }}
            </p>
            <p class="text-sm mb-2">
              <span class="font-medium">Type:</span> {{ tool.task_type }}
            </p>
            <p class="text-sm mb-2">
              <span class="font-medium">Command:</span>
            </p>
            <code
              class="block bg-gray-100 p-2 rounded text-sm font-mono break-all"
              >{{ tool.command }}</code
            >
            <div v-if="tool.tags && tool.tags.length > 0" class="mt-2">
              <span class="text-sm font-medium">Tags:</span>
              <span
                v-for="tag in tool.tags"
                :key="tag"
                class="ml-1 bg-blue-100 text-blue-700 px-1 py-0.5 rounded text-xs"
                >{{ tag }}</span
              >
            </div>
          </div>
          <button
            class="text-red-500 hover:text-red-700 ml-4"
            @click="deleteTool(tool.name)"
          >
            🗑️ Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const form = ref({
  name: '',
  description: '',
  task_type: '',
  command: '',
  tags: [],
  auto: false,
});

const tagsInput = ref('');
const tools = ref([]);

function addTag() {
  if (tagsInput.value.trim()) {
    form.value.tags.push(tagsInput.value.trim());
    tagsInput.value = '';
  }
}

function removeTag(index) {
  form.value.tags.splice(index, 1);
}

async function submit() {
  await axios.post('/api/mcp-tool', form.value);
  await fetchTools();

  // Reset form
  form.value = {
    name: '',
    description: '',
    task_type: '',
    command: '',
    tags: [],
    auto: false,
  };
  tagsInput.value = '';
}

async function fetchTools() {
  const res = await axios.get('/api/mcp-tool/list');
  tools.value = res.data;
}

async function deleteTool(name) {
  await axios.delete(`/api/mcp-tool/${name}`);
  await fetchTools();
}

onMounted(fetchTools);
</script>

<style scoped>
.input {
  @apply border rounded px-2 py-1 w-full;
}
.btn {
  @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700;
}
</style>
