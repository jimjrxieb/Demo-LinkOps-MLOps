<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Document Q&A</h1>
            <p class="mt-1 text-sm text-gray-500">
              Ask questions about your uploaded documents using local AI
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <div class="text-sm text-gray-500">
              <span class="font-medium">{{ documentCount }}</span> documents
              indexed
            </div>
            <button
              class="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              :disabled="refreshing"
              @click="refreshDocuments"
            >
              <svg
                v-if="refreshing"
                class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-500 inline"
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
              {{ refreshing ? 'Refreshing...' : 'Refresh' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Q&A Section -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Query Input -->
          <div class="bg-white rounded-lg shadow-sm border p-6">
            <div class="space-y-4">
              <label
                for="query"
                class="block text-sm font-medium text-gray-700"
              >
                Ask a question about your documents
              </label>
              <div class="flex space-x-3">
                <input
                  id="query"
                  v-model="query"
                  placeholder="e.g., What are the key points about machine learning?"
                  class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                  :disabled="loading"
                  @keyup.enter="submitQuery"
                />
                <button
                  :disabled="!query.trim() || loading"
                  class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  @click="submitQuery"
                >
                  <svg
                    v-if="loading"
                    class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline"
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
                  {{ loading ? 'Searching...' : 'Ask' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Answer Display -->
          <div
            v-if="answer || loading"
            class="bg-white rounded-lg shadow-sm border"
          >
            <div class="p-6">
              <div v-if="loading" class="space-y-4">
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 bg-blue-600 rounded-full animate-pulse" />
                  <div
                    class="w-2 h-2 bg-blue-600 rounded-full animate-pulse"
                    style="animation-delay: 0.2s"
                  />
                  <div
                    class="w-2 h-2 bg-blue-600 rounded-full animate-pulse"
                    style="animation-delay: 0.4s"
                  />
                  <span class="text-sm text-gray-500 ml-2"
                    >Searching documents...</span
                  >
                </div>
                <div class="space-y-2">
                  <div class="h-4 bg-gray-200 rounded animate-pulse" />
                  <div class="h-4 bg-gray-200 rounded animate-pulse w-3/4" />
                  <div class="h-4 bg-gray-200 rounded animate-pulse w-1/2" />
                </div>
              </div>

              <div v-else-if="answer" class="space-y-4">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-semibold text-gray-900">Answer</h3>
                  <div
                    class="flex items-center space-x-2 text-sm text-gray-500"
                  >
                    <span>{{ executionTime }}ms</span>
                    <span>•</span>
                    <span>{{ resultCount }} sources</span>
                  </div>
                </div>

                <div class="prose max-w-none">
                  <p class="text-gray-700 leading-relaxed">
                    {{ answer }}
                  </p>
                </div>

                <!-- Sources -->
                <div
                  v-if="sources && sources.length > 0"
                  class="mt-6 pt-4 border-t border-gray-200"
                >
                  <h4 class="text-sm font-medium text-gray-900 mb-3">
                    Sources
                  </h4>
                  <div class="space-y-2">
                    <div
                      v-for="(source, index) in sources"
                      :key="index"
                      class="p-3 bg-gray-50 rounded-lg border-l-4 border-blue-500"
                    >
                      <div class="flex items-start justify-between">
                        <div class="flex-1">
                          <p class="text-sm font-medium text-gray-900">
                            {{
                              source.document_name || `Document ${index + 1}`
                            }}
                          </p>
                          <p class="text-sm text-gray-600 mt-1">
                            {{ source.content }}
                          </p>
                          <div
                            class="flex items-center space-x-4 mt-2 text-xs text-gray-500"
                          >
                            <span
                              >Similarity:
                              {{ (source.similarity * 100).toFixed(1) }}%</span
                            >
                            <span v-if="source.page"
                              >Page: {{ source.page }}</span
                            >
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tenant Sources -->
            <div
              v-if="tenantSources.length > 0"
              class="mt-6 bg-white rounded-lg shadow-sm border p-6"
            >
              <h4 class="text-lg font-semibold text-gray-900 mb-4">
                👥 Tenant Sources
              </h4>
              <div class="space-y-3">
                <div
                  v-for="(source, index) in tenantSources"
                  :key="index"
                  class="p-3 bg-gray-50 rounded-lg border-l-4 border-blue-500"
                >
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center space-x-3">
                      <span class="text-sm font-medium text-gray-900">{{
                        source.tenant_name
                      }}</span>
                      <span
                        class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded"
                        >Unit {{ source.unit }}</span
                      >
                      <span
                        class="text-xs"
                        :class="{
                          'bg-green-100 text-green-800':
                            source.status === 'active',
                          'bg-red-100 text-red-800':
                            source.status === 'inactive',
                          'bg-yellow-100 text-yellow-800':
                            source.status === 'expired',
                        }"
                        >{{ source.status }}</span
                      >
                    </div>
                    <span class="text-xs text-gray-500"
                      >Score: {{ (source.score * 100).toFixed(1) }}%</span
                    >
                  </div>
                  <div
                    class="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs text-gray-600"
                  >
                    <div>
                      <span class="font-medium">Lease End:</span>
                      {{ formatDate(source.lease_end) }}
                    </div>
                    <div v-if="source.rent_amount">
                      <span class="font-medium">Rent:</span> ${{
                        formatCurrency(source.rent_amount)
                      }}
                    </div>
                    <div>
                      <span class="font-medium">Source:</span>
                      {{ source.source }}
                    </div>
                    <div>
                      <span class="font-medium">Type:</span> Tenant Record
                    </div>
                  </div>
                  <div class="mt-2 text-xs text-gray-500">
                    {{ source.content }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- No Results -->
          <div
            v-else-if="searched && !answer"
            class="bg-white rounded-lg shadow-sm border p-6 text-center"
          >
            <div class="text-gray-500">
              <svg
                class="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.47-.881-6.08-2.33"
                />
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900">
                No results found
              </h3>
              <p class="mt-1 text-sm text-gray-500">
                Try rephrasing your question or upload more documents.
              </p>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Upload Section -->
          <div class="bg-white rounded-lg shadow-sm border p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              Upload Documents
            </h3>
            <DropZone
              @file-uploaded="onFileUploaded"
              @upload-error="onUploadError"
            />
          </div>

          <!-- Recent Queries -->
          <div
            v-if="recentQueries.length > 0"
            class="bg-white rounded-lg shadow-sm border p-6"
          >
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              Recent Queries
            </h3>
            <div class="space-y-2">
              <button
                v-for="(recentQuery, index) in recentQueries"
                :key="index"
                class="w-full text-left p-2 text-sm text-gray-600 hover:bg-gray-50 rounded transition-colors"
                @click="loadQuery(recentQuery)"
              >
                {{ recentQuery }}
              </button>
            </div>
          </div>

          <!-- System Status -->
          <div class="bg-white rounded-lg shadow-sm border p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              System Status
            </h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">RAG Service</span>
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                >
                  Online
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Documents</span>
                <span class="text-sm font-medium text-gray-900">{{
                  documentCount
                }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Vector Store</span>
                <span class="text-sm font-medium text-gray-900">{{
                  vectorStoreSize
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import DropZone from '../components/DropZone.vue';

const query = ref('');
const answer = ref('');
const loading = ref(false);
const searched = ref(false);
const refreshing = ref(false);
const documentCount = ref(0);
const vectorStoreSize = ref('0 MB');
const executionTime = ref(0);
const resultCount = ref(0);
const sources = ref([]);
const tenantSources = ref([]);
const recentQueries = ref([]);

const submitQuery = async () => {
  if (!query.value.trim() || loading.value) return;

  loading.value = true;
  searched.value = true;
  answer.value = '';
  sources.value = [];
  tenantSources.value = [];

  try {
    const response = await axios.post('/api/query-simple', {
      query: query.value,
      top_k: 5,
      similarity_threshold: 0.5,
      include_metadata: true,
    });

    const data = response.data;

    if (data.results && data.results.length > 0) {
      // Use LLM to generate answer if available
      if (data.answer) {
        answer.value = data.answer;
      } else {
        // Fallback to showing top results
        answer.value = data.results[0].content;
      }

      // Handle tenant sources
      if (data.tenant_sources && data.tenant_sources.length > 0) {
        tenantSources.value = data.tenant_sources;
      }

      // Handle regular sources
      sources.value = data.results.map((result) => ({
        content: result.content,
        similarity: result.similarity || result.score,
        document_name:
          result.metadata?.document_name ||
          result.metadata?.source ||
          'Unknown',
        page: result.metadata?.page,
      }));

      resultCount.value = data.results.length;
    }

    executionTime.value = Math.round(data.execution_time * 1000);

    // Add to recent queries
    if (!recentQueries.value.includes(query.value)) {
      recentQueries.value.unshift(query.value);
      recentQueries.value = recentQueries.value.slice(0, 5); // Keep only 5 recent queries
    }
  } catch (error) {
    console.error('Query failed:', error);
    answer.value =
      'Sorry, I encountered an error while processing your query. Please try again.';
  } finally {
    loading.value = false;
  }
};

const loadQuery = (recentQuery) => {
  query.value = recentQuery;
  submitQuery();
};

const onFileUploaded = (fileData) => {
  console.log('File uploaded:', fileData);
  // Refresh document count
  refreshDocuments();
};

const onUploadError = (error) => {
  console.error('Upload error:', error);
};

const refreshDocuments = async () => {
  refreshing.value = true;
  try {
    const response = await axios.get('/api/documents');
    documentCount.value = response.data.total_documents || 0;

    const statsResponse = await axios.get('/api/stats');
    vectorStoreSize.value = statsResponse.data.vectorstore_size || '0 MB';
  } catch (error) {
    console.error('Failed to refresh documents:', error);
  } finally {
    refreshing.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString || dateString === 'Unknown') return 'N/A';
  return new Date(dateString).toLocaleDateString();
};

const formatCurrency = (amount) => {
  if (!amount) return 'N/A';
  return new Intl.NumberFormat('en-US').format(amount);
};

onMounted(() => {
  refreshDocuments();
});
</script>
