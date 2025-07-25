<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">
              📓 Custom AI Keywords
            </h1>
            <p class="mt-1 text-sm text-gray-500">
              Teach the AI how your team talks. Add your own terms and what they
              mean.
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              :disabled="loading"
              @click="loadTerms"
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
              {{ loading ? 'Loading...' : 'Refresh' }}
            </button>
            <button
              class="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              @click="addTerm"
            >
              + Add Term
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Instructions -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
        <h3 class="text-lg font-semibold text-blue-900 mb-2">
          🎯 How It Works
        </h3>
        <p class="text-blue-800 mb-4">
          Add your property management terms and their variations. The AI will
          use these to better understand your questions and find relevant
          documents.
        </p>
        <div
          class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-700"
        >
          <div>
            <strong>Example:</strong>
            <ul class="list-disc list-inside mt-1 space-y-1">
              <li>Term: "delinquency"</li>
              <li>
                Variations: "late rent", "rent not paid", "overdue payment"
              </li>
            </ul>
          </div>
          <div>
            <strong>Result:</strong>
            <ul class="list-disc list-inside mt-1 space-y-1">
              <li>When someone asks about "late rent"</li>
              <li>AI also searches for "delinquency" and "overdue payment"</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Terms Editor -->
      <div class="bg-white rounded-lg shadow-sm border">
        <div class="p-6 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">
            Domain Terms & Variations
          </h2>
          <p class="text-sm text-gray-600 mt-1">
            Define your property management terminology and its variations
          </p>
        </div>

        <div class="p-6">
          <!-- Empty State -->
          <div
            v-if="terms.length === 0"
            class="text-center py-12 text-gray-500"
          >
            <svg
              class="mx-auto h-12 w-12 text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <p class="text-lg font-medium">No terms defined yet</p>
            <p class="text-sm">Add your first domain term to get started</p>
            <button
              class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              @click="addTerm"
            >
              Add Your First Term
            </button>
          </div>

          <!-- Terms List -->
          <div v-else class="space-y-6">
            <div
              v-for="(term, index) in terms"
              :key="index"
              class="border border-gray-200 rounded-lg p-6 shadow-sm"
            >
              <div class="flex items-start justify-between mb-4">
                <h3 class="text-lg font-medium text-gray-900">
                  Term {{ index + 1 }}
                </h3>
                <button
                  class="text-red-600 hover:text-red-800 transition-colors"
                  title="Remove this term"
                  @click="removeTerm(index)"
                >
                  <svg
                    class="h-5 w-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>

              <!-- Domain Term -->
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  🏷️ Domain Term
                </label>
                <input
                  v-model="term.term"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="e.g., delinquency, eviction, lease renewal"
                  @input="validateTerm(index)"
                />
                <p v-if="term.errors.term" class="mt-1 text-sm text-red-600">
                  {{ term.errors.term }}
                </p>
              </div>

              <!-- Variations -->
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  🔄 Variations (comma separated)
                </label>
                <textarea
                  v-model="term.variations"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="e.g., late rent, rent not paid, overdue payment, payment delinquency"
                  @input="validateTerm(index)"
                />
                <p
                  v-if="term.errors.variations"
                  class="mt-1 text-sm text-red-600"
                >
                  {{ term.errors.variations }}
                </p>
                <p class="mt-1 text-xs text-gray-500">
                  Separate multiple variations with commas. These will be used
                  as synonyms for the main term.
                </p>
              </div>

              <!-- Category -->
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  📂 Category
                </label>
                <select
                  v-model="term.category"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="rent_payment">Rent Payment</option>
                  <option value="lease_management">Lease Management</option>
                  <option value="maintenance">Maintenance</option>
                  <option value="tenant_communication">
                    Tenant Communication
                  </option>
                  <option value="legal">Legal & Compliance</option>
                  <option value="financial">Financial</option>
                  <option value="property_operations">
                    Property Operations
                  </option>
                  <option value="other">Other</option>
                </select>
              </div>

              <!-- Description -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  📝 Description (Optional)
                </label>
                <textarea
                  v-model="term.description"
                  rows="2"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Brief description of what this term means in your context"
                />
              </div>

              <!-- Preview -->
              <div
                v-if="term.term && term.variations"
                class="mt-4 p-3 bg-gray-50 rounded-md"
              >
                <h4 class="text-sm font-medium text-gray-700 mb-2">Preview:</h4>
                <p class="text-sm text-gray-600">
                  <strong>{{ term.term }}</strong> →
                  <span class="text-indigo-600">{{
                    parseVariations(term.variations).join(', ')
                  }}</span>
                </p>
              </div>
            </div>
          </div>

          <!-- Add Term Button -->
          <div class="mt-6">
            <button
              class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center"
              @click="addTerm"
            >
              <svg
                class="h-4 w-4 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              Add Another Term
            </button>
          </div>
        </div>
      </div>

      <!-- Save Section -->
      <div class="mt-8 bg-white rounded-lg shadow-sm border p-6">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              Save Keywords to AI
            </h3>
            <p class="text-sm text-gray-600 mt-1">
              Save your custom terms to improve AI understanding of your domain
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <span v-if="saving" class="text-sm text-gray-500">
              <svg
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
              Saving...
            </span>
            <span v-if="saved" class="text-sm text-green-600 flex items-center">
              <svg
                class="h-4 w-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
              Saved successfully!
            </span>
            <button
              :disabled="saving || !hasValidTerms"
              class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              @click="saveTerms"
            >
              <svg
                class="h-4 w-4 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"
                />
              </svg>
              {{ saving ? 'Saving...' : 'Save Keywords' }}
            </button>
          </div>
        </div>

        <!-- Summary -->
        <div
          v-if="hasValidTerms"
          class="mt-4 p-4 bg-green-50 border border-green-200 rounded-md"
        >
          <h4 class="text-sm font-medium text-green-900 mb-2">
            Ready to Save:
          </h4>
          <div class="text-sm text-green-800">
            <p>
              <strong>{{ validTermsCount }}</strong> terms with
              <strong>{{ totalVariations }}</strong> variations
            </p>
            <p class="mt-1">
              These will be used to improve AI search and understanding of your
              domain.
            </p>
          </div>
        </div>
      </div>

      <!-- Usage Examples -->
      <div class="mt-8 bg-white rounded-lg shadow-sm border p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          💡 Usage Examples
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="font-medium text-gray-900 mb-2">Before Custom Terms:</h4>
            <div class="text-sm text-gray-600 space-y-2">
              <p><strong>User asks:</strong> "Who has late rent?"</p>
              <p><strong>AI searches for:</strong> "late rent" only</p>
              <p>
                <strong>Misses:</strong> Documents about "delinquency" or
                "overdue payments"
              </p>
            </div>
          </div>
          <div>
            <h4 class="font-medium text-gray-900 mb-2">After Custom Terms:</h4>
            <div class="text-sm text-gray-600 space-y-2">
              <p><strong>User asks:</strong> "Who has late rent?"</p>
              <p>
                <strong>AI searches for:</strong> "late rent", "delinquency",
                "overdue payments", "rent not paid"
              </p>
              <p>
                <strong>Finds:</strong> All relevant documents regardless of
                terminology used
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// Reactive data
const loading = ref(false);
const saving = ref(false);
const saved = ref(false);
const terms = ref([]);

// Computed properties
const hasValidTerms = computed(() => {
  return terms.value.some(
    (term) =>
      term.term &&
      term.variations &&
      !term.errors.term &&
      !term.errors.variations
  );
});

const validTermsCount = computed(() => {
  return terms.value.filter(
    (term) =>
      term.term &&
      term.variations &&
      !term.errors.term &&
      !term.errors.variations
  ).length;
});

const totalVariations = computed(() => {
  return terms.value.reduce((total, term) => {
    if (term.variations) {
      return total + parseVariations(term.variations).length;
    }
    return total;
  }, 0);
});

// Methods
const addTerm = () => {
  terms.value.push({
    term: '',
    variations: '',
    category: 'other',
    description: '',
    errors: { term: '', variations: '' },
  });
};

const removeTerm = (index) => {
  terms.value.splice(index, 1);
};

const parseVariations = (variations) => {
  if (!variations) return [];
  return variations
    .split(',')
    .map((v) => v.trim())
    .filter((v) => v.length > 0);
};

const validateTerm = (index) => {
  const term = terms.value[index];
  term.errors = { term: '', variations: '' };

  // Validate term
  if (!term.term.trim()) {
    term.errors.term = 'Domain term is required';
  } else if (term.term.length < 2) {
    term.errors.term = 'Term must be at least 2 characters';
  }

  // Validate variations
  if (!term.variations.trim()) {
    term.errors.variations = 'At least one variation is required';
  } else {
    const variations = parseVariations(term.variations);
    if (variations.length === 0) {
      term.errors.variations = 'At least one variation is required';
    } else if (variations.length > 10) {
      term.errors.variations = 'Maximum 10 variations allowed';
    }
  }
};

const saveTerms = async () => {
  try {
    saving.value = true;
    saved.value = false;

    // Validate all terms
    terms.value.forEach((_, index) => validateTerm(index));

    // Filter valid terms
    const validTerms = terms.value.filter(
      (term) =>
        term.term &&
        term.variations &&
        !term.errors.term &&
        !term.errors.variations
    );

    if (validTerms.length === 0) {
      alert('Please add at least one valid term before saving.');
      return;
    }

    // Format terms for API
    const formattedTerms = validTerms.map((term) => ({
      term: term.term.trim(),
      variations: parseVariations(term.variations),
      category: term.category,
      description: term.description.trim(),
    }));

    // Save to API
    await axios.post('/api/htc/prompt/keywords', { terms: formattedTerms });

    saved.value = true;
    setTimeout(() => {
      saved.value = false;
    }, 3000);
  } catch (error) {
    console.error('Failed to save terms:', error);
    alert('Failed to save terms. Please try again.');
  } finally {
    saving.value = false;
  }
};

const loadTerms = async () => {
  try {
    loading.value = true;

    const response = await axios.get('/api/htc/prompt/keywords');
    const loadedTerms = response.data.terms || [];

    terms.value = loadedTerms.map((term) => ({
      term: term.term || '',
      variations: term.variations ? term.variations.join(', ') : '',
      category: term.category || 'other',
      description: term.description || '',
      errors: { term: '', variations: '' },
    }));

    // Add empty term if none exist
    if (terms.value.length === 0) {
      addTerm();
    }
  } catch (error) {
    console.error('Failed to load terms:', error);
    // Add empty term if loading fails
    if (terms.value.length === 0) {
      addTerm();
    }
  } finally {
    loading.value = false;
  }
};

// Initialize
onMounted(() => {
  loadTerms();
});
</script>
