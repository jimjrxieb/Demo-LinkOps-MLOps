# Auto Tool Runner

## Overview

The Auto Tool Runner automatically executes MCP tools that are marked with `"auto": true` in their configuration files. It runs continuously, polling the tools directory every 5 minutes and executing any auto-enabled tools.

## Features

- **Automatic Execution**: Runs tools marked with `"auto": true`
- **Continuous Monitoring**: Polls every 5 minutes for new auto-enabled tools
- **Comprehensive Logging**: Logs all executions to SQLite database
- **Error Handling**: Graceful handling of tool failures
- **Performance Tracking**: Measures execution time for each tool

## Usage

### Quick Start

```bash
# From the DEMO-LinkOps directory
./start-auto-runner.sh
```

### Manual Start

```bash
# From the DEMO-LinkOps directory
python3 scripts/auto_runner.py
```

### Stopping the Runner

Press `Ctrl+C` to stop the auto runner gracefully.

## Configuration

### Tool Configuration

To make a tool auto-execute, add `"auto": true` to its JSON configuration:

```json
{
  "name": "system-status",
  "description": "Check system status and resources",
  "task_type": "command",
  "command": "echo '=== System Status ===' && uptime && echo '=== Memory ===' && free -h",
  "auto": true,
  "tags": ["system", "monitoring", "status"]
}
```

### Polling Interval

The default polling interval is 300 seconds (5 minutes). To change this, modify the `POLL_INTERVAL_SECONDS` variable in `scripts/auto_runner.py`.

## Logging

The Auto Tool Runner provides comprehensive logging:

- **Console Output**: Real-time status updates with emojis
- **File Logging**: Detailed logs saved to `auto_runner.log`
- **Database Logging**: All executions logged to SQLite database (`db/execution_logs.db`)

### Log Format

```
2024-01-15 10:30:00 - INFO - Auto Runner initialized
2024-01-15 10:30:00 - INFO - Found auto-enabled tool: system-status
2024-01-15 10:30:01 - INFO - Running auto tool: system-status
2024-01-15 10:30:02 - INFO - Completed system-status in 1200ms (success: True)
```

## Directory Structure

```
DEMO-LinkOps/
├── scripts/
│   ├── auto_runner.py          # Main auto runner script
│   └── README.md               # This file
├── db/
│   └── mcp_tools/              # Tool configuration files
│       ├── system-status.json  # Auto-enabled tool
│       ├── network-info.json   # Auto-enabled tool
│       └── hello-world.json    # Manual tool
├── start-auto-runner.sh        # Launcher script
└── auto_runner.log             # Log file (created when running)
```

## Auto-Enabled Tools

Currently, the following tools are configured for auto-execution:

- **system-status**: Checks system status, memory, and disk usage
- **network-info**: Displays network interface and routing information

## Monitoring

### View Recent Executions

```bash
# Query the SQLite database for recent executions
sqlite3 db/execution_logs.db "SELECT tool_name, timestamp, duration_ms, success FROM execution_logs ORDER BY timestamp DESC LIMIT 10;"
```

### Check Log File

```bash
# View recent log entries
tail -f auto_runner.log
```

## Troubleshooting

### Common Issues

1. **Tools directory not found**
   - Ensure you're running from the DEMO-LinkOps directory
   - Check that `db/mcp_tools/` exists

2. **Import errors**
   - Ensure the unified-api module is available
   - Check Python path configuration

3. **Permission errors**
   - Make sure the script is executable: `chmod +x scripts/auto_runner.py`
   - Check write permissions for log files

### Debug Mode

To run with more verbose logging, modify the logging level in `auto_runner.py`:

```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Security Considerations

- Auto-enabled tools should be carefully reviewed before deployment
- Commands are executed in a restricted environment (`/tmp` directory)
- All executions are logged for audit purposes
- Consider implementing additional security measures for production use

## Integration

The Auto Tool Runner integrates with:

- **MCP Tool Executor**: Uses the same execution engine
- **SQLite Logger**: Logs all executions to the database
- **Unified API**: Leverages existing tool infrastructure

## Future Enhancements

- Configurable polling intervals per tool
- Conditional execution based on system state
- Web dashboard for monitoring auto-executions
- Email/Slack notifications for failures
- Tool dependency management 