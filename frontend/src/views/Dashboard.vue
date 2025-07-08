<template>
  <div class="dashboard-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">Command Dashboard</h1>
      <p class="text-gray-300">LinkOps MLOps Platform Control Center</p>
    </div>

    <!-- System Overview -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-green-400 mb-2">{{ systemStatus.activeServices }}</div>
        <div class="text-sm text-gray-300">Active Services</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-blue-400 mb-2">{{ systemStatus.totalOrbs }}</div>
        <div class="text-sm text-gray-300">Generated Orbs</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-purple-400 mb-2">{{ systemStatus.totalRunes }}</div>
        <div class="text-sm text-gray-300">Generated Runes</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-yellow-400 mb-2">{{ systemStatus.uptime }}</div>
        <div class="text-sm text-gray-300">System Uptime</div>
      </div>
    </div>

    <!-- Service Status Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- MLOps Services -->
      <div class="glass-panel p-6">
        <h3 class="futuristic-subtitle text-xl mb-4">MLOps Services</h3>
        <div class="space-y-3">
          <div v-for="service in mlopsServices" :key="service.name" class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="status-indicator" :class="service.status === 'online' ? 'status-online' : 'status-offline'"></div>
              <span class="text-sm">{{ service.name }}</span>
            </div>
            <div class="text-xs text-gray-400">{{ service.port }}</div>
          </div>
        </div>
      </div>

      <!-- Shadow Agents -->
      <div class="glass-panel p-6">
        <h3 class="futuristic-subtitle text-xl mb-4">Shadow Agents</h3>
        <div class="space-y-3">
          <div v-for="agent in shadowAgents" :key="agent.name" class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="status-indicator" :class="agent.status === 'online' ? 'status-online' : 'status-offline'"></div>
              <span class="text-sm">{{ agent.name }}</span>
            </div>
            <div class="text-xs text-gray-400">{{ agent.port }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="glass-panel p-6">
      <h3 class="futuristic-subtitle text-xl mb-4">Quick Actions</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <router-link to="/whis" class="glass-panel p-4 rounded-lg hover:neon-border transition-all duration-300 text-center">
          <div class="text-2xl mb-2">🧠</div>
          <div class="text-sm">Whis Console</div>
        </router-link>
        <router-link to="/orbs" class="glass-panel p-4 rounded-lg hover:neon-border transition-all duration-300 text-center">
          <div class="text-2xl mb-2">📘</div>
          <div class="text-sm">Browse Orbs</div>
        </router-link>
        <router-link to="/runes" class="glass-panel p-4 rounded-lg hover:neon-border transition-all duration-300 text-center">
          <div class="text-2xl mb-2">🧪</div>
          <div class="text-sm">Browse Runes</div>
        </router-link>
        <router-link to="/audit" class="glass-panel p-4 rounded-lg hover:neon-border transition-all duration-300 text-center">
          <div class="text-2xl mb-2">🔍</div>
          <div class="text-sm">Audit Repo</div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Dashboard',
  setup() {
    const systemStatus = ref({
      activeServices: 18,
      totalOrbs: 47,
      totalRunes: 23,
      uptime: '12h 34m'
    })

    const mlopsServices = ref([
      { name: 'MLOps Platform', status: 'online', port: ':8000' },
      { name: 'Whis Data Input', status: 'online', port: ':8001' },
      { name: 'Whis Sanitize', status: 'online', port: ':8002' },
      { name: 'Whis Smithing', status: 'online', port: ':8003' },
      { name: 'Whis Enhance', status: 'online', port: ':8004' },
      { name: 'Whis Logic', status: 'online', port: ':8005' },
      { name: 'Whis Webscraper', status: 'online', port: ':8006' },
      { name: 'Audit Assess', status: 'online', port: ':8007' },
      { name: 'Audit Migrate', status: 'online', port: ':8008' },
      { name: 'MLOps Utils', status: 'online', port: ':8009' }
    ])

    const shadowAgents = ref([
      { name: 'Jimmie Logic', status: 'online', port: ':8010' },
      { name: 'Ficknury Evaluator', status: 'online', port: ':8011' },
      { name: 'Audit Logic', status: 'online', port: ':8012' },
      { name: 'AuditGuard Logic', status: 'online', port: ':8013' },
      { name: 'Kubernetes Specialist', status: 'online', port: ':8014' },
      { name: 'ML Data Scientist', status: 'online', port: ':8015' },
      { name: 'Platform Engineer', status: 'online', port: ':8016' },
      { name: 'DevOps Engineer', status: 'online', port: ':8017' }
    ])

    return {
      systemStatus,
      mlopsServices,
      shadowAgents
    }
  }
}
</script>

<style scoped>
@import '../assets/futuristic.css';
</style> 