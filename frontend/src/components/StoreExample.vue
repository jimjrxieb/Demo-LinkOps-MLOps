<template>
  <div class="p-6 bg-gray-900 rounded-lg border border-holo">
    <h2 class="text-2xl font-orbitron text-primary-400 mb-4">Pinia Store Example</h2>
    
    <!-- User Store Example -->
    <div class="mb-6 p-4 bg-gray-800 rounded border border-gray-700">
      <h3 class="text-lg font-orbitron text-secondary-400 mb-2">User Store</h3>
      <p class="text-gray-300">Name: {{ userStore.getUserName }}</p>
      <p class="text-gray-300">Role: {{ userStore.getUserRole }}</p>
      <button 
        @click="toggleTheme" 
        class="mt-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded text-white"
      >
        Toggle Theme ({{ userStore.getUserPreferences.theme }})
      </button>
    </div>

    <!-- Agent Store Example -->
    <div class="mb-6 p-4 bg-gray-800 rounded border border-gray-700">
      <h3 class="text-lg font-orbitron text-secondary-400 mb-2">Agent Store</h3>
      <div class="space-y-2">
        <div v-for="agent in Object.values(agentStore.agents)" :key="agent.id" class="flex items-center justify-between">
          <span class="text-gray-300">{{ agent.name }} ({{ agent.type }})</span>
          <span :class="getStatusClass(agent.status)" class="px-2 py-1 rounded text-xs">
            {{ agent.status }}
          </span>
        </div>
      </div>
      <button 
        @click="activateWhis" 
        class="mt-2 px-4 py-2 bg-accent-600 hover:bg-accent-700 rounded text-white"
      >
        Activate Whis
      </button>
    </div>

    <!-- Task Store Example -->
    <div class="mb-6 p-4 bg-gray-800 rounded border border-gray-700">
      <h3 class="text-lg font-orbitron text-secondary-400 mb-2">Task Store</h3>
      <p class="text-gray-300">Pending Tasks: {{ taskStore.getPendingTasks.length }}</p>
      <p class="text-gray-300">Processing Tasks: {{ taskStore.getProcessingTasks.length }}</p>
      <button 
        @click="createSampleTask" 
        class="mt-2 px-4 py-2 bg-secondary-600 hover:bg-secondary-700 rounded text-white"
      >
        Create Sample Task
      </button>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '../store/useUserStore'
import { useAgentStore } from '../store/useAgentStore'
import { useTaskStore } from '../store/useTaskStore'

// Initialize stores
const userStore = useUserStore()
const agentStore = useAgentStore()
const taskStore = useTaskStore()

// Methods
const toggleTheme = () => {
  const currentTheme = userStore.getUserPreferences.theme
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark'
  userStore.setTheme(newTheme)
}

const activateWhis = () => {
  agentStore.activateAgent('whis')
  agentStore.addAgentLog('whis', 'Whis agent activated by user', 'info')
}

const createSampleTask = () => {
  const task = taskStore.createTask({
    name: 'Sample Data Processing',
    description: 'Processing sample data through Whis agent',
    agentId: 'whis',
    priority: 'medium'
  })
  
  taskStore.addTaskLog(task.id, 'Task created successfully', 'info')
}

const getStatusClass = (status) => {
  const classes = {
    idle: 'bg-gray-600 text-gray-200',
    processing: 'bg-blue-600 text-white',
    success: 'bg-green-600 text-white',
    error: 'bg-red-600 text-white'
  }
  return classes[status] || 'bg-gray-600 text-gray-200'
}
</script> 