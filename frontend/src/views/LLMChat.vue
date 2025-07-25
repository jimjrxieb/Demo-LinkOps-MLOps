<!-- LLMChat.vue -->
<template>
  <div class="p-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">
        💬 AI Box Chat Interface
      </h1>
      <p class="text-gray-600">
        Ask questions about your policies, documents, and tenant data using
        AI-powered retrieval
      </p>
    </div>

    <!-- Chat Settings Panel -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-700">🎛️ Chat Settings</h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Results Count -->
        <div>
          <label class="block font-semibold mb-2 text-gray-700"
            >📊 Results:</label
          >
          <select
            v-model="chatSettings.top_k"
            class="border border-gray-300 px-4 py-2 rounded-lg w-full focus:ring-2 focus:ring-blue-500"
          >
            <option value="3">3 sources</option>
            <option value="5">5 sources</option>
            <option value="10">10 sources</option>
            <option value="15">15 sources</option>
          </select>
        </div>

        <!-- Similarity Threshold -->
        <div>
          <label class="block font-semibold mb-2 text-gray-700"
            >🎯 Accuracy:</label
          >
          <select
            v-model="chatSettings.similarity_threshold"
            class="border border-gray-300 px-4 py-2 rounded-lg w-full focus:ring-2 focus:ring-blue-500"
          >
            <option value="0.3">Low (0.3)</option>
            <option value="0.5">Medium (0.5)</option>
            <option value="0.7">High (0.7)</option>
            <option value="0.8">Very High (0.8)</option>
          </select>
        </div>

        <!-- Include Metadata -->
        <div>
          <label class="block font-semibold mb-2 text-gray-700"
            >📋 Metadata:</label
          >
          <div class="flex items-center mt-3">
            <input
              v-model="chatSettings.include_metadata"
              type="checkbox"
              class="mr-2 rounded"
            />
            <span class="text-gray-700">Include document details</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Interface -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Chat Messages (Left Column - 2/3) -->
      <div class="lg:col-span-2">
        <div
          class="bg-white rounded-lg shadow-md overflow-hidden flex flex-col h-[600px]"
        >
          <!-- Chat Header -->
          <div
            class="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="text-2xl">🤖</span>
                <div>
                  <h3 class="font-semibold">AI Assistant</h3>
                  <p class="text-sm opacity-90">Powered by RAG + LLM</p>
                </div>
              </div>
              <div class="flex gap-2">
                <button
                  class="bg-white bg-opacity-20 hover:bg-opacity-30 px-3 py-1 rounded text-sm transition-colors"
                  @click="clearChat"
                >
                  🧹 Clear
                </button>
                <button
                  :disabled="messages.length === 0"
                  class="bg-white bg-opacity-20 hover:bg-opacity-30 disabled:bg-opacity-10 px-3 py-1 rounded text-sm transition-colors"
                  @click="exportChat"
                >
                  📄 Export
                </button>
              </div>
            </div>
          </div>

          <!-- Messages Area -->
          <div
            ref="messagesContainer"
            class="flex-1 overflow-y-auto p-4 space-y-4"
          >
            <!-- Welcome Message -->
            <div v-if="messages.length === 0" class="text-center py-8">
              <div class="text-6xl mb-4">🤖</div>
              <h3 class="text-xl font-semibold text-gray-700 mb-2">
                Welcome to AI Box Chat!
              </h3>
              <p class="text-gray-600 mb-4">
                Ask me anything about your policies, documents, or tenant data.
              </p>
              <div
                class="grid grid-cols-1 md:grid-cols-2 gap-2 max-w-md mx-auto"
              >
                <button
                  v-for="suggestion in chatSuggestions"
                  :key="suggestion"
                  class="bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2 rounded-lg text-sm transition-colors"
                  @click="sendMessage(suggestion)"
                >
                  {{ suggestion }}
                </button>
              </div>
            </div>

            <!-- Chat Messages -->
            <div
              v-for="message in messages"
              :key="message.id"
              class="flex gap-3"
              :class="message.type === 'user' ? 'justify-end' : 'justify-start'"
            >
              <!-- User Message -->
              <div v-if="message.type === 'user'" class="max-w-[80%]">
                <div
                  class="bg-blue-600 text-white px-4 py-2 rounded-lg rounded-br-sm"
                >
                  <p class="whitespace-pre-wrap">
                    {{ message.content }}
                  </p>
                </div>
                <div class="text-xs text-gray-500 mt-1 text-right">
                  {{ formatTime(message.timestamp) }}
                </div>
              </div>

              <!-- AI Message -->
              <div v-else class="max-w-[85%]">
                <div class="flex items-start gap-3">
                  <div
                    class="bg-gradient-to-br from-purple-500 to-blue-500 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
                  >
                    AI
                  </div>
                  <div class="flex-1">
                    <!-- AI Answer -->
                    <div class="bg-gray-100 px-4 py-3 rounded-lg rounded-tl-sm">
                      <div
                        v-if="message.loading"
                        class="flex items-center gap-2"
                      >
                        <div class="animate-spin text-blue-600">⏳</div>
                        <span class="text-gray-600">AI is thinking...</span>
                      </div>
                      <div v-else>
                        <p class="whitespace-pre-wrap text-gray-800">
                          {{ message.content }}
                        </p>

                        <!-- Sources Section -->
                        <div
                          v-if="message.sources && message.sources.length > 0"
                          class="mt-4 pt-3 border-t border-gray-200"
                        >
                          <h4
                            class="font-semibold text-gray-700 mb-2 flex items-center gap-2"
                          >
                            <span>📚</span>
                            Sources ({{ message.sources.length }})
                          </h4>
                          <div class="space-y-2">
                            <div
                              v-for="(source, index) in message.sources"
                              :key="index"
                              class="bg-white border border-gray-200 rounded p-3"
                            >
                              <div
                                class="flex items-start justify-between mb-2"
                              >
                                <div class="flex items-center gap-2">
                                  <span
                                    class="text-sm font-medium text-blue-600"
                                    >Source {{ index + 1 }}</span
                                  >
                                  <span
                                    class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded"
                                  >
                                    {{
                                      (source.similarity_score * 100).toFixed(
                                        1
                                      )
                                    }}% match
                                  </span>
                                </div>
                                <button
                                  class="text-xs text-gray-500 hover:text-gray-700"
                                  @click="showSourceDetails(source)"
                                >
                                  👁️ View
                                </button>
                              </div>
                              <p class="text-sm text-gray-700 line-clamp-3">
                                {{ source.content.substring(0, 200) }}...
                              </p>
                              <div
                                v-if="source.metadata"
                                class="mt-2 text-xs text-gray-500"
                              >
                                📄
                                {{
                                  source.metadata.source_file ||
                                  source.document_id
                                }}
                              </div>
                            </div>
                          </div>
                        </div>

                        <!-- Query Info -->
                        <div
                          v-if="message.queryInfo"
                          class="mt-3 pt-2 border-t border-gray-200"
                        >
                          <div
                            class="flex items-center gap-4 text-xs text-gray-500"
                          >
                            <span
                              >⏱️
                              {{
                                message.queryInfo.execution_time?.toFixed(3)
                              }}s</span
                            >
                            <span
                              >🧠
                              {{
                                message.queryInfo.llm_used || 'AI Model'
                              }}</span
                            >
                            <span
                              >📊 {{ message.queryInfo.total_sources }} sources
                              found</span
                            >
                          </div>
                        </div>

                        <!-- Demo Q&A follow-up -->
                        <div
                          v-if="message.content === fallbackMessage"
                          class="mt-4"
                        >
                          <router-link
                            to="/demo-sync"
                            class="inline-block bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded"
                          >
                            ⏳ Go Sync Demo Data
                          </router-link>
                        </div>

                        <div
                          v-else-if="shouldShowSendEmails(message)"
                          class="mt-4 space-y-2"
                        >
                          <button
                            @click="confirmAndSendEmails"
                            :disabled="emailLoading"
                            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                          >
                            {{
                              emailLoading
                                ? 'Sending…'
                                : '📧 Send Reminder Emails'
                            }}
                          </button>
                          <div v-if="emailResult" class="text-green-600">
                            {{ emailResult }}
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="text-xs text-gray-500 mt-1">
                      {{ formatTime(message.timestamp) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Input Area -->
          <div class="border-t border-gray-200 p-4">
            <div class="flex gap-3">
              <div class="flex-1">
                <textarea
                  v-model="currentMessage"
                  placeholder="Ask a question about your data..."
                  class="w-full border border-gray-300 rounded-lg px-4 py-2 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows="2"
                  :disabled="isLoading"
                  @keydown.enter.prevent="handleEnter"
                />
              </div>
              <div class="flex flex-col gap-2">
                <button
                  :disabled="!currentMessage.trim() || isLoading"
                  class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg font-semibold transition-colors duration-200 flex items-center gap-2"
                  @click="sendMessage()"
                >
                  <span v-if="isLoading" class="animate-spin">⏳</span>
                  <span v-else>🚀</span>
                  {{ isLoading ? 'Asking...' : 'Send' }}
                </button>
                <button
                  :disabled="!currentMessage.trim()"
                  class="bg-gray-500 hover:bg-gray-600 disabled:bg-gray-300 text-white px-6 py-1 rounded text-sm transition-colors duration-200"
                  @click="currentMessage = ''"
                >
                  Clear
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Sidebar -->
      <div class="lg:col-span-1 space-y-6">
        <!-- Recent Questions -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3
            class="text-lg font-semibold mb-4 text-gray-700 flex items-center gap-2"
          >
            <span>📝</span>
            Recent Questions
          </h3>
          <div
            v-if="recentQuestions.length === 0"
            class="text-gray-500 text-sm"
          >
            No recent questions yet
          </div>
          <div v-else class="space-y-2">
            <button
              v-for="question in recentQuestions.slice(0, 5)"
              :key="question.id"
              class="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm transition-colors"
              @click="sendMessage(question.query)"
            >
              <div class="font-medium text-gray-800 truncate">
                {{ question.query }}
              </div>
              <div class="text-xs text-gray-500 mt-1">
                {{ formatTime(question.timestamp) }}
              </div>
            </button>
          </div>
        </div>

        <!-- Chat Statistics -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3
            class="text-lg font-semibold mb-4 text-gray-700 flex items-center gap-2"
          >
            <span>📊</span>
            Chat Statistics
          </h3>
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-gray-600">Questions Asked:</span>
              <span class="font-semibold text-blue-600">{{
                chatStats.totalQuestions
              }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Avg Response Time:</span>
              <span class="font-semibold text-green-600"
                >{{ chatStats.avgResponseTime }}s</span
              >
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Sources Found:</span>
              <span class="font-semibold text-purple-600">{{
                chatStats.totalSources
              }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Session Time:</span>
              <span class="font-semibold text-orange-600">{{
                sessionTime
              }}</span>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3
            class="text-lg font-semibold mb-4 text-gray-700 flex items-center gap-2"
          >
            <span>⚡</span>
            Quick Actions
          </h3>
          <div class="space-y-2">
            <button
              class="w-full bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2 rounded-lg text-sm transition-colors"
              @click="sendMessage('What are our security policies?')"
            >
              🔒 Security Policies
            </button>
            <button
              class="w-full bg-green-50 hover:bg-green-100 text-green-700 px-4 py-2 rounded-lg text-sm transition-colors"
              @click="sendMessage('Show me tenant information')"
            >
              👥 Tenant Info
            </button>
            <button
              class="w-full bg-purple-50 hover:bg-purple-100 text-purple-700 px-4 py-2 rounded-lg text-sm transition-colors"
              @click="sendMessage('What compliance requirements do we have?')"
            >
              📋 Compliance
            </button>
            <button
              class="w-full bg-orange-50 hover:bg-orange-100 text-orange-700 px-4 py-2 rounded-lg text-sm transition-colors"
              @click="sendMessage('Explain our data processing procedures')"
            >
              📊 Data Processing
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Source Details Modal -->
    <div
      v-if="selectedSource"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    >
      <div
        class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col"
      >
        <!-- Modal Header -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900">
              📄 Source Details - {{ selectedSource.document_id }}
            </h3>
            <button
              class="text-gray-400 hover:text-gray-600 text-2xl"
              @click="selectedSource = null"
            >
              ✕
            </button>
          </div>
        </div>

        <!-- Modal Content -->
        <div class="p-6 overflow-y-auto flex-1">
          <!-- Source Info -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div class="bg-gray-50 p-4 rounded-lg">
              <h4 class="font-semibold mb-2">📊 Source Info</h4>
              <div class="space-y-2 text-sm">
                <div>
                  <strong>Document ID:</strong> {{ selectedSource.document_id }}
                </div>
                <div>
                  <strong>Similarity Score:</strong>
                  {{ (selectedSource.similarity_score * 100).toFixed(2) }}%
                </div>
                <div>
                  <strong>Chunk Index:</strong> {{ selectedSource.chunk_index }}
                </div>
                <div v-if="selectedSource.metadata">
                  <strong>Source File:</strong>
                  {{ selectedSource.metadata.source_file || 'Unknown' }}
                </div>
              </div>
            </div>

            <div
              v-if="selectedSource.metadata"
              class="bg-gray-50 p-4 rounded-lg"
            >
              <h4 class="font-semibold mb-2">📋 Metadata</h4>
              <div class="space-y-2 text-sm">
                <div v-for="(value, key) in selectedSource.metadata" :key="key">
                  <strong>{{ key }}:</strong> {{ value }}
                </div>
              </div>
            </div>
          </div>

          <!-- Full Content -->
          <div class="mb-6">
            <h4 class="font-semibold mb-2">📄 Full Content</h4>
            <div class="bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
              <pre class="whitespace-pre-wrap text-sm text-gray-800">{{
                selectedSource.content
              }}</pre>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="p-6 border-t border-gray-200">
          <div class="flex justify-end gap-4">
            <button
              class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
              @click="copySourceContent(selectedSource)"
            >
              📋 Copy Content
            </button>
            <button
              class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg"
              @click="selectedSource = null"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// Demo fallback prompt exactly matches:
const fallbackMessage =
  "I don't have data on this topic. Go to the HTC tab and upload files to demo_data/ and press Sync.";

// track if we've synced demo data
const demoSynced = ref(false);

// email sending state
const emailLoading = ref(false);
const emailResult = ref('');

// computed: only show send-emails if we have data and asked about delinquencies
const shouldShowSendEmails = (message) => {
  const isSynced = localStorage.getItem('demoSynced') === 'true';
  const hasDelinquentQuery =
    message.userQuery && message.userQuery.toLowerCase().includes('delinqu');
  return isSynced && hasDelinquentQuery && message.content !== fallbackMessage;
};

// Reactive data
const messages = ref([]);
const currentMessage = ref('');
const isLoading = ref(false);
const selectedSource = ref(null);
const recentQuestions = ref([]);
const sessionStartTime = ref(Date.now());

// Chat settings
const chatSettings = ref({
  top_k: 5,
  similarity_threshold: 0.7,
  include_metadata: true,
});

// Chat suggestions
const chatSuggestions = ref([
  'What are our security policies?',
  'Show me compliance requirements',
  'Explain data processing procedures',
  'What tenant information do we have?',
]);

// Refs
const messagesContainer = ref(null);

// Computed properties
const chatStats = computed(() => {
  const questions = messages.value.filter((m) => m.type === 'user').length;
  const aiResponses = messages.value.filter(
    (m) => m.type === 'ai' && !m.loading
  );
  const totalTime = aiResponses.reduce(
    (sum, m) => sum + (m.queryInfo?.execution_time || 0),
    0
  );
  const avgTime = questions > 0 ? (totalTime / questions).toFixed(3) : '0.000';
  const totalSources = aiResponses.reduce(
    (sum, m) => sum + (m.sources?.length || 0),
    0
  );

  return {
    totalQuestions: questions,
    avgResponseTime: avgTime,
    totalSources: totalSources,
  };
});

const sessionTime = computed(() => {
  const elapsed = Math.floor((Date.now() - sessionStartTime.value) / 1000);
  const minutes = Math.floor(elapsed / 60);
  const seconds = elapsed % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
});

// Methods
const sendMessage = async (messageText = null) => {
  const text = messageText || currentMessage.value.trim();
  if (!text || isLoading.value) return;

  const userMessage = {
    id: Date.now(),
    type: 'user',
    content: text,
    timestamp: new Date().toISOString(),
  };

  const aiMessage = {
    id: Date.now() + 1,
    type: 'ai',
    content: '',
    loading: true,
    timestamp: new Date().toISOString(),
    sources: [],
    queryInfo: null,
    userQuery: text, // Track the user's query for demo logic
  };

  messages.value.push(userMessage, aiMessage);
  currentMessage.value = '';
  isLoading.value = true;

  // Add to recent questions
  recentQuestions.value.unshift({
    id: Date.now(),
    query: text,
    timestamp: new Date().toISOString(),
  });

  // Keep only last 10 recent questions
  if (recentQuestions.value.length > 10) {
    recentQuestions.value = recentQuestions.value.slice(0, 10);
  }

  await nextTick();
  scrollToBottom();

  try {
    const response = await axios.post('/api/rag/query-llm', {
      query: text,
      top_k: chatSettings.value.top_k,
      similarity_threshold: chatSettings.value.similarity_threshold,
      include_metadata: chatSettings.value.include_metadata,
    });

    // Update AI message with response
    const aiIndex = messages.value.findIndex((m) => m.id === aiMessage.id);
    if (aiIndex !== -1) {
      messages.value[aiIndex] = {
        ...aiMessage,
        loading: false,
        content:
          response.data.answer ||
          'I apologize, but I could not generate an answer for your question.',
        sources: response.data.sources || [],
        queryInfo: {
          execution_time: response.data.execution_time || 0,
          llm_used: response.data.llm_used || 'AI Model',
          model: response.data.model || 'Unknown',
          total_sources: response.data.total_sources || 0,
          citations: response.data.citations || [],
        },
      };
    }

    // check if we hit fallback or actual data
    demoSynced.value = localStorage.getItem('demoSynced') === 'true';

    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('❌ Chat query failed:', error);

    // Update AI message with error
    const aiIndex = messages.value.findIndex((m) => m.id === aiMessage.id);
    if (aiIndex !== -1) {
      messages.value[aiIndex] = {
        ...aiMessage,
        loading: false,
        content:
          'I apologize, but I encountered an error while processing your question. Please try again or contact support if the issue persists.',
        sources: [],
        queryInfo: null,
      };
    }

    // Show user-friendly error
    alert(
      'Failed to get AI response. Please check your connection and try again.'
    );
  } finally {
    isLoading.value = false;
  }
};

const handleEnter = (event) => {
  if (event.shiftKey) {
    // Allow new line with Shift+Enter
    return;
  }
  sendMessage();
};

const clearChat = () => {
  if (messages.value.length === 0) return;

  if (confirm('Are you sure you want to clear the chat history?')) {
    messages.value = [];
    recentQuestions.value = [];
    sessionStartTime.value = Date.now();
  }
};

const exportChat = () => {
  if (messages.value.length === 0) return;

  const chatData = {
    timestamp: new Date().toISOString(),
    settings: chatSettings.value,
    statistics: chatStats.value,
    messages: messages.value.map((m) => ({
      type: m.type,
      content: m.content,
      timestamp: m.timestamp,
      sources: m.sources ? m.sources.length : 0,
    })),
  };

  const blob = new Blob([JSON.stringify(chatData, null, 2)], {
    type: 'application/json',
  });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `ai-chat-export-${
    new Date().toISOString().split('T')[0]
  }.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

const showSourceDetails = (source) => {
  selectedSource.value = source;
};

const copySourceContent = async (source) => {
  try {
    await navigator.clipboard.writeText(source.content);
    alert('Source content copied to clipboard!');
  } catch (err) {
    console.error('Failed to copy:', err);
    alert('Failed to copy source content');
  }
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const formatTime = (timestamp) => {
  try {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return 'Unknown';
  }
};

// Send reminder emails via preloaded MCP tool
const sendEmails = async () => {
  emailLoading.value = true;
  emailResult.value = '';
  try {
    await axios.post('/api/mcp-tool/execute/send_emails');
    emailResult.value = 'Fake emails sent! Task complete.';
  } catch (e) {
    emailResult.value = 'Failed to send emails.';
  } finally {
    emailLoading.value = false;
  }
};

// Wrap with a confirmation dialog:
const confirmAndSendEmails = () => {
  if (
    confirm(
      'Are you sure you want to send reminder emails to these delinquent tenants? (Requires manager approval)'
    )
  ) {
    sendEmails();
  }
};

// Session time update
let sessionInterval = null;

onMounted(() => {
  // Update session time every second
  sessionInterval = setInterval(() => {
    // Force reactivity update by accessing computed property
    sessionTime.value;
  }, 1000);
});

onUnmounted(() => {
  if (sessionInterval) {
    clearInterval(sessionInterval);
  }
});
</script>

<style scoped>
/* Custom scrollbar for chat messages */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Animation for loading spinner */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Line clamp for source content */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Smooth scrolling */
.overflow-y-auto {
  scroll-behavior: smooth;
}

/* Chat bubble styling */
.rounded-br-sm {
  border-bottom-right-radius: 0.25rem;
}

.rounded-tl-sm {
  border-top-left-radius: 0.25rem;
}

/* Gradient backgrounds */
.bg-gradient-to-r {
  background: linear-gradient(to right, var(--tw-gradient-stops));
}

.bg-gradient-to-br {
  background: linear-gradient(to bottom right, var(--tw-gradient-stops));
}

/* Modal backdrop blur */
.fixed.inset-0 {
  backdrop-filter: blur(4px);
}

/* Responsive text sizing */
@media (max-width: 768px) {
  .text-3xl {
    font-size: 1.875rem;
  }

  .text-xl {
    font-size: 1.125rem;
  }
}
</style>
