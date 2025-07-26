<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">
              🧠 AI Feedback & Corrections
            </h1>
            <p class="mt-1 text-sm text-gray-500">
              Help improve the AI by providing corrections and feedback
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <button
              class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              :disabled="loading"
              @click="refreshFeedback"
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
              {{ loading ? 'Refreshing...' : 'Refresh' }}
            </button>
            <button
              class="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              @click="showFeedbackForm = !showFeedbackForm"
            >
              {{ showFeedbackForm ? 'Cancel' : 'Add Feedback' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Feedback Form -->
      <div
        v-if="showFeedbackForm"
        class="mb-8"
      >
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            📝 Add Feedback
          </h2>

          <form
            class="space-y-6"
            @submit.prevent="submitFeedback"
          >
            <!-- Original Question -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                ❓ Original Question
              </label>
              <input
                v-model="feedbackForm.query"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="e.g., When is rent due?"
                required
              >
            </div>

            <!-- AI's Answer -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                🤖 AI's Answer (that needs correction)
              </label>
              <textarea
                v-model="feedbackForm.generated_answer"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="The AI's response that you want to correct..."
                required
              />
            </div>

            <!-- Correct Answer -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                ✅ Correct Answer (Your Input)
              </label>
              <textarea
                v-model="feedbackForm.expected_answer"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="What the correct answer should be..."
                required
              />
            </div>

            <!-- Context -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                📄 Context (Optional)
              </label>
              <textarea
                v-model="feedbackForm.context"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Additional context that was used..."
              />
            </div>

            <!-- Category -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                🏷️ Issue Category
              </label>
              <select
                v-model="feedbackForm.category"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="incorrect_answer">
                  Incorrect Answer
                </option>
                <option value="incomplete_answer">
                  Incomplete Answer
                </option>
                <option value="wrong_context">
                  Wrong Context Used
                </option>
                <option value="missing_information">
                  Missing Information
                </option>
                <option value="unclear_response">
                  Unclear Response
                </option>
                <option value="other">
                  Other
                </option>
              </select>
            </div>

            <!-- User Notes -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                💭 Additional Notes (Optional)
              </label>
              <textarea
                v-model="feedbackForm.user_notes"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Any additional comments or explanations..."
              />
            </div>

            <!-- Submit Button -->
            <div class="flex justify-end space-x-4">
              <button
                type="button"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                @click="showFeedbackForm = false"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
              >
                <svg
                  v-if="submitting"
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
                {{ submitting ? 'Submitting...' : 'Submit Feedback' }}
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Feedback Statistics -->
      <div class="mb-8">
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            📊 Feedback Statistics
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-2xl font-bold text-blue-600">
                {{ feedbackStats.total_feedback }}
              </div>
              <div class="text-sm text-gray-600">
                Total Feedback
              </div>
            </div>
            <div class="text-center p-4 bg-yellow-50 rounded-lg">
              <div class="text-2xl font-bold text-yellow-600">
                {{ feedbackStats.pending_training }}
              </div>
              <div class="text-sm text-gray-600">
                Pending Training
              </div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <div class="text-2xl font-bold text-green-600">
                {{ feedbackStats.trained }}
              </div>
              <div class="text-sm text-gray-600">
                Trained
              </div>
            </div>
            <div class="text-center p-4 bg-purple-50 rounded-lg">
              <div class="text-2xl font-bold text-purple-600">
                {{ feedbackStats.recent_feedback }}
              </div>
              <div class="text-sm text-gray-600">
                Recent (7 days)
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Feedback Entries -->
      <div class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">
            📝 Recent Feedback Entries
          </h3>
          <div class="flex items-center space-x-2">
            <select
              v-model="filterCategory"
              class="px-3 py-1 text-sm border border-gray-300 rounded-md"
            >
              <option value="">
                All Categories
              </option>
              <option value="incorrect_answer">
                Incorrect Answer
              </option>
              <option value="incomplete_answer">
                Incomplete Answer
              </option>
              <option value="wrong_context">
                Wrong Context
              </option>
              <option value="missing_information">
                Missing Information
              </option>
              <option value="unclear_response">
                Unclear Response
              </option>
              <option value="other">
                Other
              </option>
            </select>
          </div>
        </div>

        <div
          v-if="filteredFeedback.length === 0"
          class="text-center py-12 text-gray-500"
        >
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
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <p class="mt-2 text-sm">
            No feedback entries found
          </p>
          <p class="text-xs">
            Add feedback to help improve the AI
          </p>
        </div>

        <div
          v-else
          class="space-y-4"
        >
          <div
            v-for="entry in filteredFeedback"
            :key="entry.feedback_id"
            class="bg-white rounded-lg shadow-sm border p-6"
          >
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center space-x-3">
                <span class="text-sm font-medium text-gray-900">{{
                  entry.query
                }}</span>
                <span
                  class="text-xs px-2 py-1 rounded-full"
                  :class="{
                    'bg-red-100 text-red-800':
                      entry.category === 'incorrect_answer',
                    'bg-yellow-100 text-yellow-800':
                      entry.category === 'incomplete_answer',
                    'bg-blue-100 text-blue-800':
                      entry.category === 'wrong_context',
                    'bg-purple-100 text-purple-800':
                      entry.category === 'missing_information',
                    'bg-gray-100 text-gray-800':
                      entry.category === 'unclear_response',
                    'bg-orange-100 text-orange-800': entry.category === 'other',
                  }"
                >
                  {{ formatCategory(entry.category) }}
                </span>
                <span
                  class="text-xs px-2 py-1 rounded-full"
                  :class="{
                    'bg-yellow-100 text-yellow-800':
                      entry.status === 'pending_training',
                    'bg-green-100 text-green-800': entry.status === 'trained',
                  }"
                >
                  {{ entry.status }}
                </span>
              </div>
              <span class="text-xs text-gray-500">{{
                formatDate(entry.timestamp)
              }}</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- AI's Answer -->
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-2">
                  🤖 AI's Answer
                </h4>
                <div class="p-3 bg-red-50 border border-red-200 rounded-md">
                  <p class="text-sm text-gray-700">
                    {{ entry.generated_answer }}
                  </p>
                </div>
              </div>

              <!-- Correct Answer -->
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-2">
                  ✅ Correct Answer
                </h4>
                <div class="p-3 bg-green-50 border border-green-200 rounded-md">
                  <p class="text-sm text-gray-700">
                    {{ entry.expected_answer }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Context and Notes -->
            <div
              v-if="entry.context || entry.user_notes"
              class="mt-4 space-y-2"
            >
              <div v-if="entry.context">
                <h4 class="text-sm font-medium text-gray-700 mb-1">
                  📄 Context
                </h4>
                <p class="text-sm text-gray-600">
                  {{ entry.context }}
                </p>
              </div>
              <div v-if="entry.user_notes">
                <h4 class="text-sm font-medium text-gray-700 mb-1">
                  💭 Notes
                </h4>
                <p class="text-sm text-gray-600">
                  {{ entry.user_notes }}
                </p>
              </div>
            </div>

            <!-- Actions -->
            <div
              class="mt-4 pt-4 border-t border-gray-200 flex items-center justify-between"
            >
              <div class="text-xs text-gray-500">
                ID: {{ entry.feedback_id }}
              </div>
              <div class="flex items-center space-x-2">
                <button
                  class="text-xs text-blue-600 hover:text-blue-800"
                  @click="editFeedback(entry)"
                >
                  Edit
                </button>
                <button
                  class="text-xs text-red-600 hover:text-red-800"
                  @click="deleteFeedback(entry.feedback_id)"
                >
                  Delete
                </button>
              </div>
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
const submitting = ref(false);
const showFeedbackForm = ref(false);
const filterCategory = ref('');
const feedbackEntries = ref([]);
const feedbackStats = ref({
  total_feedback: 0,
  pending_training: 0,
  trained: 0,
  recent_feedback: 0,
});

// Feedback form
const feedbackForm = ref({
  query: '',
  generated_answer: '',
  expected_answer: '',
  context: '',
  category: 'incorrect_answer',
  user_notes: '',
});

// Computed properties
const filteredFeedback = computed(() => {
  if (!filterCategory.value) {
    return feedbackEntries.value;
  }
  return feedbackEntries.value.filter(
    (entry) => entry.category === filterCategory.value
  );
});

// Methods
const submitFeedback = async () => {
  try {
    submitting.value = true;

    const response = await axios.post('/api/htc/feedback', {
      query: feedbackForm.value.query,
      answer: feedbackForm.value.generated_answer,
      expected: feedbackForm.value.expected_answer,
      context: feedbackForm.value.context,
      category: feedbackForm.value.category,
      user_notes: feedbackForm.value.user_notes,
    });

    // Reset form
    feedbackForm.value = {
      query: '',
      generated_answer: '',
      expected_answer: '',
      context: '',
      category: 'incorrect_answer',
      user_notes: '',
    };

    showFeedbackForm.value = false;

    // Refresh data
    await refreshFeedback();

    // Show success message
    alert('✅ Feedback submitted successfully!');
  } catch (error) {
    console.error('Failed to submit feedback:', error);
    alert('❌ Failed to submit feedback. Please try again.');
  } finally {
    submitting.value = false;
  }
};

const refreshFeedback = async () => {
  try {
    loading.value = true;

    // Get feedback entries
    const entriesResponse = await axios.get('/api/htc/feedback');
    feedbackEntries.value = entriesResponse.data.entries || [];

    // Get feedback stats
    const statsResponse = await axios.get('/api/htc/feedback/stats');
    feedbackStats.value = statsResponse.data || {};
  } catch (error) {
    console.error('Failed to refresh feedback:', error);
  } finally {
    loading.value = false;
  }
};

const editFeedback = (entry) => {
  // Populate form with entry data
  feedbackForm.value = {
    query: entry.query,
    generated_answer: entry.generated_answer,
    expected_answer: entry.expected_answer,
    context: entry.context || '',
    category: entry.category,
    user_notes: entry.user_notes || '',
  };

  showFeedbackForm.value = true;
};

const deleteFeedback = async (feedbackId) => {
  if (!confirm('Are you sure you want to delete this feedback entry?')) {
    return;
  }

  try {
    await axios.delete(`/api/htc/feedback/${feedbackId}`);
    await refreshFeedback();
    alert('✅ Feedback deleted successfully!');
  } catch (error) {
    console.error('Failed to delete feedback:', error);
    alert('❌ Failed to delete feedback. Please try again.');
  }
};

const formatCategory = (category) => {
  const categories = {
    incorrect_answer: 'Incorrect',
    incomplete_answer: 'Incomplete',
    wrong_context: 'Wrong Context',
    missing_information: 'Missing Info',
    unclear_response: 'Unclear',
    other: 'Other',
  };
  return categories[category] || category;
};

const formatDate = (timestamp) => {
  return (
    new Date(timestamp).toLocaleDateString() +
    ' ' +
    new Date(timestamp).toLocaleTimeString()
  );
};

// Initialize
onMounted(() => {
  refreshFeedback();
});
</script>
