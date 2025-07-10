<template>
  <div class="audit-page">
    <div class="page-header">
      <h1 class="page-title">
        Security Audit
      </h1>
      <p class="page-subtitle">
        Comprehensive security analysis and code quality assessment
      </p>
    </div>

    <!-- Audit Input -->
    <section class="input-section">
      <h2 class="section-title">
        Repository Analysis
      </h2>
      <AuditInput
        :loading="isAuditing"
        @submit="runAudit"
      />
    </section>

    <!-- Audit Results -->
    <section
      v-if="auditResults"
      class="results-section"
    >
      <h2 class="section-title">
        Audit Results
      </h2>
      <AuditResults
        :results="auditResults"
        :loading="isAuditing"
      />
    </section>

    <!-- Quick Actions -->
    <section class="actions-section">
      <h2 class="section-title">
        Quick Actions
      </h2>
      <div class="action-buttons">
        <button
          class="action-btn primary"
          :disabled="isAuditing"
          @click="runFullAudit"
        >
          <span class="btn-icon">🔍</span>
          Full Security Scan
        </button>
        <button
          class="action-btn secondary"
          :disabled="isAuditing"
          @click="runLintCheck"
        >
          <span class="btn-icon">📋</span>
          Code Quality Check
        </button>
        <button
          class="action-btn secondary"
          :disabled="isAuditing"
          @click="runDependencyScan"
        >
          <span class="btn-icon">📦</span>
          Dependency Analysis
        </button>
        <button
          class="action-btn secondary"
          :disabled="!auditResults"
          @click="exportResults"
        >
          <span class="btn-icon">📄</span>
          Export Report
        </button>
      </div>
    </section>

    <!-- Recent Audits -->
    <section
      v-if="recentAudits.length > 0"
      class="recent-section"
    >
      <h2 class="section-title">
        Recent Audits
      </h2>
      <div class="recent-audits">
        <div
          v-for="audit in recentAudits"
          :key="audit.id"
          class="audit-card"
          @click="loadAudit(audit)"
        >
          <div class="audit-header">
            <h3>{{ audit.repository }}</h3>
            <span class="audit-date">{{ formatDate(audit.date) }}</span>
          </div>
          <div class="audit-summary">
            <div class="summary-item">
              <span class="label">Security Score:</span>
              <span
                class="value"
                :class="getScoreClass(audit.securityScore)"
              >
                {{ audit.securityScore }}/100
              </span>
            </div>
            <div class="summary-item">
              <span class="label">Issues Found:</span>
              <span class="value">{{ audit.issuesCount }}</span>
            </div>
            <div class="summary-item">
              <span class="label">Status:</span>
              <span
                class="status"
                :class="audit.status"
              >
                {{ audit.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import AuditInput from '../components/AuditInput.vue'
import AuditResults from '../components/AuditResults.vue'

export default {
  name: 'Audit',
  components: {
    AuditInput,
    AuditResults
  },
  data() {
    return {
      isAuditing: false,
      auditResults: null,
      recentAudits: [
        {
          id: 1,
          repository: 'linkops/mlops-platform',
          date: new Date('2024-01-15'),
          securityScore: 85,
          issuesCount: 12,
          status: 'completed'
        },
        {
          id: 2,
          repository: 'linkops/frontend-ui',
          date: new Date('2024-01-14'),
          securityScore: 92,
          issuesCount: 5,
          status: 'completed'
        },
        {
          id: 3,
          repository: 'linkops/backend-api',
          date: new Date('2024-01-13'),
          securityScore: 78,
          issuesCount: 18,
          status: 'completed'
        }
      ]
    }
  },
  methods: {
    async runAudit(repositoryUrl) {
      this.isAuditing = true
      this.auditResults = null
      try {
        await new Promise(resolve => setTimeout(resolve, 3000))
        this.auditResults = {
          repository: repositoryUrl,
          timestamp: new Date(),
          securityScore: Math.floor(Math.random() * 30) + 70,
          codeQualityScore: Math.floor(Math.random() * 30) + 70,
          dependencyScore: Math.floor(Math.random() * 30) + 70,
          issues: [
            {
              id: 1,
              type: 'security',
              severity: 'high',
              title: 'SQL Injection Vulnerability',
              description: 'Potential SQL injection in user input validation',
              file: 'src/api/users.js:45',
              line: 45,
              recommendation: 'Use parameterized queries and input validation'
            },
            {
              id: 2,
              type: 'security',
              severity: 'medium',
              title: 'Hardcoded API Key',
              description: 'API key found in source code',
              file: 'config/database.js:12',
              line: 12,
              recommendation: 'Move API keys to environment variables'
            },
            {
              id: 3,
              type: 'quality',
              severity: 'low',
              title: 'Unused Variable',
              description: 'Variable declared but never used',
              file: 'src/utils/helpers.js:23',
              line: 23,
              recommendation: 'Remove unused variable or use it'
            }
          ],
          dependencies: [
            {
              name: 'lodash',
              version: '4.17.21',
              status: 'up-to-date',
              vulnerabilities: 0
            },
            {
              name: 'express',
              version: '4.18.2',
              status: 'outdated',
              vulnerabilities: 2
            },
            {
              name: 'axios',
              version: '1.6.2',
              status: 'up-to-date',
              vulnerabilities: 0
            }
          ]
        }
        this.recentAudits.unshift({
          id: Date.now(),
          repository: repositoryUrl,
          date: new Date(),
          securityScore: this.auditResults.securityScore,
          issuesCount: this.auditResults.issues.length,
          status: 'completed'
        })
      } catch (_error) {
        this.auditResults = {
          error: 'Audit failed. Please try again.'
        }
      } finally {
        this.isAuditing = false
      }
    },
    async runFullAudit() {
      const sampleRepo = 'https://github.com/linkops/sample-repo'
      await this.runAudit(sampleRepo)
    },
    async runLintCheck() {
      this.isAuditing = true
      try {
        await new Promise(resolve => setTimeout(resolve, 2000))
        this.auditResults = {
          repository: 'Current Repository',
          timestamp: new Date(),
          codeQualityScore: 88,
          issues: [
            {
              id: 1,
              type: 'quality',
              severity: 'low',
              title: 'Missing Semicolon',
              description: 'Missing semicolon at end of statement',
              file: 'src/components/Button.js:15',
              line: 15,
              recommendation: 'Add semicolon at end of statement'
            }
          ]
        }
      } finally {
        this.isAuditing = false
      }
    },
    async runDependencyScan() {
      this.isAuditing = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1500))
        this.auditResults = {
          repository: 'Current Repository',
          timestamp: new Date(),
          dependencyScore: 95,
          dependencies: [
            {
              name: 'vue',
              version: '3.4.21',
              status: 'up-to-date',
              vulnerabilities: 0
            },
            {
              name: 'axios',
              version: '1.6.8',
              status: 'up-to-date',
              vulnerabilities: 0
            }
          ]
        }
      } finally {
        this.isAuditing = false
      }
    },
    exportResults() {
      if (!this.auditResults) return
      const dataStr = JSON.stringify(this.auditResults, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `audit-report-${new Date().toISOString().split('T')[0]}.json`
      link.click()
    },
    loadAudit(audit) {
      // Load the specific audit results
    },
    formatDate(date) {
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }).format(date)
    },
    getScoreClass(score) {
      if (score >= 90) return 'excellent'
      if (score >= 80) return 'good'
      if (score >= 70) return 'fair'
      return 'poor'
    }
  }
}
</script>
<style scoped>
.audit-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 3rem;
  font-weight: bold;
  background: linear-gradient(45deg, #00d4ff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1.2rem;
  color: #888;
  margin: 0;
}

.input-section,
.results-section,
.actions-section,
.recent-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2rem;
  color: #00d4ff;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #00d4ff;
  padding-bottom: 0.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.primary {
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  color: white;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.action-btn.secondary {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  color: #00d4ff;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

.recent-audits {
  display: grid;
  gap: 1.5rem;
}

.audit-card {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.3s ease;
}

.audit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
}

.audit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.audit-header h3 {
  margin: 0;
  color: #00d4ff;
  font-size: 1.2rem;
}

.audit-date {
  color: #888;
  font-size: 0.9rem;
}

.audit-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
}

.value {
  font-size: 1.1rem;
  font-weight: bold;
  color: #e0e0e0;
}

.value.excellent {
  color: #00ff00;
}

.value.good {
  color: #00d4ff;
}

.value.fair {
  color: #ffaa00;
}

.value.poor {
  color: #ff0000;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status.completed {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
  border: 1px solid #00ff00;
}

.status.processing {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
  border: 1px solid #ffaa00;
}

.status.failed {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
  border: 1px solid #ff0000;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-btn {
    justify-content: center;
  }
  
  .audit-summary {
    grid-template-columns: 1fr;
  }
}
</style>
