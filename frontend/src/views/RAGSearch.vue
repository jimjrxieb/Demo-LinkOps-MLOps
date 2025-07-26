<template>
  <div class="p-6 animate-slide-in bg-gray-900 text-white min-h-screen">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-3xl font-bold mb-6 text-blue-400">
        RAG Search: Document Q&A
      </h2>
      <p class="mb-6 text-gray-300 text-lg">
        Upload documents and ask questions. Get intelligent answers based on
        your uploaded content.
      </p>

      <!-- File Upload Section -->
      <div class="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
        <h3 class="text-xl font-semibold mb-4 text-green-400">
          📄 Upload Documents
        </h3>
        <div class="space-y-4">
          <div class="flex items-center space-x-4">
            <input
              ref="fileInput"
              type="file"
              multiple
              accept=".txt,.pdf,.doc,.docx,.md"
              class="hidden"
              @change="handleFileSelect"
            >
            <button
              class="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center"
              @click="$refs.fileInput.click()"
            >
              <svg
                class="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              Select Files
            </button>
            <button
              :disabled="!selectedFiles.length || uploading"
              class="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center"
              @click="uploadFiles"
            >
              <span v-if="!uploading">Upload to RAG</span>
              <span
                v-else
                class="flex items-center"
              >
                <svg
                  class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  />
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Uploading...
              </span>
            </button>
          </div>

          <!-- Selected Files -->
          <div
            v-if="selectedFiles.length > 0"
            class="space-y-2"
          >
            <h4 class="text-sm font-medium text-gray-300">
              Selected Files:
            </h4>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="(file, index) in selectedFiles"
                :key="index"
                class="bg-gray-700 rounded-lg px-3 py-2 text-sm flex items-center space-x-2"
              >
                <span class="text-blue-400">{{ file.name }}</span>
                <span class="text-gray-400">({{ formatFileSize(file.size) }})</span>
                <button
                  class="text-red-400 hover:text-red-300"
                  @click="removeFile(index)"
                >
                  ×
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Query Input Section -->
      <div class="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
        <h3 class="text-xl font-semibold mb-4 text-green-400">
          🔍 Ask Questions
        </h3>
        <div class="flex space-x-4 mb-4">
          <input
            v-model="query"
            type="text"
            placeholder="Ask a question about your uploaded documents..."
            class="flex-1 p-3 bg-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-600"
            @keyup.enter="handleQuery"
          >
          <button
            :disabled="!query.trim() || loading"
            class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition-all duration-200"
            @click="handleQuery"
          >
            <span v-if="!loading">Search</span>
            <span
              v-else
              class="flex items-center"
            >
              <svg
                class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                />
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Searching...
            </span>
          </button>
          <button
            :disabled="!query.trim() || loading"
            class="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center"
            @click="handleLLMQuery"
          >
            <span v-if="!loading">🧠 Ask AI</span>
            <span
              v-else
              class="flex items-center"
            >
              <svg
                class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                />
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Thinking...
            </span>
          </button>
        </div>

        <!-- Quick Query Buttons -->
        <div class="flex flex-wrap gap-2">
          <button
            v-for="quickQuery in quickQueries"
            :key="quickQuery"
            class="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm transition-colors duration-200"
            @click="
              query = quickQuery;
              handleQuery();
            "
          >
            {{ quickQuery }}
          </button>
        </div>
      </div>

      <!-- Search Results Section -->
      <div
        v-if="searchResults.length > 0 || llmAnswer"
        class="bg-gray-800 rounded-lg p-6 border border-gray-700 animate-slide-in"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-semibold text-green-400">
            {{ llmAnswer ? 'AI Answer' : 'Search Results' }}
          </h3>
          <div class="text-sm text-gray-400">
            <span v-if="llmAnswer">
              Generated in {{ executionTime.toFixed(2) }}s using {{ llmModel }}
            </span>
            <span v-else>
              Found {{ searchResults.length }} results in
              {{ executionTime.toFixed(2) }}s
            </span>
          </div>
        </div>

        <!-- LLM Answer Section -->
        <div
          v-if="llmAnswer"
          class="mb-6"
        >
          <div
            class="bg-purple-900 rounded-lg p-4 border-l-4 border-purple-500 mb-4"
          >
            <div class="flex items-center space-x-2 mb-2">
              <span class="text-sm font-medium text-purple-400">🧠 AI Answer</span>
              <span class="text-xs text-gray-400">Model: {{ llmModel }}</span>
            </div>
            <p class="text-gray-200 leading-relaxed whitespace-pre-wrap">
              {{ llmAnswer }}
            </p>
          </div>

          <!-- Citations Section -->
          <div
            v-if="citations && citations.length > 0"
            class="mt-6"
          >
            <h4 class="text-lg font-medium text-green-400 mb-3">
              📚 Citations & Source Chunks
            </h4>
            <div class="space-y-3">
              <div
                v-for="(citation, index) in citations"
                :key="index"
                class="bg-gray-700 rounded-lg p-3 border-l-4 border-green-500"
              >
                <div class="flex items-start justify-between mb-2">
                  <div class="flex items-center space-x-2">
                    <span class="text-sm font-medium text-green-400">Citation {{ index + 1 }}</span>
                    <span class="text-xs text-gray-400">Source Chunk</span>
                  </div>
                  <span class="text-xs text-gray-500">Used in AI Answer</span>
                </div>

                <div class="bg-gray-600 rounded p-2">
                  <p class="text-gray-200 text-sm leading-relaxed">
                    {{ citation }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Source Documents (Detailed) -->
          <div
            v-if="searchResults.length > 0"
            class="mt-4"
          >
            <h4 class="text-lg font-medium text-blue-400 mb-3">
              📖 Detailed Source Documents
            </h4>
            <div class="space-y-3">
              <div
                v-for="(result, index) in searchResults"
                :key="index"
                class="bg-gray-700 rounded-lg p-3 border-l-4 border-blue-500"
              >
                <div class="flex items-start justify-between mb-2">
                  <div class="flex items-center space-x-2">
                    <span class="text-sm font-medium text-blue-400">Source {{ index + 1 }}</span>
                    <span class="text-xs text-gray-400">Score: {{ (result.score * 100).toFixed(1) }}%</span>
                  </div>
                  <span class="text-xs text-gray-500">{{
                    result.metadata?.source || 'Unknown source'
                  }}</span>
                </div>

                <div class="bg-gray-600 rounded p-2">
                  <p class="text-gray-200 text-sm leading-relaxed">
                    {{ result.content }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Regular Search Results -->
        <div
          v-else
          class="space-y-4"
        >
          <div
            v-for="(result, index) in searchResults"
            :key="index"
            class="bg-gray-700 rounded-lg p-4 border-l-4 border-blue-500"
          >
            <div class="flex items-start justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-sm font-medium text-blue-400">Result {{ index + 1 }}</span>
                <span class="text-xs text-gray-400">Score: {{ (result.score * 100).toFixed(1) }}%</span>
              </div>
              <span class="text-xs text-gray-500">{{
                result.metadata?.source || 'Unknown source'
              }}</span>
            </div>

            <div class="bg-gray-600 rounded p-3 mb-3">
              <p class="text-gray-200 leading-relaxed">
                {{ result.content }}
              </p>
            </div>

            <div
              v-if="result.metadata"
              class="text-xs text-gray-400"
            >
              <div
                v-if="result.metadata.page"
                class="mb-1"
              >
                Page: {{ result.metadata.page }}
              </div>
              <div
                v-if="result.metadata.chunk_id"
                class="mb-1"
              >
                Chunk ID: {{ result.metadata.chunk_id }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Query History -->
      <div
        v-if="queryHistory.length > 0"
        class="mt-8"
      >
        <h3 class="text-xl font-semibold mb-4 text-blue-400">
          Recent Queries
        </h3>
        <div class="space-y-3">
          <div
            v-for="(item, index) in queryHistory.slice(-5)"
            :key="index"
            class="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-gray-600 transition-colors duration-200 cursor-pointer"
            :class="
              item.type === 'llm' ? 'border-purple-500' : 'border-blue-500'
            "
            @click="loadQueryFromHistory(item)"
          >
            <div class="flex justify-between items-start">
              <div>
                <div class="flex items-center space-x-2">
                  <p class="font-medium text-gray-200">
                    {{ item.query }}
                  </p>
                  <span
                    v-if="item.type === 'llm'"
                    class="text-xs bg-purple-600 text-white px-2 py-1 rounded"
                  >AI</span>
                </div>
                <p class="text-sm text-gray-400 mt-1">
                  <span v-if="item.type === 'llm'">
                    AI answer using {{ item.model }} ({{
                      item.citations?.length || 0
                    }}
                    citations)
                  </span>
                  <span v-else> {{ item.results.length }} results found </span>
                </p>
              </div>
              <span class="text-xs text-gray-500">{{ item.timestamp }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- System Status -->
      <div class="mt-8 bg-gray-800 rounded-lg p-4 border border-gray-700">
        <h3 class="text-lg font-semibold mb-2 text-blue-400">
          System Status
        </h3>
        <div
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm"
        >
          <div class="flex items-center space-x-2">
            <div
              :class="systemStatus.rag ? 'bg-green-500' : 'bg-red-500'"
              class="w-2 h-2 rounded-full"
            />
            <span>RAG Service: {{ systemStatus.rag ? 'Online' : 'Offline' }}</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 rounded-full bg-blue-500" />
            <span>Documents: {{ systemStatus.documents || 0 }}</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 rounded-full bg-purple-500" />
            <span>Vector Index:
              {{ systemStatus.vectorstore ? 'Ready' : 'Not Ready' }}</span>
          </div>
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 rounded-full bg-yellow-500" />
            <span>LLM: {{ systemStatus.llm ? 'Available' : 'Not Available' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RAGSearch',
  data() {
    return {
      query: '',
      selectedFiles: [],
      uploading: false,
      loading: false,
      searchResults: [],
      llmAnswer: '',
      llmModel: '',
      citations: [],
      executionTime: 0,
      queryHistory: [],
      systemStatus: {
        rag: false,
        documents: 0,
        vectorstore: false,
        llm: false,
      },
      quickQueries: [
        'What are the main topics?',
        'Summarize the key points',
        'What are the recommendations?',
        'Explain the process',
        'What are the requirements?',
      ],
    };
  },
  async mounted() {
    await this.checkSystemStatus();
  },
  methods: {
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    handleFileSelect(event) {
      this.selectedFiles = Array.from(event.target.files);
    },

    removeFile(index) {
      this.selectedFiles.splice(index, 1);
    },

    async uploadFiles() {
      if (!this.selectedFiles.length) return;

      this.uploading = true;

      try {
        const formData = new FormData();
        this.selectedFiles.forEach((file) => {
          formData.append('files', file);
        });

        const response = await fetch('http://localhost:9000/rag/embed-batch', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          this.$toast?.success(
            `Successfully uploaded ${this.selectedFiles.length} files!`
          );
          this.selectedFiles = [];
          await this.checkSystemStatus();
        } else {
          throw new Error('Upload failed');
        }
      } catch (error) {
        console.error('Upload error:', error);
        this.$toast?.error('Failed to upload files. Please try again.');
      } finally {
        this.uploading = false;
      }
    },

    async handleQuery() {
      if (!this.query.trim()) return;

      this.loading = true;
      const startTime = Date.now();

      try {
        const response = await fetch('http://localhost:9000/rag/query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: this.query,
            top_k: 5,
            similarity_threshold: 0.5,
            include_metadata: true,
          }),
        });

        if (response.ok) {
          const result = await response.json();
          this.searchResults = result.results || [];
          this.executionTime = (Date.now() - startTime) / 1000;

          // Save to history
          this.queryHistory.push({
            query: this.query,
            results: this.searchResults,
            timestamp: new Date().toLocaleTimeString(),
            executionTime: this.executionTime,
          });

          this.$toast?.success(`Found ${this.searchResults.length} results!`);
        } else {
          throw new Error('Query failed');
        }
      } catch (error) {
        console.error('Query error:', error);
        this.$toast?.error('Failed to process query. Please try again.');
        this.searchResults = [];
      } finally {
        this.loading = false;
      }
    },

    async handleLLMQuery() {
      if (!this.query.trim()) return;

      this.loading = true;
      this.llmAnswer = '';
      this.searchResults = [];
      const startTime = Date.now();

      try {
        const response = await fetch('http://localhost:9000/rag/query-llm', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: this.query,
            top_k: 3,
            similarity_threshold: 0.5,
            include_metadata: true,
          }),
        });

        if (response.ok) {
          const result = await response.json();
          this.llmAnswer = result.answer;
          this.llmModel = result.model;
          this.searchResults = result.sources || [];
          this.citations = result.citations || [];
          this.executionTime = (Date.now() - startTime) / 1000;

          // Save to history
          this.queryHistory.push({
            query: this.query,
            results: this.searchResults,
            answer: this.llmAnswer,
            model: this.llmModel,
            citations: this.citations,
            timestamp: new Date().toLocaleTimeString(),
            executionTime: this.executionTime,
            type: 'llm',
          });

          this.$toast?.success(`AI generated answer using ${this.llmModel}!`);
        } else {
          throw new Error('LLM query failed');
        }
      } catch (error) {
        console.error('LLM query error:', error);
        this.$toast?.error('Failed to generate AI answer. Please try again.');
        this.llmAnswer = '';
        this.searchResults = [];
        this.citations = [];
      } finally {
        this.loading = false;
      }
    },

    loadQueryFromHistory(item) {
      this.query = item.query;
      if (item.type === 'llm') {
        this.llmAnswer = item.answer;
        this.llmModel = item.model;
        this.searchResults = item.results;
        this.citations = item.citations || [];
      } else {
        this.llmAnswer = '';
        this.searchResults = item.results;
        this.citations = [];
      }
      this.executionTime = item.executionTime;
    },

    async checkSystemStatus() {
      try {
        const response = await fetch('http://localhost:9000/rag/health');
        if (response.ok) {
          const status = await response.json();
          this.systemStatus.rag = status.status === 'healthy';

          // Get document count
          const docsResponse = await fetch('http://localhost:9000/rag/stats');
          if (docsResponse.ok) {
            const stats = await docsResponse.json();
            this.systemStatus.documents = stats.total_documents || 0;
            this.systemStatus.vectorstore =
              stats.vectorstore_status === 'ready';
          }

          // Test LLM availability
          try {
            const llmResponse = await fetch(
              'http://localhost:9000/rag/query-llm',
              {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  query: 'test',
                  top_k: 1,
                  similarity_threshold: 0.5,
                }),
              }
            );
            this.systemStatus.llm = llmResponse.ok;
          } catch (e) {
            this.systemStatus.llm = false;
          }
        }
      } catch (error) {
        console.error('Status check error:', error);
        this.systemStatus.rag = false;
      }
    },
  },
};
</script>

<style scoped>
@keyframes slideIn {
  0% {
    transform: translateY(20px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slide-in {
  animation: slideIn 0.5s ease-out;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #374151;
}

::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
