<template>
  <div class="whis-pipeline">
    <!-- Header Section -->
    <div class="header-section">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title">🧠 Whis Learning Pipeline</h2>
          <p class="text-gray-600">Visualize the AI-powered task processing and learning stages</p>
        </div>
        <div class="card-body">
          <div class="pipeline-overview">
            <p>The Whis pipeline processes tasks through multiple intelligent stages, each designed to enhance understanding and generate optimal solutions.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Pipeline Stages -->
    <div class="pipeline-stages">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">Pipeline Stages</h3>
        </div>
        <div class="card-body">
          <div class="stages-grid">
            <!-- Stage 1: Input -->
            <div class="stage-card">
              <div class="stage-header">
                <div class="stage-icon">📥</div>
                <div class="stage-info">
                  <h4>1. Input Processing</h4>
                  <span class="stage-status">Active</span>
                </div>
              </div>
              <div class="stage-content">
                <p>Raw task input is received and validated. The system analyzes the request format, extracts key parameters, and prepares for processing.</p>
                <ul class="stage-features">
                  <li>Input validation and sanitization</li>
                  <li>Parameter extraction</li>
                  <li>Request categorization</li>
                  <li>Priority assessment</li>
                </ul>
              </div>
            </div>

            <!-- Stage 2: Sanitization -->
            <div class="stage-card">
              <div class="stage-header">
                <div class="stage-icon">🧹</div>
                <div class="stage-info">
                  <h4>2. Sanitization</h4>
                  <span class="stage-status">Active</span>
                </div>
              </div>
              <div class="stage-content">
                <p>Input is cleaned and normalized to ensure consistency and security. This stage removes noise, validates content, and prepares for analysis.</p>
                <ul class="stage-features">
                  <li>Content cleaning and normalization</li>
                  <li>Security validation</li>
                  <li>Format standardization</li>
                  <li>Noise reduction</li>
                </ul>
              </div>
            </div>

            <!-- Stage 3: Smithing -->
            <div class="stage-card active">
              <div class="stage-header">
                <div class="stage-icon">⚒️</div>
                <div class="stage-info">
                  <h4>3. Smithing</h4>
                  <span class="stage-status active">Processing</span>
                </div>
              </div>
              <div class="stage-content">
                <p>The core AI processing stage where the system analyzes requirements, identifies patterns, and crafts intelligent solutions.</p>
                
                <div class="smithing-process">
                  <h5>Smithing Process Includes:</h5>
                  <ul class="stage-features">
                    <li>Analyze the task requirements</li>
                    <li>Identify key components and dependencies</li>
                    <li>Follow industry best practices</li>
                    <li>Implement with proper error handling</li>
                    <li>Test and validate the solution</li>
                  </ul>
                </div>
                
                <div class="smithing-details">
                  <p><strong>AI Analysis:</strong> The system uses advanced language models to understand context, extract requirements, and identify the most appropriate solution patterns.</p>
                  <p><strong>Best Practices:</strong> Solutions are crafted following DevSecOps principles, security guidelines, and industry standards.</p>
                  <p><strong>Quality Assurance:</strong> Each solution includes proper error handling, validation, and testing recommendations.</p>
                </div>
              </div>
            </div>

            <!-- Stage 4: Evaluation -->
            <div class="stage-card">
              <div class="stage-header">
                <div class="stage-icon">📊</div>
                <div class="stage-info">
                  <h4>4. Evaluation</h4>
                  <span class="stage-status">Pending</span>
                </div>
              </div>
              <div class="stage-content">
                <p>Generated solutions are evaluated for quality, security, and effectiveness. Confidence scores and recommendations are provided.</p>
                <ul class="stage-features">
                  <li>Solution quality assessment</li>
                  <li>Security compliance checking</li>
                  <li>Performance optimization</li>
                  <li>Confidence scoring</li>
                </ul>
              </div>
            </div>

            <!-- Stage 5: Output -->
            <div class="stage-card">
              <div class="stage-header">
                <div class="stage-icon">📤</div>
                <div class="stage-info">
                  <h4>5. Output Generation</h4>
                  <span class="stage-status">Pending</span>
                </div>
              </div>
              <div class="stage-content">
                <p>Final solutions are formatted and presented with explanations, confidence scores, and additional recommendations.</p>
                <ul class="stage-features">
                  <li>Solution formatting</li>
                  <li>Explanation generation</li>
                  <li>Confidence reporting</li>
                  <li>Additional recommendations</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Learning Insights -->
    <div class="learning-insights">
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">🎓 Learning Insights</h3>
        </div>
        <div class="card-body">
          <div class="insights-grid">
            <div class="insight-item">
              <div class="insight-icon">📈</div>
              <div class="insight-content">
                <h4>Continuous Learning</h4>
                <p>The Whis pipeline learns from each interaction, improving its understanding and solution quality over time.</p>
              </div>
            </div>
            
            <div class="insight-item">
              <div class="insight-icon">🔍</div>
              <div class="insight-content">
                <h4>Pattern Recognition</h4>
                <p>Advanced algorithms identify patterns in tasks and solutions, enabling faster and more accurate processing.</p>
              </div>
            </div>
            
            <div class="insight-item">
              <div class="insight-icon">🛡️</div>
              <div class="insight-content">
                <h4>Security Focus</h4>
                <p>Every solution is evaluated for security implications and compliance with best practices.</p>
              </div>
            </div>
            
            <div class="insight-item">
              <div class="insight-icon">⚡</div>
              <div class="insight-content">
                <h4>Performance Optimization</h4>
                <p>Solutions are optimized for performance, scalability, and maintainability.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Demo Notice -->
    <div class="demo-notice">
      <div class="card">
        <div class="card-body">
          <div class="notice-content">
            <div class="notice-icon">🎯</div>
            <div class="notice-text">
              <h4>Demo Mode Active</h4>
              <p>This visualization shows the Whis pipeline structure. In production, each stage processes real tasks with live AI models and generates actual solutions.</p>
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
.whis-pipeline {
  space-y: 6;
}

.header-section {
  margin-bottom: 2rem;
}

.pipeline-overview {
  color: #64748b;
  line-height: 1.6;
}

.pipeline-stages {
  margin-bottom: 2rem;
}

.stages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.stage-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stage-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stage-card.active {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.stage-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.stage-icon {
  font-size: 2rem;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.stage-info h4 {
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
}

.stage-status {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  background: #f1f5f9;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stage-status.active {
  background: #dcfce7;
  color: #166534;
}

.stage-content {
  padding: 1.5rem;
}

.stage-content p {
  color: #374151;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.stage-features {
  list-style: none;
  padding: 0;
  margin: 0;
}

.stage-features li {
  color: #64748b;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f5f9;
  position: relative;
  padding-left: 1.5rem;
}

.stage-features li:before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: bold;
}

.stage-features li:last-child {
  border-bottom: none;
}

.smithing-process {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
}

.smithing-process h5 {
  color: #0369a1;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
}

.smithing-details {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
}

.smithing-details p {
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
}

.smithing-details p:last-child {
  margin-bottom: 0;
}

.learning-insights {
  margin-bottom: 2rem;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.insight-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.insight-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.insight-content h4 {
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.insight-content p {
  color: #64748b;
  line-height: 1.6;
  margin: 0;
  font-size: 0.875rem;
}

.demo-notice {
  margin-bottom: 2rem;
}

.notice-content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 1px solid #f59e0b;
  border-radius: 12px;
}

.notice-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.notice-text h4 {
  color: #92400e;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.notice-text p {
  color: #78350f;
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 768px) {
  .stages-grid {
    grid-template-columns: 1fr;
  }
  
  .insights-grid {
    grid-template-columns: 1fr;
  }
  
  .stage-header {
    flex-direction: column;
    text-align: center;
  }
  
  .notice-content {
    flex-direction: column;
    text-align: center;
  }
}
</style>
