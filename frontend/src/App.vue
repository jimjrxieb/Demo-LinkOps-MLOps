<template>
  <div class="admin-app">
    <!-- Sidebar -->
    <Sidebar />
    
    <!-- Main Content Area -->
    <div
      class="main-content"
      :class="{ 'sidebar-collapsed': false }"
    >
      <!-- Top Header -->
      <header class="top-header">
        <div class="header-content">
          <div class="page-title">
            <h1>{{ currentPageTitle }}</h1>
            <p class="page-subtitle">
              {{ currentPageSubtitle }}
            </p>
          </div>
          <div class="header-actions">
            <div class="demo-badge">
              <span class="badge-icon">🎯</span>
              <span class="badge-text">Kubernetes/CD Demo</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="page-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'

const route = useRoute()

const currentPageTitle = computed(() => {
  const routeTitles = {
    '/': 'Kubernetes/CD Shadow Agent DEMO',
    '/pipeline': 'Whis Learning Pipeline',
    '/orbs': 'Orb Library',
    '/keys': 'API Key Management',
    '/about': 'About This Demo'
  }
  return routeTitles[route.path] || 'LinkOps Demo'
})

const currentPageSubtitle = computed(() => {
  const routeSubtitles = {
    '/': [
      'I built this AI-powered Kubernetes/CD platform from the ground up using top tools like OpenAI, LangChain, FastAPI, and Cursor.',
      'I incorporated industry-standard linters, formatters, and wrote custom Python and Bash scripts to auto-fix issues and streamline my workflow.',
      '',
      'For DevOps: I used GitHub Actions, Trivy, SonarQube, and GitGuardian.',
      'For Kubernetes: I earned my CKA and use ArgoCD to sync this platform into Docker Desktop\'s K8s environment.',
      'For Cloud Engineering: I deployed this demo into an Azure VM provisioned using Terraform.',
      'For AI/ML: I use microservices for data collection, sanitation, and a custom learning model (Whis Smithing) with feedback loops — simulating a true MLOps pipeline.'
    ].join('\n'),
    '/pipeline': 'Visualize the Whis MLOps learning process',
    '/orbs': 'Browse the Kubernetes/CD best practices library',
    '/keys': 'Configure AI API keys for enhanced features',
    '/about': [
      'I built this AI-powered Kubernetes/CD platform from the ground up using top tools like OpenAI, LangChain, FastAPI, and Cursor.',
      'I incorporated industry-standard linters, formatters, and wrote custom Python and Bash scripts to auto-fix issues and streamline my workflow.',
      '',
      'For DevOps: I used GitHub Actions, Trivy, SonarQube, and GitGuardian.',
      'For Kubernetes: I earned my CKA and use ArgoCD to sync this platform into Docker Desktop\'s K8s environment.',
      'For Platform Engineering: I deployed this demo into an Azure VM provisioned using Terraform.',
      'For AI/ML: I use microservices for data collection, sanitation, and a custom learning model (Whis Smithing) with feedback loops — simulating a true MLOps pipeline.'
    ].join('\n')
  }
  return routeSubtitles[route.path] || 'LinkOps MLOps Platform'
})
</script>

<style>
/* Reset and base styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f8fafc;
  color: #1e293b;
  line-height: 1.6;
}

.admin-app {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
}

.main-content.sidebar-collapsed {
  margin-left: 70px;
}

.top-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1.5rem 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.page-title h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.page-subtitle {
  color: #64748b;
  font-size: 0.875rem;
  max-width: 60ch;
  line-height: 1.6;
  white-space: pre-wrap;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.demo-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(251, 191, 36, 0.3);
}

.badge-icon {
  font-size: 1rem;
}

.page-content {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* Card styles for consistent UI */
.card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.card-body {
  padding: 1.5rem;
}

.card-subtitle {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0;
  line-height: 1.5;
}

.hero-section {
  margin-bottom: 2rem;
}

.hero-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero-highlight {
  color: #3b82f6;
}

.hero-description {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.7;
  margin: 0;
  max-width: 60ch;
}

.pipeline-section {
  margin-top: 1.5rem;
}

.library-section {
  margin-top: 2.5rem;
}

.demo-info-card {
  margin-top: 2.5rem;
}

/* Button styles */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
}

.btn-secondary:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.btn-success {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-success:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

/* Form styles */
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

/* Responsive design */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
  }
  
  .page-content {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .top-header {
    padding: 1rem;
  }
  
  .page-title h1 {
    font-size: 1.5rem;
  }
  
  .page-content {
    padding: 0.75rem;
  }
}
</style>
