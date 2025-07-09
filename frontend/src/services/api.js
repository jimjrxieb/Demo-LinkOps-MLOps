import axios from 'axios'

// Create axios instance with default config
const api = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Environment-based API URLs
const MLOPS_PLATFORM_URL = import.meta.env.VITE_MLOPS_PLATFORM_URL || 'http://localhost:8000'
const AUDIT_ASSESS_URL = import.meta.env.VITE_AUDIT_ASSESS_URL || 'http://localhost:8003'
const WHIS_DATA_INPUT_URL = import.meta.env.VITE_WHIS_DATA_INPUT_URL || 'http://localhost:8004'
const WHIS_ENHANCE_URL = import.meta.env.VITE_WHIS_ENHANCE_URL || 'http://localhost:8006'

// MLOps Platform API
export const mlopsPlatformAPI = axios.create({
  baseURL: MLOPS_PLATFORM_URL,
  timeout: 15000,
})

// Audit Assess API
export const auditAssessAPI = axios.create({
  baseURL: AUDIT_ASSESS_URL,
  timeout: 30000, // Longer timeout for repository scanning
})

// Whis Data Input API
export const whisDataInputAPI = axios.create({
  baseURL: WHIS_DATA_INPUT_URL,
  timeout: 15000,
})

// Whis Enhance API
export const whisEnhanceAPI = axios.create({
  baseURL: WHIS_ENHANCE_URL,
  timeout: 15000,
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    // Error log removed
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Error log removed
    
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Handle unauthorized
      // Development log removed
    } else if (error.response?.status === 503) {
      // Handle service unavailable
      // Development log removed
    }
    
    return Promise.reject(error)
  }
)

// Health check functions
export const healthChecks = {
  mlopsPlatform: () => mlopsPlatformAPI.get('/'),
  auditAssess: () => auditAssessAPI.get('/health'),
  whisDataInput: () => whisDataInputAPI.get('/health'),
  whisEnhance: () => whisEnhanceAPI.get('/health'),
}

// MLOps Platform API functions
export const mlopsPlatformService = {
  // Tasks
  getTasks: () => mlopsPlatformAPI.get('/tasks/'),
  createTask: (taskData) => mlopsPlatformAPI.post('/tasks/', taskData),
  updateTask: (taskId, taskData) => mlopsPlatformAPI.put(`/tasks/${taskId}`, taskData),
  deleteTask: (taskId) => mlopsPlatformAPI.delete(`/tasks/${taskId}`),
  getTaskStats: () => mlopsPlatformAPI.get('/tasks/stats/summary'),

  // Scripts
  getScripts: () => mlopsPlatformAPI.get('/scripts/'),
  createScript: (scriptData) => mlopsPlatformAPI.post('/scripts/', scriptData),
  updateScript: (scriptId, scriptData) => mlopsPlatformAPI.put(`/scripts/${scriptId}`, scriptData),
  deleteScript: (scriptId) => mlopsPlatformAPI.delete(`/scripts/${scriptId}`),
  executeScript: (scriptId) => mlopsPlatformAPI.post(`/scripts/${scriptId}/execute`),
  getScriptTemplates: (category) => mlopsPlatformAPI.get(`/scripts/templates/${category}`),
  getPopularScripts: () => mlopsPlatformAPI.get('/scripts/stats/popular'),

  // Workflows
  getWorkflows: () => mlopsPlatformAPI.get('/workflows/'),
  createWorkflow: (workflowData) => mlopsPlatformAPI.post('/workflows/', workflowData),
  updateWorkflow: (workflowId, workflowData) => mlopsPlatformAPI.put(`/workflows/${workflowId}`, workflowData),
  deleteWorkflow: (workflowId) => mlopsPlatformAPI.delete(`/workflows/${workflowId}`),
  executeWorkflow: (workflowId) => mlopsPlatformAPI.post(`/workflows/${workflowId}/execute`),
  getWorkflowTemplates: (category) => mlopsPlatformAPI.get(`/workflows/templates/${category}`),
  getWorkflowStats: () => mlopsPlatformAPI.get('/workflows/stats/execution'),

  // Orbs
  getOrbs: () => mlopsPlatformAPI.get('/orbs/'),
  createOrb: (orbData) => mlopsPlatformAPI.post('/orbs/', orbData),
  updateOrb: (orbId, orbData) => mlopsPlatformAPI.put(`/orbs/${orbId}`, orbData),
  deleteOrb: (orbId) => mlopsPlatformAPI.delete(`/orbs/${orbId}`),
  useOrb: (orbId) => mlopsPlatformAPI.post(`/orbs/${orbId}/use`),
  rateOrb: (orbId, rating) => mlopsPlatformAPI.post(`/orbs/${orbId}/rate`, { rating }),
  getOrbTemplates: (category) => mlopsPlatformAPI.get(`/orbs/templates/${category}`),
  getPopularOrbs: () => mlopsPlatformAPI.get('/orbs/stats/popular'),
  getHighestRatedOrbs: () => mlopsPlatformAPI.get('/orbs/stats/highest_rated'),

  // Runes
  getRunes: () => mlopsPlatformAPI.get('/runes/'),
  createRune: (runeData) => mlopsPlatformAPI.post('/runes/', runeData),
  updateRune: (runeId, runeData) => mlopsPlatformAPI.put(`/runes/${runeId}`, runeData),
  deleteRune: (runeId) => mlopsPlatformAPI.delete(`/runes/${runeId}`),
  executeRune: (runeId) => mlopsPlatformAPI.post(`/runes/${runeId}/execute`),
  provideRuneFeedback: (runeId, success, feedback) => mlopsPlatformAPI.post(`/runes/${runeId}/feedback`, { success, feedback }),
  getRuneTemplates: (category) => mlopsPlatformAPI.get(`/runes/templates/${category}`),
  getMostSuccessfulRunes: () => mlopsPlatformAPI.get('/runes/stats/most_successful'),
  getMostUsedRunes: () => mlopsPlatformAPI.get('/runes/stats/most_used'),

  // Digest
  getDigestEntries: (params) => mlopsPlatformAPI.get('/digest/', { params }),
  createDigestEntry: (entryData) => mlopsPlatformAPI.post('/digest/', entryData),
  updateDigestEntry: (entryId, entryData) => mlopsPlatformAPI.put(`/digest/${entryId}`, entryData),
  deleteDigestEntry: (entryId) => mlopsPlatformAPI.delete(`/digest/${entryId}`),
  getTodaySummary: () => mlopsPlatformAPI.get('/digest/today/summary'),
  getWeeklyStats: () => mlopsPlatformAPI.get('/digest/stats/weekly'),
  getMonthlyStats: () => mlopsPlatformAPI.get('/digest/stats/monthly'),
  exportDigest: (startDate, endDate) => mlopsPlatformAPI.post('/digest/export', { start_date: startDate, end_date: endDate }),
  getProductivityInsights: () => mlopsPlatformAPI.get('/digest/insights/productivity'),
}

// Legacy service mappings for backward compatibility
export const jamesService = {
  activateShadowArmy: () => mlopsPlatformService.createTask({
    title: "Activate Shadow Army",
    description: "Activate all shadow agents for coordinated operations",
    category: "mlops",
    priority: "high"
  }),
  submitTask: (taskData) => mlopsPlatformService.createTask(taskData),
  askQuestion: (question) => mlopsPlatformService.createTask({
    title: "Question",
    description: question,
    category: "mlops",
    priority: "medium"
  }),
  submitInfoDump: (data) => mlopsPlatformService.createTask({
    title: "Info Dump",
    description: JSON.stringify(data),
    category: "mlops",
    priority: "medium"
  }),
  extractFromImage: (imageData) => mlopsPlatformService.createTask({
    title: "Image Extraction",
    description: `Extract information from image: ${JSON.stringify(imageData)}`,
    category: "mlops",
    priority: "medium"
  }),
  generateSolution: (problemData) => mlopsPlatformService.createTask({
    title: "Generate Solution",
    description: JSON.stringify(problemData),
    category: "mlops",
    priority: "high"
  }),
  voiceInteraction: (audioData) => mlopsPlatformService.createTask({
    title: "Voice Interaction",
    description: `Process voice input: ${JSON.stringify(audioData)}`,
    category: "mlops",
    priority: "medium"
  }),
  describeImage: (imageData) => mlopsPlatformService.createTask({
    title: "Describe Image",
    description: `Generate image description: ${JSON.stringify(imageData)}`,
    category: "mlops",
    priority: "medium"
  }),
}

export const whisService = {
  getTrainingQueue: () => mlopsPlatformService.getTasks(),
  getDigest: (date) => mlopsPlatformService.getDigestEntries({ date }),
  getApprovalQueue: () => mlopsPlatformService.getTasks(),
  approveItem: (type, id) => mlopsPlatformService.updateTask(id, { status: "completed" }),
  rejectItem: (type, id) => mlopsPlatformService.updateTask(id, { status: "blocked" }),
  getAnalytics: () => mlopsPlatformService.getTaskStats(),
  generateOrbs: (data) => mlopsPlatformService.createOrb(data),
  generateRunes: (data) => mlopsPlatformAPI.post('/runes/', data),
  getSmithingLog: () => mlopsPlatformService.getRunes(),
}

export const igrisService = {
  getInfrastructureStatus: () => mlopsPlatformService.getWorkflows(),
  analyzeCosts: () => mlopsPlatformService.getTaskStats(),
  getSecurityAudit: () => mlopsPlatformService.getTasks(),
  deployInfrastructure: (config) => mlopsPlatformService.createWorkflow(config),
  getCapabilities: () => mlopsPlatformService.getScripts(),
  getEnhancedRunes: () => mlopsPlatformService.getRunes(),
  runSimulation: (params) => mlopsPlatformService.createWorkflow(params),
  getAgentStats: () => mlopsPlatformService.getTaskStats(),
}

export const katieService = {
  getKubernetesStatus: () => mlopsPlatformService.getWorkflows(),
  getTasksHandled: () => mlopsPlatformService.getTasks(),
  getYAMLVisualizer: () => mlopsPlatformService.getOrbs(),
  getAgentLogicTree: () => mlopsPlatformService.getRunes(),
  getHelmCharts: () => mlopsPlatformService.getOrbs(),
  getTroubleshootingLog: () => mlopsPlatformService.getDigestEntries(),
  scaleDeployment: (params) => mlopsPlatformService.createScript({
    name: "Scale Deployment",
    description: "Scale Kubernetes deployment",
    category: "kubernetes",
    content: `kubectl scale deployment ${params.deployment} --replicas=${params.replicas}`,
    language: "bash"
  }),
  describeResource: (params) => mlopsPlatformService.createScript({
    name: "Describe Resource",
    description: "Describe Kubernetes resource",
    category: "kubernetes",
    content: `kubectl describe ${params.resource} ${params.name}`,
    language: "bash"
  }),
  getLogs: (params) => mlopsPlatformService.createScript({
    name: "Get Logs",
    description: "Get Kubernetes logs",
    category: "kubernetes",
    content: `kubectl logs ${params.pod} --tail=${params.lines || 100}`,
    language: "bash"
  }),
  patchResource: (params) => mlopsPlatformService.createScript({
    name: "Patch Resource",
    description: "Patch Kubernetes resource",
    category: "kubernetes",
    content: `kubectl patch ${params.resource} ${params.name} -p '${JSON.stringify(params.patch)}'`,
    language: "bash"
  }),
}

export const ficknuryService = {
  getIncomingTasks: () => mlopsPlatformService.getTasks(),
  getFeasibilityRanking: () => mlopsPlatformService.getTaskStats(),
  getAgentAssignmentStats: () => mlopsPlatformService.getTaskStats(),
  getDecisionMatrix: () => mlopsPlatformService.getWorkflows(),
  getProcessingQueue: () => mlopsPlatformService.getTasks(),
  getFallbackAnalysis: () => mlopsPlatformService.getDigestEntries(),
  evaluateTask: (taskData) => mlopsPlatformService.createTask(taskData),
  routeTask: (taskData) => mlopsPlatformService.createTask(taskData),
}

export const dataCollectorService = {
  collectData: (data) => mlopsPlatformService.createTask({
    title: "Data Collection",
    description: JSON.stringify(data),
    category: "mlops",
    priority: "medium"
  }),
  getCollectionStats: () => mlopsPlatformService.getTaskStats(),
  submitYouTubeData: (url) => mlopsPlatformService.createTask({
    title: "YouTube Data",
    description: `Process YouTube URL: ${url}`,
    category: "mlops",
    priority: "medium"
  }),
  submitManualTask: (taskData) => mlopsPlatformService.createTask(taskData),
  downloadYouTubeTranscript: (data) => mlopsPlatformService.createTask({
    title: "YouTube Transcript",
    description: JSON.stringify(data),
    category: "mlops",
    priority: "medium"
  }),
}

export const sanitizerService = {
  sanitizeData: (data) => mlopsPlatformService.createTask({
    title: "Data Sanitization",
    description: JSON.stringify(data),
    category: "mlops",
    priority: "medium"
  }),
  getSanitizationStats: () => mlopsPlatformService.getTaskStats(),
  getDataLake: () => mlopsPlatformService.getDigestEntries(),
  getSanitizedInputs: () => mlopsPlatformService.getTasks(),
}

// Audit Assess API functions
export const auditAssessService = {
  // Repository scanning
  scanRepository: (repoData) => auditAssessAPI.post('/scan/repo/', repoData),
  auditRepository: (repoData) => auditAssessAPI.post('/scan/audit', repoData),
  getSuggestions: () => auditAssessAPI.get('/scan/suggestions/'),
  getScaffoldPlan: () => auditAssessAPI.get('/scan/scaffold-plan/'),
  
  // Health and status
  getHealth: () => auditAssessAPI.get('/health'),
}

// Whis Data Input API functions
export const whisDataInputService = {
  // YouTube data collection
  submitYouTubeData: (url) => whisDataInputAPI.post('/youtube', { url }),
  downloadTranscript: (data) => whisDataInputAPI.post('/youtube/transcript', data),
  
  // Q&A data
  submitQAData: (data) => whisDataInputAPI.post('/qna', data),
  
  // CSV data
  submitCSVData: (data) => whisDataInputAPI.post('/csv', data),
  
  // Manual task submission
  submitManualTask: (taskData) => whisDataInputAPI.post('/manual', taskData),
  
  // Health and status
  getHealth: () => whisDataInputAPI.get('/health'),
}

// Whis Enhance API functions
export const whisEnhanceService = {
  // Content enhancement
  enhanceContent: (contentData) => whisEnhanceAPI.post('/enhance', contentData),
  enhanceBatch: (batchData) => whisEnhanceAPI.post('/enhance/batch', batchData),
  
  // Quality assessment
  getQualityScore: (contentData) => whisEnhanceAPI.get('/enhance/quality/score', { params: contentData }),
  analyzeMetadata: (contentData) => whisEnhanceAPI.get('/enhance/metadata/analyze', { params: contentData }),
  
  // Loopback refinement
  triggerLoopback: (threshold = 2) => whisEnhanceAPI.post('/loopback', { threshold }),
  getLoopbackStats: () => whisEnhanceAPI.get('/loopback/stats'),
  
  // Health and status
  getHealth: () => whisEnhanceAPI.get('/health'),
}

export default api 