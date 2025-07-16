<template>
  <div class="about-demo">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="card">
        <div class="card-body text-center">
          <div class="hero-icon">
            🚀
          </div>
          <h1 class="hero-title">
            Kubernetes/CD Platform Engineering Demo
          </h1>
          <p class="hero-subtitle">
            A full-stack platform engineering showcase demonstrating DevOps, Kubernetes, AI/ML, and MLOps skills
          </p>
          <div class="hero-badges">
            <span class="hero-badge">🎯 Recruiter Ready</span>
            <span class="hero-badge">🚀 Production Grade</span>
            <span class="hero-badge">🧠 AI/ML Powered</span>
            <span class="hero-badge">☸️ Kubernetes Native</span>
          </div>
        </div>
      </div>
    </div>

    <!-- My Story Section -->
    <div class="story-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            👨‍💻 My Platform Engineering Journey
          </h2>
        </div>
        <div class="card-body">
          <div class="story-content">
            <p class="story-text">
              I built this AI-powered Kubernetes/CD platform from the ground up using industry-standard tools like OpenAI, LangChain, FastAPI, and Cursor. 
              Every Kubernetes-related Jira task I'm assigned — or errors I've encountered and solved using tools like ChatGPT and K8sGPT — 
              gets entered into this system, where it is structured, learned from, and versioned.
            </p>
            <p class="story-text">
              Over time, it becomes a reflection of my real-world experience, industry best practices, and troubleshooting patterns. 
              The long-term goal is to reach a state where this system can autonomously complete any Kubernetes or CD-related task I receive.
            </p>
            <div class="story-highlights">
              <div class="highlight-item">
                <span class="highlight-icon">🔧</span>
                <span class="highlight-text">Custom Python and Bash scripts to auto-fix issues</span>
              </div>
              <div class="highlight-item">
                <span class="highlight-icon">🎯</span>
                <span class="highlight-text">Industry-standard linters and formatters</span>
              </div>
              <div class="highlight-item">
                <span class="highlight-icon">🚀</span>
                <span class="highlight-text">Streamlined development workflow</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Skills Demonstrated -->
    <div class="skills-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            🎯 Skills Demonstrated
          </h2>
        </div>
        <div class="card-body">
          <div class="skills-grid">
            <div class="skill-category">
              <div class="skill-header">
                <div class="skill-icon">
                  🔧
                </div>
                <h3>DevOps Engineering</h3>
              </div>
              <ul class="skill-list">
                <li>GitHub Actions CI/CD pipeline with security scanning</li>
                <li>Trivy vulnerability scanning and GitGuardian secret detection</li>
                <li>Docker containerization with multi-stage builds</li>
                <li>Automated versioning and deployment workflows</li>
                <li>Infrastructure as Code with Terraform</li>
              </ul>
            </div>
            
            <div class="skill-category">
              <div class="skill-header">
                <div class="skill-icon">
                  ☸️
                </div>
                <h3>Kubernetes Expertise</h3>
              </div>
              <ul class="skill-list">
                <li>CKA certified with real-world Kubernetes patterns</li>
                <li>Helm charts for multi-service deployments</li>
                <li>ArgoCD for GitOps-style deployments</li>
                <li>Multi-service architecture with proper networking</li>
                <li>Resource management and scaling strategies</li>
              </ul>
            </div>
            
            <div class="skill-category">
              <div class="skill-header">
                <div class="skill-icon">
                  ☁️
                </div>
                <h3>Cloud/Platform Engineering</h3>
              </div>
              <ul class="skill-list">
                <li>Azure VM deployment with Terraform</li>
                <li>Multi-cloud architecture considerations</li>
                <li>Platform engineering best practices</li>
                <li>Service mesh and API gateway patterns</li>
                <li>Observability and monitoring setup</li>
              </ul>
            </div>
            
            <div class="skill-category">
              <div class="skill-header">
                <div class="skill-icon">
                  🧠
                </div>
                <h3>AI/ML Engineering</h3>
              </div>
              <ul class="skill-list">
                <li>Custom TensorFlow classifier for task categorization</li>
                <li>MLOps pipeline with model versioning and retraining</li>
                <li>Human-in-loop workflows for continuous learning</li>
                <li>Fallback logic between ML models and LLMs</li>
                <li>Training Orbs with versioned model management</li>
              </ul>
            </div>
            
            <div class="skill-category">
              <div class="skill-header">
                <div class="skill-icon">
                  💻
                </div>
                <h3>Full-Stack Development</h3>
              </div>
              <ul class="skill-list">
                <li>Vue.js 3 with Composition API and modern tooling</li>
                <li>FastAPI microservices with proper API design</li>
                <li>Modular component architecture</li>
                <li>TypeScript and Python type hints</li>
                <li>Responsive design with Tailwind CSS</li>
              </ul>
            </div>
            
            <div class="skill-category">
              <div class="skill-header">
                <div class="skill-icon">
                  🛡️
                </div>
                <h3>Security & Quality</h3>
              </div>
              <ul class="skill-list">
                <li>Security scanning throughout the pipeline</li>
                <li>Code quality tools (Ruff, ESLint, Prettier)</li>
                <li>Secret management and secure configurations</li>
                <li>Vulnerability assessment and remediation</li>
                <li>Compliance and best practices implementation</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- The Whis Pipeline -->
    <div class="pipeline-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            🧠 The Whis Learning Pipeline
          </h2>
        </div>
        <div class="card-body">
          <div class="pipeline-content">
            <p class="pipeline-intro">
              The core innovation is the <strong>Whis Pipeline</strong> - an AI-powered system that learns from Kubernetes/CD tasks 
              and continuously improves through human feedback and automated retraining.
            </p>
            
            <div class="pipeline-stages">
              <div class="stage-item">
                <div class="stage-number">
                  1
                </div>
                <div class="stage-content">
                  <h4>Data Input</h4>
                  <p>Collects tasks from UI, Q&A, image OCR, and transcript tools using FastAPI and JSON Schema</p>
                  <div class="stage-tools">
                    📦 FastAPI, JSON Schema, CLI agent intake
                  </div>
                </div>
              </div>
              
              <div class="stage-item">
                <div class="stage-number">
                  2
                </div>
                <div class="stage-content">
                  <h4>Sanitization</h4>
                  <p>Cleans and validates input data, removes sensitive information, and standardizes format</p>
                  <div class="stage-tools">
                    🧹 Data validation, PII detection, format standardization
                  </div>
                </div>
              </div>
              
              <div class="stage-item">
                <div class="stage-number">
                  3a
                </div>
                <div class="stage-content">
                  <h4>ML Classification</h4>
                  <p>TensorFlow model classifies task type with confidence scoring. Falls back to LLM if confidence is low</p>
                  <div class="stage-tools">
                    🤖 TensorFlow, Keras, scikit-learn, pandas
                  </div>
                </div>
              </div>
              
              <div class="stage-item">
                <div class="stage-number">
                  3b
                </div>
                <div class="stage-content">
                  <h4>LLM Processing</h4>
                  <p>OpenAI/LangChain generates execution plans and best practices when ML confidence is insufficient</p>
                  <div class="stage-tools">
                    🧠 LangChain, OpenAI, prompt engineering
                  </div>
                </div>
              </div>
              
              <div class="stage-item">
                <div class="stage-number">
                  4
                </div>
                <div class="stage-content">
                  <h4>Human Approval</h4>
                  <p>Manual approval workflow with feedback collection for continuous learning and improvement</p>
                  <div class="stage-tools">
                    👥 Manual approval + Vue.js tagging
                  </div>
                </div>
              </div>
              
              <div class="stage-item">
                <div class="stage-number">
                  5
                </div>
                <div class="stage-content">
                  <h4>Execution & Scoring</h4>
                  <p>Semantic retrieval, scoring, and execution using scikit-learn, TF-IDF, and cosine similarity</p>
                  <div class="stage-tools">
                    📊 scikit-learn, TF-IDF, cosine similarity
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Technology Stack -->
    <div class="tech-stack-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            🛠️ Technology Stack
          </h2>
        </div>
        <div class="card-body">
          <div class="tech-grid">
            <div class="tech-category">
              <h3>Frontend</h3>
              <div class="tech-items">
                <span class="tech-item">Vue.js 3</span>
                <span class="tech-item">Composition API</span>
                <span class="tech-item">Tailwind CSS</span>
                <span class="tech-item">Vite</span>
                <span class="tech-item">Axios</span>
              </div>
            </div>
            
            <div class="tech-category">
              <h3>Backend</h3>
              <div class="tech-items">
                <span class="tech-item">FastAPI</span>
                <span class="tech-item">Python 3.11</span>
                <span class="tech-item">Type Hints</span>
                <span class="tech-item">Microservices</span>
                <span class="tech-item">REST APIs</span>
              </div>
            </div>
            
            <div class="tech-category">
              <h3>AI & ML</h3>
              <div class="tech-items">
                <span class="tech-item">TensorFlow 2.15</span>
                <span class="tech-item">scikit-learn</span>
                <span class="tech-item">OpenAI GPT-4</span>
                <span class="tech-item">LangChain</span>
                <span class="tech-item">Pandas</span>
              </div>
            </div>
            
            <div class="tech-category">
              <h3>DevOps & Infrastructure</h3>
              <div class="tech-items">
                <span class="tech-item">GitHub Actions</span>
                <span class="tech-item">Docker</span>
                <span class="tech-item">Kubernetes</span>
                <span class="tech-item">Helm Charts</span>
                <span class="tech-item">ArgoCD</span>
              </div>
            </div>
            
            <div class="tech-category">
              <h3>Security & Quality</h3>
              <div class="tech-items">
                <span class="tech-item">Trivy</span>
                <span class="tech-item">GitGuardian</span>
                <span class="tech-item">Bandit</span>
                <span class="tech-item">Ruff</span>
                <span class="tech-item">ESLint</span>
              </div>
            </div>
            
            <div class="tech-category">
              <h3>Cloud & Platform</h3>
              <div class="tech-items">
                <span class="tech-item">Azure VM</span>
                <span class="tech-item">Terraform</span>
                <span class="tech-item">PostgreSQL</span>
                <span class="tech-item">Redis</span>
                <span class="tech-item">Docker Hub</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Interview Talking Points -->
    <div class="interview-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            🎯 Interview-Ready Talking Points
          </h2>
        </div>
        <div class="card-body">
          <div class="interview-grid">
            <div class="interview-category">
              <h3>For DevOps Engineers</h3>
              <ul>
                <li>"I built a complete CI/CD pipeline with GitHub Actions, including security scanning with Trivy and GitGuardian"</li>
                <li>"The system uses Docker for containerization and can deploy to any Kubernetes cluster"</li>
                <li>"I implemented proper secret management and infrastructure as code"</li>
              </ul>
            </div>
            
            <div class="interview-category">
              <h3>For Kubernetes Engineers</h3>
              <ul>
                <li>"I designed a multi-service architecture with Helm charts for easy deployment"</li>
                <li>"The system integrates with ArgoCD for GitOps-style deployments"</li>
                <li>"I earned my CKA and this demo shows real-world Kubernetes patterns"</li>
              </ul>
            </div>
            
            <div class="interview-category">
              <h3>For AI/ML Engineers</h3>
              <ul>
                <li>"I built a custom TensorFlow classifier that learns from engineering tasks"</li>
                <li>"The system includes proper MLOps practices like model versioning and retraining"</li>
                <li>"I implemented human-in-loop workflows for continuous learning"</li>
              </ul>
            </div>
            
            <div class="interview-category">
              <h3>For Platform Engineers</h3>
              <ul>
                <li>"This demonstrates end-to-end platform engineering from frontend to infrastructure"</li>
                <li>"I used microservices architecture with proper API design and documentation"</li>
                <li>"The system is designed for scalability and maintainability"</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Demo Features -->
    <div class="features-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            ✨ Demo Features
          </h2>
        </div>
        <div class="card-body">
          <div class="features-grid">
            <div class="feature-item">
              <div class="feature-icon">
                🎯
              </div>
              <h3>Task Processing</h3>
              <p>Submit Kubernetes/CD tasks and watch real-time processing through the Whis pipeline with AI-powered matching</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                📚
              </div>
              <h3>Orb Library</h3>
              <p>Browse categorized best practices and solutions, including Training Orbs with ML model versioning</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                🧠
              </div>
              <h3>Learning System</h3>
              <p>Human-in-loop approval workflow with continuous learning from approved tasks and model retraining</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                🔍
              </div>
              <h3>Intelligent Matching</h3>
              <p>Advanced algorithms using TensorFlow and semantic search to match tasks with relevant solutions</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                ⚡
              </div>
              <h3>Real-time Pipeline</h3>
              <p>Visual representation of the Whis pipeline with step-by-step processing and tool details</p>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                🛡️
              </div>
              <h3>Professional UI</h3>
              <p>Modern, responsive design with real-time updates and interactive components</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Getting Started -->
    <div class="getting-started-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            🚀 Getting Started
          </h2>
        </div>
        <div class="card-body">
          <div class="started-grid">
            <div class="started-item">
              <h3>1. Try the Demo</h3>
              <p>Submit Kubernetes tasks like "create a pod named test with image nginx" and watch the AI processing</p>
            </div>
            
            <div class="started-item">
              <h3>2. Explore the Pipeline</h3>
              <p>Navigate to the Whis Pipeline page to see the step-by-step processing with tool details</p>
            </div>
            
            <div class="started-item">
              <h3>3. Browse Orbs</h3>
              <p>Check out the Orb Library to see both execution Orbs and Training Orbs with ML models</p>
            </div>
            
            <div class="started-item">
              <h3>4. Add API Keys</h3>
              <p>Configure AI API keys in the Keys page to enable real AI processing instead of demo mode</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact Section -->
    <div class="contact-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">
            📞 About This Demo
          </h2>
        </div>
        <div class="card-body">
          <div class="contact-content">
            <p class="contact-text">
              This demo represents the kind of systems I'd build and maintain in a real platform engineering role. 
              It showcases my ability to work across the entire stack - from frontend development to infrastructure automation, 
              from AI/ML integration to DevOps best practices.
            </p>
            <p class="contact-text">
              The platform demonstrates real-world skills that are directly applicable to modern engineering teams: 
              microservices architecture, containerization, CI/CD automation, security scanning, and AI/ML integration.
            </p>
            <div class="contact-badges">
              <span class="contact-badge">🎯 Production Ready</span>
              <span class="contact-badge">🧠 AI/ML Powered</span>
              <span class="contact-badge">☸️ Kubernetes Native</span>
              <span class="contact-badge">🚀 Scalable Architecture</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No additional logic needed for this component
</script>

<style scoped>
.about-demo {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  margin-bottom: 2rem;
}

.hero-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: #64748b;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-badges {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-badge {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.story-section {
  margin-bottom: 2rem;
}

.story-text {
  font-size: 1.125rem;
  line-height: 1.7;
  color: #374151;
  margin-bottom: 1.5rem;
}

.story-highlights {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 4px solid #3b82f6;
}

.highlight-icon {
  font-size: 1.5rem;
}

.highlight-text {
  font-weight: 500;
  color: #1e293b;
}

.skills-section {
  margin-bottom: 2rem;
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.skill-category {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
}

.skill-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.skill-icon {
  font-size: 2rem;
}

.skill-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.skill-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.skill-list li {
  padding: 0.5rem 0;
  color: #64748b;
  position: relative;
  padding-left: 1.5rem;
}

.skill-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: bold;
}

.pipeline-section {
  margin-bottom: 2rem;
}

.pipeline-intro {
  font-size: 1.125rem;
  line-height: 1.7;
  color: #374151;
  margin-bottom: 2rem;
}

.pipeline-stages {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stage-item {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.stage-number {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.125rem;
  flex-shrink: 0;
}

.stage-content h4 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.stage-content p {
  color: #64748b;
  margin: 0 0 1rem 0;
  line-height: 1.6;
}

.stage-tools {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.tech-stack-section {
  margin-bottom: 2rem;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.tech-category h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

.tech-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tech-item {
  background: #e0e7ff;
  color: #3730a3;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.interview-section {
  margin-bottom: 2rem;
}

.interview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.interview-category h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
}

.interview-category ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.interview-category li {
  padding: 0.75rem 0;
  color: #64748b;
  line-height: 1.6;
  border-bottom: 1px solid #f1f5f9;
}

.interview-category li:last-child {
  border-bottom: none;
}

.features-section {
  margin-bottom: 2rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-item {
  text-align: center;
  padding: 2rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-item h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

.feature-item p {
  color: #64748b;
  line-height: 1.6;
}

.getting-started-section {
  margin-bottom: 2rem;
}

.started-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.started-item {
  padding: 1.5rem;
  background: #f0f9ff;
  border-radius: 12px;
  border: 1px solid #bae6fd;
}

.started-item h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #0c4a6e;
  margin-bottom: 1rem;
}

.started-item p {
  color: #0369a1;
  line-height: 1.6;
}

.contact-section {
  margin-bottom: 2rem;
}

.contact-content {
  text-align: center;
}

.contact-text {
  font-size: 1.125rem;
  line-height: 1.7;
  color: #374151;
  margin-bottom: 2rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.contact-badges {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.contact-badge {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .skills-grid,
  .tech-grid,
  .interview-grid,
  .features-grid,
  .started-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-badges,
  .contact-badges {
    flex-direction: column;
    align-items: center;
  }
  
  .stage-item {
    flex-direction: column;
    text-align: center;
  }
  
  .stage-number {
    align-self: center;
  }
}
</style> 