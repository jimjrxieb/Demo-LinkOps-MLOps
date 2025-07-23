<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">AI Agent Builder</h1>
            <p class="mt-1 text-sm text-gray-500">
              Create custom AI agents with drag-and-drop workflow builder
            </p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              @click="saveWorkflow"
              :disabled="!canSave"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Save Workflow
            </button>
            <button
              @click="createAgent"
              :disabled="!canCreate"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Build Agent
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Toolbox Panel -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Toolbox</h2>
            
            <!-- Agent Types -->
            <div class="mb-6">
              <h3 class="text-sm font-medium text-gray-700 mb-3">Agent Types</h3>
              <div class="space-y-2">
                <div
                  v-for="type in agentTypes"
                  :key="type.value"
                  @click="selectAgentType(type.value)"
                  :class="[
                    'p-3 border rounded-lg cursor-pointer transition-colors',
                    selectedAgentType === type.value
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  ]"
                >
                  <div class="flex items-center">
                    <div class="flex-shrink-0">
                      <component :is="type.icon" class="h-5 w-5 text-gray-400" />
                    </div>
                    <div class="ml-3">
                      <p class="text-sm font-medium text-gray-900">{{ type.label }}</p>
                      <p class="text-xs text-gray-500">{{ type.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Available Tools -->
            <div class="mb-6">
              <h3 class="text-sm font-medium text-gray-700 mb-3">Available Tools</h3>
              <div class="space-y-2">
                <div
                  v-for="tool in availableTools"
                  :key="tool.id"
                  @click="addTool(tool)"
                  class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:border-gray-300 transition-colors"
                >
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ tool.name }}</p>
                      <p class="text-xs text-gray-500">{{ tool.description }}</p>
                    </div>
                    <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Security Level -->
            <div class="mb-6">
              <h3 class="text-sm font-medium text-gray-700 mb-3">Security Level</h3>
              <select
                v-model="securityLevel"
                class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
              >
                <option value="low">Low - Basic validation</option>
                <option value="medium">Medium - Enhanced security</option>
                <option value="high">High - Maximum security</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Workflow Canvas -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-lg font-medium text-gray-900">Workflow Canvas</h2>
              <button
                @click="clearCanvas"
                class="text-sm text-red-600 hover:text-red-500"
              >
                Clear Canvas
              </button>
            </div>
            
            <!-- Agent Configuration -->
            <div class="mb-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Agent Name
                </label>
                <input
                  v-model="agentName"
                  type="text"
                  placeholder="Enter agent name"
                  class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  v-model="agentDescription"
                  rows="3"
                  placeholder="Describe what this agent does"
                  class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                ></textarea>
              </div>
            </div>

            <!-- Workflow Steps -->
            <div class="space-y-4">
              <h3 class="text-sm font-medium text-gray-700">Workflow Steps</h3>
              
              <div
                v-for="(step, index) in workflowSteps"
                :key="index"
                class="p-4 border border-gray-200 rounded-lg"
              >
                <div class="flex items-center justify-between mb-3">
                  <h4 class="text-sm font-medium text-gray-900">Step {{ index + 1 }}</h4>
                  <button
                    @click="removeStep(index)"
                    class="text-red-600 hover:text-red-500"
                  >
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
                
                <div class="space-y-3">
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">
                      Action Type
                    </label>
                    <select
                      v-model="step.action"
                      class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-xs"
                    >
                      <option value="data_processing">Data Processing</option>
                      <option value="file_operation">File Operation</option>
                      <option value="network_request">Network Request</option>
                      <option value="command_execution">Command Execution</option>
                      <option value="validation">Validation</option>
                      <option value="notification">Notification</option>
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">
                      Parameters
                    </label>
                    <textarea
                      v-model="step.parameters"
                      rows="2"
                      placeholder="Enter parameters (JSON format)"
                      class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-xs"
                    ></textarea>
                  </div>
                  
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">
                      Error Handling
                    </label>
                    <select
                      v-model="step.errorHandling"
                      class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-xs"
                    >
                      <option value="retry">Retry</option>
                      <option value="skip">Skip</option>
                      <option value="stop">Stop</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <button
                @click="addStep"
                class="w-full p-3 border-2 border-dashed border-gray-300 rounded-lg text-sm text-gray-600 hover:border-gray-400 hover:text-gray-700 transition-colors"
              >
                + Add Step
              </button>
            </div>
          </div>
        </div>

        <!-- Preview & Results Panel -->
        <div class="lg:col-span-1">
          <div class="space-y-6">
            <!-- Agent Preview -->
            <div class="bg-white rounded-lg shadow p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Agent Preview</h3>
              
              <div v-if="agentName" class="space-y-3">
                <div>
                  <span class="text-xs font-medium text-gray-500">Name:</span>
                  <p class="text-sm text-gray-900">{{ agentName }}</p>
                </div>
                
                <div v-if="agentDescription">
                  <span class="text-xs font-medium text-gray-500">Description:</span>
                  <p class="text-sm text-gray-900">{{ agentDescription }}</p>
                </div>
                
                <div>
                  <span class="text-xs font-medium text-gray-500">Type:</span>
                  <p class="text-sm text-gray-900">{{ getAgentTypeLabel(selectedAgentType) }}</p>
                </div>
                
                <div>
                  <span class="text-xs font-medium text-gray-500">Security:</span>
                  <p class="text-sm text-gray-900 capitalize">{{ securityLevel }}</p>
                </div>
                
                <div>
                  <span class="text-xs font-medium text-gray-500">Steps:</span>
                  <p class="text-sm text-gray-900">{{ workflowSteps.length }}</p>
                </div>
              </div>
              
              <div v-else class="text-center py-8 text-gray-500">
                Configure your agent to see preview
              </div>
            </div>

            <!-- Generation Results -->
            <div v-if="generationResult" class="bg-white rounded-lg shadow p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Generation Result</h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-gray-700">Status:</span>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Success
                  </span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-gray-700">Agent Path:</span>
                  <span class="text-sm text-gray-900 truncate">{{ generationResult.path }}</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-gray-700">Generated At:</span>
                  <span class="text-sm text-gray-900">{{ formatDate(generationResult.timestamp) }}</span>
                </div>
                <div class="mt-4">
                  <button
                    @click="downloadAgent"
                    class="w-full px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  >
                    Download Agent
                  </button>
                </div>
              </div>
            </div>

            <!-- Error Display -->
            <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800">Error</h3>
                  <div class="mt-2 text-sm text-red-700">
                    {{ error }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
            <svg class="animate-spin h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900 mt-4">Building Agent</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              Please wait while we build your AI agent...
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

// Reactive data
const agentName = ref('')
const agentDescription = ref('')
const selectedAgentType = ref('taskbot')
const securityLevel = ref('medium')
const workflowSteps = ref([])
const generationResult = ref(null)
const error = ref(null)
const isLoading = ref(false)

// Agent types
const agentTypes = [
  {
    value: 'taskbot',
    label: 'TaskBot',
    description: 'Execute specific tasks and workflows',
    icon: 'TaskIcon'
  },
  {
    value: 'commandbot',
    label: 'CommandBot',
    description: 'Execute system commands safely',
    icon: 'CommandIcon'
  },
  {
    value: 'assistant',
    label: 'Assistant',
    description: 'Conversational AI assistant',
    icon: 'AssistantIcon'
  },
  {
    value: 'workflow',
    label: 'Workflow',
    description: 'Orchestrate complex workflows',
    icon: 'WorkflowIcon'
  }
]

// Available tools
const availableTools = [
  {
    id: 'data_processing',
    name: 'Data Processing',
    description: 'Process and transform data'
  },
  {
    id: 'file_operations',
    name: 'File Operations',
    description: 'Read, write, and manage files'
  },
  {
    id: 'network_requests',
    name: 'Network Requests',
    description: 'Make HTTP requests to APIs'
  },
  {
    id: 'command_execution',
    name: 'Command Execution',
    description: 'Execute system commands'
  },
  {
    id: 'validation',
    name: 'Validation',
    description: 'Validate inputs and outputs'
  },
  {
    id: 'notification',
    name: 'Notification',
    description: 'Send notifications and alerts'
  }
]

// Computed properties
const canSave = computed(() => {
  return agentName.value.trim() && workflowSteps.value.length > 0
})

const canCreate = computed(() => {
  return canSave.value && selectedAgentType.value
})

// Methods
function selectAgentType(type) {
  selectedAgentType.value = type
}

function addTool(tool) {
  // Add tool to workflow steps
  addStep()
  const lastStep = workflowSteps.value[workflowSteps.value.length - 1]
  lastStep.action = tool.id
  lastStep.parameters = JSON.stringify({ tool: tool.name }, null, 2)
}

function addStep() {
  workflowSteps.value.push({
    action: 'data_processing',
    parameters: '',
    errorHandling: 'retry'
  })
}

function removeStep(index) {
  workflowSteps.value.splice(index, 1)
}

function clearCanvas() {
  workflowSteps.value = []
  error.value = null
  generationResult.value = null
}

function getAgentTypeLabel(type) {
  const agentType = agentTypes.find(t => t.value === type)
  return agentType ? agentType.label : type
}

async function saveWorkflow() {
  // Save workflow configuration
  try {
    const workflow = {
      name: agentName.value,
      description: agentDescription.value,
      type: selectedAgentType.value,
      security_level: securityLevel.value,
      steps: workflowSteps.value
    }
    
    localStorage.setItem('saved_workflow', JSON.stringify(workflow))
    // You could also save to backend here
  } catch (err) {
    console.error('Error saving workflow:', err)
    error.value = 'Failed to save workflow'
  }
}

async function createAgent() {
  if (!canCreate.value) return
  
  isLoading.value = true
  error.value = null
  
  try {
    const agentConfig = {
      agent_name: agentName.value,
      agent_type: selectedAgentType.value,
      description: agentDescription.value,
      security_level: securityLevel.value,
      capabilities: workflowSteps.value.map(step => step.action),
      workflow_steps: workflowSteps.value,
      tools: availableTools.filter(tool => 
        workflowSteps.value.some(step => step.action === tool.id)
      ).map(tool => tool.name)
    }
    
    const response = await axios.post('http://localhost:8003/generate-agent', agentConfig)
    generationResult.value = response.data
  } catch (err) {
    console.error('Error creating agent:', err)
    error.value = err.response?.data?.detail || 'Failed to create agent. Please try again.'
  } finally {
    isLoading.value = false
  }
}

function downloadAgent() {
  if (generationResult.value?.path) {
    const link = document.createElement('a')
    link.href = `http://localhost:8003/download/${generationResult.value.path}`
    link.download = `${agentName.value}_agent.py`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleString()
}

// Icons (you can replace these with actual icon components)
const TaskIcon = {
  template: '<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>'
}

const CommandIcon = {
  template: '<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>'
}

const AssistantIcon = {
  template: '<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>'
}

const WorkflowIcon = {
  template: '<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>'
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style> 