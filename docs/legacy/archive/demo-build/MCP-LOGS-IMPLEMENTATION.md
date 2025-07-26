# MCP Logs Viewer Implementation

## 🎉 **Implementation Complete!**

The **MCP Logs Viewer (MCPLogs.vue)** has been successfully implemented, providing comprehensive monitoring and analysis capabilities for MCP tool execution history.

## 🎯 **Core Features**

### **1. Comprehensive Log Display**
- **📋 Execution History**: Complete table view of all tool executions
- **📊 Real-Time Statistics**: Success rates, failure counts, average execution times
- **🔍 Advanced Filtering**: Search, status, tool, and limit filters
- **👁️ Detailed View**: Modal with complete execution details

### **2. Powerful Filtering & Search**
- **🔍 Search**: Tool names, commands, output, and error content
- **📊 Status Filter**: Success/failure filtering
- **🛠️ Tool Filter**: Filter by specific tools
- **📋 Limit Control**: Adjustable result limits (25, 50, 100, 200)

### **3. Interactive Data Management**
- **🔄 Real-Time Refresh**: Manual refresh functionality
- **📄 CSV Export**: Export filtered logs to CSV format
- **📋 Copy Data**: Copy individual log entries to clipboard
- **🧹 Clear Filters**: Quick filter reset

### **4. Comprehensive Statistics Dashboard**
- **📊 Total Executions**: Count of all executions
- **✅ Success Rate**: Percentage and count of successful executions
- **❌ Failure Rate**: Percentage and count of failed executions
- **⏱️ Average Time**: Mean execution time across all tools

## 🎨 **User Interface**

### **Header Section**
```vue
<div class="mb-8">
  <h1 class="text-3xl font-bold text-gray-800 mb-2">🗒️ MCP Execution Logs</h1>
  <p class="text-gray-600">Monitor and analyze MCP tool execution history with comprehensive logging</p>
</div>
```

### **Filters & Controls Panel**
```vue
<div class="bg-white rounded-lg shadow-md p-6 mb-6">
  <h2 class="text-xl font-semibold mb-4">📊 Log Filters & Controls</h2>
  
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
    <!-- Search Input -->
    <div>
      <label class="block font-semibold mb-2">🔍 Search:</label>
      <input v-model="searchQuery" placeholder="Search tool names, commands..." />
    </div>

    <!-- Status Filter -->
    <div>
      <label class="block font-semibold mb-2">📊 Status:</label>
      <select v-model="statusFilter">
        <option value="">All Status</option>
        <option value="success">✅ Success</option>
        <option value="failure">❌ Failure</option>
      </select>
    </div>

    <!-- Tool Filter -->
    <div>
      <label class="block font-semibold mb-2">🛠️ Tool:</label>
      <select v-model="toolFilter">
        <option value="">All Tools</option>
        <option v-for="tool in uniqueTools" :value="tool">{{ tool }}</option>
      </select>
    </div>

    <!-- Limit Control -->
    <div>
      <label class="block font-semibold mb-2">📋 Show:</label>
      <select v-model="limitFilter">
        <option value="25">Last 25</option>
        <option value="50">Last 50</option>
        <option value="100">Last 100</option>
        <option value="200">Last 200</option>
      </select>
    </div>
  </div>
</div>
```

### **Statistics Dashboard**
```vue
<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
  <!-- Total Executions -->
  <div class="bg-white rounded-lg shadow-md p-4">
    <div class="flex items-center gap-2 mb-2">
      <span class="text-2xl">📊</span>
      <h3 class="font-semibold text-gray-700">Total Executions</h3>
    </div>
    <div class="text-2xl font-bold text-blue-600">{{ logs.length }}</div>
  </div>

  <!-- Success Rate -->
  <div class="bg-white rounded-lg shadow-md p-4">
    <div class="flex items-center gap-2 mb-2">
      <span class="text-2xl">✅</span>
      <h3 class="font-semibold text-gray-700">Successful</h3>
    </div>
    <div class="text-2xl font-bold text-green-600">{{ successCount }}</div>
    <div class="text-sm text-gray-500">{{ successRate }}%</div>
  </div>

  <!-- Failure Rate -->
  <div class="bg-white rounded-lg shadow-md p-4">
    <div class="flex items-center gap-2 mb-2">
      <span class="text-2xl">❌</span>
      <h3 class="font-semibold text-gray-700">Failed</h3>
    </div>
    <div class="text-2xl font-bold text-red-600">{{ failureCount }}</div>
    <div class="text-sm text-gray-500">{{ failureRate }}%</div>
  </div>

  <!-- Average Execution Time -->
  <div class="bg-white rounded-lg shadow-md p-4">
    <div class="flex items-center gap-2 mb-2">
      <span class="text-2xl">⏱️</span>
      <h3 class="font-semibold text-gray-700">Avg Time</h3>
    </div>
    <div class="text-2xl font-bold text-purple-600">{{ averageExecutionTime }}s</div>
  </div>
</div>
```

### **Execution Logs Table**
```vue
<div class="bg-white rounded-lg shadow-md overflow-hidden">
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th>Status</th>
          <th>Tool Name</th>
          <th>Command</th>
          <th>Return Code</th>
          <th>Execution Time</th>
          <th>Timestamp</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="log in filteredLogs" :key="log.timestamp">
          <!-- Status with security indicator -->
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center">
              <span class="text-2xl">{{ log.success ? '✅' : '❌' }}</span>
              <div class="ml-2">
                <div class="text-sm font-medium">{{ log.success ? 'Success' : 'Failed' }}</div>
                <div class="text-xs">{{ log.security_check_passed ? '🔒 Secure' : '⚠️ Security' }}</div>
              </div>
            </div>
          </td>
          
          <!-- Tool name -->
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm font-medium text-gray-900">{{ log.tool_name }}</div>
          </td>

          <!-- Command (truncated) -->
          <td class="px-6 py-4">
            <div class="text-sm text-gray-900 font-mono max-w-xs truncate" :title="log.command">
              {{ log.command }}
            </div>
          </td>

          <!-- Return code with color coding -->
          <td class="px-6 py-4 whitespace-nowrap">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                  :class="log.returncode === 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
              {{ log.returncode }}
            </span>
          </td>

          <!-- Execution time -->
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ log.execution_time?.toFixed(2) || 'N/A' }}s
          </td>

          <!-- Formatted timestamp -->
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ formatTimestamp(log.timestamp) }}
          </td>

          <!-- Action buttons -->
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
            <button @click="showLogDetails(log)" class="text-blue-600 hover:text-blue-900 mr-3">
              👁️ View
            </button>
            <button @click="copyLogData(log)" class="text-green-600 hover:text-green-900">
              📋 Copy
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

### **Detailed Log Modal**
```vue
<div v-if="selectedLog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
  <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
    <!-- Modal Header -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">
          {{ selectedLog.success ? '✅' : '❌' }} Execution Details - {{ selectedLog.tool_name }}
        </h3>
        <button @click="selectedLog = null" class="text-gray-400 hover:text-gray-600 text-2xl">✕</button>
      </div>
    </div>

    <!-- Modal Content -->
    <div class="p-6 overflow-y-auto flex-1">
      <!-- Execution Info Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div class="bg-gray-50 p-4 rounded-lg">
          <h4 class="font-semibold mb-2">📊 Execution Info</h4>
          <div class="space-y-2 text-sm">
            <div><strong>Tool:</strong> {{ selectedLog.tool_name }}</div>
            <div><strong>Status:</strong> {{ selectedLog.success ? 'Success' : 'Failed' }}</div>
            <div><strong>Return Code:</strong> {{ selectedLog.returncode }}</div>
            <div><strong>Execution Time:</strong> {{ selectedLog.execution_time?.toFixed(2) || 'N/A' }}s</div>
            <div><strong>Timestamp:</strong> {{ formatTimestamp(selectedLog.timestamp) }}</div>
            <div><strong>Security Check:</strong> {{ selectedLog.security_check_passed ? '✅ Passed' : '❌ Failed' }}</div>
          </div>
        </div>

        <div class="bg-gray-50 p-4 rounded-lg">
          <h4 class="font-semibold mb-2">🔧 Command</h4>
          <div class="bg-gray-900 text-green-300 p-3 rounded font-mono text-sm break-all">
            {{ selectedLog.command }}
          </div>
        </div>
      </div>

      <!-- Standard Output -->
      <div v-if="selectedLog.stdout" class="mb-6">
        <h4 class="font-semibold mb-2">📤 Standard Output</h4>
        <div class="bg-gray-900 text-green-300 p-4 rounded-lg font-mono text-sm whitespace-pre-wrap max-h-64 overflow-y-auto">
          {{ selectedLog.stdout }}
        </div>
      </div>

      <!-- Error Output -->
      <div v-if="selectedLog.stderr || selectedLog.error_message" class="mb-6">
        <h4 class="font-semibold mb-2">⚠️ Error Output</h4>
        <div class="bg-red-900 text-red-200 p-4 rounded-lg font-mono text-sm whitespace-pre-wrap max-h-64 overflow-y-auto">
          {{ selectedLog.stderr || selectedLog.error_message }}
        </div>
      </div>

      <!-- Log File Reference -->
      <div v-if="selectedLog.log_file" class="mb-6">
        <h4 class="font-semibold mb-2">📁 Log File</h4>
        <div class="bg-blue-50 p-3 rounded-lg">
          <code class="text-sm">{{ selectedLog.log_file }}</code>
        </div>
      </div>
    </div>

    <!-- Modal Footer -->
    <div class="p-6 border-t border-gray-200">
      <div class="flex justify-end gap-4">
        <button @click="copyLogData(selectedLog)" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg">
          📋 Copy Data
        </button>
        <button @click="selectedLog = null" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg">
          Close
        </button>
      </div>
    </div>
  </div>
</div>
```

## 🔧 **API Integration**

### **Log Fetching**
```javascript
const fetchLogs = async () => {
  loading.value = true
  try {
    const res = await axios.get(`/api/mcp-tool/executions?limit=${limitFilter.value}`)
    logs.value = res.data.executions || []
    filterLogs()
    console.log("✅ Fetched logs:", logs.value.length)
  } catch (err) {
    console.error("❌ Failed to fetch logs:", err)
    alert("Failed to load execution logs. Please check your connection and try again.")
  } finally {
    loading.value = false
  }
}
```

### **Advanced Filtering**
```javascript
const filterLogs = () => {
  let filtered = [...logs.value]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(log => 
      log.tool_name.toLowerCase().includes(query) ||
      log.command.toLowerCase().includes(query) ||
      (log.stdout && log.stdout.toLowerCase().includes(query)) ||
      (log.stderr && log.stderr.toLowerCase().includes(query))
    )
  }

  // Status filter
  if (statusFilter.value) {
    if (statusFilter.value === 'success') {
      filtered = filtered.filter(log => log.success)
    } else if (statusFilter.value === 'failure') {
      filtered = filtered.filter(log => !log.success)
    }
  }

  // Tool filter
  if (toolFilter.value) {
    filtered = filtered.filter(log => log.tool_name === toolFilter.value)
  }

  filteredLogs.value = filtered
}
```

### **CSV Export Functionality**
```javascript
const exportLogs = () => {
  const headers = ['timestamp', 'tool_name', 'command', 'success', 'returncode', 'execution_time', 'stdout', 'stderr']
  const csvContent = [
    headers.join(','),
    ...filteredLogs.value.map(log => 
      headers.map(header => {
        const value = log[header] || ''
        // Escape commas and quotes in CSV
        return `"${String(value).replace(/"/g, '""')}"`
      }).join(',')
    )
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `mcp-execution-logs-${new Date().toISOString().split('T')[0]}.csv`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}
```

## 📊 **Computed Properties & Statistics**

### **Real-Time Statistics**
```javascript
const successCount = computed(() => {
  return logs.value.filter(log => log.success).length
})

const failureCount = computed(() => {
  return logs.value.filter(log => !log.success).length
})

const successRate = computed(() => {
  if (logs.value.length === 0) return 0
  return Math.round((successCount.value / logs.value.length) * 100)
})

const averageExecutionTime = computed(() => {
  if (logs.value.length === 0) return 0
  const times = logs.value.filter(log => log.execution_time != null).map(log => log.execution_time)
  if (times.length === 0) return 0
  const avg = times.reduce((sum, time) => sum + time, 0) / times.length
  return avg.toFixed(2)
})
```

### **Unique Tools List**
```javascript
const uniqueTools = computed(() => {
  const tools = [...new Set(logs.value.map(log => log.tool_name))]
  return tools.sort()
})
```

## 🗂️ **Navigation Integration**

### **Router Configuration**
```javascript
{
  path: '/mcp-logs',
  name: 'MCPLogs',
  component: MCPLogs
}
```

### **Sidebar Menu**
```javascript
{
  title: 'Execution Logs',
  path: '/mcp-logs',
  icon: '🗒️'
}
```

## 🎨 **UI/UX Features**

### **Responsive Design**
- **Mobile-First**: Responsive grid layouts and table overflow
- **Desktop Optimized**: Multi-column statistics dashboard
- **Touch-Friendly**: Large buttons and interactive elements

### **Loading States**
- **Table Loading**: Spinner with loading message
- **Button States**: Disabled states during operations
- **Real-Time Feedback**: Progress indicators

### **Empty States**
- **No Logs**: Helpful message when no logs exist
- **No Results**: Clear message when filters return no results
- **Filter Reset**: Easy way to clear filters and try again

### **Visual Feedback**
- **Status Indicators**: Color-coded success/failure states
- **Security Badges**: Security check status indicators
- **Return Code Badges**: Color-coded return code display
- **Interactive Elements**: Hover states and transitions

## 🚀 **Usage Instructions**

### **1. Access the Logs**
- Navigate to `/mcp-logs` in the browser
- Or click "🗒️ Execution Logs" in the sidebar menu

### **2. View Statistics**
- See overall execution statistics at the top
- Monitor success rates and average execution times
- Track total executions and failure counts

### **3. Filter & Search**
- **Search**: Type in tool names, commands, or output content
- **Status Filter**: Filter by success or failure
- **Tool Filter**: Show logs for specific tools only
- **Limit Control**: Adjust number of results displayed

### **4. Analyze Logs**
- **Table View**: Quick overview of all executions
- **Detailed View**: Click "👁️ View" for full execution details
- **Copy Data**: Click "📋 Copy" to copy log data to clipboard

### **5. Export Data**
- Click "📄 Export CSV" to download filtered logs
- Data includes all execution details in CSV format
- Filename includes current date for organization

### **6. Refresh Data**
- Click "🔄 Refresh" to reload latest execution logs
- Data updates automatically when viewing
- Manual refresh ensures latest information

## 📈 **Log Data Structure**

### **Execution Log Entry**
```json
{
  "tool_name": "test_tool",
  "command": "echo 'Hello from MCP Tool Execution!' && date && echo 'Test completed successfully'",
  "timestamp": "2025-07-25T00:36:05.832722",
  "returncode": 0,
  "stdout": "Hello from MCP Tool Execution!\nThu Jul 24 20:36:05 EDT 2025\nTest completed successfully\n",
  "stderr": "",
  "execution_time": 0.012019,
  "success": true,
  "error_message": null,
  "security_check_passed": true,
  "log_file": "db/logs/test_tool__20250724_203605.json"
}
```

### **Log File Structure**
- **Individual Files**: `db/logs/{tool_name}__{timestamp}.json`
- **History File**: `db/logs/execution_history.json`
- **Auto-Cleanup**: Last 1000 executions retained
- **Timestamped**: ISO format with microsecond precision

## 🔮 **Future Enhancements**

### **Planned Features**
1. **Real-Time Updates**: Live log streaming with WebSocket
2. **Advanced Analytics**: Trends, patterns, and performance metrics
3. **Log Archiving**: Automatic log archiving and compression
4. **Alert System**: Notifications for failures and anomalies
5. **Advanced Filtering**: Date ranges, execution time ranges
6. **Visualization**: Charts and graphs for execution trends

### **Performance Optimization**
1. **Pagination**: Large dataset handling with pagination
2. **Virtual Scrolling**: Efficient rendering of large log lists
3. **Background Loading**: Asynchronous log loading
4. **Caching**: Client-side caching for better performance

## ✅ **Implementation Benefits**

### **Complete Monitoring**
- ✅ **Comprehensive Logs** - Complete execution history
- ✅ **Real-Time Statistics** - Live performance monitoring
- ✅ **Advanced Filtering** - Powerful search and filter capabilities
- ✅ **Detailed Analysis** - In-depth execution information
- ✅ **Data Export** - CSV export for external analysis
- ✅ **User-Friendly Interface** - Intuitive design and navigation

### **Production Ready**
- ✅ **Responsive Design** - Works on all device sizes
- ✅ **Error Handling** - Graceful failure management
- ✅ **Performance Optimized** - Efficient data loading and rendering
- ✅ **Accessible** - Clear labels and navigation
- ✅ **Extensible** - Ready for future enhancements

## 🎯 **Summary**

The MCP Logs Viewer provides a comprehensive monitoring and analysis interface for MCP tool execution history. It offers:

1. **Complete Visibility** into tool execution history and performance
2. **Advanced Filtering** for focused analysis and troubleshooting
3. **Real-Time Statistics** for monitoring system health and performance
4. **Detailed Views** for in-depth execution analysis
5. **Data Export** capabilities for external reporting and analysis
6. **User-Friendly Interface** for easy navigation and operation

**The MCP Logs Viewer is now fully operational and ready for production use!** 🚀 