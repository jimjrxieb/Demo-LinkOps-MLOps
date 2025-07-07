<template>
  <div class="dashboard-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">LinkOps Dashboard</h1>
      <p class="text-gray-600">MLOps Platform Overview & Analytics</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total Tasks</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalTasks }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Completed</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.completedTasks }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-yellow-100">
            <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Pending</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.pendingTasks }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Success Rate</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.successRate }}%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Recent Tasks -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-800">Recent Tasks</h2>
          <button @click="loadTasks" class="text-blue-600 hover:text-blue-800 text-sm">View All</button>
        </div>
        
        <div class="space-y-4">
          <div v-for="task in recentTasks" :key="task.id" class="border-l-4 border-blue-500 pl-4">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="font-medium text-gray-800">{{ task.title }}</h3>
                <p class="text-sm text-gray-600 mt-1">{{ task.description }}</p>
                <div class="flex items-center space-x-4 mt-2">
                  <span class="text-xs text-gray-500">{{ task.category }}</span>
                  <span class="text-xs text-gray-500">{{ formatDate(task.created_at) }}</span>
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="{
                      'bg-green-100 text-green-800': task.status === 'completed',
                      'bg-yellow-100 text-yellow-800': task.status === 'pending',
                      'bg-red-100 text-red-800': task.status === 'failed'
                    }"
                  >
                    {{ task.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Audit Results -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-800">Recent Audits</h2>
          <button @click="loadAuditHistory" class="text-blue-600 hover:text-blue-800 text-sm">View All</button>
        </div>
        
        <div class="space-y-4">
          <div v-for="audit in recentAudits" :key="audit.id" class="border-l-4 border-green-500 pl-4">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="font-medium text-gray-800">{{ audit.repo_name }}</h3>
                <div class="flex items-center space-x-4 mt-2">
                  <span class="text-sm text-gray-600">Security: {{ audit.security_score }}</span>
                  <span class="text-sm text-gray-600">GitOps: {{ audit.gitops_score }}</span>
                  <span class="text-sm text-gray-600">Grade: {{ audit.grade }}</span>
                </div>
                <div class="flex items-center space-x-4 mt-2">
                  <span class="text-xs text-gray-500">{{ formatDate(audit.timestamp) }}</span>
                  <span class="text-xs text-gray-500">{{ audit.total_issues }} issues</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Training Summary -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-800">Training Summary</h2>
          <button @click="loadTrainingStats" class="text-blue-600 hover:text-blue-800 text-sm">View Details</button>
        </div>
        
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-2xl font-bold text-blue-600">{{ trainingStats.totalOrbs }}</div>
              <div class="text-sm text-blue-700">Orbs Created</div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <div class="text-2xl font-bold text-green-600">{{ trainingStats.totalRunes }}</div>
              <div class="text-sm text-green-700">Runes Generated</div>
            </div>
          </div>
          
          <div class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Learning Progress</span>
              <span class="text-gray-800">{{ trainingStats.learningProgress }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="bg-blue-600 h-2 rounded-full" 
                :style="{ width: trainingStats.learningProgress + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Health -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-800">System Health</h2>
          <button @click="checkHealth" class="text-blue-600 hover:text-blue-800 text-sm">Refresh</button>
        </div>
        
        <div class="space-y-4">
          <div v-for="service in systemHealth" :key="service.name" class="flex items-center justify-between">
            <div class="flex items-center">
              <div 
                class="w-3 h-3 rounded-full mr-3"
                :class="{
                  'bg-green-500': service.status === 'healthy',
                  'bg-yellow-500': service.status === 'warning',
                  'bg-red-500': service.status === 'unhealthy'
                }"
              ></div>
              <span class="text-sm font-medium text-gray-800">{{ service.name }}</span>
            </div>
            <span 
              class="text-xs px-2 py-1 rounded"
              :class="{
                'bg-green-100 text-green-800': service.status === 'healthy',
                'bg-yellow-100 text-yellow-800': service.status === 'warning',
                'bg-red-100 text-red-800': service.status === 'unhealthy'
              }"
            >
              {{ service.status }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mt-8 bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Quick Actions</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button 
          @click="createNewTask"
          class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <svg class="w-6 h-6 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          <div class="text-left">
            <div class="font-medium text-gray-800">New Task</div>
            <div class="text-sm text-gray-600">Create a new task</div>
          </div>
        </button>
        
        <button 
          @click="runAudit"
          class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <svg class="w-6 h-6 text-green-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <div class="text-left">
            <div class="font-medium text-gray-800">Run Audit</div>
            <div class="text-sm text-gray-600">Audit a repository</div>
          </div>
        </button>
        
        <button 
          @click="viewAnalytics"
          class="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <svg class="w-6 h-6 text-purple-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
          <div class="text-left">
            <div class="font-medium text-gray-800">Analytics</div>
            <div class="text-sm text-gray-600">View detailed analytics</div>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { mlopsPlatformService, healthChecks } from '@/services/api'

export default {
  name: 'Dashboard',
  setup() {
    const stats = ref({
      totalTasks: 0,
      completedTasks: 0,
      pendingTasks: 0,
      successRate: 0
    })

    const recentTasks = ref([])
    const recentAudits = ref([])
    const trainingStats = ref({
      totalOrbs: 0,
      totalRunes: 0,
      learningProgress: 0
    })

    const systemHealth = ref([
      { name: 'MLOps Platform', status: 'healthy' },
      { name: 'Audit Assess', status: 'healthy' },
      { name: 'Whis Data Input', status: 'healthy' },
      { name: 'Whis Enhance', status: 'healthy' }
    ])

    const loadDashboardData = async () => {
      try {
        // Load task statistics
        const taskStats = await mlopsPlatformService.getTaskStats()
        stats.value = {
          totalTasks: taskStats.total_tasks || 0,
          completedTasks: taskStats.completed_tasks || 0,
          pendingTasks: taskStats.pending_tasks || 0,
          successRate: taskStats.success_rate || 0
        }

        // Load recent tasks
        const tasks = await mlopsPlatformService.getTasks()
        recentTasks.value = tasks.slice(0, 5)

        // Load training statistics
        const orbs = await mlopsPlatformService.getOrbs()
        const runes = await mlopsPlatformService.getRunes()
        trainingStats.value = {
          totalOrbs: orbs.length,
          totalRunes: runes.length,
          learningProgress: Math.min(100, Math.round((orbs.length + runes.length) * 5))
        }

        // Check system health
        await checkHealth()

      } catch (error) {
        console.error('Error loading dashboard data:', error)
      }
    }

    const checkHealth = async () => {
      try {
        const healthPromises = [
          healthChecks.mlopsPlatform().then(() => 'healthy').catch(() => 'unhealthy'),
          healthChecks.auditAssess().then(() => 'healthy').catch(() => 'unhealthy'),
          healthChecks.whisDataInput().then(() => 'healthy').catch(() => 'unhealthy'),
          healthChecks.whisEnhance().then(() => 'healthy').catch(() => 'unhealthy')
        ]

        const results = await Promise.allSettled(healthPromises)
        systemHealth.value = [
          { name: 'MLOps Platform', status: results[0].value || 'unhealthy' },
          { name: 'Audit Assess', status: results[1].value || 'unhealthy' },
          { name: 'Whis Data Input', status: results[2].value || 'unhealthy' },
          { name: 'Whis Enhance', status: results[3].value || 'unhealthy' }
        ]
      } catch (error) {
        console.error('Error checking health:', error)
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const createNewTask = () => {
      // Navigate to task creation
      console.log('Navigate to task creation')
    }

    const runAudit = () => {
      // Navigate to audit page
      console.log('Navigate to audit page')
    }

    const viewAnalytics = () => {
      // Navigate to analytics page
      console.log('Navigate to analytics page')
    }

    const loadTasks = () => {
      // Navigate to tasks page
      console.log('Navigate to tasks page')
    }

    const loadAuditHistory = () => {
      // Navigate to audit history
      console.log('Navigate to audit history')
    }

    const loadTrainingStats = () => {
      // Navigate to training stats
      console.log('Navigate to training stats')
    }

    onMounted(() => {
      loadDashboardData()
    })

    return {
      stats,
      recentTasks,
      recentAudits,
      trainingStats,
      systemHealth,
      formatDate,
      createNewTask,
      runAudit,
      viewAnalytics,
      loadTasks,
      loadAuditHistory,
      loadTrainingStats,
      checkHealth
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}
</style> 