<template>
  <div class="audit-input">
    <div class="input-section">
      <label class="input-label">Repository URL or Path</label>
      <div class="input-group">
        <input
          v-model="repositoryUrl"
          type="text"
          placeholder="https://github.com/username/repo or /path/to/repo"
          class="repo-input"
          :disabled="loading"
          @keyup.enter="submitAudit"
        />
        <button
          class="submit-btn"
          :disabled="loading || !repositoryUrl.trim()"
          @click="submitAudit"
        >
          <span v-if="loading" class="spinner" />
          <span v-else class="btn-icon">🔍</span>
          {{ loading ? 'Scanning...' : 'Run Audit' }}
        </button>
      </div>
    </div>

    <div class="options-section">
      <h3 class="options-title">Audit Options</h3>
      <div class="options-grid">
        <div class="option-group">
          <label class="option-label">
            <input
              v-model="options.securityScan"
              type="checkbox"
              :disabled="loading"
            />
            Security Scan
          </label>
          <p class="option-description">Vulnerability and security analysis</p>
        </div>

        <div class="option-group">
          <label class="option-label">
            <input
              v-model="options.codeQuality"
              type="checkbox"
              :disabled="loading"
            />
            Code Quality
          </label>
          <p class="option-description">Linting and code style analysis</p>
        </div>

        <div class="option-group">
          <label class="option-label">
            <input
              v-model="options.dependencyScan"
              type="checkbox"
              :disabled="loading"
            />
            Dependency Analysis
          </label>
          <p class="option-description">Outdated and vulnerable dependencies</p>
        </div>

        <div class="option-group">
          <label class="option-label">
            <input
              v-model="options.secretScan"
              type="checkbox"
              :disabled="loading"
            />
            Secret Detection
          </label>
          <p class="option-description">
            API keys and sensitive data detection
          </p>
        </div>
      </div>
    </div>

    <!-- Quick Templates -->
    <div class="templates-section">
      <h3 class="templates-title">Quick Templates</h3>
      <div class="template-buttons">
        <button
          class="template-btn"
          :disabled="loading"
          @click="loadTemplate('linkops')"
        >
          LinkOps Platform
        </button>
        <button
          class="template-btn"
          :disabled="loading"
          @click="loadTemplate('frontend')"
        >
          Frontend UI
        </button>
        <button
          class="template-btn"
          :disabled="loading"
          @click="loadTemplate('backend')"
        >
          Backend API
        </button>
        <button
          class="template-btn"
          :disabled="loading"
          @click="loadTemplate('custom')"
        >
          Custom Path
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuditInput',
  emits: ['submit'],
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      repositoryUrl: '',
      options: {
        securityScan: true,
        codeQuality: true,
        dependencyScan: true,
        secretScan: true,
      },
    };
  },
  methods: {
    submitAudit() {
      if (!this.repositoryUrl.trim()) return;

      this.$emit('submit', {
        repositoryUrl: this.repositoryUrl.trim(),
        options: { ...this.options },
      });
    },
    loadTemplate(type) {
      const templates = {
        linkops: 'https://github.com/shadow-link-industries/linkops-platform',
        frontend:
          '/home/jimjrxieb/shadow-link-industries/LinkOps-MLOps/frontend',
        backend: '/home/jimjrxieb/shadow-link-industries/LinkOps-MLOps/backend',
        custom: '',
      };

      this.repositoryUrl = templates[type] || '';
    },
  },
};
</script>

<style scoped>
.audit-input {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #00d4ff;
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.input-section {
  margin-bottom: 2rem;
}

.input-label {
  display: block;
  color: #00d4ff;
  font-weight: bold;
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
}

.input-group {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.repo-input {
  flex: 1;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #333;
  border-radius: 8px;
  padding: 0.75rem;
  color: #e0e0e0;
  font-family: 'Orbitron', 'Courier New', monospace;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.repo-input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
}

.repo-input::placeholder {
  color: #666;
}

.submit-btn {
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
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
  min-width: 140px;
  justify-content: center;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 212, 255, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.btn-icon {
  font-size: 1.1rem;
}

.options-section {
  margin-bottom: 2rem;
}

.options-title {
  color: #00d4ff;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.option-group {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.3s ease;
}

.option-group:hover {
  border-color: #00d4ff;
  background: rgba(0, 212, 255, 0.1);
}

.option-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e0e0e0;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 0.5rem;
}

.option-label input[type='checkbox'] {
  width: 18px;
  height: 18px;
  accent-color: #00d4ff;
}

.option-description {
  color: #888;
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.4;
}

.templates-section {
  margin-top: 2rem;
}

.templates-title {
  color: #00d4ff;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.template-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.template-btn {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid #333;
  border-radius: 6px;
  padding: 0.75rem 1rem;
  color: #e0e0e0;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  min-width: 120px;
}

.template-btn:hover:not(:disabled) {
  border-color: #00d4ff;
  background: rgba(0, 212, 255, 0.1);
  color: #00d4ff;
}

.template-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 768px) {
  .audit-input {
    padding: 1.5rem;
  }

  .input-group {
    flex-direction: column;
    gap: 0.75rem;
  }

  .submit-btn {
    width: 100%;
  }

  .options-grid {
    grid-template-columns: 1fr;
  }

  .template-buttons {
    flex-direction: column;
  }

  .template-btn {
    width: 100%;
  }
}
</style>
