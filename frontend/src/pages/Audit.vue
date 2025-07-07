<template>
  <div class="audit-container">
    <!-- Header -->
    <div class="audit-header">
      <h1 class="audit-title">
        <span class="title-glow">Audit</span> Guardian
      </h1>
      <div class="audit-status">
        <div class="status-indicator">
          <div class="status-dot active"></div>
          <span>Guardian Active</span>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="audit-content">
      <!-- Input Section -->
      <div class="input-section">
        <div class="input-card">
          <h2>🔍 Repository Analysis</h2>
          <p class="input-description">
            Enter a public repository URL to analyze its security posture, code quality, and get improvement recommendations.
          </p>
          
          <div class="url-input-group">
            <label>Repository URL:</label>
            <div class="url-input-wrapper">
              <input 
                v-model="repoUrl" 
                type="url" 
                placeholder="https://github.com/username/repository"
                class="url-input"
              >
              <button 
                class="btn-primary" 
                @click="startAudit"
                :disabled="!repoUrl || isAuditing"
              >
                <span v-if="!isAuditing">🔍 Start Audit</span>
                <span v-else>⏳ Auditing...</span>
              </button>
            </div>
          </div>

          <!-- Quick Examples -->
          <div class="examples-section">
            <h3>Quick Examples:</h3>
            <div class="example-buttons">
              <button 
                v-for="example in examples" 
                :key="example.url"
                class="example-btn"
                @click="useExample(example.url)"
              >
                {{ example.name }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Audit Progress -->
      <div v-if="isAuditing" class="progress-section">
        <div class="progress-card">
          <h2>📊 Audit Progress</h2>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: auditProgress + '%' }"></div>
          </div>
          <p class="progress-text">{{ currentStep }}</p>
          
          <div class="audit-steps">
            <div 
              v-for="step in auditSteps" 
              :key="step.id"
              :class="['audit-step', step.status]"
            >
              <div class="step-icon">{{ step.icon }}</div>
              <div class="step-info">
                <h3>{{ step.name }}</h3>
                <p>{{ step.description }}</p>
              </div>
              <div class="step-status">
                <span class="status-badge" :class="step.status">
                  {{ step.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="auditResults" class="results-section">
        <div class="results-card">
          <h2>📋 Audit Results</h2>
          
          <!-- Repository Info -->
          <div class="repo-info">
            <div class="repo-header">
              <h3>{{ auditResults.repoName }}</h3>
              <div class="repo-stats">
                <span class="stat">⭐ {{ auditResults.stars }}</span>
                <span class="stat">🔀 {{ auditResults.forks }}</span>
                <span class="stat">👀 {{ auditResults.watchers }}</span>
              </div>
            </div>
            <p class="repo-description">{{ auditResults.description }}</p>
          </div>

          <!-- Security Score -->
          <div class="security-score">
            <h3>🛡️ Security Score</h3>
            <div class="score-display">
              <div class="score-circle" :style="{ '--score': auditResults.securityScore }">
                <span class="score-value">{{ auditResults.securityScore }}/100</span>
              </div>
              <div class="score-breakdown">
                <div class="score-item">
                  <span class="score-label">Vulnerabilities:</span>
                  <span class="score-value" :class="getScoreClass(auditResults.vulnerabilities)">
                    {{ auditResults.vulnerabilities }}
                  </span>
                </div>
                <div class="score-item">
                  <span class="score-label">Dependencies:</span>
                  <span class="score-value" :class="getScoreClass(auditResults.dependencies)">
                    {{ auditResults.dependencies }}
                  </span>
                </div>
                <div class="score-item">
                  <span class="score-label">Code Quality:</span>
                  <span class="score-value" :class="getScoreClass(auditResults.codeQuality)">
                    {{ auditResults.codeQuality }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Issues Found -->
          <div class="issues-section">
            <h3>🚨 Issues Found</h3>
            <div class="issues-tabs">
              <button 
                v-for="category in issueCategories" 
                :key="category.id"
                :class="['issue-tab', { active: activeIssueTab === category.id }]"
                @click="activeIssueTab = category.id"
              >
                {{ category.label }}
                <span class="issue-count">{{ getIssueCount(category.id) }}</span>
              </button>
            </div>
            
            <div class="issues-list">
              <div 
                v-for="issue in getIssuesByCategory(activeIssueTab)" 
                :key="issue.id"
                :class="['issue-item', issue.severity]"
              >
                <div class="issue-header">
                  <div class="issue-severity">
                    <span class="severity-dot" :class="issue.severity"></span>
                    {{ issue.severity.toUpperCase() }}
                  </div>
                  <div class="issue-location">{{ issue.location }}</div>
                </div>
                <h4>{{ issue.title }}</h4>
                <p>{{ issue.description }}</p>
                <div class="issue-recommendation">
                  <strong>Recommendation:</strong> {{ issue.recommendation }}
                </div>
              </div>
            </div>
          </div>

          <!-- Recommendations -->
          <div class="recommendations-section">
            <h3>💡 Improvement Recommendations</h3>
            <div class="recommendations-list">
              <div 
                v-for="rec in auditResults.recommendations" 
                :key="rec.id"
                class="recommendation-item"
              >
                <div class="rec-icon">{{ rec.icon }}</div>
                <div class="rec-content">
                  <h4>{{ rec.title }}</h4>
                  <p>{{ rec.description }}</p>
                  <div class="rec-priority">
                    <span class="priority-badge" :class="rec.priority">
                      {{ rec.priority }} Priority
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <button class="btn-primary" @click="generateReport">
              📄 Generate Full Report
            </button>
            <button class="btn-secondary" @click="exportResults">
              📊 Export Results
            </button>
            <button class="btn-secondary" @click="shareResults">
              🔗 Share Results
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Audit',
  data() {
    return {
      repoUrl: '',
      isAuditing: false,
      auditProgress: 0,
      currentStep: 'Initializing audit...',
      activeIssueTab: 'security',
      auditResults: null,
      auditSteps: [
        {
          id: 1,
          name: 'Repository Access',
          description: 'Validating repository access and permissions',
          icon: '🔐',
          status: 'pending'
        },
        {
          id: 2,
          name: 'Security Scan',
          description: 'Scanning for vulnerabilities and security issues',
          icon: '🛡️',
          status: 'pending'
        },
        {
          id: 3,
          name: 'Dependency Analysis',
          description: 'Analyzing dependencies and their security',
          icon: '📦',
          status: 'pending'
        },
        {
          id: 4,
          name: 'Code Quality',
          description: 'Assessing code quality and best practices',
          icon: '📝',
          status: 'pending'
        },
        {
          id: 5,
          name: 'Infrastructure',
          description: 'Reviewing infrastructure and deployment',
          icon: '🏗️',
          status: 'pending'
        },
        {
          id: 6,
          name: 'Generate Report',
          description: 'Compiling comprehensive audit report',
          icon: '📋',
          status: 'pending'
        }
      ],
      examples: [
        { name: 'React App', url: 'https://github.com/facebook/react' },
        { name: 'Vue.js', url: 'https://github.com/vuejs/vue' },
        { name: 'Node.js', url: 'https://github.com/nodejs/node' },
        { name: 'Python', url: 'https://github.com/python/cpython' }
      ],
      issueCategories: [
        { id: 'security', label: 'Security' },
        { id: 'quality', label: 'Code Quality' },
        { id: 'dependencies', label: 'Dependencies' },
        { id: 'performance', label: 'Performance' }
      ]
    }
  },
  methods: {
    useExample(url) {
      this.repoUrl = url;
    },
    async startAudit() {
      if (!this.repoUrl) {
        alert('Please enter a repository URL');
        return;
      }

      this.isAuditing = true;
      this.auditProgress = 0;
      this.auditResults = null;

      // Simulate audit process
      for (let i = 0; i < this.auditSteps.length; i++) {
        const step = this.auditSteps[i];
        step.status = 'running';
        this.currentStep = step.description;
        this.auditProgress = ((i + 1) / this.auditSteps.length) * 100;
        
        await this.delay(2000);
        
        step.status = 'completed';
        
        if (i === this.auditSteps.length - 1) {
          this.generateMockResults();
        }
      }
      
      this.isAuditing = false;
    },
    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    generateMockResults() {
      this.auditResults = {
        repoName: 'Example Repository',
        description: 'A sample repository for demonstration purposes',
        stars: 1234,
        forks: 567,
        watchers: 89,
        securityScore: 78,
        vulnerabilities: 3,
        dependencies: 85,
        codeQuality: 92,
        issues: [
          {
            id: 1,
            category: 'security',
            severity: 'high',
            title: 'SQL Injection Vulnerability',
            description: 'Potential SQL injection in user input handling',
            location: 'src/database.js:45',
            recommendation: 'Use parameterized queries or an ORM'
          },
          {
            id: 2,
            category: 'security',
            severity: 'medium',
            title: 'Weak Password Policy',
            description: 'Password requirements are too lenient',
            location: 'src/auth.js:23',
            recommendation: 'Implement stronger password requirements'
          },
          {
            id: 3,
            category: 'quality',
            severity: 'low',
            title: 'Code Duplication',
            description: 'Similar code patterns found in multiple files',
            location: 'src/utils.js:12',
            recommendation: 'Extract common functionality into reusable functions'
          }
        ],
        recommendations: [
          {
            id: 1,
            icon: '🔒',
            title: 'Implement Security Headers',
            description: 'Add security headers to prevent common web vulnerabilities',
            priority: 'high'
          },
          {
            id: 2,
            icon: '📦',
            title: 'Update Dependencies',
            description: 'Update outdated dependencies to latest secure versions',
            priority: 'medium'
          },
          {
            id: 3,
            icon: '🧪',
            title: 'Add Unit Tests',
            description: 'Increase test coverage to improve code reliability',
            priority: 'low'
          }
        ]
      };
    },
    getScoreClass(score) {
      if (score >= 90) return 'excellent';
      if (score >= 70) return 'good';
      if (score >= 50) return 'fair';
      return 'poor';
    },
    getIssueCount(categoryId) {
      if (!this.auditResults) return 0;
      return this.auditResults.issues.filter(issue => issue.category === categoryId).length;
    },
    getIssuesByCategory(categoryId) {
      if (!this.auditResults) return [];
      return this.auditResults.issues.filter(issue => issue.category === categoryId);
    },
    generateReport() {
      alert('Generating comprehensive audit report...');
    },
    exportResults() {
      alert('Exporting audit results...');
    },
    shareResults() {
      alert('Sharing audit results...');
    }
  }
}
</script>

<style scoped>
.audit-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  padding: 2rem;
}

.audit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.audit-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.title-glow {
  background: linear-gradient(45deg, #00ff88, #00ffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
}

.audit-status {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ff4444;
  animation: pulse 2s infinite;
}

.status-dot.active {
  background: #00ff88;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.audit-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.input-card, .progress-card, .results-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.input-card h2, .progress-card h2, .results-card h2 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.input-description {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1.5rem;
}

.url-input-group {
  margin-bottom: 1.5rem;
}

.url-input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

.url-input-wrapper {
  display: flex;
  gap: 1rem;
}

.url-input {
  flex: 1;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #fff;
  font-family: inherit;
}

.url-input:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
}

.examples-section {
  margin-top: 1.5rem;
}

.examples-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
}

.example-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.example-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.example-btn:hover {
  background: rgba(0, 255, 136, 0.2);
  border-color: #00ff88;
}

/* Progress Section */
.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ff88, #00ffff);
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1.5rem;
}

.audit-steps {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.audit-step {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.audit-step.running {
  border-color: #ffaa00;
  background: rgba(255, 170, 0, 0.1);
  animation: pulse 1s infinite;
}

.audit-step.completed {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.1);
}

.step-icon {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
}

.step-info {
  flex: 1;
}

.step-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.step-info p {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

/* Results Section */
.repo-info {
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
}

.repo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.repo-header h3 {
  margin: 0;
  font-size: 1.3rem;
}

.repo-stats {
  display: flex;
  gap: 1rem;
}

.stat {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.repo-description {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
}

/* Security Score */
.security-score {
  margin-bottom: 2rem;
}

.security-score h3 {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: conic-gradient(
    #00ff88 calc(var(--score) * 3.6deg),
    rgba(255, 255, 255, 0.1) calc(var(--score) * 3.6deg)
  );
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.score-circle::before {
  content: '';
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
}

.score-value {
  position: relative;
  font-size: 1.2rem;
  font-weight: 700;
}

.score-breakdown {
  flex: 1;
}

.score-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.score-label {
  color: rgba(255, 255, 255, 0.8);
}

.score-value.excellent { color: #00ff88; }
.score-value.good { color: #00ffff; }
.score-value.fair { color: #ffaa00; }
.score-value.poor { color: #ff4444; }

/* Issues Section */
.issues-section {
  margin-bottom: 2rem;
}

.issues-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
}

.issues-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.issue-tab {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.issue-tab.active {
  background: linear-gradient(45deg, #00ff88, #00ffff);
  color: #000;
  border-color: transparent;
}

.issue-count {
  background: rgba(0, 0, 0, 0.2);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.issue-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border-left: 4px solid rgba(255, 255, 255, 0.2);
}

.issue-item.high {
  border-left-color: #ff4444;
}

.issue-item.medium {
  border-left-color: #ffaa00;
}

.issue-item.low {
  border-left-color: #00ff88;
}

.issue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.issue-severity {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.severity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.severity-dot.high { background: #ff4444; }
.severity-dot.medium { background: #ffaa00; }
.severity-dot.low { background: #00ff88; }

.issue-location {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

.issue-item h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.issue-item p {
  margin: 0 0 0.5rem 0;
  color: rgba(255, 255, 255, 0.8);
}

.issue-recommendation {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

/* Recommendations */
.recommendations-section {
  margin-bottom: 2rem;
}

.recommendations-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
}

.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recommendation-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.rec-icon {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
}

.rec-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.rec-content p {
  margin: 0 0 0.5rem 0;
  color: rgba(255, 255, 255, 0.8);
}

.priority-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.priority-badge.high {
  background: rgba(255, 68, 68, 0.2);
  color: #ff4444;
}

.priority-badge.medium {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
}

.priority-badge.low {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(45deg, #00ff88, #00ffff);
  color: #000;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-primary:hover, .btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Status Badges */
.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.pending {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.7);
}

.status-badge.running {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
}

.status-badge.completed {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
}

/* Responsive Design */
@media (max-width: 768px) {
  .audit-container {
    padding: 1rem;
  }
  
  .audit-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .audit-title {
    font-size: 2rem;
  }
  
  .url-input-wrapper {
    flex-direction: column;
  }
  
  .score-display {
    flex-direction: column;
    text-align: center;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .recommendation-item {
    flex-direction: column;
    text-align: center;
  }
}
</style> 