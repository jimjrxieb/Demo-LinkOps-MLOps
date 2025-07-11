<template>
  ; ; ; ; ; ;
  <div>
    ; ; ; ; ; ;
    <DashboardView />;
  </div>
  ;
</template>
;

<script setup>
import DashboardView from './views/DashboardView.vue';
</script>
;

<style>
@import './assets/holo-theme.css';

.holo-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: #e0e0e0;
  font-family: 'Orbitron', 'Courier New', monospace;
}

.holo-nav {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 2px solid #00d4ff;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.brand-text {
  font-size: 2rem;
  font-weight: bold;
  background: linear-gradient(45deg, #00d4ff, #ff00ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
}

.brand-subtitle {
  font-size: 0.8rem;
  color: #888;
  margin-top: -0.5rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-actions {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-role {
  color: #00d4ff;
  font-weight: bold;
  font-size: 0.9rem;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 0, 0, 0.2);
  border: 1px solid #ff0000;
  color: #ff0000;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 0, 0, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 0, 0, 0.3);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  color: #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.nav-link:hover {
  background: rgba(0, 212, 255, 0.1);
  border-color: #00d4ff;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
  transform: translateY(-2px);
}

.nav-link.active {
  background: rgba(0, 212, 255, 0.2);
  border-color: #00d4ff;
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
}

.nav-icon {
  font-size: 1.2rem;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.holo-footer {
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid #00d4ff;
  padding: 1rem 2rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #888;
}

.footer-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    gap: 1rem;
  }

  .nav-actions {
    margin-top: 1rem;
  }

  .user-info {
    flex-direction: column;
    gap: 0.5rem;
  }

  .main-content {
    padding: 1rem;
  }

  .footer-content {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
;
