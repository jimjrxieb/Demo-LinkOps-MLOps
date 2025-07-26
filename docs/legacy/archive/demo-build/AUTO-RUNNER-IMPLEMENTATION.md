# Auto Tool Runner Implementation

## Overview

The Auto Tool Runner is a secure, auditable backend system that executes MCP tools with comprehensive validation, logging, and monitoring. It provides a bridge between the validated MCP tool schema and actual task execution.

## 🎯 **Core Components**

### **1. Auto Runner Engine**
- **File**: `unified-api/executor/auto_runner.py`
- **Class**: `AutoRunner`
- **Purpose**: Secure tool execution with validation and logging

### **2. Execution Result Model**
- **Class**: `ExecutionResult`
- **Fields**: Comprehensive execution metadata
- **Logging**: Automatic file and history logging

### **3. API Integration**
- **Router**: Enhanced `unified-api/routers/mcp_tool.py`
- **Endpoints**: Execution, history, and status endpoints

## 🔒 **Security Features**

### **Runtime Security Validation**

The Auto Runner performs multiple security checks:

```python
# Dangerous command patterns
DANGEROUS_PATTERNS = [
    r'\brm\s+-rf\b',                    # rm -rf
    r'\bdd\s+if=/dev/',                 # dd with device input
    r'\b:\(\)\s*\{\s*:\s*\|:\s*&\s*\}', # fork bomb
    r'\bchmod\s+777\b',                 # overly permissive chmod
    r'\bchown\s+root\b',                # changing ownership to root
    r'\b>\s*/\w+',                      # output redirection to system files
    r'\b\|\s*bash\b',                   # piping to bash
    r'\b\|\s*sh\b',                     # piping to sh
    r'\bshutdown\b',                    # system shutdown
    r'\breboot\b',                      # system reboot
    r'\bmkfs\b',                        # filesystem creation
    r'\bformat\b',                      # disk formatting
    r'\bwipe\b',                        # disk wiping
    r'\bdd\s+of=/dev/',                 # dd output to device
]

# Interactive patterns
INTERACTIVE_PATTERNS = [
    r'\bread\b',                        # read command
    r'\bprompt\b',                      # prompt keyword
    r'\bconfirm\b',                     # confirm keyword
    r'\by/n\b',                         # yes/no prompts
    r'\bpassword\b',                    # password prompts
    r'\binteractive\b',                 # interactive keyword
]
```

### **Execution Safety**

- **Timeout Protection**: 30-second default timeout
- **Process Isolation**: New process group creation
- **Output Limiting**: 1MB max output size
- **Error Handling**: Comprehensive exception handling

## 📋 **Execution Flow**

### **1. Tool Loading & Validation**
```python
def load_tool(self, name: str) -> MCPTool:
    # Load tool from file
    # Validate with schema
    # Check auto-execution setting
```

### **2. Security Validation**
```python
def is_safe_command(self, command: str) -> Tuple[bool, Optional[str]]:
    # Check dangerous patterns
    # Check interactive patterns
    # Return safety status and error message
```

### **3. Command Execution**
```python
def execute_command(self, command: str) -> Tuple[int, str, str, float]:
    # Execute with timeout
    # Capture stdout/stderr
    # Measure execution time
    # Handle timeouts and errors
```

### **4. Result Logging**
```python
def _log_execution(self, result: ExecutionResult) -> None:
    # Save to execution history
    # Create individual log file
    # Update result metadata
```

## 🔧 **API Endpoints**

### **Tool Execution**

#### **POST** `/api/mcp-tool/execute/{tool_name}`
Execute an MCP tool with full validation and logging.

**Request:**
```bash
curl -X POST "http://localhost:9000/api/mcp-tool/execute/restart_apache"
```

**Response:**
```json
{
    "status": "success",
    "message": "Tool 'restart_apache' execution completed",
    "result": {
        "tool_name": "restart_apache",
        "command": "sudo systemctl restart apache2",
        "timestamp": "2024-01-15T10:30:00Z",
        "returncode": 0,
        "stdout": "Systemd service restart successful",
        "stderr": "",
        "execution_time": 2.45,
        "success": true,
        "error_message": null,
        "security_check_passed": true,
        "log_file": "db/logs/restart_apache__20240115_103000.json"
    }
}
```

### **Execution History**

#### **GET** `/api/mcp-tool/executions`
Get recent execution history.

**Request:**
```bash
curl "http://localhost:9000/api/mcp-tool/executions?limit=10"
```

**Response:**
```json
{
    "executions": [
        {
            "tool_name": "restart_apache",
            "command": "sudo systemctl restart apache2",
            "timestamp": "2024-01-15T10:30:00Z",
            "returncode": 0,
            "stdout": "Systemd service restart successful",
            "stderr": "",
            "execution_time": 2.45,
            "success": true
        }
    ],
    "count": 1,
    "limit": 10
}
```

#### **GET** `/api/mcp-tool/executions/{tool_name}`
Get execution history for a specific tool.

**Request:**
```bash
curl "http://localhost:9000/api/mcp-tool/executions/restart_apache?limit=5"
```

### **System Status**

#### **GET** `/api/mcp-tool/status`
Get overall system status.

**Request:**
```bash
curl "http://localhost:9000/api/mcp-tool/status"
```

**Response:**
```json
{
    "total_tools": 5,
    "auto_enabled_tools": 3,
    "auto_tools": ["restart_apache", "check_disk_space", "system_status"],
    "recent_executions": 12,
    "system_status": "operational"
}
```

## 📊 **Logging & Monitoring**

### **Execution Logs**

Each execution is logged to:

1. **Individual Log File**: `db/logs/{tool_name}__{timestamp}.json`
2. **Execution History**: `db/logs/execution_history.json`

### **Log Structure**

```json
{
    "tool_name": "restart_apache",
    "command": "sudo systemctl restart apache2",
    "timestamp": "2024-01-15T10:30:00Z",
    "returncode": 0,
    "stdout": "Systemd service restart successful",
    "stderr": "",
    "execution_time": 2.45,
    "success": true,
    "error_message": null,
    "security_check_passed": true,
    "log_file": "db/logs/restart_apache__20240115_103000.json"
}
```

### **History Management**

- **Max Entries**: 1000 execution records
- **Auto Cleanup**: Oldest entries removed automatically
- **Persistent Storage**: JSON-based file storage

## 🧪 **Testing**

### **Test Suite: `test_auto_runner.py`**

The test suite validates:

1. **Valid Execution**: Simple command execution
2. **Auto Execution Check**: Non-auto tools rejected
3. **Security Validation**: Dangerous commands blocked
4. **Interactive Commands**: Interactive patterns blocked
5. **Timeout Handling**: Long-running commands timed out
6. **Logging Functionality**: Execution properly logged
7. **Error Handling**: Various failure scenarios
8. **Execution History**: History retrieval and structure

### **Running Tests**

```bash
cd /home/jimjrxieb/shadow-link-industries/DEMO-LinkOps
python3 test_auto_runner.py
```

## 🚀 **Usage Examples**

### **Python API Usage**

```python
from executor.auto_runner import run_tool, get_execution_history

# Execute a tool
result = run_tool("restart_apache")
print(f"Success: {result['success']}")
print(f"Output: {result['stdout']}")

# Get execution history
history = get_execution_history(limit=10)
for entry in history:
    print(f"{entry['tool_name']}: {entry['success']}")
```

### **Direct Class Usage**

```python
from executor.auto_runner import AutoRunner

# Create runner instance
runner = AutoRunner(timeout=60)  # Custom timeout

# Execute tool
result = runner.run_tool("check_disk_space")

# Get tool-specific history
tool_history = runner.get_tool_executions("check_disk_space", limit=5)
```

### **Error Handling**

```python
try:
    result = run_tool("dangerous_tool")
    if not result['success']:
        print(f"Execution failed: {result['error_message']}")
        if not result['security_check_passed']:
            print("Security check failed")
except Exception as e:
    print(f"System error: {e}")
```

## 🔧 **Configuration**

### **Execution Settings**

```python
# Default configuration
DEFAULT_TIMEOUT = 30  # seconds
MAX_OUTPUT_SIZE = 1024 * 1024  # 1MB
MAX_LOG_ENTRIES = 1000  # Keep last 1000 executions
```

### **Custom Configuration**

```python
# Create runner with custom settings
runner = AutoRunner(timeout=60)  # 60-second timeout

# Or modify global instance
from executor.auto_runner import auto_runner
auto_runner.timeout = 45
```

## 📈 **Performance & Monitoring**

### **Execution Metrics**

- **Execution Time**: Measured for each command
- **Success Rate**: Tracked per tool and overall
- **Error Patterns**: Categorized error types
- **Security Violations**: Blocked command attempts

### **Monitoring Endpoints**

- **System Status**: Overall health and statistics
- **Execution History**: Recent activity and trends
- **Tool Performance**: Per-tool success rates and timing

## 🔮 **Future Enhancements**

### **Planned Features**

1. **Scheduled Execution**
   - Cron-like scheduling
   - Recurring task support
   - Time-based execution

2. **Advanced Security**
   - Machine learning threat detection
   - Custom security rules
   - Sandboxed execution

3. **Performance Optimization**
   - Async execution
   - Parallel processing
   - Resource monitoring

4. **Enhanced Logging**
   - Structured logging
   - Log aggregation
   - Performance analytics

5. **Integration Features**
   - Webhook notifications
   - Email alerts
   - Slack integration

## ✅ **Summary**

The Auto Tool Runner provides:

- ✅ **Secure Execution** with comprehensive validation
- ✅ **Comprehensive Logging** with file and history storage
- ✅ **API Integration** with RESTful endpoints
- ✅ **Error Handling** with detailed error messages
- ✅ **Performance Monitoring** with execution metrics
- ✅ **Testing Coverage** with comprehensive test suite
- ✅ **Extensible Architecture** for future enhancements

The system ensures that all MCP tool executions are secure, auditable, and properly monitored while providing a robust API for integration with frontend applications. 