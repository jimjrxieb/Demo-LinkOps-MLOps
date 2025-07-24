<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">🧠 MCP Tool Creator</h1>

    <div class="mb-4">
      <label>Name:</label>
      <input v-model="form.name" class="input" />
    </div>

    <div class="mb-4">
      <label>Description:</label>
      <textarea v-model="form.description" class="input" />
    </div>

    <div class="mb-4">
      <label>Task Type:</label>
      <input v-model="form.task_type" class="input" />
    </div>

    <div class="mb-4">
      <label>Command (to execute):</label>
      <textarea v-model="form.command" class="input" />
    </div>

    <div class="mb-4">
      <label>Tags:</label>
      <input v-model="tagsInput" @keyup.enter="addTag" class="input" />
      <div class="mt-1 flex gap-2 flex-wrap">
        <span
          v-for="(tag, index) in form.tags"
          :key="index"
          class="bg-blue-100 text-blue-700 px-2 py-1 rounded"
        >
          {{ tag }}
          <button @click="removeTag(index)">x</button>
        </span>
      </div>
    </div>

    <button @click="submit" class="btn btn-primary">💾 Save MCP Tool</button>

    <hr class="my-6" />

    <h2 class="text-xl font-bold mb-2">📚 Saved Tools</h2>
    <ul>
      <li v-for="tool in tools" :key="tool.name" class="mb-2 border-b pb-2">
        <strong>{{ tool.name }}</strong>: {{ tool.description }}
        <br />
        <code>{{ tool.command }}</code>
        <button @click="deleteTool(tool.name)" class="ml-2 text-red-500">🗑️ Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const form = ref({
  name: "",
  description: "",
  task_type: "",
  command: "",
  tags: [],
});

const tagsInput = ref("");
const tools = ref([]);

function addTag() {
  if (tagsInput.value.trim()) {
    form.value.tags.push(tagsInput.value.trim());
    tagsInput.value = "";
  }
}

function removeTag(index) {
  form.value.tags.splice(index, 1);
}

async function submit() {
  await axios.post("/api/mcp-tool", form.value);
  await fetchTools();
}

async function fetchTools() {
  const res = await axios.get("/api/mcp-tool/list");
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