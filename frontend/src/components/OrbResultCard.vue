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

      <!-- Rune ID Section -->
      <div
        v-if="orb.rune_id"
        class="rune-section"
      >
        <span class="rune-label">Rune ID:</span>
        <code class="rune-code">{{ orb.rune_id }}</code>
      </div>

      <!-- Best Practice Checklist Section -->
      <div
        v-if="orb.best_practice_checklist && orb.best_practice_checklist.length"
        class="checklist-section"
      >
        <h4 class="section-title">
          ✅ Best Practice Checklist
        </h4>
        <div class="checklist-container">
          <div
            v-for="(item, index) in orb.best_practice_checklist"
            :key="index"
            class="checklist-item"
            :class="{
              header:
                item.startsWith('📋') ||
                item.startsWith('🔧') ||
                item.startsWith('🔐') ||
                item.startsWith('⚙️') ||
                item.startsWith('🚀') ||
                item.startsWith('🔄') ||
                item.startsWith('🔒') ||
                item.startsWith('✅'),
              empty: item.trim() === '',
            }"
          >
            <span
              v-if="item.trim() !== ''"
              v-html="formatChecklistItem(item)"
            />
          </div>
          <button
            class="copy-btn checklist-copy"
            @click="copyCommand(orb.best_practice_checklist.join('\\n'))"
          >
            📋 Copy Full Checklist
          </button>
        </div>
      </div>

      <!-- Declarative Template Section -->
      <div
        v-if="orb.declarative_template"
        class="template-section"
      >
        <h4 class="section-title">
          📄 Declarative Template
        </h4>
        <div class="code-block">
          <pre><code>{{ orb.declarative_template }}</code></pre>
        </div>
      </div>

      <!-- Imperative Commands Section -->
      <div
        v-if="orb.imperative_commands"
        class="commands-section"
      >
        <h4 class="section-title">
          ⚡ Imperative Commands
        </h4>
        <div class="commands-list">
          <div
            v-for="(command, index) in orb.imperative_commands"
            :key="index"
            class="command-item"
            :class="{
              comment: command.startsWith('#'),
              empty: command.trim() === '',
            }"
          >
            <span
              v-if="command.trim() !== '' && !command.startsWith('#')"
              class="command-number"
            >{{ getCommandNumber(index) }}.</span>
            <code
              v-if="command.trim() !== ''"
              class="command-code"
            >{{
              command
            }}</code>
            <button
              v-if="command.trim() !== '' && !command.startsWith('#')"
              class="copy-btn"
              title="Copy command"
              @click="copyCommand(command)"
            >
              📋
            </button>
          </div>
        </div>
      </div>

      <!-- Training Required Status -->
      <div
        v-if="orb.needsTraining"
        class="training-status"
      >
        <div class="training-badge">
          🧠 Training Required
        </div>
        <div class="training-message">
          <h4>{{ orb.trainingMessage.title }}</h4>
          <p>{{ orb.trainingMessage.message }}</p>
          <button
            class="btn btn-primary training-btn"
            @click="goToWhisTraining"
          >
            {{ orb.trainingMessage.action }}
          </button>
        </div>
      </div>

      <!-- Approval Status -->
      <div
        v-else-if="orb.needsApproval"
        class="approval-status"
      >
        <div class="approval-badge pending">
          ⏳ Awaiting Approval
        </div>
        <p class="approval-text">
          This solution was generated by the Whis pipeline and needs your
          approval before being saved to the Orb Library.
        </p>
      </div>

      <div
        v-else-if="orb.approved"
        class="approval-status"
      >
        <div class="approval-badge approved">
          ✅ Approved & Saved
        </div>
        <p class="approval-text">
          This solution has been approved and saved to the Orb Library.
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="action-buttons">
        <button
          v-if="!orb.needsApproval"
          class="btn btn-primary"
          @click="useOrb"
        >
          🚀 Use This Orb
        </button>
        <button
          class="btn btn-secondary"
          @click="viewDetails"
        >
          📖 View Details
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  orb: Object,
  confidence: [String, Number],
});

const copyCommand = (command) => {
  navigator.clipboard.writeText(command);
  // Simple feedback - you could enhance this with a toast notification
  console.log('Command copied to clipboard:', command);
};

const formatChecklistItem = (item) => {
  // Format markdown-style text with code blocks and bold text
  let formatted = item
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold text
    .replace(/`(.*?)`/g, '<code>$1</code>') // Inline code
    .replace(/□/g, '<input type="checkbox" disabled>') // Checkboxes
    .replace(/- /g, '• '); // Bullet points

  return formatted;
};

const getCommandNumber = (index) => {
  // Count only non-comment, non-empty commands before this index
  let commandCount = 0;
  for (let i = 0; i <= index; i++) {
    const cmd = props.orb.imperative_commands[i];
    if (cmd && cmd.trim() !== '' && !cmd.startsWith('#')) {
      commandCount++;
    }
  }
  return commandCount;
};

const goToWhisTraining = () => {
  // Navigate to Whis Pipeline tab with the training task
  window.location.href = '/pipeline';
};

const useOrb = () => {
  console.log('Using orb:', orb.title);
  // Implement orb usage logic
};

const viewDetails = () => {
  console.log('Viewing orb details:', orb.title);
  // Implement detailed view logic
};
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
  margin-bottom: 1rem;
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

.rune-section {
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.rune-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #9ca3af;
}

.rune-code {
  background: rgba(0, 0, 0, 0.3);
  color: #fbbf24;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  border: 1px solid rgba(251, 191, 36, 0.3);
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #d1fae5;
  margin: 1.5rem 0 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.template-section,
.commands-section {
  margin: 1.5rem 0;
}

.code-block {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  padding: 1rem;
  overflow-x: auto;
}

.code-block pre {
  margin: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
  line-height: 1.4;
  color: #e5e7eb;
}

.commands-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.command-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 6px;
  padding: 0.75rem;
}

.command-number {
  font-size: 0.875rem;
  font-weight: 600;
  color: #fbbf24;
  min-width: 1.5rem;
}

.command-code {
  flex: 1;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875rem;
  color: #e5e7eb;
  background: none;
}

.copy-btn {
  background: rgba(16, 185, 129, 0.2);
  border: 1px solid rgba(16, 185, 129, 0.4);
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.copy-btn:hover {
  background: rgba(16, 185, 129, 0.3);
  transform: scale(1.05);
}

.action-buttons {
  margin-top: 1.5rem;
  display: flex;
  gap: 0.75rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
}

.btn-secondary {
  background: rgba(16, 185, 129, 0.2);
  color: #d1fae5;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.btn-secondary:hover {
  background: rgba(16, 185, 129, 0.3);
  transform: translateY(-1px);
}

.approval-status {
  margin: 1.5rem 0;
  padding: 1rem;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.approval-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.approval-badge.pending {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.4);
}

.approval-badge.approved {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.approval-text {
  color: #cbd5e1;
  font-size: 0.875rem;
  line-height: 1.4;
  margin: 0;
}

/* Checklist Section */
.checklist-section {
  margin: 1.5rem 0;
}

.checklist-container {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.checklist-item {
  margin: 0.5rem 0;
  line-height: 1.6;
  color: #e5e7eb;
  font-size: 0.875rem;
}

.checklist-item.header {
  font-weight: 600;
  color: #10b981;
  font-size: 1rem;
  margin: 1rem 0 0.75rem 0;
  border-bottom: 1px solid rgba(16, 185, 129, 0.3);
  padding-bottom: 0.5rem;
}

.checklist-item.empty {
  margin: 0.25rem 0;
  height: 0.25rem;
}

.checklist-item input[type='checkbox'] {
  margin-right: 0.5rem;
  accent-color: #10b981;
}

.checklist-item code {
  background: rgba(16, 185, 129, 0.2);
  color: #d1fae5;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-size: 0.8rem;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.checklist-item strong {
  color: #10b981;
  font-weight: 600;
}

.checklist-copy {
  margin-top: 1rem;
  width: 100%;
}

/* Enhanced Command Styling */
.command-item.comment {
  opacity: 0.7;
  font-style: italic;
}

.command-item.comment .command-code {
  color: #9ca3af;
}

.command-item.empty {
  height: 0.5rem;
}

/* Training Status */
.training-status {
  margin: 1.5rem 0;
  padding: 1.5rem;
  border-radius: 8px;
  background: rgba(147, 51, 234, 0.1);
  border: 1px solid rgba(147, 51, 234, 0.3);
}

.training-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
  background: rgba(147, 51, 234, 0.2);
  color: #a855f7;
  border: 1px solid rgba(147, 51, 234, 0.4);
}

.training-message h4 {
  color: #a855f7;
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
}

.training-message p {
  color: #cbd5e1;
  font-size: 0.875rem;
  line-height: 1.4;
  margin: 0 0 1.25rem 0;
}

.training-btn {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.training-btn:hover {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}
</style>
