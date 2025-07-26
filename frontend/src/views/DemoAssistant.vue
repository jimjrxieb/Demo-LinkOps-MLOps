<template>
  <div class="jade-chat-wrapper">
    <div class="chat-header">🟢 Jade – Your Secure AI Assistant</div>

    <div class="chat-history" ref="chatHistory">
      <div v-for="(msg, i) in messages" :key="i" :class="msg.sender">
        <div class="bubble">
          <p>{{ msg.text }}</p>

          <!-- Tool execution results -->
          <div
            v-if="msg.tool_run"
            class="tool-result"
            :class="msg.tool_run.status"
          >
            <div class="tool-header">
              🔧 Tool Execution: <code>{{ msg.tool_run.tool }}</code>
            </div>
            <div v-if="msg.tool_run.status === 'success'" class="tool-output">
              <pre>{{ JSON.stringify(msg.tool_run.result, null, 2) }}</pre>
            </div>
            <div v-else class="tool-error">
              {{ msg.tool_run.error }}
            </div>
          </div>

          <!-- Sources with highlights -->
          <div v-if="msg.sources?.length" class="sources-wrapper">
            <div class="sources-header">📚 Sources:</div>
            <div
              v-for="(source, idx) in msg.sources"
              :key="idx"
              class="source-item"
            >
              <div class="source-file">
                📄 {{ source.file }}
                <span class="source-score"
                  >{{ Math.round(source.score * 100) }}% match</span
                >
              </div>
              <div class="source-content" v-html="source.highlight"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <form @submit.prevent="sendMessage" class="chat-input-form">
      <input
        v-model="userInput"
        type="text"
        class="chat-input"
        placeholder="Ask Jade anything about your data..."
      />
      <button type="submit" :disabled="loading || !userInput" class="send-btn">
        <span v-if="!loading">Send</span>
        <span v-else class="loader">...</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const userInput = ref('')
const messages = ref([{ sender: 'jade', text: 'Hi! I'm Jade. Ask me anything about your tenant data.' }])
const loading = ref(false)
const chatHistory = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    const el = chatHistory.value
    el.scrollTop = el.scrollHeight
  })
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return
  const userMsg = { sender: 'user', text: userInput.value }
  messages.value.push(userMsg)
  loading.value = true

  try {
    const res = await axios.post('/jade/chat', { message: userInput.value })
    messages.value.push({
      sender: 'jade',
      text: res.data.answer,
      sources: res.data.sources,
      tool_run: res.data.tool_run
    })
  } catch (err) {
    messages.value.push({ sender: 'jade', text: '❌ Error reaching Jade backend.' })
  } finally {
    userInput.value = ''
    loading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.jade-chat-wrapper {
  @apply bg-white/10 backdrop-blur p-6 rounded-xl shadow-xl w-full max-w-2xl mx-auto mt-6 text-white flex flex-col;
}
.chat-header {
  @apply text-xl font-bold mb-3 border-b border-white/10 pb-2;
}
.chat-history {
  @apply flex flex-col gap-3 overflow-y-auto max-h-80 p-2 mb-3;
}
.user {
  @apply text-right;
}
.jade {
  @apply text-left;
}
.bubble {
  @apply inline-block bg-white/10 rounded-xl px-4 py-2;
}
.chat-input-form {
  @apply flex gap-2 items-center;
}
.chat-input {
  @apply flex-1 rounded-xl px-4 py-2 bg-white/10 text-white placeholder-white/50 focus:outline-none;
}
.send-btn {
  @apply px-4 py-2 bg-teal-600 hover:bg-teal-500 rounded-xl font-semibold transition disabled:opacity-50;
}
.loader {
  @apply animate-pulse text-sm;
}

/* Source styling */
.sources-wrapper {
  @apply mt-2 pt-2 border-t border-white/10;
}
.sources-header {
  @apply text-sm font-semibold text-teal-400 mb-1;
}
.source-item {
  @apply mt-2 text-sm bg-black/20 rounded p-2;
}
.source-file {
  @apply flex items-center justify-between text-xs text-teal-300 mb-1;
}
.source-score {
  @apply text-xs text-teal-400/80;
}
.source-content {
  @apply text-gray-300 text-sm;
}
.source-content :deep(mark) {
  @apply bg-teal-400/20 text-teal-300 px-1 rounded;
}

/* Tool execution styling */
.tool-result {
  @apply mt-2 pt-2 border-t border-white/10;
}
.tool-header {
  @apply text-sm font-semibold mb-1;
}
.tool-result.success .tool-header {
  @apply text-green-400;
}
.tool-result.error .tool-header {
  @apply text-red-400;
}
.tool-output {
  @apply mt-1 p-2 bg-black/20 rounded text-xs font-mono text-teal-300;
}
.tool-error {
  @apply mt-1 p-2 bg-black/20 rounded text-xs font-mono text-red-300;
}
</style>
