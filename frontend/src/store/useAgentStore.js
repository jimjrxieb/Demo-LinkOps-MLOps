// src/store/useAgentStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAgentStore = defineStore('agent', () => {
  // State
  const agents = ref({
    whis: {
      id: 'whis',
      name: 'Whis',
      status: 'idle', // idle, processing, error, success
      type: 'data-processor',
      lastActivity: null,
      capabilities: ['data-input', 'data-processing', 'api-integration']
    },
    igris: {
      id: 'igris',
      name: 'Igris',
      status: 'idle',
      type: 'logic-engine',
      lastActivity: null,
      capabilities: ['logic-processing', 'decision-making', 'workflow-orchestration']
    },
    katie: {
      id: 'katie',
      name: 'Katie',
      status: 'idle',
      type: 'sanitization-engine',
      lastActivity: null,
      capabilities: ['data-sanitization', 'validation', 'quality-control']
    }
  })

  const activeAgent = ref(null)
  const agentLogs = ref([])

  // Getters
  const getAgentById = computed(() => {
    return (id) => agents.value[id] || null
  })

  const getActiveAgents = computed(() => {
    return Object.values(agents.value).filter(agent => agent.status === 'processing')
  })

  const getAgentStatus = computed(() => {
    return (id) => agents.value[id]?.status || 'unknown'
  })

  // Actions
  const setAgentStatus = (agentId, status) => {
    if (agents.value[agentId]) {
      agents.value[agentId].status = status
      agents.value[agentId].lastActivity = new Date().toISOString()
    }
  }

  const activateAgent = (agentId) => {
    activeAgent.value = agentId
    setAgentStatus(agentId, 'processing')
  }

  const deactivateAgent = (agentId) => {
    if (activeAgent.value === agentId) {
      activeAgent.value = null
    }
    setAgentStatus(agentId, 'idle')
  }

  const addAgentLog = (agentId, message, level = 'info') => {
    agentLogs.value.push({
      id: Date.now(),
      agentId,
      message,
      level,
      timestamp: new Date().toISOString()
    })
  }

  const clearAgentLogs = () => {
    agentLogs.value = []
  }

  return {
    // State
    agents,
    activeAgent,
    agentLogs,
    
    // Getters
    getAgentById,
    getActiveAgents,
    getAgentStatus,
    
    // Actions
    setAgentStatus,
    activateAgent,
    deactivateAgent,
    addAgentLog,
    clearAgentLogs
  }
}) 