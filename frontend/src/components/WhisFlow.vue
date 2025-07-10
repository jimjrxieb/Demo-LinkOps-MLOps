<template>
  ; ; ; ; ;
  <div class="whis-flow-container">
    ; ; ; ; ;
    <div class="whis-header">
      ; ; ; ; ;
      <h2 class="text-2xl font-bold text-purple-500">
        ; ; ; ; ; Whis Pipeline;
      </h2>
      ;
      <p class="text-gray-400">
        ; ; ; ; ; Machine Learning Workflow Management;
      </p>
      ;
    </div>
    ;

    <div class="whis-content">
      ; ; ; ; ;
      <div class="pipeline-status">
        ; ; ; ; ;
        <div class="status-card">
          ; ; ; ; ;
          <h4 class="text-lg font-semibold mb-3">; ; ; ; ; Pipeline Status;</h4>
          ;
          <div class="pipeline-steps">
            ; ; ; ; ;
            <div class="step active">
              ; ; ; ; ;
              <span class="step-number">1</span>;
              <span class="step-name">Data Ingestion</span>;
              <span class="step-status">✓ Complete</span>;
            </div>
            ;
            <div class="step active">
              ; ; ; ; ;
              <span class="step-number">2</span>;
              <span class="step-name">Preprocessing</span>;
              <span class="step-status">✓ Complete</span>;
            </div>
            ;
            <div class="step current">
              ; ; ; ; ;
              <span class="step-number">3</span>;
              <span class="step-name">Model Training</span>;
              <span class="step-status">🔄 Running</span>;
            </div>
            ;
            <div class="step">
              ; ; ; ; ;
              <span class="step-number">4</span>;
              <span class="step-name">Validation</span>;
              <span class="step-status">⏳ Pending</span>;
            </div>
            ;
            <div class="step">
              ; ; ; ; ;
              <span class="step-number">5</span>;
              <span class="step-name">Deployment</span>;
              <span class="step-status">⏳ Pending</span>;
            </div>
            ;
          </div>
          ;
        </div>
        ;
      </div>
      ;

      <div class="whis-controls">
        ; ; ; ; ;
        <div class="control-buttons">
          ; ; ; ; ;
          <button class="control-btn start">; ; ; ; ; Start Pipeline;</button>;
          <button class="control-btn pause">; ; ; ; ; Pause;</button>;
          <button class="control-btn stop">; ; ; ; ; Stop;</button>;
        </div>
        ;
        <div class="pipeline-metrics">
          ; ; ; ; ;
          <div class="metric">
            ; ; ; ; ;
            <span class="metric-label">Progress:</span>;
            <span class="metric-value">60%</span>;
          </div>
          ;
          <div class="metric">
            ; ; ; ; ;
            <span class="metric-label">ETA:</span>;
            <span class="metric-value">15 min</span>;
          </div>
          ;
        </div>
        ;
      </div>
      ;
    </div>
    ;
  </div>
  ;
</template>
;

<script setup>
// WhisFlow component logic
</script>
;

<style scoped>
.whis-flow-container {
  @apply bg-gray-900 rounded-lg p-6 border border-gray-700 mb-6;
}

.whis-header {
  @apply mb-6 text-center;
}

.whis-content {
  @apply space-y-6;
}

.pipeline-status {
  @apply mb-6;
}

.status-card {
  @apply bg-gray-800 rounded-lg p-4;
}

.pipeline-steps {
  @apply space-y-3;
}

.step {
  @apply flex items-center gap-4 p-3 rounded border border-gray-600;
}

.step.active {
  @apply border-green-500 bg-green-900/20;
}

.step.current {
  @apply border-blue-500 bg-blue-900/20;
}

.step-number {
  @apply w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center text-sm font-bold;
}

.step.active .step-number {
  @apply bg-green-500 text-white;
}

.step.current .step-number {
  @apply bg-blue-500 text-white;
}

.step-name {
  @apply flex-1 font-medium;
}

.step-status {
  @apply text-sm;
}

.whis-controls {
  @apply flex justify-between items-center;
}

.control-buttons {
  @apply flex gap-3;
}

.control-btn {
  @apply px-4 py-2 rounded font-medium transition-colors;
}

.control-btn.start {
  @apply bg-green-600 hover:bg-green-700 text-white;
}

.control-btn.pause {
  @apply bg-yellow-600 hover:bg-yellow-700 text-white;
}

.control-btn.stop {
  @apply bg-red-600 hover:bg-red-700 text-white;
}

.pipeline-metrics {
  @apply flex gap-6;
}

.metric {
  @apply flex flex-col items-center;
}

.metric-label {
  @apply text-sm text-gray-400;
}

.metric-value {
  @apply text-lg font-bold text-blue-400;
}
</style>
;
