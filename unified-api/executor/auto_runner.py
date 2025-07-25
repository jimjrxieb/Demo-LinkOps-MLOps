#!/usr/bin/env python3
"""
Auto Tool Runner Backend
========================

This module provides secure, auditable execution of MCP tools with:
- Runtime validation and security checks
- Comprehensive logging and monitoring
- Error handling and timeout protection
- Integration with the MCP tool schema
"""

import datetime
import json
import logging
import os
import re
import signal
import subprocess

# Import our schema for validation
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent))
from schemas.mcp_tool_schema import MCPTool, validate_mcp_tool_data

logger = logging.getLogger(__name__)

# Configuration
MCP_TOOL_DIR = Path("db/mcp_tools")
LOG_DIR = Path("db/logs")
EXECUTION_LOG_FILE = LOG_DIR / "execution_history.json"

# Ensure directories exist
MCP_TOOL_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Security patterns for runtime validation
DANGEROUS_PATTERNS = [
    r"\brm\s+-rf\b",  # rm -rf
    r"\bdd\s+if=/dev/",  # dd with device input
    r"\b:\(\)\s*\{\s*:\s*\|:\s*&\s*\}",  # fork bomb
    r"\bchmod\s+777\b",  # overly permissive chmod
    r"\bchown\s+root\b",  # changing ownership to root
    r"\b>\s*/\w+",  # output redirection to system files
    r"\b\|\s*bash\b",  # piping to bash
    r"\b\|\s*sh\b",  # piping to sh
    r"\bshutdown\b",  # system shutdown
    r"\breboot\b",  # system reboot
    r"\bmkfs\b",  # filesystem creation
    r"\bformat\b",  # disk formatting
    r"\bwipe\b",  # disk wiping
    r"\bdd\s+of=/dev/",  # dd output to device
]

# Interactive patterns that should not be auto-executed
INTERACTIVE_PATTERNS = [
    r"\bread\b",  # read command
    r"\bprompt\b",  # prompt keyword
    r"\bconfirm\b",  # confirm keyword
    r"\by/n\b",  # yes/no prompts
    r"\bpassword\b",  # password prompts
    r"\binteractive\b",  # interactive keyword
]

# Execution configuration
DEFAULT_TIMEOUT = 30  # seconds
MAX_OUTPUT_SIZE = 1024 * 1024  # 1MB
MAX_LOG_ENTRIES = 1000  # Keep last 1000 executions


@dataclass
class ExecutionResult:
    """Result of tool execution with comprehensive metadata."""

    tool_name: str
    command: str
    timestamp: str
    returncode: int
    stdout: str
    stderr: str
    execution_time: float
    success: bool
    error_message: Optional[str] = None
    security_check_passed: bool = True
    log_file: Optional[str] = None


class AutoRunner:
    """Main class for handling MCP tool execution with security and logging."""

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.execution_history: list[dict] = []
        self._load_execution_history()

    def _load_execution_history(self) -> None:
        """Load execution history from file."""
        try:
            if EXECUTION_LOG_FILE.exists():
                with open(EXECUTION_LOG_FILE) as f:
                    self.execution_history = json.load(f)
                logger.info(f"Loaded {len(self.execution_history)} execution records")
        except Exception as e:
            logger.warning(f"Could not load execution history: {e}")
            self.execution_history = []

    def _save_execution_history(self) -> None:
        """Save execution history to file."""
        try:
            # Keep only the last MAX_LOG_ENTRIES
            if len(self.execution_history) > MAX_LOG_ENTRIES:
                self.execution_history = self.execution_history[-MAX_LOG_ENTRIES:]

            with open(EXECUTION_LOG_FILE, "w") as f:
                json.dump(self.execution_history, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save execution history: {e}")

    def load_tool(self, name: str) -> MCPTool:
        """Load and validate an MCP tool by name."""
        try:
            filepath = MCP_TOOL_DIR / f"{name}.json"
            if not filepath.exists():
                raise FileNotFoundError(f"Tool '{name}' not found")

            with open(filepath) as f:
                data = json.load(f)

            # Validate the tool data
            tool = validate_mcp_tool_data(data)
            logger.info(f"✅ Loaded tool: {tool.name} (auto: {tool.auto})")
            return tool

        except Exception as e:
            logger.error(f"❌ Failed to load tool '{name}': {e}")
            raise

    def is_safe_command(self, command: str) -> tuple[bool, Optional[str]]:
        """Check if command is safe to execute."""
        command_lower = command.lower()

        # Check for dangerous patterns
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, command_lower):
                return False, f"Command contains dangerous pattern: {pattern}"

        # Check for interactive patterns
        for pattern in INTERACTIVE_PATTERNS:
            if re.search(pattern, command_lower):
                return False, f"Command contains interactive pattern: {pattern}"

        return True, None

    def execute_command(self, command: str) -> tuple[int, str, str, float]:
        """Execute a command with timeout and output capture."""
        start_time = datetime.datetime.now()

        try:
            # Execute with timeout
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                preexec_fn=os.setsid,  # Create new process group
            )

            execution_time = (datetime.datetime.now() - start_time).total_seconds()

            # Limit output size
            stdout = result.stdout[:MAX_OUTPUT_SIZE] if result.stdout else ""
            stderr = result.stderr[:MAX_OUTPUT_SIZE] if result.stderr else ""

            return result.returncode, stdout, stderr, execution_time

        except subprocess.TimeoutExpired:
            # Kill the process group if timeout
            try:
                os.killpg(os.getpgid(result.pid), signal.SIGTERM)
            except Exception:
                pass
            execution_time = (datetime.datetime.now() - start_time).total_seconds()
            return (
                -1,
                "",
                f"Command timed out after {self.timeout} seconds",
                execution_time,
            )

        except Exception as e:
            execution_time = (datetime.datetime.now() - start_time).total_seconds()
            return -1, "", f"Execution error: {str(e)}", execution_time

    def run_tool(self, name: str) -> ExecutionResult:
        """Execute an MCP tool with full validation and logging."""
        logger.info(f"🚀 Starting execution of tool: {name}")

        try:
            # Load and validate tool
            tool = self.load_tool(name)

            # Check if tool is set for auto-execution
            if not tool.auto:
                error_msg = f"Tool '{name}' is not set for auto-execution"
                logger.warning(f"❌ {error_msg}")
                return ExecutionResult(
                    tool_name=name,
                    command=tool.command,
                    timestamp=datetime.datetime.utcnow().isoformat(),
                    returncode=-1,
                    stdout="",
                    stderr="",
                    execution_time=0.0,
                    success=False,
                    error_message=error_msg,
                    security_check_passed=False,
                )

            # Runtime security check
            is_safe, security_error = self.is_safe_command(tool.command)
            if not is_safe:
                error_msg = f"Security check failed: {security_error}"
                logger.warning(f"❌ {error_msg}")
                return ExecutionResult(
                    tool_name=name,
                    command=tool.command,
                    timestamp=datetime.datetime.utcnow().isoformat(),
                    returncode=-1,
                    stdout="",
                    stderr="",
                    execution_time=0.0,
                    success=False,
                    error_message=error_msg,
                    security_check_passed=False,
                )

            # Execute the command
            logger.info(f"🔧 Executing command: {tool.command}")
            returncode, stdout, stderr, execution_time = self.execute_command(
                tool.command
            )

            # Determine success
            success = returncode == 0
            error_message = (
                None if success else f"Command failed with return code {returncode}"
            )

            # Create result
            result = ExecutionResult(
                tool_name=name,
                command=tool.command,
                timestamp=datetime.datetime.utcnow().isoformat(),
                returncode=returncode,
                stdout=stdout,
                stderr=stderr,
                execution_time=execution_time,
                success=success,
                error_message=error_message,
                security_check_passed=True,
            )

            # Log the execution
            self._log_execution(result)

            # Log result
            status = "✅" if success else "❌"
            logger.info(
                f"{status} Tool '{name}' executed in {execution_time:.2f}s (return code: {returncode})"
            )

            return result

        except Exception as e:
            logger.error(f"❌ Error executing tool '{name}': {e}")
            return ExecutionResult(
                tool_name=name,
                command="",
                timestamp=datetime.datetime.utcnow().isoformat(),
                returncode=-1,
                stdout="",
                stderr="",
                execution_time=0.0,
                success=False,
                error_message=str(e),
                security_check_passed=False,
            )

    def _log_execution(self, result: ExecutionResult) -> None:
        """Log execution result to file and history."""
        try:
            # Create detailed log entry
            log_entry = asdict(result)

            # Add to execution history
            self.execution_history.append(log_entry)
            self._save_execution_history()

            # Create individual log file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"{result.tool_name}__{timestamp}.json"
            log_filepath = LOG_DIR / log_filename

            with open(log_filepath, "w") as f:
                json.dump(log_entry, f, indent=2)

            # Update result with log file path
            result.log_file = str(log_filepath)

            logger.info(f"📝 Execution logged to: {log_filepath}")

        except Exception as e:
            logger.error(f"❌ Failed to log execution: {e}")

    def get_execution_history(self, limit: int = 50) -> list[dict]:
        """Get recent execution history."""
        return self.execution_history[-limit:] if self.execution_history else []

    def get_tool_executions(self, tool_name: str, limit: int = 20) -> list[dict]:
        """Get execution history for a specific tool."""
        tool_executions = [
            entry
            for entry in self.execution_history
            if entry.get("tool_name") == tool_name
        ]
        return tool_executions[-limit:] if tool_executions else []


# Global instance for easy access
auto_runner = AutoRunner()


def run_tool(name: str) -> dict:
    """Convenience function to run a tool and return result as dict."""
    result = auto_runner.run_tool(name)
    return asdict(result)


def get_execution_history(limit: int = 50) -> list[dict]:
    """Get recent execution history."""
    return auto_runner.get_execution_history(limit)


def get_tool_executions(tool_name: str, limit: int = 20) -> list[dict]:
    """Get execution history for a specific tool."""
    return auto_runner.get_tool_executions(tool_name, limit)


# Example usage and testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Test execution
    try:
        print("🧪 Testing Auto Runner...")

        # Test with a simple command
        result = run_tool("test_tool")  # Change to an existing tool name
        print(f"✅ Execution completed: {result['success']}")
        print(f"📊 Return code: {result['returncode']}")
        print(f"⏱️  Execution time: {result['execution_time']:.2f}s")

    except Exception as e:
        print(f"❌ Test failed: {e}")
