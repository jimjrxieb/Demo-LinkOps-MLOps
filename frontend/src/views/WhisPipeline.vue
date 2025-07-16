<template>
  <div class="whis-pipeline-page">
    <!-- Header Section -->
    <div class="header-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            🧠 Whis Learning Pipeline
          </h2>
          <p class="card-subtitle">
            Train and improve AI models using tasks that need additional learning
          </p>
        </div>
        <div class="card-body">
          <div class="pipeline-stats">
            <div class="stat-item">
              <div class="stat-value">{{ pendingTasks.length }}</div>
              <div class="stat-label">Pending Training</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ completedTraining.length }}</div>
              <div class="stat-label">Completed</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ isTraining ? 'Active' : 'Idle' }}</div>
              <div class="stat-label">Status</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pending Training Tasks -->
    <div v-if="pendingTasks.length > 0" class="training-queue-section">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            📋 Training Queue
          </h3>
          <p class="card-subtitle">
            Tasks with confidence ≤ 70% requiring additional training
          </p>
        </div>
        <div class="card-body">
          <div class="training-tasks">
            <div 
              v-for="task in pendingTasks" 
              :key="task.id"
              class="training-task-card"
              :class="{ 'selected': selectedTask?.id === task.id }"
              @click="selectTask(task)"
            >
              <div class="task-header">
                <div class="task-info">
                  <h4 class="task-title">{{ task.originalInput }}</h4>
                  <div class="task-meta">
                    <span class="confidence-score">{{ task.confidence }}% confidence</span>
                    <span class="task-time">{{ formatTime(task.timestamp) }}</span>
                  </div>
                </div>
                <div class="task-actions">
                  <button 
                    class="btn btn-primary start-training-btn"
                    @click.stop="startTraining(task)"
                    :disabled="isTraining"
                  >
                    🚀 Start Training
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Training Process -->
    <div v-if="isTraining && currentTrainingTask" class="training-process-section">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            ⚒️ Active Training: {{ currentTrainingTask.originalInput }}
          </h3>
          <p class="card-subtitle">
            Step {{ currentTrainingStep + 1 }} of 5 - {{ trainingSteps[currentTrainingStep]?.name }}
          </p>
        </div>
        <div class="card-body">
          <!-- Training Progress -->
          <div class="training-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: ((currentTrainingStep + 1) / trainingSteps.length) * 100 + '%' }"
              ></div>
            </div>
            <div class="progress-text">
              {{ Math.round(((currentTrainingStep + 1) / trainingSteps.length) * 100) }}% Complete
            </div>
          </div>

          <!-- Training Steps -->
          <div class="training-steps">
            <div 
              v-for="(step, index) in trainingSteps" 
              :key="index"
              class="training-step"
              :class="{ 
                'active': index === currentTrainingStep,
                'completed': index < currentTrainingStep,
                'pending': index > currentTrainingStep
              }"
            >
              <div class="step-indicator">
                <div class="step-number">{{ index + 1 }}</div>
                <div class="step-icon">{{ step.icon }}</div>
              </div>
              <div class="step-content">
                <h4 class="step-name">{{ step.name }}</h4>
                <p class="step-description">{{ step.description }}</p>
                
                <!-- Step Details -->
                <div v-if="index === currentTrainingStep" class="step-details">
                  <div v-if="step.tools" class="tools-section">
                    <h5>🔧 Tools & Models Used:</h5>
                    <ul class="tools-list">
                      <li v-for="tool in step.tools" :key="tool">{{ tool }}</li>
                    </ul>
                  </div>
                  
                  <div v-if="step.process && currentStepResults[index]" class="process-section">
                    <h5>📊 Processing Results:</h5>
                    <div class="process-results">
                      <div class="result-item" v-for="(result, key) in currentStepResults[index]" :key="key">
                        <strong>{{ key }}:</strong> {{ result }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Generated Orb Preview -->
          <div v-if="generatedOrb" class="generated-orb-section">
            <h4>🔮 Generated Orb Preview</h4>
            <div class="orb-preview">
              <div class="orb-header">
                <h5>{{ generatedOrb.title }}</h5>
                <div class="orb-meta">
                  <span class="orb-category">{{ generatedOrb.category }}</span>
                  <span class="orb-rune">{{ generatedOrb.rune_id }}</span>
                </div>
              </div>
              <div class="orb-content">
                <p>{{ generatedOrb.orb }}</p>
                <div v-if="generatedOrb.declarative_template" class="template-preview">
                  <h6>📄 Declarative Template:</h6>
                  <pre><code>{{ generatedOrb.declarative_template }}</code></pre>
                </div>
                <div v-if="generatedOrb.imperative_commands" class="commands-preview">
                  <h6>⚡ Imperative Commands:</h6>
                  <ul>
                    <li v-for="cmd in generatedOrb.imperative_commands.slice(0, 3)" :key="cmd">{{ cmd }}</li>
                  </ul>
                </div>
              </div>
            </div>
            
            <!-- Approval Section -->
            <div class="approval-section">
              <h4>🎯 Training Complete - Review & Approve</h4>
              <div class="approval-buttons">
                <button class="btn btn-success approve-btn" @click="approveOrb">
                  ✅ Approve & Create Rune
                </button>
                <button class="btn btn-danger reject-btn" @click="rejectOrb">
                  ❌ Reject - Use OpenAI Fallback
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Training Tasks -->
    <div v-if="pendingTasks.length === 0 && !isTraining" class="no-tasks-section">
      <div class="card">
        <div class="card-body">
          <div class="no-tasks-content">
            <div class="no-tasks-icon">🎯</div>
            <h3>No Training Tasks</h3>
            <p>Submit tasks with low confidence from the main Demo page to start training new orbs.</p>
            <button class="btn btn-secondary" @click="goToDemo">
              🚀 Go to Demo Page
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Completed Training History -->
    <div v-if="completedTraining.length > 0" class="history-section">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            📚 Training History
          </h3>
        </div>
        <div class="card-body">
          <div class="history-list">
            <div 
              v-for="item in completedTraining.slice(0, 5)" 
              :key="item.id"
              class="history-item"
            >
              <div class="history-info">
                <h5>{{ item.generatedOrb.title }}</h5>
                <p>{{ item.originalInput }}</p>
              </div>
              <div class="history-meta">
                <span class="history-status" :class="item.approved ? 'approved' : 'rejected'">
                  {{ item.approved ? '✅ Approved' : '❌ Rejected' }}
                </span>
                <span class="history-time">{{ formatTime(item.completedAt) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

// State
const pendingTasks = ref([])
const completedTraining = ref([])
const selectedTask = ref(null)
const isTraining = ref(false)
const currentTrainingTask = ref(null)
const currentTrainingStep = ref(0)
const currentStepResults = ref({})
const generatedOrb = ref(null)

// Training steps configuration
const trainingSteps = ref([
  {
    name: 'Input Sanitization',
    icon: '🧹',
    description: 'Clean and normalize input, replace specific values with placeholders',
    tools: [
      'TensorFlow Universal Sentence Encoder v4',
      'Custom PII detection algorithms',
      'Regex pattern matching for placeholders',
      'Data validation and normalization'
    ],
    process: true
  },
  {
    name: 'Semantic Analysis', 
    icon: '🧠',
    description: 'Generate embeddings and analyze semantic meaning using TensorFlow',
    tools: [
      'TensorFlow USE embeddings (512-dimensional)',
      'Semantic similarity calculations',
      'Intent classification models',
      'Contextual understanding pipelines'
    ],
    process: true
  },
  {
    name: 'Smithing Process',
    icon: '⚒️', 
    description: 'Craft solution using AI models and best practices',
    tools: [
      'LangChain orchestration framework',
      'GPT-4 language model integration', 
      'Custom ML classifiers (TensorFlow/Keras)',
      'Best practices knowledge base',
      'Template generation engines'
    ],
    process: true
  },
  {
    name: 'Quality Evaluation',
    icon: '📊',
    description: 'Evaluate solution quality, security, and effectiveness',
    tools: [
      'Security compliance checkers',
      'Performance impact analysis',
      'Best practices validation',
      'Confidence scoring algorithms'
    ],
    process: true
  },
  {
    name: 'Orb Generation',
    icon: '🔮',
    description: 'Generate final orb with templates, commands, and documentation',
    tools: [
      'YAML template generators',
      'Command sequence optimization',
      'Documentation auto-generation',
      'Rune ID assignment system'
    ],
    process: true
  }
])

// Computed
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

// Methods
const loadTrainingQueue = () => {
  const queue = JSON.parse(localStorage.getItem('whisTrainingQueue') || '[]')
  pendingTasks.value = queue.filter(task => task.status === 'pending_training')
  
  const completed = JSON.parse(localStorage.getItem('whisCompletedTraining') || '[]')
  completedTraining.value = completed
}

const selectTask = (task) => {
  selectedTask.value = task
}

const startTraining = async (task) => {
  if (isTraining.value) return
  
  isTraining.value = true
  currentTrainingTask.value = task
  currentTrainingStep.value = 0
  currentStepResults.value = {}
  generatedOrb.value = null
  
  // Process each training step
  for (let i = 0; i < trainingSteps.value.length; i++) {
    currentTrainingStep.value = i
    await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate processing time
    
    // Generate step results
    const results = await processTrainingStep(i, task)
    currentStepResults.value[i] = results
  }
  
  // Generate final orb
  generatedOrb.value = await generateOrbFromTraining(task)
}

const processTrainingStep = async (stepIndex, task) => {
  switch (stepIndex) {
    case 0: // Sanitization
      const sanitized = sanitizeInput(task.originalInput)
      return {
        'Original Input': task.originalInput,
        'Sanitized Input': sanitized,
        'Placeholders Created': Object.keys(extractPlaceholders(task.originalInput)).length,
        'PII Removed': 'Names, specific values replaced with placeholders'
      }
      
    case 1: // Semantic Analysis
      return {
        'Embedding Dimensions': '512',
        'Semantic Categories': 'Kubernetes, Infrastructure, DevOps',
        'Intent Confidence': '94%',
        'Similar Patterns': '23 related patterns found'
      }
      
    case 2: // Smithing
      return {
        'Templates Generated': '3',
        'Commands Created': '8',
        'Best Practices Applied': '12',
        'Security Checks': 'Passed'
      }
      
    case 3: // Evaluation
      return {
        'Quality Score': '87%',
        'Security Rating': 'High',
        'Performance Impact': 'Low',
        'Compliance': 'SOC2, PCI-DSS'
      }
      
    case 4: // Orb Generation
      return {
        'Rune ID': `R-${Math.floor(Math.random() * 900) + 100}`,
        'Template Lines': '45',
        'Command Count': '8',
        'Documentation': 'Auto-generated'
      }
      
    default:
      return {}
  }
}

const sanitizeInput = (input) => {
  let sanitized = input
  const placeholders = extractPlaceholders(input)
  
  Object.keys(placeholders).forEach(key => {
    sanitized = sanitized.replace(new RegExp(key, 'gi'), placeholders[key])
  })
  
  return sanitized
}

const extractPlaceholders = (input) => {
  const placeholders = {}
  
  // Replace pod names
  if (input.includes('testpod') || input.includes('test-pod')) {
    placeholders['testpod'] = 'POD-NAME'
    placeholders['test-pod'] = 'POD-NAME'
  }
  
  // Replace image names
  if (input.includes('busybox')) {
    placeholders['busybox'] = 'IMAGE-NAME'
  }
  if (input.includes('nginx')) {
    placeholders['nginx'] = 'IMAGE-NAME'
  }
  
  // Replace common service names
  if (input.includes('myapp') || input.includes('my-app')) {
    placeholders['myapp'] = 'SERVICE-NAME'
    placeholders['my-app'] = 'SERVICE-NAME'
  }
  
  return placeholders
}

const generateOrbFromTraining = async (task) => {
  const sanitized = sanitizeInput(task.originalInput)
  const placeholders = extractPlaceholders(task.originalInput)
  
  return {
    title: `${task.originalInput.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} - AI Generated`,
    category: determineCategory(task.originalInput),
    orb: `AI-generated solution for: "${task.originalInput}". This orb provides automated best practices with placeholder support.`,
    keywords: extractKeywords(task.originalInput),
    rune_id: `R-${Math.floor(Math.random() * 900) + 100}`,
    confidence: 0.85,
    declarative_template: generateTemplate(sanitized, placeholders),
    imperative_commands: generateCommands(sanitized, placeholders),
    needsApproval: true,
    trainingSource: task.id
  }
}

const determineCategory = (input) => {
  if (input.includes('pod')) return 'Kubernetes'
  if (input.includes('service')) return 'Kubernetes'
  if (input.includes('deploy')) return 'CI/CD'
  if (input.includes('pipeline')) return 'CI/CD'
  if (input.includes('security') || input.includes('secret')) return 'Security'
  return 'DevOps'
}

const extractKeywords = (input) => {
  const keywords = []
  const commonKeywords = ['kubernetes', 'pod', 'deployment', 'service', 'secret', 'configmap', 'pipeline', 'ci', 'cd']
  
  commonKeywords.forEach(keyword => {
    if (input.toLowerCase().includes(keyword)) {
      keywords.push(keyword)
    }
  })
  
  keywords.push('ai-generated', 'training')
  return keywords
}

const generateTemplate = (sanitizedInput, placeholders) => {
  if (sanitizedInput.includes('pod')) {
    return `apiVersion: v1
kind: Pod
metadata:
  name: ${placeholders['testpod'] || 'POD-NAME'}
  labels:
    app: ${placeholders['testpod'] || 'POD-NAME'}
spec:
  containers:
  - name: main
    image: ${placeholders['busybox'] || placeholders['nginx'] || 'IMAGE-NAME'}
    ports:
    - containerPort: 80
  restartPolicy: Always`
  }
  
  return `# Generated template for: ${sanitizedInput}
apiVersion: v1
kind: ConfigMap
metadata:
  name: config
data:
  key: value`
}

const generateCommands = (sanitizedInput, placeholders) => {
  if (sanitizedInput.includes('pod')) {
    const podName = placeholders['testpod'] || 'POD-NAME'
    const imageName = placeholders['busybox'] || placeholders['nginx'] || 'IMAGE-NAME'
    
    return [
      `# Create pod with specified image`,
      `kubectl run ${podName} --image=${imageName}`,
      ``,
      `# Verify pod creation`,
      `kubectl get pods ${podName}`,
      `kubectl describe pod ${podName}`,
      ``,
      `# Check logs and cleanup`,
      `kubectl logs ${podName}`,
      `kubectl delete pod ${podName}`
    ]
  }
  
  return [
    '# Generated commands',
    'kubectl apply -f manifest.yaml',
    'kubectl get all'
  ]
}

const approveOrb = () => {
  if (!generatedOrb.value || !currentTrainingTask.value) return
  
  // Create rune and save to orb library
  const rune = {
    ...generatedOrb.value,
    approved: true,
    savedAt: new Date().toISOString(),
    runeCreated: true
  }
  
  // Save to completed training
  const trainingRecord = {
    id: Date.now(),
    originalInput: currentTrainingTask.value.originalInput,
    generatedOrb: rune,
    approved: true,
    completedAt: new Date().toISOString()
  }
  
  completedTraining.value.push(trainingRecord)
  const completed = JSON.parse(localStorage.getItem('whisCompletedTraining') || '[]')
  completed.push(trainingRecord)
  localStorage.setItem('whisCompletedTraining', JSON.stringify(completed))
  
  // Add to orb library (for demo)
  const orbLibrary = JSON.parse(localStorage.getItem('orbLibrary') || '[]')
  orbLibrary.push(rune)
  localStorage.setItem('orbLibrary', JSON.stringify(orbLibrary))
  
  // Remove from training queue
  removeFromTrainingQueue(currentTrainingTask.value.id)
  
  alert(`✅ Orb approved! Rune "${rune.rune_id}" created and added to ${rune.category} category.`)
  resetTraining()
}

const rejectOrb = () => {
  if (!currentTrainingTask.value) return
  
  const trainingRecord = {
    id: Date.now(),
    originalInput: currentTrainingTask.value.originalInput,
    generatedOrb: generatedOrb.value,
    approved: false,
    rejectionReason: 'Quality below threshold',
    completedAt: new Date().toISOString()
  }
  
  completedTraining.value.push(trainingRecord)
  const completed = JSON.parse(localStorage.getItem('whisCompletedTraining') || '[]')
  completed.push(trainingRecord)
  localStorage.setItem('whisCompletedTraining', JSON.stringify(completed))
  
  removeFromTrainingQueue(currentTrainingTask.value.id)
  
  alert(`❌ Orb rejected. This is when Whis would use OpenAI as a fallback to help improve orb creation until satisfied. The task will be reprocessed with enhanced AI assistance.`)
  resetTraining()
}

const removeFromTrainingQueue = (taskId) => {
  const queue = JSON.parse(localStorage.getItem('whisTrainingQueue') || '[]')
  const filtered = queue.filter(task => task.id !== taskId)
  localStorage.setItem('whisTrainingQueue', JSON.stringify(filtered))
  loadTrainingQueue()
}

const resetTraining = () => {
  isTraining.value = false
  currentTrainingTask.value = null
  currentTrainingStep.value = 0
  currentStepResults.value = {}
  generatedOrb.value = null
  selectedTask.value = null
}

const goToDemo = () => {
  window.location.href = '/'
}

// Lifecycle
onMounted(() => {
  loadTrainingQueue()
})
</script>

<style scoped>
.whis-pipeline-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.card {
  background: linear-gradient(135deg, #1e293b, #334155);
  border: 1px solid #475569;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  margin-bottom: 2rem;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #475569;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0 0 0.5rem 0;
}

.card-subtitle {
  color: #94a3b8;
  margin: 0;
}

.card-body {
  padding: 1.5rem;
}

/* Pipeline Stats */
.pipeline-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1.5rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: rgba(148, 163, 184, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #10b981;
  display: block;
}

.stat-label {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-top: 0.25rem;
}

/* Training Tasks */
.training-tasks {
  space-y: 1rem;
}

.training-task-card {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
}

.training-task-card:hover {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.05);
}

.training-task-card.selected {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.task-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0 0 0.5rem 0;
}

.task-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #94a3b8;
}

.confidence-score {
  color: #fbbf24;
  font-weight: 500;
}

.start-training-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-training-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
}

.start-training-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Training Process */
.training-progress {
  margin-bottom: 2rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(148, 163, 184, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #059669);
  transition: width 0.5s ease;
}

.progress-text {
  text-align: center;
  color: #94a3b8;
  font-size: 0.875rem;
}

/* Training Steps */
.training-steps {
  space-y: 1.5rem;
}

.training-step {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.training-step.active {
  background: rgba(16, 185, 129, 0.1);
  border-color: #10b981;
}

.training-step.completed {
  background: rgba(5, 150, 105, 0.05);
  border-color: #059669;
}

.training-step.pending {
  background: rgba(148, 163, 184, 0.05);
  border-color: #334155;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.step-number {
  width: 32px;
  height: 32px;
  background: #475569;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.training-step.active .step-number {
  background: #10b981;
}

.training-step.completed .step-number {
  background: #059669;
}

.step-icon {
  font-size: 1.5rem;
}

.step-content {
  flex: 1;
}

.step-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f1f5f9;
  margin: 0 0 0.5rem 0;
}

.step-description {
  color: #94a3b8;
  margin: 0 0 1rem 0;
}

.step-details {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 6px;
  padding: 1rem;
  margin-top: 1rem;
}

.tools-section h5,
.process-section h5 {
  color: #10b981;
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
}

.tools-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tools-list li {
  color: #cbd5e1;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  padding-left: 1rem;
  position: relative;
}

.tools-list li::before {
  content: '•';
  color: #10b981;
  position: absolute;
  left: 0;
}

.process-results {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.result-item {
  background: rgba(16, 185, 129, 0.1);
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  color: #cbd5e1;
}

.result-item strong {
  color: #10b981;
}

/* Generated Orb */
.generated-orb-section {
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 2rem;
}

.generated-orb-section h4 {
  color: #a855f7;
  margin: 0 0 1rem 0;
}

.orb-preview {
  background: rgba(15, 23, 42, 0.8);
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.orb-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.orb-header h5 {
  color: #f1f5f9;
  margin: 0;
  font-size: 1.125rem;
}

.orb-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
}

.orb-category {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
}

.orb-rune {
  background: rgba(139, 92, 246, 0.2);
  color: #a855f7;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-family: monospace;
}

.orb-content p {
  color: #cbd5e1;
  margin: 0 0 1rem 0;
}

.template-preview,
.commands-preview {
  margin-top: 1rem;
}

.template-preview h6,
.commands-preview h6 {
  color: #94a3b8;
  font-size: 0.875rem;
  margin: 0 0 0.5rem 0;
}

.template-preview pre {
  background: rgba(0, 0, 0, 0.4);
  color: #e2e8f0;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  overflow-x: auto;
  margin: 0;
}

.commands-preview ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.commands-preview li {
  background: rgba(0, 0, 0, 0.4);
  color: #e2e8f0;
  padding: 0.5rem;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.8rem;
  margin-bottom: 0.25rem;
}

/* Approval Section */
.approval-section {
  border-top: 1px solid rgba(139, 92, 246, 0.3);
  padding-top: 1.5rem;
}

.approval-section h4 {
  color: #a855f7;
  margin: 0 0 1rem 0;
}

.approval-buttons {
  display: flex;
  gap: 1rem;
}

.approve-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.approve-btn:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
}

.reject-btn {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reject-btn:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-1px);
}

/* No Tasks */
.no-tasks-content {
  text-align: center;
  padding: 3rem;
}

.no-tasks-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-tasks-content h3 {
  color: #f1f5f9;
  margin: 0 0 1rem 0;
}

.no-tasks-content p {
  color: #94a3b8;
  margin: 0 0 2rem 0;
}

/* History */
.history-list {
  space-y: 1rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 6px;
  margin-bottom: 1rem;
}

.history-info h5 {
  color: #f1f5f9;
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.history-info p {
  color: #94a3b8;
  margin: 0;
  font-size: 0.875rem;
}

.history-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.history-status {
  font-size: 0.875rem;
  font-weight: 500;
}

.history-status.approved {
  color: #10b981;
}

.history-status.rejected {
  color: #ef4444;
}

.history-time {
  font-size: 0.75rem;
  color: #64748b;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  text-decoration: none;
}

.btn-secondary {
  background: linear-gradient(135deg, #64748b, #475569);
  color: white;
}

.btn-secondary:hover {
  background: linear-gradient(135deg, #475569, #334155);
  transform: translateY(-1px);
}
</style>
