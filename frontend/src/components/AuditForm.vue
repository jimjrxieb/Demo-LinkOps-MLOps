<template>
  <div class="audit-form-container">
    <!-- Audit Form -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Repository Audit</h2>
      
      <form @submit.prevent="submitAudit" class="space-y-4">
        <div>
          <label for="repoUrl" class="block text-sm font-medium text-gray-700 mb-2">
            GitHub Repository URL
          </label>
          <input
            id="repoUrl"
            v-model="formData.repoUrl"
            type="url"
            placeholder="https://github.com/username/repository"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        
        <div>
          <label for="branch" class="block text-sm font-medium text-gray-700 mb-2">
            Branch (optional)
          </label>
          <input
            id="branch"
            v-model="formData.branch"
            type="text"
            placeholder="main"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div class="flex items-center space-x-4">
          <label class="flex items-center">
            <input
              v-model="formData.generateMigration"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">Generate migration plan</span>
          </label>
        </div>
        
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Auditing Repository...
          </span>
          <span v-else>Start Audit</span>
        </button>
      </form>
    </div>

    <!-- Audit Results -->
    <div v-if="auditResults" class="bg-white rounded-lg shadow-md p-6">
      <h3 class="text-xl font-bold text-gray-800 mb-4">Audit Results</h3>
      
      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-blue-50 p-4 rounded-lg">
          <div class="text-2xl font-bold text-blue-600">{{ auditResults.summary.security_score }}</div>
          <div class="text-sm text-blue-700">Security Score</div>
        </div>
        
        <div class="bg-green-50 p-4 rounded-lg">
          <div class="text-2xl font-bold text-green-600">{{ auditResults.summary.gitops_score }}</div>
          <div class="text-sm text-green-700">GitOps Score</div>
        </div>
        
        <div class="bg-yellow-50 p-4 rounded-lg">
          <div class="text-2xl font-bold text-yellow-600">{{ auditResults.summary.total_issues }}</div>
          <div class="text-sm text-yellow-700">Total Issues</div>
        </div>
        
        <div class="bg-purple-50 p-4 rounded-lg">
          <div class="text-2xl font-bold text-purple-600">{{ auditResults.summary.grade }}</div>
          <div class="text-sm text-purple-700">Grade</div>
        </div>
      </div>

      <!-- Security Issues -->
      <div v-if="auditResults.report.security_scan" class="mb-6">
        <h4 class="text-lg font-semibold text-gray-800 mb-3">Security Analysis</h4>
        
        <div class="space-y-3">
          <div v-if="auditResults.report.security_scan.secrets" class="bg-red-50 p-4 rounded-lg">
            <h5 class="font-medium text-red-800 mb-2">
              Secrets Found: {{ auditResults.report.security_scan.secrets.length }}
            </h5>
            <div v-for="secret in auditResults.report.security_scan.secrets.slice(0, 3)" :key="secret.file" class="text-sm text-red-700">
              • {{ secret.file }}:{{ secret.line }} - {{ secret.severity }}
            </div>
            <div v-if="auditResults.report.security_scan.secrets.length > 3" class="text-sm text-red-600 mt-2">
              +{{ auditResults.report.security_scan.secrets.length - 3 }} more secrets found
            </div>
          </div>
          
          <div v-if="auditResults.report.security_scan.vulnerabilities" class="bg-orange-50 p-4 rounded-lg">
            <h5 class="font-medium text-orange-800 mb-2">
              Vulnerabilities Found: {{ auditResults.report.security_scan.vulnerabilities.length }}
            </h5>
            <div v-for="vuln in auditResults.report.security_scan.vulnerabilities.slice(0, 3)" :key="vuln.file" class="text-sm text-orange-700">
              • {{ vuln.file }} - {{ vuln.severity }}: {{ vuln.title }}
            </div>
            <div v-if="auditResults.report.security_scan.vulnerabilities.length > 3" class="text-sm text-orange-600 mt-2">
              +{{ auditResults.report.security_scan.vulnerabilities.length - 3 }} more vulnerabilities found
            </div>
          </div>
        </div>
      </div>

      <!-- GitOps Compliance -->
      <div v-if="auditResults.report.gitops_compliance" class="mb-6">
        <h4 class="text-lg font-semibold text-gray-800 mb-3">GitOps Compliance</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="(category, name) in auditResults.report.gitops_compliance.categories" :key="name" class="bg-gray-50 p-4 rounded-lg">
            <h5 class="font-medium text-gray-800 mb-2 capitalize">{{ name.replace('_', ' ') }}</h5>
            <div class="text-2xl font-bold text-blue-600">{{ category.score }}/{{ category.max }}</div>
            <div class="text-sm text-gray-600">{{ category.items.length }} items checked</div>
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div v-if="auditResults.report.gitops_compliance.recommendations" class="mb-6">
        <h4 class="text-lg font-semibold text-gray-800 mb-3">Recommendations</h4>
        
        <div class="space-y-3">
          <div v-for="rec in auditResults.report.gitops_compliance.recommendations" :key="rec.title" class="border-l-4 border-blue-500 pl-4">
            <h5 class="font-medium text-gray-800">{{ rec.title }}</h5>
            <p class="text-sm text-gray-600 mb-2">{{ rec.description }}</p>
            <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
              {{ rec.priority }} priority
            </span>
          </div>
        </div>
      </div>

      <!-- Repository Structure -->
      <div v-if="auditResults.report.structure" class="mb-6">
        <h4 class="text-lg font-semibold text-gray-800 mb-3">Repository Structure</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-gray-50 p-4 rounded-lg">
            <div class="text-2xl font-bold text-gray-800">{{ auditResults.report.structure.total_files }}</div>
            <div class="text-sm text-gray-600">Total Files</div>
          </div>
          
          <div class="bg-gray-50 p-4 rounded-lg">
            <div class="text-2xl font-bold text-gray-800">{{ auditResults.report.structure.depth }}</div>
            <div class="text-sm text-gray-600">Directory Depth</div>
          </div>
          
          <div class="bg-gray-50 p-4 rounded-lg">
            <div class="text-2xl font-bold text-gray-800">{{ auditResults.report.languages.length }}</div>
            <div class="text-sm text-gray-600">Languages</div>
          </div>
        </div>
        
        <div class="mt-4">
          <h5 class="font-medium text-gray-800 mb-2">Detected Languages</h5>
          <div class="flex flex-wrap gap-2">
            <span v-for="lang in auditResults.report.languages" :key="lang" class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
              {{ lang }}
            </span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex space-x-4">
        <button
          @click="downloadReport"
          class="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
        >
          Download Report
        </button>
        
        <button
          v-if="formData.generateMigration"
          @click="generateMigration"
          :disabled="isGeneratingMigration"
          class="bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50"
        >
          <span v-if="isGeneratingMigration">Generating...</span>
          <span v-else>Generate Migration Plan</span>
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mt-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">Audit Failed</h3>
          <div class="mt-2 text-sm text-red-700">{{ error }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { auditAssessService } from '@/services/api'

export default {
  name: 'AuditForm',
  setup() {
    const formData = reactive({
      repoUrl: '',
      branch: 'main',
      generateMigration: false
    })

    const isLoading = ref(false)
    const isGeneratingMigration = ref(false)
    const auditResults = ref(null)
    const error = ref(null)

    const submitAudit = async () => {
      isLoading.value = true
      error.value = null
      auditResults.value = null

      try {
        const response = await auditAssessService.auditRepository({
          repo_url: formData.repoUrl,
          branch: formData.branch
        })

        auditResults.value = response
        // Development log removed
      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Audit failed'
        // Error log removed
      } finally {
        isLoading.value = false
      }
    }

    const downloadReport = () => {
      if (!auditResults.value) return

      const dataStr = JSON.stringify(auditResults.value, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `audit-report-${Date.now()}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }

    const generateMigration = async () => {
      if (!auditResults.value) return

      isGeneratingMigration.value = true
      try {
        // This would call the audit_migrate service
        // Development log removed
        // const response = await auditMigrateService.generateMigration(auditResults.value)
        // Handle migration response
      } catch (err) {
        error.value = 'Failed to generate migration plan: ' + err.message
      } finally {
        isGeneratingMigration.value = false
      }
    }

    return {
      formData,
      isLoading,
      isGeneratingMigration,
      auditResults,
      error,
      submitAudit,
      downloadReport,
      generateMigration
    }
  }
}
</script>

<style scoped>
.audit-form-container {
  max-width: 1200px;
  margin: 0 auto;
}
</style> 