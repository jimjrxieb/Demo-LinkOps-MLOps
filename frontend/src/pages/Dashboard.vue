<template>
  <div class="dashboard-container">
    <!-- Header with glowing title -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">
        <span class="title-glow">LinkOps</span> Command Center
      </h1>
      <div class="status-indicator">
        <div class="status-dot active"></div>
        <span>System Online</span>
      </div>
    </div>

    <!-- Main dashboard grid -->
    <div class="dashboard-grid">
      <!-- Orbs Section -->
      <div class="dashboard-card orb-section">
        <div class="card-header">
          <h2>🔮 Active Orbs</h2>
          <div class="card-actions">
            <button class="btn-primary">Create New</button>
          </div>
        </div>
        <div class="orb-grid">
          <div v-for="orb in orbs" :key="orb.id" class="orb-item">
            <div class="orb-visual">
              <div class="orb-core" :style="{ backgroundColor: orb.color }"></div>
              <div class="orb-rings"></div>
            </div>
            <div class="orb-info">
              <h3>{{ orb.name }}</h3>
              <p>{{ orb.description }}</p>
              <div class="orb-stats">
                <span class="stat">Status: {{ orb.status }}</span>
                <span class="stat">Created: {{ orb.created }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Runes Section -->
      <div class="dashboard-card rune-section">
        <div class="card-header">
          <h2>⚡ Rune Collection</h2>
          <div class="card-actions">
            <button class="btn-secondary">View All</button>
          </div>
        </div>
        <div class="rune-grid">
          <div v-for="rune in runes" :key="rune.id" class="rune-item">
            <div class="rune-symbol">{{ rune.symbol }}</div>
            <div class="rune-info">
              <h3>{{ rune.name }}</h3>
              <p>{{ rune.power }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Models Section -->
      <div class="dashboard-card model-section">
        <div class="card-header">
          <h2>🤖 AI Models</h2>
          <div class="card-actions">
            <button class="btn-primary">Deploy New</button>
          </div>
        </div>
        <div class="model-list">
          <div v-for="model in models" :key="model.id" class="model-item">
            <div class="model-icon">🤖</div>
            <div class="model-info">
              <h3>{{ model.name }}</h3>
              <p>{{ model.type }}</p>
              <div class="model-status">
                <span class="status-badge" :class="model.status">{{ model.status }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Stats -->
      <div class="dashboard-card stats-section">
        <div class="card-header">
          <h2>📊 System Statistics</h2>
        </div>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-value">{{ stats.totalOrbs }}</div>
            <div class="stat-label">Total Orbs</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.activeRunes }}</div>
            <div class="stat-label">Active Runes</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.deployedModels }}</div>
            <div class="stat-label">Deployed Models</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.uptime }}</div>
            <div class="stat-label">Uptime (hrs)</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      orbs: [
        {
          id: 1,
          name: 'Data Processing Orb',
          description: 'Handles raw data transformation',
          status: 'Active',
          created: '2024-01-15',
          color: '#00ff88'
        },
        {
          id: 2,
          name: 'Analysis Orb',
          description: 'Performs deep data analysis',
          status: 'Active',
          created: '2024-01-10',
          color: '#ff0088'
        }
      ],
      runes: [
        {
          id: 1,
          symbol: '⚡',
          name: 'Speed Rune',
          power: 'Accelerates processing by 300%'
        },
        {
          id: 2,
          symbol: '🛡️',
          name: 'Protection Rune',
          power: 'Enhances security protocols'
        },
        {
          id: 3,
          symbol: '🔍',
          name: 'Insight Rune',
          power: 'Reveals hidden patterns'
        }
      ],
      models: [
        {
          id: 1,
          name: 'Whis Data Input',
          type: 'Data Processing',
          status: 'running'
        },
        {
          id: 2,
          name: 'Whis Sanitize',
          type: 'Data Cleaning',
          status: 'running'
        },
        {
          id: 3,
          name: 'Whis Logic',
          type: 'Decision Engine',
          status: 'deployed'
        }
      ],
      stats: {
        totalOrbs: 12,
        activeRunes: 8,
        deployedModels: 15,
        uptime: 168
      }
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  padding: 2rem;
}

.dashboard-header {
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

.dashboard-title {
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

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 255, 136, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.btn-primary, .btn-secondary {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
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

/* Orb Styles */
.orb-grid {
  display: grid;
  gap: 1rem;
}

.orb-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.orb-visual {
  position: relative;
  width: 60px;
  height: 60px;
}

.orb-core {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  position: relative;
  animation: float 3s ease-in-out infinite;
}

.orb-rings {
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  animation: rotate 10s linear infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.orb-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.orb-info p {
  margin: 0 0 0.5rem 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.orb-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
}

.stat {
  color: rgba(255, 255, 255, 0.6);
}

/* Rune Styles */
.rune-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.rune-item {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.3s ease;
}

.rune-item:hover {
  transform: scale(1.05);
}

.rune-symbol {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.rune-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.rune-info p {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.8rem;
}

/* Model Styles */
.model-list {
  display: grid;
  gap: 1rem;
}

.model-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.model-icon {
  font-size: 1.5rem;
}

.model-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.model-info p {
  margin: 0 0 0.5rem 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.running {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
}

.status-badge.deployed {
  background: rgba(0, 123, 255, 0.2);
  color: #007bff;
}

/* Stats Styles */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #00ff88;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .dashboard-title {
    font-size: 2rem;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style> 