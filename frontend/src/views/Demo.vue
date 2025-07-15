<template>
  <div class="p-6 space-y-6">
    <!-- Welcome Header -->
    <div class="text-center space-y-4">
      <h1 class="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-500 bg-clip-text text-transparent">
        🛡️ DevSecOps Shadow Agent Demo
      </h1>
      <p class="text-lg text-gray-300 max-w-3xl mx-auto">
        This is a demonstration of one of the Shadow Agents developed by LinkOps, tailored specifically for DevSecOps workflows.
      </p>
    </div>

    <!-- Demo Mode Banner -->
    <div class="bg-yellow-200 text-yellow-900 text-center py-3 rounded-lg font-semibold">
      🎯 Demo Mode: Results are simulated. No real AI or API keys required.
    </div>

    <!-- How It Works Section -->
    <div class="border border-gray-700 rounded-2xl p-6 bg-black/30">
      <h2 class="text-2xl font-bold mb-4 text-purple-400">🧠 How It Works</h2>
      
      <div class="space-y-6">
        <!-- Step 1 -->
        <div class="border-l-4 border-blue-500 pl-4">
          <h3 class="text-xl font-semibold text-blue-400">Step 1: Submit a Task You Would Give Me</h3>
          <p class="text-gray-300 mt-2">
            This input bar simulates a Jira-style task — anything you would assign a junior platform or DevSecOps engineer.
          </p>
          <p class="text-gray-400 italic mt-1">
            Example: "Deploy an app with Helm and ArgoCD", "Scan this repo for security issues", "Convert to GitOps"
          </p>
        </div>

        <!-- Step 2 -->
        <div class="border-l-4 border-green-500 pl-4">
          <h3 class="text-xl font-semibold text-green-400">Step 2: Orb Search and Ranking</h3>
          <p class="text-gray-300 mt-2">
            We search our Orb Library for matching best practices (Orbs) and score its ability to complete your task.
          </p>
          <div class="mt-3 space-y-2">
            <div class="flex items-start space-x-2">
              <span class="text-green-400">✅</span>
              <div>
                <strong class="text-green-400">If an Orb Exists:</strong>
                <ul class="text-sm text-gray-300 mt-1 ml-4 list-disc">
                  <li>Orb Title + Summary</li>
                  <li>Rune ID (compiled script)</li>
                  <li>Confidence Score</li>
                </ul>
              </div>
            </div>
            <div class="flex items-start space-x-2">
              <span class="text-red-400">🚫</span>
              <div>
                <strong class="text-red-400">If No Match or Low Confidence:</strong>
                <p class="text-sm text-gray-300 mt-1">Task is routed to <strong>Whis</strong>, our MLOps model, to learn it for future automation.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3 -->
        <div class="border-l-4 border-purple-500 pl-4">
          <h3 class="text-xl font-semibold text-purple-400">Step 3: Whis Learning Process</h3>
          <p class="text-gray-300 mt-2 italic">
            Whis is the AI/ML model powering LinkOps agent intelligence.
          </p>
          <div class="mt-3 space-y-3">
            <div>
              <strong class="text-purple-400">📥 Input Sources:</strong>
              <ul class="text-sm text-gray-300 mt-1 ml-4 list-disc">
                <li>Task submission</li>
                <li>Q&A entries</li>
                <li>Data dumps (e.g., guides or docs)</li>
                <li>Image OCR & YouTube transcript downloads</li>
              </ul>
            </div>
            <div>
              <strong class="text-purple-400">🧼 Sanitization Pipeline:</strong>
              <p class="text-sm text-gray-300 mt-1">Cleans and formats data using data engineering techniques, redacts sensitive info and replaces with placeholders</p>
            </div>
            <div>
              <strong class="text-purple-400">⚙️ Smithing Phase:</strong>
              <p class="text-sm text-gray-300 mt-1">Whis applies machine learning and LLM APIs to extract best practices (Orbs) and solution steps (Runes)</p>
            </div>
            <div>
              <strong class="text-purple-400">✅ Approval + Enhancement:</strong>
              <p class="text-sm text-gray-300 mt-1">Human-in-the-loop verifies and approves logic, Whis injects approved logic into future agent capabilities</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Task Submission UI -->
    <div class="border border-gray-700 rounded-2xl p-6 bg-black/30">
      <h2 class="text-xl font-semibold mb-4 text-blue-400">🚀 Try It Now</h2>
      <label class="text-lg font-medium block mb-3">Task You Would Give Me</label>
      <textarea 
        v-model="taskInput" 
        class="w-full p-3 rounded-lg bg-black border border-gray-700 text-white resize-none" 
        rows="3" 
        placeholder="e.g., create a pod named test with image nginx, or scan repo for security vulnerabilities"
      ></textarea>
      <div class="flex justify-end mt-3 gap-3">
        <button 
          @click="submitTask" 
          :disabled="loading" 
          class="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-xl hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 font-semibold"
        >
          {{ loading ? '🔍 Searching...' : '🔍 Search Orb' }}
        </button>
        <button 
          @click="clearResults" 
          class="bg-gray-700 text-white px-6 py-3 rounded-xl hover:bg-gray-600 font-semibold"
        >
          Clear
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center text-gray-400 py-6">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500 mx-auto mb-2"></div>
      Searching and scoring your task...
    </div>

    <!-- Results -->
    <div v-if="matchingOrb || generatedOrb" class="space-y-4">
      <!-- Best Match Found -->
      <div v-if="matchingOrb" class="border border-green-500 bg-black/20 p-6 rounded-2xl">
        <div class="flex items-center space-x-2 mb-4">
          <span class="text-2xl">✅</span>
          <h2 class="text-xl font-bold text-green-400">Orb Found!</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p><strong class="text-gray-300">Task:</strong> <span class="text-white">{{ taskInput }}</span></p>
            <p><strong class="text-gray-300">Matching Orb:</strong> <span class="text-green-400">{{ matchingOrb.title }}</span></p>
            <p><strong class="text-gray-300">Confidence Score:</strong> <span class="text-yellow-400">{{ confidenceScore }}%</span></p>
            <p><strong class="text-gray-300">Category:</strong> <span class="text-blue-400">{{ matchingOrb.category }}</span></p>
          </div>
          <div>
            <p><strong class="text-gray-300">Description:</strong></p>
            <p class="text-sm text-gray-300 mt-1">{{ matchingOrb.description }}</p>
            <p class="text-sm text-gray-400 mt-2"><strong>Tags:</strong> {{ matchingOrb.tags?.join(', ') }}</p>
          </div>
        </div>
        <div class="mt-4 p-4 bg-gray-800 rounded-lg">
          <p><strong class="text-gray-300">Corresponding Rune:</strong> <span class="text-purple-400">#{{ matchingOrb.rune }}</span></p>
          <button class="mt-3 px-4 py-2 bg-gray-700 rounded-lg hover:bg-gray-600 text-white">
            🔍 View Orb Details
          </button>
        </div>
        <div class="mt-4 space-y-2 text-sm">
          <p class="italic text-yellow-400">⚠️ Runes not available in demo. They are compiled solution path scripts.</p>
          <p class="italic text-yellow-400">⚠️ "Send to Agent?" → Feature not available in demo. FickNury sends tasks that are 100% autonomous to field agents.</p>
        </div>
      </div>

      <!-- AI Generated Orb -->
      <div v-else-if="generatedOrb" class="border border-blue-500 bg-black/20 p-6 rounded-2xl">
        <div class="flex items-center space-x-2 mb-4">
          <span class="text-2xl">✨</span>
          <h2 class="text-xl font-bold text-blue-400">No Orb Found - Generated Best Practice</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p><strong class="text-gray-300">Task:</strong> <span class="text-white">{{ taskInput }}</span></p>
            <p><strong class="text-gray-300">Confidence Score:</strong> <span class="text-yellow-400">{{ confidenceScore }}%</span></p>
            <p class="text-sm italic text-green-400 mt-2">🔄 Sent to Whis for Learning...</p>
          </div>
          <div>
            <p><strong class="text-gray-300">Generated by:</strong> <span class="text-purple-400">{{ generatedOrb.model }}</span></p>
            <p><strong class="text-gray-300">Category:</strong> <span class="text-blue-400">{{ generatedOrb.category }}</span></p>
          </div>
        </div>
        <div class="mt-4 p-4 bg-gray-800 rounded-lg">
          <h3 class="text-lg font-bold text-green-300 mb-3">Best Practice for: {{ taskInput }}</h3>
          <ul class="list-disc list-inside text-white space-y-1">
            <li v-for="(step, idx) in generatedOrb.steps" :key="idx">{{ step }}</li>
          </ul>
          <p class="text-xs text-gray-400 mt-3">Generated by: Whis Logic | Model: {{ generatedOrb.model }}</p>
        </div>
        <div class="flex gap-3 mt-4">
          <button class="px-4 py-2 rounded-lg bg-green-700 hover:bg-green-600 text-white font-semibold">
            ✅ Approve & Save
          </button>
          <button class="px-4 py-2 rounded-lg bg-red-700 hover:bg-red-600 text-white font-semibold">
            ❌ Reject
          </button>
        </div>
      </div>
    </div>

    <!-- Purpose Section -->
    <div class="border border-gray-700 rounded-2xl p-6 bg-black/30">
      <h2 class="text-2xl font-bold mb-4 text-purple-400">💡 Purpose of This Demo</h2>
      <div class="space-y-3 text-gray-300">
        <p>• Show how tasks are matched to existing automation</p>
        <p>• Show fallback logic when task is new or incomplete</p>
        <p>• Educate on <strong>how</strong> the model learns and <strong>what tech</strong> powers it</p>
      </div>
      
      <div class="mt-6 p-4 bg-gray-800 rounded-lg">
        <h3 class="text-lg font-semibold text-yellow-400 mb-2">✅ What You Can Do Here</h3>
        <ul class="space-y-1 text-sm">
          <li class="flex items-center space-x-2">
            <span class="text-green-400">✅</span>
            <span>Submit tasks like you would in a real job</span>
          </li>
          <li class="flex items-center space-x-2">
            <span class="text-green-400">✅</span>
            <span>View how LinkOps agents rank automation readiness</span>
          </li>
          <li class="flex items-center space-x-2">
            <span class="text-red-400">❌</span>
            <span>No agent execution or full pipeline is available in this demo</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const taskInput = ref('')
const generatedOrb = ref(null)
const matchingOrb = ref(null)
const confidenceScore = ref(null)
const loading = ref(false)

const submitTask = async () => {
  loading.value = true
  try {
    const response = await axios.post('/api/demo/search-orb', {
      task: taskInput.value
    })
    if (response.data.match) {
      matchingOrb.value = response.data.match
      confidenceScore.value = response.data.confidence
      generatedOrb.value = null
    } else {
      matchingOrb.value = null
      confidenceScore.value = response.data.confidence
      generatedOrb.value = response.data.generated_orb
    }
  } catch (error) {
    console.error(error)
    // Fallback demo response
    matchingOrb.value = null
    confidenceScore.value = 72
    generatedOrb.value = {
      title: `Best Practice for: ${taskInput.value}`,
      description: 'AI-generated best practice for the submitted task.',
      steps: [
        'Analyze the task requirements',
        'Identify key components and dependencies',
        'Follow industry best practices',
        'Implement with proper error handling',
        'Test and validate the solution',
      ],
      model: 'Grok API',
      category: 'General',
    }
  } finally {
    loading.value = false
  }
}

const clearResults = () => {
  taskInput.value = ''
  generatedOrb.value = null
  matchingOrb.value = null
  confidenceScore.value = null
}
</script>

<style scoped>
textarea:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}
</style>

