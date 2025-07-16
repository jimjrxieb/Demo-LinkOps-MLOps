<template>
  <div class="orb-result-card">
    <div class="card-header">
      <h2 class="card-title">
        ✅ Orb Match Found!
      </h2>
    </div>
    <div class="card-body">
      <h3 class="orb-title">
        {{ orb.title }}
      </h3>
      <p class="orb-category">
        Category: {{ orb.category }}
      </p>
      <p class="orb-description">
        {{ orb.orb }}
      </p>
      <p class="confidence-score">
        Confidence: {{ confidence }}%
      </p>
      <div class="orb-keywords">
        <span class="keywords-label">Tags:</span>
        <div class="keyword-tags">
          <span
            v-for="tag in orb.keywords"
            :key="tag"
            class="keyword-tag"
          >#{{ tag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  orb: Object,
  confidence: [String, Number]
});
</script>

<style scoped>
.orb-result-card {
  background: linear-gradient(135deg, #065f46, #047857);
  border: 1px solid #10b981;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.orb-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #d1fae5;
  margin: 0 0 0.5rem 0;
}

.orb-category {
  font-size: 0.875rem;
  color: #9ca3af;
  font-style: italic;
  margin-bottom: 1rem;
}

.orb-description {
  color: #e5e7eb;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.confidence-score {
  font-size: 0.875rem;
  color: #93c5fd;
  font-weight: 500;
  margin-bottom: 1rem;
}

.orb-keywords {
  margin-top: 1rem;
}

.keywords-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #9ca3af;
  margin-bottom: 0.5rem;
  display: block;
}

.keyword-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.keyword-tag {
  background: rgba(16, 185, 129, 0.2);
  color: #d1fae5;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
</style> 