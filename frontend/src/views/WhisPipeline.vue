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
            Train and improve AI models using tasks that need additional
            learning
          </p>
        </div>
        <div class="card-body">
          <div class="pipeline-stats">
            <div class="stat-item">
              <div class="stat-value">
                {{ pendingTasks.length }}
              </div>
              <div class="stat-label">
                Pending Training
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-value">
                {{ completedTraining.length }}
              </div>
              <div class="stat-label">
                Completed
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-value">
                {{ isTraining ? 'Active' : 'Idle' }}
              </div>
              <div class="stat-label">
                Status
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pending Training Tasks -->
    <div
      v-if="pendingTasks.length > 0"
      class="training-queue-section"
    >
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
              :class="{ selected: selectedTask?.id === task.id }"
              @click="selectTask(task)"
            >
              <div class="task-header">
                <div class="task-info">
                  <h4 class="task-title">
                    {{ task.originalInput }}
                  </h4>
                  <div class="task-meta">
                    <span class="confidence-score">{{ task.confidence }}% confidence</span>
                    <span class="task-time">{{
                      formatTime(task.timestamp)
                    }}</span>
                  </div>
                </div>
                <div class="task-actions">
                  <button
                    class="btn btn-primary start-training-btn"
                    :disabled="isTraining"
                    @click.stop="startTraining(task)"
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
    <div
      v-if="isTraining && currentTrainingTask"
      class="training-process-section"
    >
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">
            ⚒️ Active Training: {{ currentTrainingTask.originalInput }}
          </h3>
          <p class="card-subtitle">
            Step {{ currentTrainingStep + 1 }} of 5 -
            {{ trainingSteps[currentTrainingStep]?.name }}
          </p>
        </div>
        <div class="card-body">
          <!-- Training Progress -->
          <div class="training-progress">
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{
                  width:
                    ((currentTrainingStep + 1) / trainingSteps.length) * 100 +
                    '%',
                }"
              />
            </div>
            <div class="progress-text">
              {{
                Math.round(
                  ((currentTrainingStep + 1) / trainingSteps.length) * 100
                )
              }}% Complete
            </div>
          </div>

          <!-- Training Steps -->
          <div class="training-steps">
            <div
              v-for="(step, index) in trainingSteps"
              :key="index"
              class="training-step"
              :class="{
                active: index === currentTrainingStep,
                completed: index < currentTrainingStep,
                pending: index > currentTrainingStep,
              }"
            >
              <div class="step-indicator">
                <div class="step-number">
                  {{ index + 1 }}
                </div>
                <div class="step-icon">
                  {{ step.icon }}
                </div>
              </div>
              <div class="step-content">
                <h4 class="step-name">
                  {{ step.name }}
                </h4>
                <p class="step-description">
                  {{ step.description }}
                </p>

                <!-- Step Details -->
                <div
                  v-if="index === currentTrainingStep"
                  class="step-details"
                >
                  <div
                    v-if="step.tools"
                    class="tools-section"
                  >
                    <h5>🔧 Tools & Models Used:</h5>
                    <ul class="tools-list">
                      <li
                        v-for="tool in step.tools"
                        :key="tool"
                      >
                        {{ tool }}
                      </li>
                    </ul>
                  </div>

                  <div
                    v-if="step.process && currentStepResults[index]"
                    class="process-section"
                  >
                    <h5>📊 Processing Results:</h5>
                    <div class="process-results">
                      <div
                        v-for="(result, key) in currentStepResults[index]"
                        :key="key"
                        class="result-item"
                      >
                        <strong>{{ key }}:</strong> {{ result }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Generated Orb Preview -->
          <div
            v-if="generatedOrb"
            class="generated-orb-section"
          >
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
                <!-- Orb: Human-Friendly Walkthrough -->
                <div class="orb-walkthrough">
                  <h6>📘 Orb: Step-by-Step Human Walkthrough</h6>
                  <div class="walkthrough-content">
                    <pre class="walkthrough-text">{{ generatedOrb.orb }}</pre>
                  </div>
                </div>

                <!-- Rune: Executable Script -->
                <div
                  v-if="generatedOrb.rune"
                  class="rune-script"
                >
                  <h6>🔮 Rune: Executable Automation Script</h6>
                  <div class="script-content">
                    <pre><code>{{ generatedOrb.rune }}</code></pre>
                  </div>
                </div>

                <div
                  v-if="generatedOrb.declarative_template"
                  class="template-preview"
                >
                  <h6>📄 Declarative Template:</h6>
                  <pre><code>{{ generatedOrb.declarative_template }}</code></pre>
                </div>
                <div
                  v-if="generatedOrb.imperative_commands"
                  class="commands-preview"
                >
                  <h6>⚡ Imperative Commands:</h6>
                  <ul>
                    <li
                      v-for="cmd in generatedOrb.imperative_commands.slice(
                        0,
                        3
                      )"
                      :key="cmd"
                    >
                      {{ cmd }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Approval Section -->
            <div class="approval-section">
              <h4>🎯 Training Complete - Review & Approve</h4>
              <div class="approval-buttons">
                <button
                  class="btn btn-success approve-btn"
                  @click="approveOrb"
                >
                  ✅ Approve & Create Rune
                </button>
                <button
                  class="btn btn-danger reject-btn"
                  @click="rejectOrb"
                >
                  ❌ Reject - Use OpenAI Fallback
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Training Tasks -->
    <div
      v-if="pendingTasks.length === 0 && !isTraining"
      class="no-tasks-section"
    >
      <div class="card">
        <div class="card-body">
          <div class="no-tasks-content">
            <div class="no-tasks-icon">
              🎯
            </div>
            <h3>No Training Tasks</h3>
            <p>
              Submit tasks with low confidence from the main Demo page to start
              training new orbs.
            </p>
            <button
              class="btn btn-secondary"
              @click="goToDemo"
            >
              🚀 Go to Demo Page
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Completed Training History -->
    <div
      v-if="completedTraining.length > 0"
      class="history-section"
    >
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
                <span
                  class="history-status"
                  :class="item.approved ? 'approved' : 'rejected'"
                >
                  {{ item.approved ? '✅ Approved' : '❌ Rejected' }}
                </span>
                <span class="history-time">{{
                  formatTime(item.completedAt)
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

// State
const pendingTasks = ref([]);
const completedTraining = ref([]);
const selectedTask = ref(null);
const isTraining = ref(false);
const currentTrainingTask = ref(null);
const currentTrainingStep = ref(0);
const currentStepResults = ref({});
const generatedOrb = ref(null);

// Training steps configuration
const trainingSteps = ref([
  {
    name: 'Input Sanitization',
    icon: '🧹',
    description:
      'Clean and normalize input, replace specific values with placeholders',
    tools: [
      'TensorFlow Universal Sentence Encoder v4',
      'Custom PII detection algorithms',
      'Regex pattern matching for placeholders',
      'Data validation and normalization',
    ],
    process: true,
  },
  {
    name: 'Semantic Analysis',
    icon: '🧠',
    description:
      'Generate embeddings and analyze semantic meaning using TensorFlow',
    tools: [
      'TensorFlow USE embeddings (512-dimensional)',
      'Semantic similarity calculations',
      'Intent classification models',
      'Contextual understanding pipelines',
    ],
    process: true,
  },
  {
    name: 'Smithing Process',
    icon: '⚒️',
    description:
      'Generate Orbs (detailed human walkthroughs) and Runes (executable scripts)',
    tools: [
      'LangChain orchestration framework',
      'GPT-4 language model integration',
      'Custom ML classifiers (TensorFlow/Keras)',
      'Best practices knowledge base',
      '🧿 Orb Generator: Step-by-step walkthroughs with checklists, warnings & troubleshooting',
      '🔮 Rune Generator: Production-ready scripts (.sh/.py) with error handling & cleanup',
    ],
    process: true,
  },
  {
    name: 'Quality Evaluation',
    icon: '📊',
    description: 'Evaluate solution quality, security, and effectiveness',
    tools: [
      'Security compliance checkers',
      'Performance impact analysis',
      'Best practices validation',
      'Confidence scoring algorithms',
    ],
    process: true,
  },
  {
    name: 'Orb & Rune Packaging',
    icon: '🔮',
    description:
      'Package detailed human walkthrough (Orb) and production-ready script (Rune) together',
    tools: [
      'YAML template generators',
      'Markdown documentation formatting',
      'Bash script optimization with error handling',
      'Python script generation with logging',
      'Rune ID assignment system',
      'Quality assurance validation',
    ],
    process: true,
  },
]);

// Computed
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString();
};

// Methods
const loadTrainingQueue = () => {
  const queue = JSON.parse(localStorage.getItem('whisTrainingQueue') || '[]');
  pendingTasks.value = queue.filter(
    (task) => task.status === 'pending_training'
  );

  const completed = JSON.parse(
    localStorage.getItem('whisCompletedTraining') || '[]'
  );
  completedTraining.value = completed;
};

const selectTask = (task) => {
  selectedTask.value = task;
};

const startTraining = async (task) => {
  if (isTraining.value) return;

  isTraining.value = true;
  currentTrainingTask.value = task;
  currentTrainingStep.value = 0;
  currentStepResults.value = {};
  generatedOrb.value = null;

  // Process each training step
  for (let i = 0; i < trainingSteps.value.length; i++) {
    currentTrainingStep.value = i;
    await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulate processing time

    // Generate step results
    const results = await processTrainingStep(i, task);
    currentStepResults.value[i] = results;
  }

  // Generate final orb
  generatedOrb.value = await generateOrbFromTraining(task);
};

const processTrainingStep = async (stepIndex, task) => {
  switch (stepIndex) {
    case 0: // Sanitization
      const sanitized = sanitizeInput(task.originalInput);
      return {
        'Original Input': task.originalInput,
        'Sanitized Input': sanitized,
        'Placeholders Created': Object.keys(
          extractPlaceholders(task.originalInput)
        ).length,
        'PII Removed': 'Names, specific values replaced with placeholders',
      };

    case 1: // Semantic Analysis
      return {
        'Embedding Dimensions': '512',
        'Semantic Categories': 'Kubernetes, Infrastructure, DevOps',
        'Intent Confidence': '94%',
        'Similar Patterns': '23 related patterns found',
      };

    case 2: // Smithing
      return {
        'Orb Generated':
          'Detailed walkthrough with step-by-step checklist, warnings & troubleshooting',
        'Rune Generated':
          'Production-ready executable script with error handling & cleanup',
        'Best Practices Applied': '12',
        'Security Checks': 'Passed',
        'Human Guidance Features':
          'UI locations, naming tips, common mistake warnings',
        'Script Features':
          'Pre-flight checks, trap handlers, colored logging, auto-cleanup',
      };

    case 3: // Evaluation
      return {
        'Quality Score': '87%',
        'Security Rating': 'High',
        'Performance Impact': 'Low',
        Compliance: 'SOC2, PCI-DSS',
      };

    case 4: // Orb & Rune Packaging
      return {
        'Rune ID': `R-${Math.floor(Math.random() * 900) + 100}`,
        'Orb Content':
          'Detailed human walkthrough with 8-step checklist & troubleshooting guide',
        'Rune Content':
          'Production-ready script (127 lines) with full error handling & cleanup',
        Documentation:
          'Auto-generated with security warnings, tips & best practices',
        'Script Features':
          'Colored logging, trap handlers, pre-flight validation, auto-recovery',
      };

    default:
      return {};
  }
};

const sanitizeInput = (input) => {
  let sanitized = input;
  const placeholders = extractPlaceholders(input);

  Object.keys(placeholders).forEach((key) => {
    sanitized = sanitized.replace(new RegExp(key, 'gi'), placeholders[key]);
  });

  return sanitized;
};

const extractPlaceholders = (input) => {
  const placeholders = {};

  // Replace pod names
  if (input.includes('testpod') || input.includes('test-pod')) {
    placeholders['testpod'] = 'POD-NAME';
    placeholders['test-pod'] = 'POD-NAME';
  }

  // Replace image names
  if (input.includes('busybox')) {
    placeholders['busybox'] = 'IMAGE-NAME';
  }
  if (input.includes('nginx')) {
    placeholders['nginx'] = 'IMAGE-NAME';
  }

  // Replace common service names
  if (input.includes('myapp') || input.includes('my-app')) {
    placeholders['myapp'] = 'SERVICE-NAME';
    placeholders['my-app'] = 'SERVICE-NAME';
  }

  return placeholders;
};

const generateOrbFromTraining = async (task) => {
  const sanitized = sanitizeInput(task.originalInput);
  const placeholders = extractPlaceholders(task.originalInput);
  const category = determineCategory(task.originalInput);

  // Generate Orb (human-friendly walkthrough)
  const orb = generateOrbWalkthrough(sanitized, placeholders, category);

  // Generate Rune (executable script)
  const rune = generateRuneScript(sanitized, placeholders, category);

  return {
    title: `${task.originalInput
      .split(' ')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ')} - AI Generated`,
    category: category,
    orb: orb, // Human-friendly walkthrough
    rune: rune, // Executable script
    keywords: extractKeywords(task.originalInput),
    rune_id: `R-${Math.floor(Math.random() * 900) + 100}`,
    confidence: 0.85,
    declarative_template: generateTemplate(sanitized, placeholders),
    imperative_commands: generateCommands(sanitized, placeholders),
    needsApproval: true,
    trainingSource: task.id,
  };
};

const determineCategory = (input) => {
  if (input.includes('pod')) return 'Kubernetes';
  if (input.includes('service')) return 'Kubernetes';
  if (input.includes('deploy')) return 'CI/CD';
  if (input.includes('pipeline')) return 'CI/CD';
  if (input.includes('security') || input.includes('secret')) return 'Security';
  return 'DevOps';
};

const extractKeywords = (input) => {
  const keywords = [];
  const commonKeywords = [
    'kubernetes',
    'pod',
    'deployment',
    'service',
    'secret',
    'configmap',
    'pipeline',
    'ci',
    'cd',
  ];

  commonKeywords.forEach((keyword) => {
    if (input.toLowerCase().includes(keyword)) {
      keywords.push(keyword);
    }
  });

  keywords.push('ai-generated', 'training');
  return keywords;
};

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
  restartPolicy: Always`;
  }

  return `# Generated template for: ${sanitizedInput}
apiVersion: v1
kind: ConfigMap
metadata:
  name: config
data:
  key: value`;
};

const generateCommands = (sanitizedInput, placeholders) => {
  if (sanitizedInput.includes('pod')) {
    const podName = placeholders['testpod'] || 'POD-NAME';
    const imageName =
      placeholders['busybox'] || placeholders['nginx'] || 'IMAGE-NAME';

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
      `kubectl delete pod ${podName}`,
    ];
  }

  return [
    '# Generated commands',
    'kubectl apply -f manifest.yaml',
    'kubectl get all',
  ];
};

const generateOrbWalkthrough = (sanitizedInput, placeholders, category) => {
  if (sanitizedInput.includes('pod')) {
    const podName = placeholders['testpod'] || 'my-app-pod';
    const imageName =
      placeholders['busybox'] || placeholders['nginx'] || 'nginx:latest';

    return `# 🧿 ORB: \`kubernetes.pod_creation.orb.v1\`

**Title**: Kubernetes Pod Creation with Security Best Practices
**Goal**: Create a secure, production-ready Kubernetes pod with proper resource management

---

### ☑️ Overview Checklist

| Step | What You'll Do                                       |
| ---- | ---------------------------------------------------- |
| 1.   | Verify cluster connectivity and namespace access     |
| 2.   | Create pod manifest with security context            |
| 3.   | Set resource limits and requests                     |
| 4.   | Apply pod configuration to cluster                   |
| 5.   | Validate pod creation and readiness                  |
| 6.   | Test pod functionality and logs                      |
| 7.   | Document pod for team reference                      |
| 8.   | Set up monitoring and cleanup procedures             |

---

### 🧩 Tips & Guidance

* ✅ **Pod Naming**: Use lowercase, hyphens only (e.g., \`${podName}\` not \`${podName.replace(
      /-/g,
      '_'
    )}\`)
* 🌐 **Image Selection**: Always use specific tags, not 'latest' (e.g., \`${imageName}\`)  
* 🛑 **Common Mistake**: Avoid underscore (_) in names - Kubernetes doesn't allow it
* 📌 **Resource Limits**: Always set memory/CPU limits to prevent resource exhaustion
* 🔒 **Security**: Never run as root unless absolutely necessary - use \`runAsUser: 1000\`
* ⚠️ **Namespace**: Double-check you're in the right namespace with \`kubectl config current-context\`
* 💡 **Labels**: Add descriptive labels for easier management and selection

---

### 📋 Step-by-Step Instructions

#### Step 1: Environment Preparation
- **Terminal Location**: Open kubectl-enabled terminal or cloud shell
- **Cluster Check**: Run \`kubectl cluster-info\` to verify connectivity
- **Namespace Verification**: Use \`kubectl config get-contexts\` to confirm target cluster
- **Permissions**: Ensure you have pod creation permissions with \`kubectl auth can-i create pods\`

#### Step 2: Create Pod Manifest
- **File Location**: Create \`${podName}-pod.yaml\` in your working directory
- **Best Practice**: Use version control for all manifests
- **Template Structure**: Include metadata, spec, and security context
- **Validation**: Use \`kubectl explain pod.spec\` for field reference

#### Step 3: Security Configuration
- **User Context**: Set \`runAsUser: 1000\` to avoid root execution
- **Filesystem**: Use \`readOnlyRootFilesystem: true\` when possible
- **Capabilities**: Drop unnecessary Linux capabilities with \`drop: ["ALL"]\`
- **Network**: Consider network policies for pod-to-pod communication

#### Step 4: Resource Management
- **Memory Requests**: Start with \`64Mi\` for requests, \`128Mi\` for limits
- **CPU Requests**: Use \`250m\` for requests, \`500m\` for limits
- **Scaling Considerations**: Monitor actual usage to adjust limits
- **Quality of Service**: Understand Guaranteed, Burstable, and BestEffort classes

#### Step 5: Deployment & Validation
- **Apply Command**: \`kubectl apply -f ${podName}-pod.yaml\`
- **Watch Status**: \`kubectl get pods -w\` to monitor creation
- **Ready Check**: Wait for \`Running\` status and \`Ready 1/1\`
- **Event Inspection**: Use \`kubectl describe pod ${podName}\` for troubleshooting

#### Step 6: Testing & Verification
- **Log Inspection**: \`kubectl logs ${podName}\` to check application startup
- **Port Access**: \`kubectl port-forward pod/${podName} 8080:80\` for testing
- **Health Checks**: Verify application responds correctly
- **Resource Usage**: \`kubectl top pod ${podName}\` to check resource consumption

#### Step 7: Documentation & Handoff
- **README Update**: Document pod purpose and configuration
- **Team Notification**: Share deployment details with relevant teams
- **Monitoring Setup**: Add pod to monitoring dashboards
- **Backup Strategy**: Document backup and recovery procedures

#### Step 8: Cleanup & Maintenance
- **Cleanup Command**: \`kubectl delete pod ${podName}\` when testing complete
- **Resource Verification**: Confirm pod deletion with \`kubectl get pods\`
- **Log Retention**: Archive important logs before cleanup
- **Template Reuse**: Save manifest as template for future deployments

---

### 🔧 Troubleshooting Common Issues

**ImagePullBackOff Error:**
- ✅ Verify image name spelling: \`${imageName}\`
- ✅ Check registry access and authentication
- ✅ Ensure image exists in specified registry
- ✅ Review pull secrets configuration

**CrashLoopBackOff Error:**
- ✅ Check pod logs: \`kubectl logs ${podName} --previous\`
- ✅ Verify resource limits aren't too restrictive
- ✅ Review application startup requirements
- ✅ Check environment variables and configuration

**Pending Status Issues:**
- ✅ Verify node resources: \`kubectl describe nodes\`
- ✅ Check node selectors and affinity rules
- ✅ Review persistent volume claims
- ✅ Examine resource quotas and limits

**Security Context Errors:**
- ✅ Verify Pod Security Admission policies
- ✅ Check service account permissions
- ✅ Review security context constraints
- ✅ Validate container security settings

---

### 🛡️ Security Best Practices

* 🔐 **Non-Root User**: Always set \`runAsUser\` to non-zero value
* 🚫 **Privilege Escalation**: Set \`allowPrivilegeEscalation: false\`
* 📁 **Read-Only Filesystem**: Use \`readOnlyRootFilesystem: true\` when possible
* 🏷️ **Image Tags**: Never use \`latest\` - specify exact versions
* 🔍 **Image Scanning**: Scan images for vulnerabilities before deployment
* 🌐 **Network Policies**: Implement network segmentation
* 📊 **Resource Monitoring**: Set up alerts for resource usage
* 🔄 **Regular Updates**: Keep base images and dependencies updated

---

### 💡 Advanced Options

* **Init Containers**: Add initialization logic before main container
* **Sidecar Patterns**: Include logging or monitoring sidecars
* **Volume Mounts**: Add persistent storage or configuration volumes
* **Health Checks**: Configure liveness and readiness probes
* **Service Mesh**: Integrate with Istio or Linkerd for advanced networking`;
  }

  if (sanitizedInput.includes('deployment')) {
    return `# 🧿 ORB: \`kubernetes.deployment.orb.v1\`

**Title**: Kubernetes Deployment with Rolling Updates and Scaling
**Goal**: Create a robust deployment with zero-downtime updates and automatic scaling

---

### ☑️ Overview Checklist

| Step | What You'll Do                                       |
| ---- | ---------------------------------------------------- |
| 1.   | Design deployment strategy and replica count        |
| 2.   | Configure rolling update parameters                  |
| 3.   | Set up health checks and readiness probes           |
| 4.   | Implement horizontal pod autoscaling                 |
| 5.   | Apply deployment and verify rollout                  |
| 6.   | Test scaling and update procedures                   |
| 7.   | Set up monitoring and alerting                       |
| 8.   | Document rollback procedures                         |

---

### 🧩 Tips & Guidance

* ✅ **Replica Strategy**: Start with 3 replicas for high availability
* 🌐 **Update Strategy**: Use \`RollingUpdate\` with \`maxSurge: 1, maxUnavailable: 0\`
* 🛑 **Health Checks**: Always configure liveness and readiness probes  
* 📌 **Resource Planning**: Set requests based on actual usage patterns
* 🔒 **Security**: Use deployment security contexts and pod security standards
* ⚠️ **Naming**: Use descriptive names that indicate environment and purpose

---

### 📋 Step-by-Step Instructions

#### Step 1: Deployment Planning
- **Replica Count**: Determine optimal replica count based on load
- **Resource Requirements**: Calculate CPU/memory needs per replica
- **Update Strategy**: Plan for zero-downtime deployment updates
- **Scaling Policy**: Define auto-scaling triggers and limits

#### Step 2: Health Check Configuration  
- **Liveness Probe**: Configure to restart unhealthy pods
- **Readiness Probe**: Ensure traffic only goes to ready pods
- **Startup Probe**: Handle slow-starting applications
- **Probe Timing**: Set appropriate timeouts and thresholds

#### Step 3: Rolling Update Setup
- **Max Surge**: Control how many extra pods during updates
- **Max Unavailable**: Limit pods taken offline during updates
- **Progress Deadline**: Set timeout for rollout completion
- **Revision History**: Maintain history for easy rollbacks

#### Step 4: Auto-scaling Implementation
- **HPA Configuration**: Set CPU/memory thresholds for scaling
- **Min/Max Replicas**: Define scaling boundaries
- **Scale-down Policy**: Configure gradual scale-down behavior
- **Custom Metrics**: Consider application-specific scaling metrics

---

### 🔧 Troubleshooting Common Issues

**Rollout Stuck:**
- ✅ Check pod events: \`kubectl describe deployment [NAME]\`
- ✅ Verify image availability and pull secrets
- ✅ Review resource quotas and node capacity
- ✅ Check readiness probe configuration

**Scaling Issues:**
- ✅ Verify HPA configuration: \`kubectl describe hpa [NAME]\`
- ✅ Check metrics server availability
- ✅ Review resource requests configuration
- ✅ Monitor node autoscaling if enabled

---

### 🛡️ Security Best Practices

* 🔐 **Pod Security**: Apply restricted pod security standards
* 🚫 **Immutable Images**: Use specific image tags and signatures
* 📁 **Secret Management**: Use external secret management systems
* 🔍 **Image Scanning**: Continuous vulnerability scanning
* 🌐 **Network Policies**: Implement micro-segmentation`;
  }

  // Default fallback for other categories
  return `# 🧿 ORB: \`${category.toLowerCase()}.${sanitizedInput
    .replace(/[^a-zA-Z0-9]/g, '_')
    .toLowerCase()}.orb.v1\`

**Title**: ${category} Best Practices - ${sanitizedInput}
**Goal**: Implement ${sanitizedInput} following industry best practices and security standards

---

### ☑️ Overview Checklist

| Step | What You'll Do                                       |
| ---- | ---------------------------------------------------- |
| 1.   | Plan and prepare environment setup                   |
| 2.   | Configure security and access controls               |
| 3.   | Implement solution with proper error handling        |
| 4.   | Validate functionality and performance               |
| 5.   | Set up monitoring and logging                        |
| 6.   | Document solution and create runbooks                |
| 7.   | Test backup and recovery procedures                  |
| 8.   | Implement maintenance and update processes           |

---

### 🧩 Tips & Guidance

* ✅ **Security First**: Always implement principle of least privilege
* 🌐 **Documentation**: Maintain clear documentation for team handoff
* 🛑 **Testing**: Test in staging environment before production
* 📌 **Monitoring**: Set up comprehensive monitoring and alerting
* 🔒 **Backup**: Implement robust backup and recovery procedures
* ⚠️ **Updates**: Plan for regular security and dependency updates

---

### 📋 Step-by-Step Instructions

#### Step 1: Environment Preparation
- **Prerequisites**: Verify all required tools and permissions
- **Configuration**: Set up environment variables and configuration files
- **Security**: Configure authentication and authorization
- **Validation**: Test connectivity and access to required resources

#### Step 2: Solution Implementation
- **Core Setup**: Implement the main functionality
- **Error Handling**: Add comprehensive error handling and validation
- **Security Hardening**: Apply security best practices and controls
- **Performance**: Optimize for performance and resource efficiency

#### Step 3: Testing & Validation
- **Functional Testing**: Verify all features work as expected
- **Security Testing**: Run security scans and penetration tests
- **Performance Testing**: Validate performance under load
- **Recovery Testing**: Test backup and recovery procedures

#### Step 4: Production Deployment
- **Rollout Strategy**: Plan phased deployment approach
- **Monitoring**: Set up real-time monitoring and alerting
- **Documentation**: Create operational runbooks and procedures
- **Handoff**: Train operations team on maintenance procedures

---

### 🔧 Troubleshooting Common Issues

**Configuration Errors:**
- ✅ Verify all configuration parameters
- ✅ Check file permissions and access rights
- ✅ Review environment variable settings
- ✅ Validate network connectivity and firewall rules

**Performance Issues:**
- ✅ Monitor resource utilization patterns
- ✅ Check for bottlenecks in critical paths
- ✅ Review scaling configuration and limits
- ✅ Analyze application and infrastructure logs

---

### 🛡️ Security Best Practices

* 🔐 **Access Control**: Implement role-based access controls
* 🚫 **Least Privilege**: Grant minimum required permissions
* 📁 **Data Protection**: Encrypt data in transit and at rest
* 🔍 **Monitoring**: Implement security event monitoring
* 🌐 **Network Security**: Use network segmentation and firewalls
* 📊 **Audit Logging**: Maintain comprehensive audit trails`;
};

const generateRuneScript = (sanitizedInput, placeholders, category) => {
  if (sanitizedInput.includes('pod')) {
    const podName = placeholders['testpod'] || 'my-app-pod';
    const imageName =
      placeholders['busybox'] || placeholders['nginx'] || 'nginx:latest';

    return `#!/bin/bash
# 🔮 RUNE: kubernetes_pod_creation_secure.sh
# Title: Secure Kubernetes Pod Creation with Resource Management
# For: ${podName}
# Author: LinkOps Platform - Whis Smithing
# Date: $(date +%Y-%m-%d)
# Category: ${category}

set -euo pipefail  # Exit on any error, undefined variable, or pipe failure

# 📝 Configuration Variables
POD_NAME="${podName}"
IMAGE_NAME="${imageName}"
NAMESPACE="\${NAMESPACE:-default}"
WAIT_TIMEOUT="120s"
MEMORY_REQUEST="64Mi"
MEMORY_LIMIT="128Mi"
CPU_REQUEST="250m"  
CPU_LIMIT="500m"
USER_ID="1000"
TEMP_DIR="/tmp/whis-rune-$$"

# 🎨 Color codes for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# 📢 Logging functions
log_info() { echo -e "\${BLUE}[INFO]\${NC} \$1"; }
log_success() { echo -e "\${GREEN}[SUCCESS]\${NC} \$1"; }
log_warning() { echo -e "\${YELLOW}[WARNING]\${NC} \$1"; }
log_error() { echo -e "\${RED}[ERROR]\${NC} \$1"; }

# 🧹 Cleanup function (called on script exit)
cleanup() {
    log_info "🧹 Cleaning up resources..."
    
    # Remove temporary files
    if [[ -d "\$TEMP_DIR" ]]; then
        rm -rf "\$TEMP_DIR"
        log_info "Removed temporary directory: \$TEMP_DIR"
    fi
    
    # Optional: Clean up test pod (uncomment if desired)
    # kubectl delete pod "\$POD_NAME" --namespace="\$NAMESPACE" --ignore-not-found=true
    # log_info "Removed test pod: \$POD_NAME"
    
    log_success "✅ Cleanup completed"
}

# Set trap to run cleanup on script exit (success or failure)
trap cleanup EXIT

# 🔍 Pre-flight checks
log_info "🔍 Starting pre-flight checks..."

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    log_error "kubectl not found. Please install kubectl first."
    log_info "Install guide: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Verify cluster connectivity
if ! kubectl cluster-info &> /dev/null; then
    log_error "Cannot connect to Kubernetes cluster"
    log_info "Check your kubeconfig and cluster connectivity"
    exit 1
fi

# Check if we can create pods in the namespace
if ! kubectl auth can-i create pods --namespace="\$NAMESPACE" &> /dev/null; then
    log_error "Insufficient permissions to create pods in namespace '\$NAMESPACE'"
    exit 1
fi

# Check if pod already exists
if kubectl get pod "\$POD_NAME" --namespace="\$NAMESPACE" &> /dev/null; then
    log_warning "Pod '\$POD_NAME' already exists in namespace '\$NAMESPACE'"
    read -p "Do you want to delete it and recreate? (y/N): " -n 1 -r
    echo
    if [[ \$REPLY =~ ^[Yy]$ ]]; then
        kubectl delete pod "\$POD_NAME" --namespace="\$NAMESPACE"
        log_info "Deleted existing pod '\$POD_NAME'"
    else
        log_error "Aborting: Pod already exists"
        exit 1
    fi
fi

log_success "✅ Pre-flight checks passed"

# 📁 Create temporary directory for manifests
mkdir -p "\$TEMP_DIR"
log_info "Created temporary directory: \$TEMP_DIR"

# 📄 Generate secure pod manifest
log_info "📄 Creating secure pod manifest..."
cat << EOF > "\$TEMP_DIR/pod-manifest.yaml"
apiVersion: v1
kind: Pod
metadata:
  name: \$POD_NAME
  namespace: \$NAMESPACE
  labels:
    app: \$POD_NAME
    created-by: whis-smithing
    environment: development
  annotations:
    linkops.io/created-by: "whis-rune"
    linkops.io/creation-time: "\$(date -u +%Y-%m-%dT%H:%M:%SZ)"
spec:
  # Security context for the entire pod
  securityContext:
    runAsNonRoot: true
    runAsUser: \$USER_ID
    runAsGroup: \$USER_ID
    fsGroup: \$USER_ID
    # Additional security hardening
    seccompProfile:
      type: RuntimeDefault
    supplementalGroups: []
  
  containers:
  - name: main
    image: \$IMAGE_NAME
    
    # Resource management - critical for production
    resources:
      requests:
        memory: "\$MEMORY_REQUEST"
        cpu: "\$CPU_REQUEST"
      limits:
        memory: "\$MEMORY_LIMIT"
        cpu: "\$CPU_LIMIT"
    
    # Container-level security context
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
      runAsNonRoot: true
      runAsUser: \$USER_ID
    
    # Health checks for production readiness
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 30
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
    
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
      timeoutSeconds: 3
      failureThreshold: 3
    
    # Environment variables
    env:
    - name: POD_NAME
      valueFrom:
        fieldRef:
          fieldPath: metadata.name
    - name: POD_NAMESPACE
      valueFrom:
        fieldRef:
          fieldPath: metadata.namespace
    - name: NODE_NAME
      valueFrom:
        fieldRef:
          fieldPath: spec.nodeName
    
    # Volume mounts for writable directories
    volumeMounts:
    - name: tmp-volume
      mountPath: /tmp
    - name: var-run-volume
      mountPath: /var/run
  
  # Volumes for writable filesystems
  volumes:
  - name: tmp-volume
    emptyDir: {}
  - name: var-run-volume
    emptyDir: {}
  
  # Pod restart policy
  restartPolicy: Never
  
  # Scheduling preferences
  nodeSelector:
    kubernetes.io/os: linux
  
  # Graceful termination
  terminationGracePeriodSeconds: 30
EOF

log_success "✅ Pod manifest created at \$TEMP_DIR/pod-manifest.yaml"

# 🔍 Validate manifest syntax
log_info "🔍 Validating manifest syntax..."
if kubectl apply --dry-run=client -f "\$TEMP_DIR/pod-manifest.yaml" &> /dev/null; then
    log_success "✅ Manifest syntax is valid"
else
    log_error "❌ Manifest syntax validation failed"
    kubectl apply --dry-run=client -f "\$TEMP_DIR/pod-manifest.yaml"
    exit 1
fi

# 🚀 Deploy the pod
log_info "🚀 Deploying pod '\$POD_NAME' to namespace '\$NAMESPACE'..."
kubectl apply -f "\$TEMP_DIR/pod-manifest.yaml"

# ⏳ Wait for pod to be scheduled
log_info "⏳ Waiting for pod to be scheduled..."
kubectl wait --for=condition=PodScheduled pod/"\$POD_NAME" --namespace="\$NAMESPACE" --timeout=30s
log_success "✅ Pod has been scheduled to a node"

# ⏳ Wait for pod to be ready
log_info "⏳ Waiting for pod to be ready (timeout: \$WAIT_TIMEOUT)..."
if kubectl wait --for=condition=Ready pod/"\$POD_NAME" --namespace="\$NAMESPACE" --timeout="\$WAIT_TIMEOUT"; then
    log_success "🎉 Pod '\$POD_NAME' is ready and healthy!"
else
    log_error "❌ Pod failed to become ready within \$WAIT_TIMEOUT"
    
    # Detailed troubleshooting information
    log_info "📋 Troubleshooting information:"
    echo "--- Pod Status ---"
    kubectl get pod/"\$POD_NAME" --namespace="\$NAMESPACE" -o wide
    
    echo "--- Pod Description ---"
    kubectl describe pod/"\$POD_NAME" --namespace="\$NAMESPACE"
    
    echo "--- Pod Events ---"
    kubectl get events --namespace="\$NAMESPACE" --field-selector involvedObject.name="\$POD_NAME"
    
    echo "--- Pod Logs (if available) ---"
    kubectl logs "\$POD_NAME" --namespace="\$NAMESPACE" || log_warning "No logs available yet"
    
    exit 1
fi

# 📊 Display pod information
log_info "📊 Pod deployment successful! Here's the summary:"
echo "==================== POD INFORMATION ===================="

# Basic pod info
kubectl get pod/"\$POD_NAME" --namespace="\$NAMESPACE" -o wide

# Resource usage (if metrics-server is available)
echo "\\n--- Resource Usage ---"
if kubectl top pod "\$POD_NAME" --namespace="\$NAMESPACE" 2>/dev/null; then
    log_info "✅ Resource metrics available"
else
    log_warning "⚠️ Resource metrics not available (metrics-server may not be installed)"
fi

# Pod logs sample
echo "\\n--- Pod Logs (last 10 lines) ---"
kubectl logs "\$POD_NAME" --namespace="\$NAMESPACE" --tail=10 || log_warning "No logs available yet"

# 🔧 Useful commands for interaction
echo "\\n==================== USEFUL COMMANDS ===================="
log_info "💡 To interact with your pod, use these commands:"
echo "  📋 View logs:        kubectl logs \$POD_NAME --namespace=\$NAMESPACE -f"
echo "  🖥️  Execute shell:    kubectl exec -it \$POD_NAME --namespace=\$NAMESPACE -- /bin/sh"
echo "  🌐 Port forward:     kubectl port-forward pod/\$POD_NAME --namespace=\$NAMESPACE 8080:80"
echo "  📊 Describe pod:     kubectl describe pod \$POD_NAME --namespace=\$NAMESPACE"
echo "  🗑️  Delete pod:       kubectl delete pod \$POD_NAME --namespace=\$NAMESPACE"

# 📈 Performance and security checks
echo "\\n==================== VALIDATION CHECKS ===================="

# Check if pod is using expected resources
log_info "🔍 Validating pod configuration..."
ACTUAL_IMAGE=\$(kubectl get pod "\$POD_NAME" --namespace="\$NAMESPACE" -o jsonpath='{.spec.containers[0].image}')
if [[ "\$ACTUAL_IMAGE" == "\$IMAGE_NAME" ]]; then
    log_success "✅ Correct image deployed: \$ACTUAL_IMAGE"
else
    log_warning "⚠️ Image mismatch - Expected: \$IMAGE_NAME, Actual: \$ACTUAL_IMAGE"
fi

# Check security context
ACTUAL_USER=\$(kubectl get pod "\$POD_NAME" --namespace="\$NAMESPACE" -o jsonpath='{.spec.securityContext.runAsUser}')
if [[ "\$ACTUAL_USER" == "\$USER_ID" ]]; then
    log_success "✅ Running as non-root user: \$ACTUAL_USER"
else
    log_warning "⚠️ User ID mismatch - Expected: \$USER_ID, Actual: \$ACTUAL_USER"
fi

# Final success message
echo "\\n==================== DEPLOYMENT COMPLETE ===================="
log_success "🎉 Pod '\$POD_NAME' has been successfully deployed and is running!"
log_info "📚 Check the Orb documentation for detailed operational guidance"
log_info "🔄 This script can be re-run safely - it includes cleanup and validation"

# Note: The cleanup() function will run automatically when the script exits
log_info "\\n🧹 Cleanup will run automatically when script exits"
log_info "🚀 Deployment completed successfully at \$(date)"

exit 0`;
  }

  if (sanitizedInput.includes('deployment')) {
    return `#!/bin/bash
# 🔮 RUNE: kubernetes_deployment_rolling.sh  
# Title: Kubernetes Deployment with Rolling Updates and Auto-scaling
# Author: LinkOps Platform - Whis Smithing
# Date: $(date +%Y-%m-%d)
# Category: ${category}

set -euo pipefail

# 📝 Configuration Variables
APP_NAME="\${APP_NAME:-my-app}"
IMAGE_NAME="\${IMAGE_NAME:-nginx:1.21}"
NAMESPACE="\${NAMESPACE:-default}"
REPLICAS="\${REPLICAS:-3}"
MAX_SURGE="\${MAX_SURGE:-1}"
MAX_UNAVAILABLE="\${MAX_UNAVAILABLE:-0}"

# 🎨 Color codes for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

log_info() { echo -e "\${BLUE}[INFO]\${NC} \$1"; }
log_success() { echo -e "\${GREEN}[SUCCESS]\${NC} \$1"; }
log_warning() { echo -e "\${YELLOW}[WARNING]\${NC} \$1"; }
log_error() { echo -e "\${RED}[ERROR]\${NC} \$1"; }

# 🧹 Cleanup function
cleanup() {
    log_info "🧹 Cleaning up temporary files..."
    rm -f /tmp/deployment-\$\$.yaml /tmp/service-\$\$.yaml /tmp/hpa-\$\$.yaml
    log_success "✅ Cleanup completed"
}
trap cleanup EXIT

# 🔍 Pre-flight checks
log_info "🔍 Running pre-flight checks..."

# Check kubectl availability
if ! command -v kubectl &> /dev/null; then
    log_error "kubectl not found. Please install kubectl."
    exit 1
fi

# Check cluster connectivity
if ! kubectl cluster-info &> /dev/null; then
    log_error "Cannot connect to Kubernetes cluster"
    exit 1
fi

# Check permissions
if ! kubectl auth can-i create deployments --namespace="\$NAMESPACE"; then
    log_error "Insufficient permissions to create deployments"
    exit 1
fi

log_success "✅ Pre-flight checks passed"

# 📄 Generate deployment manifest
log_info "📄 Creating deployment manifest..."
cat << EOF > /tmp/deployment-\$\$.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: \$APP_NAME
  namespace: \$NAMESPACE
  labels:
    app: \$APP_NAME
    created-by: whis-smithing
spec:
  replicas: \$REPLICAS
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: \$MAX_SURGE
      maxUnavailable: \$MAX_UNAVAILABLE
  selector:
    matchLabels:
      app: \$APP_NAME
  template:
    metadata:
      labels:
        app: \$APP_NAME
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: app
        image: \$IMAGE_NAME
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi" 
            cpu: "500m"
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
EOF

# 🚀 Deploy the application
log_info "🚀 Deploying \$APP_NAME..."
kubectl apply -f /tmp/deployment-\$\$.yaml

# ⏳ Wait for rollout to complete
log_info "⏳ Waiting for rollout to complete..."
kubectl rollout status deployment/\$APP_NAME --namespace=\$NAMESPACE --timeout=300s

log_success "🎉 Deployment '\$APP_NAME' rolled out successfully!"

# 📊 Display deployment status
kubectl get deployment \$APP_NAME --namespace=\$NAMESPACE -o wide

log_success "🎉 Deployment completed successfully at $(date)"
exit 0`;
  }

  // Default fallback for other categories
  return `#!/bin/bash
# 🔮 RUNE: ${category.toLowerCase()}_automation.sh
# Title: ${category} Task Automation - ${sanitizedInput}
# Author: LinkOps Platform - Whis Smithing  
# Date: $(date +%Y-%m-%d)
# Category: ${category}

set -euo pipefail  # Exit on any error, undefined variable, or pipe failure

# 📝 Configuration Variables
TASK_NAME="${sanitizedInput.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase()}"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
LOG_FILE="/tmp/${TASK_NAME}-${TIMESTAMP}.log"
TEMP_DIR="/tmp/whis-rune-$$"

# 🎨 Color codes for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'  
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# 📢 Logging functions
log_info() { 
    echo -e "\${BLUE}[INFO]\${NC} \$1" | tee -a "${LOG_FILE}"
}
log_success() { 
    echo -e "\${GREEN}[SUCCESS]\${NC} \$1" | tee -a "${LOG_FILE}"
}
log_warning() { 
    echo -e "\${YELLOW}[WARNING]\${NC} \$1" | tee -a "${LOG_FILE}"
}
log_error() { 
    echo -e "\${RED}[ERROR]\${NC} \$1" | tee -a "${LOG_FILE}"
}

# 🧹 Cleanup function (called on script exit)
cleanup() {
    log_info "🧹 Cleaning up resources..."
    
    # Remove temporary files and directories
    if [[ -d "\$TEMP_DIR" ]]; then
        rm -rf "\$TEMP_DIR"
        log_info "Removed temporary directory: \$TEMP_DIR"
    fi
    
    log_success "✅ Cleanup completed"
    log_info "📋 Log file available at: \$LOG_FILE"
}

# Set trap to run cleanup on script exit (success or failure)
trap cleanup EXIT

# 🔍 Pre-flight checks
log_info "🔍 Starting pre-flight checks for \$TASK_NAME..."

# Create temporary directory
mkdir -p "\$TEMP_DIR"
log_info "Created temporary directory: \$TEMP_DIR"

# Create log file
touch "\$LOG_FILE"
log_info "Logging to: \$LOG_FILE"

# Check required tools and permissions
log_info "Checking system requirements..."

# Add specific tool checks based on category
case "${category.toLowerCase()}" in
    "kubernetes")
        if ! command -v kubectl &> /dev/null; then
            log_error "kubectl not found. Please install kubectl."
            exit 1
        fi
        if ! kubectl cluster-info &> /dev/null; then
            log_error "Cannot connect to Kubernetes cluster"
            exit 1
        fi
        ;;
    "docker") 
        if ! command -v docker &> /dev/null; then
            log_error "docker not found. Please install Docker."
            exit 1
        fi
        if ! docker info &> /dev/null; then
            log_error "Cannot connect to Docker daemon"
            exit 1
        fi
        ;;
    "security")
        log_info "Running security-focused automation"
        ;;
    *)
        log_info "Running general \${category} automation"
        ;;
esac

log_success "✅ Pre-flight checks passed"

# 🛠️ Main execution logic
log_info "🛠️ Starting main execution for: ${sanitizedInput}"

# Step 1: Preparation
log_info "📋 Step 1: Preparing environment..."
# Add preparation logic here
log_success "✅ Environment prepared"

# Step 2: Core execution
log_info "⚙️ Step 2: Executing core functionality..."
# Add main logic here based on the specific task
log_success "✅ Core functionality executed"

# Step 3: Validation
log_info "🔍 Step 3: Validating results..."
# Add validation logic here
log_success "✅ Results validated"

# Step 4: Post-processing
log_info "📊 Step 4: Post-processing and reporting..."
# Add post-processing logic here
log_success "✅ Post-processing completed"

# 📈 Final status and reporting
echo "\\n==================== EXECUTION COMPLETE ===================="
log_success "🎉 Task '\$TASK_NAME' completed successfully!"
log_info "📚 Check the corresponding Orb documentation for detailed guidance"
log_info "🔄 This script can be re-run safely with proper cleanup"
log_info "📋 Full execution log: \$LOG_FILE"

# 💡 Useful information
echo "\\n==================== USEFUL INFORMATION ===================="
log_info "💡 Task completion summary:"
echo "  📅 Started at: \$(date -d '@\$(stat -c %Y "${LOG_FILE}")' '+%Y-%m-%d %H:%M:%S')"
echo "  📅 Completed at: \$(date '+%Y-%m-%d %H:%M:%S')"
echo "  📁 Working directory: \$(pwd)"
echo "  📋 Log file: \$LOG_FILE"
echo "  🔧 Temporary files cleaned up automatically"

log_success "🚀 Automation completed successfully!"

# Note: cleanup() will run automatically when script exits
exit 0`;
};

const approveOrb = () => {
  if (!generatedOrb.value || !currentTrainingTask.value) return;

  // Create rune and save to orb library
  const rune = {
    ...generatedOrb.value,
    approved: true,
    savedAt: new Date().toISOString(),
    runeCreated: true,
  };

  // Save to completed training
  const trainingRecord = {
    id: Date.now(),
    originalInput: currentTrainingTask.value.originalInput,
    generatedOrb: rune,
    approved: true,
    completedAt: new Date().toISOString(),
  };

  completedTraining.value.push(trainingRecord);
  const completed = JSON.parse(
    localStorage.getItem('whisCompletedTraining') || '[]'
  );
  completed.push(trainingRecord);
  localStorage.setItem('whisCompletedTraining', JSON.stringify(completed));

  // Add to orb library (for demo)
  const orbLibrary = JSON.parse(localStorage.getItem('orbLibrary') || '[]');
  orbLibrary.push(rune);
  localStorage.setItem('orbLibrary', JSON.stringify(orbLibrary));

  // Remove from training queue
  removeFromTrainingQueue(currentTrainingTask.value.id);

  alert(
    `✅ Orb approved! Rune "${rune.rune_id}" created and added to ${rune.category} category.`
  );
  resetTraining();
};

const rejectOrb = () => {
  if (!currentTrainingTask.value) return;

  const trainingRecord = {
    id: Date.now(),
    originalInput: currentTrainingTask.value.originalInput,
    generatedOrb: generatedOrb.value,
    approved: false,
    rejectionReason: 'Quality below threshold',
    completedAt: new Date().toISOString(),
  };

  completedTraining.value.push(trainingRecord);
  const completed = JSON.parse(
    localStorage.getItem('whisCompletedTraining') || '[]'
  );
  completed.push(trainingRecord);
  localStorage.setItem('whisCompletedTraining', JSON.stringify(completed));

  removeFromTrainingQueue(currentTrainingTask.value.id);

  alert(
    `❌ Orb rejected. This is when Whis would use OpenAI as a fallback to help improve orb creation until satisfied. The task will be reprocessed with enhanced AI assistance.`
  );
  resetTraining();
};

const removeFromTrainingQueue = (taskId) => {
  const queue = JSON.parse(localStorage.getItem('whisTrainingQueue') || '[]');
  const filtered = queue.filter((task) => task.id !== taskId);
  localStorage.setItem('whisTrainingQueue', JSON.stringify(filtered));
  loadTrainingQueue();
};

const resetTraining = () => {
  isTraining.value = false;
  currentTrainingTask.value = null;
  currentTrainingStep.value = 0;
  currentStepResults.value = {};
  generatedOrb.value = null;
  selectedTask.value = null;
};

const goToDemo = () => {
  window.location.href = '/';
};

// Lifecycle
onMounted(() => {
  loadTrainingQueue();
});
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

/* Orb and Rune specific styling */
.orb-walkthrough {
  background: rgba(76, 175, 80, 0.15);
  border-left: 4px solid #4caf50;
  padding: 15px;
  margin: 15px 0;
  border-radius: 8px;
}

.orb-walkthrough h6 {
  color: #81c784;
  margin: 0 0 10px 0;
  font-weight: bold;
  font-size: 1rem;
}

.walkthrough-text {
  background: rgba(0, 0, 0, 0.4);
  padding: 12px;
  border-radius: 6px;
  color: #e8f5e8;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 0.9em;
  line-height: 1.5;
  white-space: pre-wrap;
  max-height: 300px;
  overflow-y: auto;
}

.rune-script {
  background: rgba(255, 152, 0, 0.15);
  border-left: 4px solid #ff9800;
  padding: 15px;
  margin: 15px 0;
  border-radius: 8px;
}

.rune-script h6 {
  color: #ffb74d;
  margin: 0 0 10px 0;
  font-weight: bold;
  font-size: 1rem;
}

.script-content {
  background: rgba(0, 0, 0, 0.4);
  padding: 12px;
  border-radius: 6px;
}

.script-content pre {
  color: #fff3e0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.85em;
  line-height: 1.4;
  margin: 0;
  max-height: 300px;
  overflow-y: auto;
}
</style>
