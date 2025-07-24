<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">📊 System Dashboard</h1>
            <p class="mt-1 text-sm text-gray-500">
              Real-time monitoring of tenant sync and system status
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <div class="text-sm text-gray-500">
              <span class="font-medium">{{ lastUpdate }}</span>
            </div>
            <button
              @click="refreshData"
              class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              :disabled="loading"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Refreshing...' : 'Refresh' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- System Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total Tenants -->
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Total Tenants</p>
              <p class="text-2xl font-bold text-gray-900">{{ summary.tenant_count || 0 }}</p>
            </div>
          </div>
        </div>

        <!-- Active Tenants -->
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Active Tenants</p>
              <p class="text-2xl font-bold text-gray-900">{{ summary.active_tenants || 0 }}</p>
            </div>
          </div>
        </div>

        <!-- Expiring Leases -->
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Expiring Soon</p>
              <p class="text-2xl font-bold text-gray-900">{{ summary.expiring_leases || 0 }}</p>
            </div>
          </div>
        </div>

        <!-- Total Rent -->
        <div class="bg-white rounded-lg shadow-sm border p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Monthly Rent</p>
              <p class="text-2xl font-bold text-gray-900">${{ formatCurrency(summary.total_rent || 0) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Synced Files -->
          <div class="bg-white rounded-lg shadow-sm border">
            <div class="p-6 border-b border-gray-200">
              <h2 class="text-lg font-semibold text-gray-900">📂 Synced Files</h2>
              <p class="text-sm text-gray-500 mt-1">Files processed by the sync engine</p>
            </div>
            <div class="p-6">
              <div v-if="summary.source_files && summary.source_files.length > 0" class="space-y-3">
                <div
                  v-for="file in summary.source_files"
                  :key="file.file"
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div class="flex items-center space-x-3">
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <span class="text-sm font-medium text-gray-900">{{ file.file }}</span>
                  </div>
                  <span class="text-sm text-gray-500">{{ file.count }} tenants</span>
                </div>
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <p class="mt-2 text-sm">No files synced yet</p>
                <p class="text-xs">Drop CSV files in the watch directory to get started</p>
              </div>
            </div>
          </div>

          <!-- Recent Sync Operations -->
          <div class="bg-white rounded-lg shadow-sm border">
            <div class="p-6 border-b border-gray-200">
              <h2 class="text-lg font-semibold text-gray-900">🔄 Recent Sync Operations</h2>
              <p class="text-sm text-gray-500 mt-1">Latest file processing activities</p>
            </div>
            <div class="p-6">
              <div v-if="summary.recent_syncs && summary.recent_syncs.length > 0" class="space-y-3">
                <div
                  v-for="sync in summary.recent_syncs"
                  :key="sync.synced_at"
                  class="flex items-center justify-between p-3 border rounded-lg"
                  :class="sync.status === 'success' ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'"
                >
                  <div class="flex items-center space-x-3">
                    <div class="flex-shrink-0">
                      <svg v-if="sync.status === 'success'" class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <svg v-else class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                      </svg>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ sync.file_name }}</p>
                      <p class="text-xs text-gray-500">{{ formatDate(sync.synced_at) }}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="text-sm font-medium" :class="sync.status === 'success' ? 'text-green-600' : 'text-red-600'">
                      {{ sync.status }}
                    </p>
                    <p class="text-xs text-gray-500">{{ sync.records_processed }} records</p>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                <p class="mt-2 text-sm">No sync operations yet</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column -->
        <div class="space-y-6">
          <!-- System Status -->
          <div class="bg-white rounded-lg shadow-sm border p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">⚙️ System Status</h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Database</span>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Connected
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Sync Engine</span>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Running
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Last Sync</span>
                <span class="text-sm font-medium text-gray-900">{{ formatDate(summary.last_sync) || 'Never' }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Files Processed</span>
                <span class="text-sm font-medium text-gray-900">{{ summary.file_count || 0 }}</span>
              </div>
            </div>
          </div>

          <!-- Upcoming Lease Expirations -->
          <div class="bg-white rounded-lg shadow-sm border">
            <div class="p-6 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">⏳ Upcoming Lease Expirations</h3>
              <p class="text-sm text-gray-500 mt-1">Leases expiring within 30 days</p>
            </div>
            <div class="p-6">
              <div v-if="summary.expiring_leases && summary.expiring_leases.length > 0" class="space-y-3">
                <div
                  v-for="lease in summary.expiring_leases"
                  :key="lease.unit"
                  class="p-3 border border-yellow-200 bg-yellow-50 rounded-lg"
                >
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ lease.name }}</p>
                      <p class="text-xs text-gray-500">Unit {{ lease.unit }}</p>
                    </div>
                    <div class="text-right">
                      <p class="text-sm font-medium text-yellow-800">{{ formatDate(lease.lease_end) }}</p>
                      <p class="text-xs text-gray-500">{{ getDaysUntil(lease.lease_end) }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p class="mt-2 text-sm">No expiring leases</p>
                <p class="text-xs">All leases are current</p>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-lg shadow-sm border p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">🚀 Quick Actions</h3>
            <div class="space-y-3">
              <button
                @click="downloadSampleCSV"
                class="w-full px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                📥 Download Sample CSV
              </button>
              <button
                @click="viewTenants"
                class="w-full px-4 py-2 text-sm bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                👥 View All Tenants
              </button>
              <button
                @click="viewAnalytics"
                class="w-full px-4 py-2 text-sm bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                📊 View Analytics
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const summary = ref({
  tenant_count: 0,
  file_count: 0,
  active_tenants: 0,
  expiring_leases: 0,
  total_rent: 0,
  source_files: [],
  expiring_leases: [],
  recent_syncs: [],
  last_sync: null,
  system_status: 'no_data'
})

const loading = ref(false)
const lastUpdate = ref('Never')
let refreshInterval = null

const fetchStatus = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/status/summary')
    summary.value = response.data
    lastUpdate.value = new Date().toLocaleTimeString()
  } catch (error) {
    console.error('Failed to fetch status:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  fetchStatus()
}

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US').format(amount)
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const getDaysUntil = (dateString) => {
  if (!dateString) return ''
  const days = Math.ceil((new Date(dateString) - new Date()) / (1000 * 60 * 60 * 24))
  return `${days} days`
}

const downloadSampleCSV = () => {
  const csvContent = `tenant_name,unit,status,lease_start,lease_end,rent_amount,email,phone
John Smith,101,active,2024-01-01,2024-12-31,1500,john.smith@email.com,555-0101
Jane Doe,102,active,2024-02-01,2024-11-30,1600,jane.doe@email.com,555-0102
Bob Johnson,103,active,2024-03-01,2024-10-31,1400,bob.johnson@email.com,555-0103`
  
  const blob = new Blob([csvContent], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'sample_tenants.csv'
  a.click()
  window.URL.revokeObjectURL(url)
}

const viewTenants = () => {
  // Navigate to tenants view (if implemented)
  console.log('View tenants clicked')
}

const viewAnalytics = () => {
  // Navigate to analytics view (if implemented)
  console.log('View analytics clicked')
}

onMounted(() => {
  fetchStatus()
  // Refresh every 30 seconds
  refreshInterval = setInterval(fetchStatus, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script> 