<template>;
  <div class='dashboard'>;
    <div class='dashboard-header'>;
      <h1 class='page-title'>Dashboard</h1>;
      <p class='page-subtitle'>MLOps Command Center Overview</p>;
    </div>;

    <!-- System Status Grid -->;
    <div class='status-grid'>;
      <div class='status-card system-status'>;
        <div class='status-icon'>🟢</div>;
        <div class='status-content'>;
          <h3>System Status</h3>;
          <p>All services operational</p>;
        </div>;
      </div>;
      
      <div class='status-card active-jobs'>;
        <div class='status-icon'>⚡</div>;
        <div class='status-content'>;
          <h3>Active Jobs</h3>;
          <p>{{ activeJobs }} running</p>;
        </div>;
      </div>;
      
      <div class='status-card completed-jobs'>;
        <div class='status-icon'>✅</div>;
        <div class='status-content'>;
          <h3>Completed Today</h3>;
          <p>{{ completedJobs }} jobs</p>;
        </div>;
      </div>;
      
      <div class='status-card error-count'>;
        <div class='status-icon'>⚠️</div>;
        <div class='status-content'>;
          <h3>Errors</h3>;
          <p>{{ errorCount }} issues</p>;
        </div>;
      </div>;
    </div>;

    <!-- Orbs Section -->;
    <section class='dashboard-section'>;
      <h2 class='section-title'>Active Orbs</h2>;
      <div class='orbs-grid'>;
        <OrbCard;
          v-for='orb in activeOrbs';
          :key='orb.id';
          :orb='orb';
          @click='selectOrb(orb)';
        />;
      </div>;
    </section>;

    <!-- Runes Section -->;
    <section class='dashboard-section'>;
      <h2 class='section-title'>Available Runes</h2>;
      <div class='runes-grid'>;
        <RuneCard;
          v-for='rune in availableRunes';
          :key='rune.id';
          :rune='rune';
          @click='activateRune(rune)';
        />;
      </div>;
    </section>;

    <!-- Quick Actions -->;
    <section class='dashboard-section'>;
      <h2 class='section-title'>Quick Actions</h2>;
      <div class='quick-actions'>;
        <button class="action-btn primary" @click="startWhisPipeline">;
          <span class='btn-icon'>⚡</span>;
          Start Whis Pipeline;
        </button>;
        <button class="action-btn secondary" @click="runSecurityAudit">;
          <span class='btn-icon'>🔍</span>;
          Security Audit;
        </button>;
        <button class="action-btn secondary" @click="viewLogs">;
          <span class='btn-icon'>📋</span>;
          View Logs;
        </button>;
      </div>;
    </section>;

    <!-- Search Component -->;
    <section class='dashboard-section'>;
      <h2 class='section-title'>Find Orbs & Tasks</h2>;
      <FicknurySearch @search='handleSearch' />;
    </section>;
  </div>;
</template>;

<script>;
import OrbCard from '../components/OrbCard.vue'
import RuneCard from '../components/RuneCard.vue'
import FicknurySearch from '../components/FicknurySearch.vue'

export default {
  name: 'Dashboard',
  components: {
    OrbCard,
    RuneCard,
    FicknurySearch;
  },
  data() {
    return {
      activeJobs: 3,
      completedJobs: 12,
      errorCount: 0,
      activeOrbs: [;
        {
          id: 1,
          title: 'Data Pipeline Optimization',
          description: 'Optimize ML data processing pipeline for faster training',
          score: 85,
          status: 'active',
          priority: 'high';
        },
        {
          id: 2,
          title: 'Model Deployment',
          description: 'Deploy new ML model to production environment',
          score: 92,
          status: 'active',
          priority: 'critical';
        },
        {
          id: 3,
          title: 'Security Scan',
          description: 'Run comprehensive security audit on codebase',
          score: 78,
          status: 'pending',
          priority: 'medium';
        }
      ],
      availableRunes: [;
        {
          id: 1,
          name: 'Whis Enhancement',
          description: 'Enhance data quality through Whis pipeline',
          type: 'data-processing',
          cost: 100;
        },
        {
          id: 2,
          name: 'Security Audit',
          description: 'Comprehensive security and vulnerability scan',
          type: 'security',
          cost: 50;
        },
        {
          id: 3,
          name: 'Performance Tuning',
          description: 'Optimize system performance and resource usage',
          type: 'optimization',
          cost: 75;
        }
      ];
    }
  },
  methods: {
    selectOrb(orb) {
 // Removed console statement: console.log('Selected orb:', orb)
      // Navigate to orb details or open modal
    },
    activateRune(rune) {
 // Removed console statement: console.log('Activated rune:', rune)
      // Activate the rune and show effects
    },
    startWhisPipeline() {
      this.$router.push('/whis');
    },
    runSecurityAudit() {
      this.$router.push('/audit');
    },
    viewLogs() {
 // Removed console statement: console.log('Viewing logs...')
      // Open logs viewer
    },
    handleSearch(query) {
 // Removed console statement: console.log('Search query:', query)
      // Handle search functionality
    }
  }
}
</script>;

<style scoped>;
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
</style>;