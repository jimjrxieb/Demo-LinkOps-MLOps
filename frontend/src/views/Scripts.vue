<template>
  <div class="scripts-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">💻 Scripts Management</h1>
      <p class="text-gray-300">Execute and manage automation scripts across the platform</p>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="glass-panel p-6 text-center hover:neon-border transition-all duration-300 cursor-pointer">
        <div class="text-3xl mb-2">🚀</div>
        <div class="text-sm font-medium text-white">Deploy Services</div>
        <div class="text-xs text-gray-400">{{ deploymentStats.total }} scripts</div>
      </div>
      <div class="glass-panel p-6 text-center hover:neon-border transition-all duration-300 cursor-pointer">
        <div class="text-3xl mb-2">🔍</div>
        <div class="text-sm font-medium text-white">Health Checks</div>
        <div class="text-xs text-gray-400">{{ healthStats.total }} monitors</div>
      </div>
      <div class="glass-panel p-6 text-center hover:neon-border transition-all duration-300 cursor-pointer">
        <div class="text-3xl mb-2">🔧</div>
        <div class="text-sm font-medium text-white">Maintenance</div>
        <div class="text-xs text-gray-400">{{ maintenanceStats.total }} tasks</div>
      </div>
      <div class="glass-panel p-6 text-center hover:neon-border transition-all duration-300 cursor-pointer">
        <div class="text-3xl mb-2">📊</div>
        <div class="text-sm font-medium text-white">Monitoring</div>
        <div class="text-xs text-gray-400">{{ monitoringStats.total }} dashboards</div>
      </div>
    </div>

    <!-- Script Categories -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Platform Scripts -->
      <div class="glass-panel p-6">
        <h3 class="futuristic-subtitle text-xl mb-4">Platform Scripts</h3>
        <div class="space-y-3">
          <div
            v-for="script in platformScripts"
            :key="script.id"
            class="script-item glass-panel p-4 rounded-lg"
            :class="{ 'script-running': script.status === 'running' }"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <div class="status-indicator" :class="getStatusClass(script.status)"></div>
                <span class="font-medium">{{ script.name }}</span>
              </div>
              <div class="flex space-x-2">
                <button
                  @click="executeScript(script)"
                  :disabled="script.status === 'running'"
                  class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
                  :class="{ 'opacity-50': script.status === 'running' }"
                >
                  {{ script.status === 'running' ? '⏳ Running' : '▶️ Execute' }}
                </button>
                <button
                  @click="viewLogs(script)"
                  class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
                >
                  📋 Logs
                </button>
              </div>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ script.description }}</p>
            <div class="flex items-center justify-between text-xs text-gray-400">
              <span>Last run: {{ script.lastRun }}</span>
              <span>{{ script.language }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Service Scripts -->
      <div class="glass-panel p-6">
        <h3 class="futuristic-subtitle text-xl mb-4">Service Scripts</h3>
        <div class="space-y-3">
          <div
            v-for="script in serviceScripts"
            :key="script.id"
            class="script-item glass-panel p-4 rounded-lg"
            :class="{ 'script-running': script.status === 'running' }"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <div class="status-indicator" :class="getStatusClass(script.status)"></div>
                <span class="font-medium">{{ script.name }}</span>
              </div>
              <div class="flex space-x-2">
                <button
                  @click="executeScript(script)"
                  :disabled="script.status === 'running'"
                  class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
                  :class="{ 'opacity-50': script.status === 'running' }"
                >
                  {{ script.status === 'running' ? '⏳ Running' : '▶️ Execute' }}
                </button>
                <button
                  @click="viewLogs(script)"
                  class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
                >
                  📋 Logs
                </button>
              </div>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ script.description }}</p>
            <div class="flex items-center justify-between text-xs text-gray-400">
              <span>Last run: {{ script.lastRun }}</span>
              <span>{{ script.language }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Execution Logs -->
    <div v-if="selectedScript" class="glass-panel p-6 mb-8">
      <div class="flex items-center justify-between mb-4">
        <h3 class="futuristic-subtitle text-xl">
          Execution Logs: {{ selectedScript.name }}
        </h3>
        <div class="flex space-x-2">
          <button
            @click="clearLogs"
            class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
          >
            🗑️ Clear
          </button>
          <button
            @click="selectedScript = null"
            class="px-3 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
          >
            ✕ Close
          </button>
        </div>
      </div>
      <div class="log-container glass-panel p-4 rounded-lg bg-gray-900 font-mono text-sm max-h-96 overflow-y-auto">
        <div
          v-for="(log, index) in executionLogs"
          :key="index"
          class="log-line"
          :class="getLogClass(log.level)"
        >
          <span class="log-timestamp text-gray-500">[{{ log.timestamp }}]</span>
          <span class="log-level" :class="getLogLevelClass(log.level)">[{{ log.level.toUpperCase() }}]</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
        <div v-if="executionLogs.length === 0" class="text-gray-500 text-center py-8">
          No logs available. Execute a script to see output.
        </div>
      </div>
    </div>

    <!-- Recent Executions -->
    <div class="glass-panel p-6">
      <h3 class="futuristic-subtitle text-xl mb-4">Recent Executions</h3>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-700">
              <th class="text-left py-2">Script</th>
              <th class="text-left py-2">Status</th>
              <th class="text-left py-2">Duration</th>
              <th class="text-left py-2">Exit Code</th>
              <th class="text-left py-2">Started</th>
              <th class="text-left py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="execution in recentExecutions"
              :key="execution.id"
              class="border-b border-gray-800 hover:bg-gray-800 transition-colors"
            >
              <td class="py-2">{{ execution.scriptName }}</td>
              <td class="py-2">
                <span class="status-badge" :class="execution.status">
                  {{ execution.status }}
                </span>
              </td>
              <td class="py-2">{{ execution.duration }}</td>
              <td class="py-2">
                <span :class="execution.exitCode === 0 ? 'text-green-400' : 'text-red-400'">
                  {{ execution.exitCode }}
                </span>
              </td>
              <td class="py-2 text-gray-400">{{ execution.startTime }}</td>
              <td class="py-2">
                <button
                  @click="viewExecutionLogs(execution)"
                  class="px-2 py-1 text-xs glass-panel rounded hover:neon-border transition-all duration-300"
                >
                  View Logs
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Scripts',
  setup() {
    const selectedScript = ref(null)
    const executionLogs = ref([])

    const deploymentStats = ref({ total: 12 })
    const healthStats = ref({ total: 8 })
    const maintenanceStats = ref({ total: 6 })
    const monitoringStats = ref({ total: 4 })

    const platformScripts = ref([
      {
        id: 1,
        name: 'Start Platform',
        description: 'Start all LinkOps platform services',
        language: 'bash',
        status: 'idle',
        lastRun: '2 hours ago'
      },
      {
        id: 2,
        name: 'Deploy Shadow Agents',
        description: 'Deploy all shadow agent microservices',
        language: 'bash',
        status: 'idle',
        lastRun: '4 hours ago'
      },
      {
        id: 3,
        name: 'Platform Health Check',
        description: 'Comprehensive health check of all services',
        language: 'python',
        status: 'running',
        lastRun: 'Running now'
      },
      {
        id: 4,
        name: 'Database Backup',
        description: 'Create backup of PostgreSQL database',
        language: 'bash',
        status: 'idle',
        lastRun: '1 day ago'
      }
    ])

    const serviceScripts = ref([
      {
        id: 5,
        name: 'Restart MLOps Platform',
        description: 'Restart the main MLOps platform service',
        language: 'bash',
        status: 'idle',
        lastRun: '6 hours ago'
      },
      {
        id: 6,
        name: 'Clear Cache',
        description: 'Clear Redis cache and restart services',
        language: 'python',
        status: 'idle',
        lastRun: '12 hours ago'
      },
      {
        id: 7,
        name: 'Update Dependencies',
        description: 'Update Python dependencies across services',
        language: 'bash',
        status: 'idle',
        lastRun: '2 days ago'
      },
      {
        id: 8,
        name: 'Security Scan',
        description: 'Run security vulnerability scan',
        language: 'python',
        status: 'idle',
        lastRun: '1 day ago'
      }
    ])

    const recentExecutions = ref([
      {
        id: 1,
        scriptName: 'Platform Health Check',
        status: 'running',
        duration: '2m 34s',
        exitCode: null,
        startTime: '10:30 AM'
      },
      {
        id: 2,
        scriptName: 'Database Backup',
        status: 'completed',
        duration: '45s',
        exitCode: 0,
        startTime: '09:15 AM'
      },
      {
        id: 3,
        scriptName: 'Security Scan',
        status: 'failed',
        duration: '1m 12s',
        exitCode: 1,
        startTime: '08:45 AM'
      },
      {
        id: 4,
        scriptName: 'Clear Cache',
        status: 'completed',
        duration: '15s',
        exitCode: 0,
        startTime: '08:30 AM'
      }
    ])

    const getStatusClass = (status) => {
      switch (status) {
        case 'running': return 'status-processing'
        case 'completed': return 'status-online'
        case 'failed': return 'status-offline'
        default: return 'status-idle'
      }
    }

    const getLogClass = (level) => {
      switch (level) {
        case 'error': return 'text-red-400'
        case 'warn': return 'text-yellow-400'
        case 'info': return 'text-blue-400'
        case 'success': return 'text-green-400'
        default: return 'text-gray-300'
      }
    }

    const getLogLevelClass = (level) => {
      switch (level) {
        case 'error': return 'text-red-500'
        case 'warn': return 'text-yellow-500'
        case 'info': return 'text-blue-500'
        case 'success': return 'text-green-500'
        default: return 'text-gray-500'
      }
    }

    const executeScript = (script) => {
      script.status = 'running'
      selectedScript.value = script
      
      // Simulate script execution with logs
      executionLogs.value = [
        { timestamp: new Date().toLocaleTimeString(), level: 'info', message: `Starting execution of ${script.name}` },
        { timestamp: new Date().toLocaleTimeString(), level: 'info', message: 'Checking prerequisites...' },
        { timestamp: new Date().toLocaleTimeString(), level: 'success', message: 'Prerequisites validated' },
        { timestamp: new Date().toLocaleTimeString(), level: 'info', message: 'Executing main script logic...' }
      ]

      // Simulate completion after 3 seconds
      setTimeout(() => {
        script.status = 'completed'
        script.lastRun = 'Just now'
        executionLogs.value.push(
          { timestamp: new Date().toLocaleTimeString(), level: 'success', message: 'Script execution completed successfully' },
          { timestamp: new Date().toLocaleTimeString(), level: 'info', message: 'Exit code: 0' }
        )
      }, 3000)
    }

    const viewLogs = (script) => {
      selectedScript.value = script
      executionLogs.value = [
        { timestamp: '10:30:15', level: 'info', message: 'Previous execution logs for ' + script.name },
        { timestamp: '10:30:16', level: 'info', message: 'Checking system status...' },
        { timestamp: '10:30:17', level: 'success', message: 'All systems operational' },
        { timestamp: '10:30:18', level: 'info', message: 'Execution completed' }
      ]
    }

    const viewExecutionLogs = (execution) => {
      selectedScript.value = { name: execution.scriptName }
      executionLogs.value = [
        { timestamp: execution.startTime, level: 'info', message: `Execution logs for ${execution.scriptName}` },
        { timestamp: execution.startTime, level: 'info', message: 'Starting script execution...' },
        { timestamp: execution.startTime, level: execution.status === 'failed' ? 'error' : 'success', 
          message: execution.status === 'failed' ? 'Script execution failed' : 'Script completed successfully' }
      ]
    }

    const clearLogs = () => {
      executionLogs.value = []
    }

    return {
      selectedScript,
      executionLogs,
      deploymentStats,
      healthStats,
      maintenanceStats,
      monitoringStats,
      platformScripts,
      serviceScripts,
      recentExecutions,
      getStatusClass,
      getLogClass,
      getLogLevelClass,
      executeScript,
      viewLogs,
      viewExecutionLogs,
      clearLogs
    }
  }
}
</script>

<style scoped>
@import '../assets/futuristic.css';

.script-running {
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 5px rgba(99, 102, 241, 0.3); }
  50% { box-shadow: 0 0 15px rgba(99, 102, 241, 0.6); }
}

.log-container {
  font-family: 'Courier New', monospace;
}

.log-line {
  margin-bottom: 2px;
  word-break: break-all;
}

.log-timestamp {
  font-size: 11px;
}

.log-level {
  font-weight: bold;
  font-size: 11px;
  margin: 0 8px;
}

.status-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
}

.status-badge.running { background-color: rgba(59, 130, 246, 0.2); color: #3b82f6; }
.status-badge.completed { background-color: rgba(34, 197, 94, 0.2); color: #22c55e; }
.status-badge.failed { background-color: rgba(239, 68, 68, 0.2); color: #ef4444; }

.status-idle { background-color: #6b7280; }
.status-processing { background-color: #3b82f6; animation: pulse 2s infinite; }
.status-online { background-color: #10b981; }
.status-offline { background-color: #ef4444; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style> 