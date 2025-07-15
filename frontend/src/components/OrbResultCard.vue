<template>
  <div class="bg-green-900 border-l-4 border-green-400 text-white p-4 rounded shadow">
    <h2 class="text-lg font-bold text-green-200 mb-1">✅ Orb Match Found!</h2>
    <p class="text-xl font-semibold text-teal-300">{{ orb.title }}</p>
    <p class="text-sm text-gray-300 mb-2 italic">Category: {{ orb.category }}</p>
    <p class="mb-2">{{ orb.orb }}</p>
    <p class="text-sm text-blue-300">Confidence: {{ confidence }}%</p>
    <div class="text-xs text-blue-200 mt-2">
      Tags:
      <span v-for="tag in orb.keywords" :key="tag" class="mr-2">#{{ tag }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  orb: Object,
  confidence: [String, Number]
});
</script> 