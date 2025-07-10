<template>
  <div class="audit-results">
    <div
      v-if="loading"
      class="loading-state"
    >
      <div class="spinner" />
      <p>Loading audit results...</p>
    </div>
    <div v-else>
      <!-- Summary Section -->
      <div class="summary-grid">
        <div class="summary-card">
          <div class="summary-icon">
            🔒
          </div>
          <div class="summary-content">
            <h3>Security Score</h3>
            <div
              class="score-value"
              :class="getScoreClass(results.securityScore)"
            >
              {{ results.securityScore }}/100
            </div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-icon">
            🧹
          </div>
          <div class="summary-content">
            <h3>Code Quality</h3>
            <div
              class="score-value"
              :class="getScoreClass(results.qualityScore)"
            >
              {{ results.qualityScore }}/100
            </div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-icon">
            📦
          </div>
          <div class="summary-content">
            <h3>Dependencies</h3>
            <div
              class="score-value"
              :class="getScoreClass(results.dependencyScore)"
            >
              {{ results.dependencyScore }}/100
            </div>
          </div>
        </div>
      </div>
      <!-- Issues Section -->
      <div
        v-if="results.issues && results.issues.length > 0"
        class="issues-section"
      >
        <h2 class="section-title">
          Issues Found ({{ results.issues.length }})
        </h2>
        <div class="issues-filters">
          <button
            v-for="severity in ['all', 'high', 'medium', 'low']"
            :key="severity"
            class="filter-btn"
            :class="{ active: activeFilter === severity }"
            @click="activeFilter = severity"
          >
            {{ severity.charAt(0).toUpperCase() + severity.slice(1) }}
            <span class="filter-count">{{ getFilterCount(severity) }}</span>
          </button>
        </div>
        <div class="issues-list">
          <div
            v-for="issue in filteredIssues"
            :key="issue.id"
            class="issue-card"
            :class="issue.severity"
          >
            <div class="issue-header">
              <div class="issue-severity">
                <span class="severity-icon">{{ getSeverityIcon(issue.severity) }}</span>
                <span class="severity-text">{{ issue.severity.toUpperCase() }}</span>
              </div>
              <div class="issue-type">
                {{ issue.type }}
              </div>
            </div>
            <h3 class="issue-title">
              {{ issue.title }}
            </h3>
            <p class="issue-description">
              {{ issue.description }}
            </p>
            <div class="issue-location">
              <span class="location-label">Location:</span>
              <span class="location-file">{{ issue.file }}</span>
              <span class="location-line">Line {{ issue.line }}</span>
            </div>
            <div class="issue-recommendation">
              <span class="recommendation-label">Recommendation:</span>
              <p class="recommendation-text">
                {{ issue.recommendation }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Dependencies Section -->
    <div
      v-if="results.dependencies && results.dependencies.length > 0"
      class="dependencies-section"
    >
      <h2 class="section-title">
        Dependencies Analysis
      </h2>
      <div class="dependencies-table">
        <div class="table-header">
          <div class="header-cell">
            Package
          </div>
          <div class="header-cell">
            Version
          </div>
          <div class="header-cell">
            Status
          </div>
          <div class="header-cell">
            Vulnerabilities
          </div>
        </div>
        <div
          v-for="dep in results.dependencies"
          :key="dep.name"
          class="table-row"
          :class="dep.status"
        >
          <div class="table-cell package-name">
            {{ dep.name }}
          </div>
          <div class="table-cell package-version">
            {{ dep.version }}
          </div>
          <div class="table-cell package-status">
            <span
              class="status-badge"
              :class="dep.status"
            >
              {{ dep.status }}
            </span>
          </div>
          <div class="table-cell vulnerabilities">
            <span v-if="dep.vulnerabilities && dep.vulnerabilities.length > 0">
              {{ dep.vulnerabilities.join(', ') }}
            </span>
            <span v-else>None</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'AuditResults',
  props: {
    results: {
      type: Object,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    hasIssues() {
      return this.results && this.results.issues && this.results.issues.length > 0
    },
    hasDependencies() {
      return this.results && this.results.dependencies && this.results.dependencies.length > 0
    }
  },
  methods: {
    getSeverityClass(severity) {
      switch (severity) {
        case 'high': return 'high-severity'
        case 'medium': return 'medium-severity'
        case 'low': return 'low-severity'
        default: return ''
      }
    },
    getStatusClass(status) {
      switch (status) {
        case 'up-to-date': return 'status-up-to-date'
        case 'outdated': return 'status-outdated'
        default: return ''
      }
    }
  }
}
</script>;
<style scoped>;
.audit-results {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.loading-state,
.error-state {
  text-align: center;
  padding: 3rem 1rem;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(0, 212, 255, 0.3);
  border-top: 4px solid #00d4ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 1rem auto 0;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(0, 212, 255, 0.2);
  transition: all 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
}

.summary-icon {
  font-size: 2.5rem;
  min-width: 60px;
  text-align: center;
}

.summary-content h3 {
  color: #e0e0e0;
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.score-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.score-value.excellent {
  color: #00ff00;
}

.score-value.good {
  color: #00d4ff;
}

.score-value.fair {
  color: #ffaa00;
}

.score-value.poor {
  color: #ff0000;
}

.section-title {
  color: #00d4ff;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  border-bottom: 2px solid #00d4ff;
  padding-bottom: 0.5rem;
}

.issues-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  color: #00d4ff;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn.active {
  background: rgba(0, 212, 255, 0.2);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
}

.filter-count {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 10px;
  padding: 0.2rem 0.5rem;
  font-size: 0.8rem;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.issue-card {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.issue-card.high {
  border-left: 4px solid #ff0000;
}

.issue-card.medium {
  border-left: 4px solid #ffaa00;
}

.issue-card.low {
  border-left: 4px solid #00ff00;
}

.issue-card:hover {
  background: rgba(0, 212, 255, 0.1);
  transform: translateX(5px);
}

.issue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.issue-severity {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.severity-icon {
  font-size: 1.2rem;
}

.severity-text {
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.8rem;
}

.issue-type {
  background: rgba(0, 212, 255, 0.2);
  color: #00d4ff;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.7rem;
  text-transform: uppercase;
  font-weight: bold;
}

.issue-title {
  color: #e0e0e0;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.issue-description {
  color: #e0e0e0;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.issue-location {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.location-label {
  color: #888;
}

.location-file {
  color: #00d4ff;
  font-family: 'Courier New', monospace;
}

.location-line {
  color: #ffaa00;
}

.issue-recommendation {
  background: rgba(0, 255, 0, 0.1);
  border: 1px solid rgba(0, 255, 0, 0.3);
  border-radius: 8px;
  padding: 1rem;
}

.recommendation-label {
  color: #00ff00;
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
}

.recommendation-text {
  color: #e0e0e0;
  margin: 0;
  line-height: 1.4;
}

.dependencies-table {
  background: rgba(0, 0, 0, 0.4);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  background: rgba(0, 212, 255, 0.2);
  padding: 1rem;
  font-weight: bold;
  color: #00d4ff;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 212, 255, 0.1);
  transition: all 0.3s ease;
}

.table-row:hover {
  background: rgba(0, 212, 255, 0.1);
}

.table-row.outdated {
  background: rgba(255, 170, 0, 0.1);
}

.table-cell {
  display: flex;
  align-items: center;
}

.package-name {
  font-weight: bold;
  color: #e0e0e0;
}

.package-version {
  color: #888;
  font-family: 'Courier New', monospace;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status-badge.up-to-date {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
  border: 1px solid #00ff00;
}

.status-badge.outdated {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
  border: 1px solid #ffaa00;
}

.vuln-count {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: bold;
}

.vuln-count.high {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
  border: 1px solid #ff0000;
}

.vuln-count.safe {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
  border: 1px solid #00ff00;
}

.export-section {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 212, 255, 0.2);
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 1rem 2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 auto;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.export-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

/* Responsive Design */
@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
  
  .issues-filters {
    flex-direction: column;
  }
  
  .filter-btn {
    justify-content: center;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .table-header {
    display: none;
  }
  
  .table-cell {
    justify-content: space-between;
  }
  
  .table-cell::before {
    content: attr(data-label);
    font-weight: bold;
    color: #00d4ff;
  }
}
</style>;
