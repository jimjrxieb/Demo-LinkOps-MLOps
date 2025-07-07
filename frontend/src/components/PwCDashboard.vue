<template>
  <div class="p-6 bg-gray-900 min-h-screen holo-bg">
    <div class="max-w-7xl mx-auto">
      <!-- Header with Cyberpunk Effects -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white mb-2 neon-text glitch" data-text="MLOps Platform">MLOps Platform</h1>
        <p class="text-gray-400 typewriter">Unified AI training, runtime agents, and orchestration platform</p>
      </div>

      <!-- Platform Overview Cards with Holographic Effects -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-gray-800 p-6 rounded-xl border border-blue-600 holo-hover pulse-cyber">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Total Tasks</p>
              <p class="text-2xl font-bold text-blue-400 neon-text">{{ stats.totalTasks }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center status-indicator">
              <span class="text-xl">📋</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl border border-green-600 holo-hover pulse-cyber">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Active Scripts</p>
              <p class="text-2xl font-bold text-green-400 neon-text">{{ stats.activeScripts }}</p>
            </div>
            <div class="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center status-indicator">
              <span class="text-xl">⚡</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl border border-purple-600 holo-hover pulse-cyber">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Available Orbs</p>
              <p class="text-2xl font-bold text-purple-400 neon-text">{{ stats.availableOrbs }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center status-indicator">
              <span class="text-xl">🔮</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl border border-yellow-600 holo-hover pulse-cyber">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Active Runes</p>
              <p class="text-2xl font-bold text-yellow-400 neon-text">{{ stats.activeRunes }}</p>
            </div>
            <div class="w-12 h-12 bg-yellow-600 rounded-full flex items-center justify-center status-indicator">
              <span class="text-xl">⚔️</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Platform Components with Holographic Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div class="bg-gray-800 p-6 rounded-xl holo-card-3d">
          <h2 class="text-xl font-bold text-white mb-4 neon-text">Task Categories</h2>
          <div class="space-y-4">
            <div v-for="(count, category) in stats.taskCategories" :key="category" class="flex items-center justify-between holo-hover">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full mr-3" :class="getCategoryColor(category)"></div>
                <span class="text-gray-300 capitalize">{{ category }}</span>
              </div>
              <span class="text-white font-semibold neon-text">{{ count }}</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl holo-card-3d">
          <h2 class="text-xl font-bold text-white mb-4 neon-text">Recent Activity</h2>
          <div class="space-y-4">
            <div v-for="(count, type) in stats.recentActivity" :key="type" class="flex items-center justify-between holo-hover">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full mr-3 flex items-center justify-center text-sm font-bold status-indicator" :class="getActivityBgColor(type)">
                  {{ getActivityIcon(type) }}
                </div>
                <span class="text-gray-300 capitalize">{{ type }}</span>
              </div>
              <span class="text-white font-semibold neon-text">{{ count }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Tasks with Cyberpunk Styling -->
      <div class="bg-gray-800 p-6 rounded-xl mb-8 holo-card-3d">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-white neon-text">Recent Tasks</h2>
          <div class="flex space-x-2">
            <select v-model="selectedCategory" class="bg-gray-700 text-white px-3 py-1 rounded text-sm border border-cyan-500 focus:border-cyan-300 focus:outline-none">
              <option value="">All Categories</option>
              <option value="mlops">MLOps</option>
              <option value="training">Training</option>
              <option value="deployment">Deployment</option>
              <option value="monitoring">Monitoring</option>
            </select>
            <select v-model="selectedStatus" class="bg-gray-700 text-white px-3 py-1 rounded text-sm border border-cyan-500 focus:border-cyan-300 focus:outline-none">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
            </select>
          </div>
        </div>

        <div class="space-y-4">
          <div v-for="task in filteredTasks" :key="task.id" class="bg-gray-700 p-4 rounded-lg border-l-4 holo-hover" :class="getTaskBorderColor(task)">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center mb-2">
                  <span class="text-sm font-semibold neon-text" :class="getCategoryTextColor(task.category)">{{ task.category }}</span>
                  <span class="text-xs text-gray-400 ml-2">{{ formatDate(task.created_at) }}</span>
                  <div v-if="task.status === 'completed'" class="ml-2 px-2 py-1 bg-green-600 text-white text-xs rounded pulse-cyber">Completed</div>
                  <div v-else-if="task.status === 'in_progress'" class="ml-2 px-2 py-1 bg-blue-600 text-white text-xs rounded pulse-cyber">In Progress</div>
                  <div v-else-if="task.status === 'failed'" class="ml-2 px-2 py-1 bg-red-600 text-white text-xs rounded pulse-cyber">Failed</div>
                  <div v-else class="ml-2 px-2 py-1 bg-gray-600 text-white text-xs rounded">Pending</div>
                </div>
                <p class="text-white font-medium mb-1">{{ task.title }}</p>
                <p class="text-gray-300 text-sm mb-2 terminal-text">{{ task.description }}</p>
                <div v-if="task.priority" class="text-yellow-300 text-sm">
                  <strong>Priority:</strong> {{ task.priority }}
                </div>
                <div v-if="task.tags" class="flex flex-wrap gap-1 mt-2">
                  <span v-for="tag in task.tags" :key="tag" 
                        class="px-2 py-1 bg-gray-600 text-white text-xs rounded border border-cyan-500">
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredTasks.length === 0" class="text-center py-8 text-gray-400">
          <div class="cyber-spinner mx-auto mb-4"></div>
          No tasks found matching the selected filters.
        </div>
      </div>

      <!-- Quick Actions with Cyberpunk Buttons -->
      <div class="bg-gray-800 p-6 rounded-xl holo-card-3d">
        <h2 class="text-xl font-bold text-white mb-4 neon-text">Quick Actions</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button @click="createNewTask" class="cyber-button bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
            📝 Create Task
          </button>
          <button @click="executeScript" class="cyber-button bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors">
            ⚡ Execute Script
          </button>
          <button @click="useOrb" class="cyber-button bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
            🔮 Use Orb
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { mlopsPlatformService } from '../services/api.js'

const stats = ref({
  totalTasks: 0,
  activeScripts: 0,
  availableOrbs: 0,
  activeRunes: 0,
  taskCategories: {},
  recentActivity: {}
})

const tasks = ref([])
const selectedCategory = ref('')
const selectedStatus = ref('')

const filteredTasks = computed(() => {
  let filtered = tasks.value

  if (selectedCategory.value) {
    filtered = filtered.filter(task => task.category === selectedCategory.value)
  }

  if (selectedStatus.value) {
    filtered = filtered.filter(task => task.status === selectedStatus.value)
  }

  return filtered.slice(0, 10) // Show last 10
})

const getCategoryColor = (category) => {
  const colors = {
    'mlops': 'bg-blue-500',
    'training': 'bg-green-500',
    'deployment': 'bg-purple-500',
    'monitoring': 'bg-yellow-500'
  }
  return colors[category] || 'bg-gray-500'
}

const getCategoryTextColor = (category) => {
  const colors = {
    'mlops': 'text-blue-400',
    'training': 'text-green-400',
    'deployment': 'text-purple-400',
    'monitoring': 'text-yellow-400'
  }
  return colors[category] || 'text-gray-400'
}

const getActivityBgColor = (type) => {
  const colors = {
    'tasks': 'bg-blue-600',
    'scripts': 'bg-green-600',
    'orbs': 'bg-purple-600',
    'runes': 'bg-yellow-600'
  }
  return colors[type] || 'bg-gray-600'
}

const getActivityIcon = (type) => {
  const icons = {
    'tasks': '📋',
    'scripts': '⚡',
    'orbs': '🔮',
    'runes': '⚔️'
  }
  return icons[type] || '📊'
}

const getTaskBorderColor = (task) => {
  if (task.status === 'failed') return 'border-red-500'
  if (task.status === 'completed') return 'border-green-500'
  if (task.status === 'in_progress') return 'border-blue-500'
  return 'border-gray-500'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const fetchStats = async () => {
  try {
    const [tasksRes, scriptsRes, orbsRes, runesRes, taskStatsRes] = await Promise.all([
      mlopsPlatformService.getTasks(),
      mlopsPlatformService.getScripts(),
      mlopsPlatformService.getOrbs(),
      mlopsPlatformService.getRunes(),
      mlopsPlatformService.getTaskStats()
    ])

    const tasksData = tasksRes.data
    const scriptsData = scriptsRes.data
    const orbsData = orbsRes.data
    const runesData = runesRes.data
    const taskStatsData = taskStatsRes.data

    // Calculate task categories
    const categoryCount = {}
    tasksData.forEach(task => {
      categoryCount[task.category] = (categoryCount[task.category] || 0) + 1
    })

    // Calculate recent activity
    const activityCount = {
      tasks: tasksData.length,
      scripts: scriptsData.length,
      orbs: orbsData.length,
      runes: runesData.length
    }

    stats.value = {
      totalTasks: tasksData.length,
      activeScripts: scriptsData.filter(s => s.status === 'active').length,
      availableOrbs: orbsData.filter(o => o.status === 'available').length,
      activeRunes: runesData.filter(r => r.status === 'active').length,
      taskCategories: categoryCount,
      recentActivity: activityCount
    }

    tasks.value = tasksData
  } catch (error) {
    console.error('Failed to fetch MLOps Platform data:', error)
  }
}

const createNewTask = async () => {
  try {
    const newTask = {
      title: "New MLOps Task",
      description: "Task created from dashboard",
      category: "mlops",
      priority: "medium",
      tags: ["dashboard", "quick-action"]
    }
    
    await mlopsPlatformService.createTask(newTask)
    await fetchStats() // Refresh stats
    alert('Task created successfully')
  } catch (error) {
    console.error('Failed to create task:', error)
    alert('Failed to create task')
  }
}

const executeScript = async () => {
  try {
    // Get the first available script
    const scriptsRes = await mlopsPlatformService.getScripts()
    const scripts = scriptsRes.data
    
    if (scripts.length > 0) {
      await mlopsPlatformService.executeScript(scripts[0].id)
      await fetchStats() // Refresh stats
      alert('Script executed successfully')
    } else {
      alert('No scripts available to execute')
    }
  } catch (error) {
    console.error('Failed to execute script:', error)
    alert('Failed to execute script')
  }
}

const useOrb = async () => {
  try {
    // Get the first available orb
    const orbsRes = await mlopsPlatformService.getOrbs()
    const orbs = orbsRes.data
    
    if (orbs.length > 0) {
      await mlopsPlatformService.useOrb(orbs[0].id)
      await fetchStats() // Refresh stats
      alert('Orb used successfully')
    } else {
      alert('No orbs available to use')
    }
  } catch (error) {
    console.error('Failed to use orb:', error)
    alert('Failed to use orb')
  }
}

onMounted(() => {
  fetchStats()
})
</script> 