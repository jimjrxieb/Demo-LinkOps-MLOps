<template>
  <div class="demo-dashboard">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="card">
        <div class="card-body">
          <h1 class="hero-title">🧠 AI Box Demo Dashboard</h1>
          <p class="hero-subtitle">Project Summary</p>
        </div>
      </div>
    </div>

    <!-- About This Project Section -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">🚀 About This Project</h2>
      </div>
      <div class="card-body">
        <p class="project-description">
          I built an
          <strong>offline, user-friendly AI/ML platform</strong> designed to
          bring artificial intelligence to companies that are still hesitant to
          adopt it due to privacy or complexity concerns.
        </p>
        <p class="project-description">
          This is the <strong>demo version</strong> of my full
          <strong>AI Box</strong> system built for a
          <strong>property management client (ZRS Management)</strong>. The goal
          was to demonstrate that, even though I haven't officially worked for a
          tech company, I have the real-world experience, problem-solving
          mindset, and technical skills to architect secure, enterprise-level
          solutions from scratch.
        </p>
      </div>
    </div>

    <!-- DevSecOps Experience Section -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">🔐 DevSecOps Experience</h2>
      </div>
      <div class="card-body">
        <p class="section-description">
          My DevSecOps journey is represented by building this platform
          securely, from backend architecture to full deployment:
        </p>

        <div class="experience-grid">
          <div class="experience-item">
            <h4>🔁 GitHub Actions (GHA) for CI/CD</h4>
            <p>
              Tools used: <code>flake8</code>, <code>black</code>,
              <code>bandit</code>, <code>pytest</code>, <code>buildx</code>,
              <code>docker scan</code>, <code>trivy</code>, <code>snyk</code>
            </p>
          </div>

          <div class="experience-item">
            <h4>🚀 Deployment</h4>
            <ul>
              <li>Deployed securely to my <strong>Azure VM</strong></li>
              <li>
                Integrated <strong>Cloudflare Zero Trust Tunnel</strong> to
                expose the platform on my <strong>custom domain name</strong>
              </li>
              <li>Full offline operation, with no outside API calls</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- AI/ML Experience Section -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">🧠 AI/ML Experience</h2>
      </div>
      <div class="card-body">
        <p class="section-description">
          The entire project is centered around responsible and
          <strong>offline AI/ML workflows</strong>, including:
        </p>

        <div class="experience-grid">
          <div class="experience-item">
            <h4>🦙 Offline Ollama LLM (e.g., LLaMA3)</h4>
            <p>For inference</p>
          </div>

          <div class="experience-item">
            <h4>🔎 RAG system</h4>
            <p>Using FAISS + Chroma for document memory</p>
          </div>

          <div class="experience-item">
            <h4>🧪 Tool stack includes:</h4>
            <p>
              <code>LangChain</code>, <code>spaCy</code>,
              <code>scikit-learn</code>, <code>pandas</code>,
              <code>PyMuPDF</code>, <code>Playwright</code>,
              <code>pydantic</code>, <code>LoRA</code> fine-tuning
            </p>
          </div>

          <div class="experience-item">
            <h4>🛠️ Used Cursor + ChatGPT</h4>
            <p>For development and iterative coding</p>
          </div>

          <div class="experience-item">
            <h4>✅ Code was repeatedly linted, tested, and formatted</h4>
            <p>To meet production standards</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Walkthrough Section -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">🎥 Walkthrough of This Demo</h2>
      </div>
      <div class="card-body">
        <div class="walkthrough-intro">
          <p>A visual demonstration of the platform, available in the GUI:</p>
        </div>

        <div class="walkthrough-steps">
          <div class="step-item">
            <div class="step-number">1</div>
            <div class="step-content">
              <h4>📁 File Upload</h4>
              <p>
                Drag-and-drop documents, PDFs, CSVs, or reports into the system
              </p>
            </div>
          </div>

          <div class="step-item">
            <div class="step-number">2</div>
            <div class="step-content">
              <h4>🧼 Preprocessing + Sync</h4>
              <p>
                Automatically sanitize, redact PII, and sync files into memory
                (RAG)
              </p>
            </div>
          </div>

          <div class="step-item">
            <div class="step-number">3</div>
            <div class="step-content">
              <h4>🧠 RAG Search</h4>
              <p>
                Type questions and get document-aware AI answers, even offline
              </p>
            </div>
          </div>

          <div class="step-item">
            <div class="step-number">4</div>
            <div class="step-content">
              <h4>📊 ML Builder Tab</h4>
              <p>
                Upload a CSV, choose a column to predict, and train an ML model
                instantly
              </p>
            </div>
          </div>

          <div class="step-item">
            <div class="step-number">5</div>
            <div class="step-content">
              <h4>🤖 Agent Execution</h4>
              <p>
                Trigger automated workflows (e.g., generate reports, summarize
                leases)
              </p>
            </div>
          </div>

          <div class="step-item">
            <div class="step-number">6</div>
            <div class="step-content">
              <h4>🧠 HTC Feedback Tab</h4>
              <p>Submit corrections to improve the model over time</p>
            </div>
          </div>

          <div class="step-item">
            <div class="step-number">7</div>
            <div class="step-content">
              <h4>🔤 AI Keywords Tab</h4>
              <p>
                Define your own domain-specific language, like Grammarly for AI
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Conclusion Section -->
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">💡 Conclusion</h2>
      </div>
      <div class="card-body">
        <p class="conclusion-text">
          This demo was crafted to reflect
          <strong>how much I've learned</strong> and
          <strong>how much value I can deliver</strong>, even as someone
          breaking into tech. It's not just about theory — it's
          <strong
            >real DevSecOps, real AI/ML, and real client-inspired
            engineering</strong
          >.
        </p>
      </div>
    </div>

    <!-- Navigation Cards -->
    <div class="navigation-section">
      <h3 class="navigation-title">Explore the Demo</h3>
      <div class="navigation-grid">
        <router-link to="/demo" class="nav-card">
          <div class="nav-card-icon">🎯</div>
          <h4>Task Processing</h4>
          <p>Submit Kubernetes/CD tasks and see AI processing</p>
        </router-link>

        <router-link to="/rag" class="nav-card">
          <div class="nav-card-icon">🔍</div>
          <h4>RAG Search</h4>
          <p>Search documents with AI-powered retrieval</p>
        </router-link>

        <router-link to="/ml-builder" class="nav-card">
          <div class="nav-card-icon">📊</div>
          <h4>ML Builder</h4>
          <p>Train machine learning models instantly</p>
        </router-link>

        <router-link to="/whis-pipeline" class="nav-card">
          <div class="nav-card-icon">⚙️</div>
          <h4>Whis Pipeline</h4>
          <p>View the AI processing pipeline in action</p>
        </router-link>

        <router-link to="/htc" class="nav-card">
          <div class="nav-card-icon">🧠</div>
          <h4>HTC Feedback</h4>
          <p>Improve models with human feedback</p>
        </router-link>

        <router-link to="/reports" class="nav-card">
          <div class="nav-card-icon">📈</div>
          <h4>Reports</h4>
          <p>View system analytics and performance</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Component logic can be added here if needed
onMounted(() => {
  console.log('Demo Dashboard loaded');
});
</script>

<style scoped>
.demo-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  space-y: 6;
}

.hero-section {
  text-align: center;
  margin-bottom: 3rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #64748b;
  font-weight: 500;
}

.project-description {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #374151;
  margin-bottom: 1.5rem;
}

.section-description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #4b5563;
  margin-bottom: 2rem;
}

.experience-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.experience-item {
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.experience-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.experience-item h4 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-weight: 600;
  font-size: 1.1rem;
}

.experience-item p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.experience-item ul {
  color: #64748b;
  line-height: 1.6;
  padding-left: 1.5rem;
}

.experience-item li {
  margin-bottom: 0.5rem;
}

.experience-item code {
  background: #f1f5f9;
  color: #0f172a;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9rem;
}

.walkthrough-intro {
  margin-bottom: 2rem;
}

.walkthrough-intro p {
  font-size: 1.1rem;
  color: #4b5563;
  font-style: italic;
}

.walkthrough-steps {
  space-y: 2;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  margin-bottom: 1rem;
  transition: transform 0.2s ease;
}

.step-item:hover {
  transform: translateX(5px);
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.step-content h4 {
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 1.1rem;
}

.step-content p {
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.conclusion-text {
  font-size: 1.2rem;
  line-height: 1.7;
  color: #374151;
  text-align: center;
  font-weight: 500;
}

.navigation-section {
  margin-top: 4rem;
}

.navigation-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 2rem;
}

.navigation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.nav-card {
  display: block;
  padding: 2rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  text-align: center;
}

.nav-card:hover {
  border-color: #667eea;
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15);
  text-decoration: none;
  color: inherit;
}

.nav-card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.nav-card h4 {
  color: #1e293b;
  margin-bottom: 0.75rem;
  font-weight: 600;
  font-size: 1.2rem;
}

.nav-card p {
  color: #64748b;
  line-height: 1.5;
  margin: 0;
  font-size: 0.95rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .demo-dashboard {
    padding: 1rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .experience-grid {
    grid-template-columns: 1fr;
  }

  .step-item {
    flex-direction: column;
    text-align: center;
  }

  .navigation-grid {
    grid-template-columns: 1fr;
  }

  .nav-card {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .project-description,
  .section-description {
    font-size: 1rem;
  }
}
</style>
