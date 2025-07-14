<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1 class="page-title">LinkOps Dashboard</h1>
      <p class="page-subtitle">MLOps Platform Control Center</p>
    </div>

    <!-- Status Overview -->
    <section class="dashboard-section">
      <h2 class="section-title">System Status</h2>
      <div class="status-grid">
        <div class="status-card">
          <div class="status-icon">⚡</div>
          <div class="status-content">
            <h3>Active Jobs</h3>
            <div class="status-value">
              {{ activeJobs }}
            </div>
          </div>
        </div>
        <div class="status-card">
          <div class="status-icon">✅</div>
          <div class="status-content">
            <h3>Completed</h3>
            <div class="status-value">
              {{ completedJobs }}
            </div>
          </div>
        </div>
        <div class="status-card">
          <div class="status-icon">⚠️</div>
          <div class="status-content">
            <h3>Errors</h3>
            <div class="status-value error">
              {{ errorCount }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Orbs Section -->
    <section class="dashboard-section">
      <h2 class="section-title">Active Orbs</h2>
      <div class="orbs-grid">
        <OrbCard
          v-for="orb in activeOrbs"
          :key="orb.id"
          :orb="orb"
          @click="selectOrb(orb)"
        />
      </div>
    </section>

    <!-- Runes Section -->
    <section class="dashboard-section">
      <h2 class="section-title">Available Runes</h2>
      <div class="runes-grid">
        <RuneCard
          v-for="rune in availableRunes"
          :key="rune.id"
          :rune="rune"
          @click="activateRune(rune)"
        />
      </div>
    </section>

    <!-- Quick Actions -->
    <section class="dashboard-section">
      <h2 class="section-title">Quick Actions</h2>
      <div class="quick-actions">
        <button class="action-btn primary" @click="startWhisPipeline">
          <span class="btn-icon">⚡</span>
          Start Whis Pipeline
        </button>
        <button class="action-btn secondary" @click="runSecurityAudit">
          <span class="btn-icon">🔍</span>
          Security Audit
        </button>
        <button class="action-btn secondary" @click="viewLogs">
          <span class="btn-icon">📋</span>
          View Logs
        </button>
      </div>
    </section>

    <!-- Search Component -->
    <section class="dashboard-section">
      <h2 class="section-title">Find Orbs & Tasks</h2>
      <FicknurySearch @search="handleSearch" />
    </section>

    <!-- Demo Mode Indicator -->
    <section class="dashboard-section">
      <div class="demo-mode-banner">
        <div class="demo-icon">⚠️</div>
        <div class="demo-content">
          <h3>Demo Mode Active</h3>
          <p>You're currently running in <strong>demo mode</strong>. AI model capabilities are disabled.</p>
          <div class="demo-actions">
            <input 
              type="text" 
              placeholder="Paste your API key (OpenAI, Grok, Claude)" 
              disabled 
              class="api-key-input"
            />
            <button disabled class="connect-btn">
              Connect API Key (Disabled in Demo)
            </button>
          </div>
          <div class="demo-info">
            <p><strong>Supported Models:</strong> Grok (xAI), OpenAI (ChatGPT), Anthropic (Claude)</p>
            <p><strong>To enable:</strong> Add your API key to the environment and restart the platform</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import OrbCard from '../components/OrbCard.vue';
import RuneCard from '../components/RuneCard.vue';
import FicknurySearch from '../components/FicknurySearch.vue';

export default {
  name: 'Dashboard',
  components: {
    OrbCard,
    RuneCard,
    FicknurySearch,
  },
  data() {
    return {
      activeJobs: 3,
      completedJobs: 12,
      errorCount: 0,
      activeOrbs: [
        {
          id: 1,
          title: 'Data Pipeline Optimization',
          description:
            'Optimize ML data processing pipeline for faster training',
          score: 85,
          status: 'active',
          priority: 'high',
        },
        {
          id: 2,
          title: 'Model Deployment',
          description: 'Deploy new ML model to production environment',
          score: 92,
          status: 'active',
          priority: 'critical',
        },
        {
          id: 3,
          title: 'Security Scan',
          description: 'Run comprehensive security audit on codebase',
          score: 78,
          status: 'pending',
          priority: 'medium',
        },
      ],
      availableRunes: [
        {
          id: 1,
          name: 'Whis Enhancement',
          description: 'Enhance data quality through Whis pipeline',
          type: 'data-processing',
          cost: 100,
        },
        {
          id: 2,
          name: 'Security Audit',
          description: 'Comprehensive security and vulnerability scan',
          type: 'security',
          cost: 50,
        },
        {
          id: 3,
          name: 'Performance Tuning',
          description: 'Optimize system performance and resource usage',
          type: 'optimization',
          cost: 75,
        },
      ],
    };
  },
  methods: {
    selectOrb() {
      // Navigate to orb details or open modal
    },
    activateRune() {
      // Activate the rune and show effects
    },
    startWhisPipeline() {
      this.$router.push('/whis');
    },
    runSecurityAudit() {
      this.$router.push('/audit');
    },
    viewLogs() {
      // Open logs viewer
    },
    handleSearch() {
      // Handle search functionality
    },
  },
};
</script>
;
<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
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

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.status-card {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.status-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
}

.status-icon {
  font-size: 2rem;
  min-width: 60px;
  text-align: center;
}

.status-content h3 {
  margin: 0 0 0.5rem 0;
  color: #00d4ff;
  font-size: 1.2rem;
}

.status-content p {
  margin: 0;
  color: #e0e0e0;
  font-size: 1.1rem;
}

.dashboard-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2rem;
  color: #00d4ff;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #00d4ff;
  padding-bottom: 0.5rem;
}

.orbs-grid,
.runes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.quick-actions {
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
  text-decoration: none;
  color: white;
}

.action-btn.primary {
  background: linear-gradient(45deg, #00d4ff, #0099cc);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.action-btn.secondary {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  color: #00d4ff;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .status-grid {
    grid-template-columns: 1fr;
  }

  .orbs-grid,
  .runes-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions {
    flex-direction: column;
  }

  .action-btn {
    justify-content: center;
  }
}

/* Demo Mode Banner Styles */
.demo-mode-banner {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  border: 2px solid #ff8c00;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
}

.demo-icon {
  font-size: 2rem;
  min-width: 40px;
  margin-top: 0.25rem;
}

.demo-content h3 {
  margin: 0 0 0.5rem 0;
  color: #8b4513;
  font-size: 1.3rem;
  font-weight: bold;
}

.demo-content p {
  margin: 0 0 1rem 0;
  color: #654321;
  line-height: 1.5;
}

.demo-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.api-key-input {
  flex: 1;
  min-width: 300px;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  background-color: #f5f5f5;
  color: #666;
  opacity: 0.6;
  cursor: not-allowed;
}

.connect-btn {
  padding: 0.75rem 1.5rem;
  background-color: #ccc;
  color: #666;
  border: none;
  border-radius: 6px;
  cursor: not-allowed;
  font-weight: bold;
  opacity: 0.6;
}

.demo-info {
  background: rgba(255, 255, 255, 0.7);
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #ff8c00;
}

.demo-info p {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #654321;
}

.demo-info p:last-child {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .demo-mode-banner {
    flex-direction: column;
    text-align: center;
  }
  
  .demo-actions {
    flex-direction: column;
  }
  
  .api-key-input {
    min-width: auto;
  }
}
</style>
;
