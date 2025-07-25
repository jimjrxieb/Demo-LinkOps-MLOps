#!/usr/bin/env python3
"""
MCP Tool Execution Logic
=======================

This module provides secure execution of MCP tool commands with proper
error handling, timeout management, and output capture.
"""

import logging
import subprocess
import time
from typing import Any

logger = logging.getLogger(__name__)


def run_tool_command(command: str, timeout: int = 30) -> dict[str, Any]:
    """
    Execute a tool command securely and return the results.

    Args:
        command: The command string to execute
        timeout: Maximum execution time in seconds (default: 30)

    Returns:
        Dictionary containing stdout, stderr, returncode, and execution metadata
    """
    start_time = time.time()

    try:
        logger.info(f"🔧 Executing tool command: {command}")

        # Execute command with timeout and output capture
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="/tmp",  # Execute in safe directory
        )

        execution_time = time.time() - start_time

        response = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "execution_time": round(execution_time, 2),
            "success": result.returncode == 0,
            "command": command,
        }

        if result.returncode == 0:
            logger.info(f"✅ Tool execution successful in {execution_time:.2f}s")
        else:
            logger.warning(f"⚠️ Tool execution failed with code {result.returncode}")

        return response

    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        logger.error(f"⏰ Tool execution timed out after {timeout}s")
        return {
            "error": f"Command timed out after {timeout} seconds",
            "execution_time": round(execution_time, 2),
            "success": False,
            "command": command,
            "stdout": "",
            "stderr": f"Timeout after {timeout}s",
            "returncode": -1,
        }

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"❌ Tool execution failed: {str(e)}")
        return {
            "error": str(e),
            "execution_time": round(execution_time, 2),
            "success": False,
            "command": command,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
        }


def validate_command(command: str) -> dict[str, Any]:
    """
    Validate a command for security and safety.

    Args:
        command: The command string to validate

    Returns:
        Dictionary with validation results
    """
    # List of potentially dangerous commands
    dangerous_commands = [
        "rm -rf",
        "dd",
        "mkfs",
        "fdisk",
        "shutdown",
        "reboot",
        "sudo",
        "su",
        "chmod 777",
        "chown root",
        "passwd",
    ]

    # Check for dangerous commands
    for dangerous in dangerous_commands:
        if dangerous in command.lower():
            return {
                "valid": False,
                "error": f"Command contains potentially dangerous operation: {dangerous}",
                "command": command,
            }

    # Check command length
    if len(command) > 1000:
        return {
            "valid": False,
            "error": "Command too long (max 1000 characters)",
            "command": command,
        }

    return {"valid": True, "command": command}


def get_command_info(command: str) -> dict[str, Any]:
    """
    Get information about a command without executing it.

    Args:
        command: The command string to analyze

    Returns:
        Dictionary with command analysis
    """
    # Extract the main command (first word)
    main_command = command.split()[0] if command.strip() else ""

    # Common command categories
    command_categories = {
        "file_operations": ["ls", "cat", "head", "tail", "grep", "find", "cp", "mv"],
        "system_info": ["ps", "top", "df", "du", "free", "uname", "who", "w"],
        "network": ["ping", "curl", "wget", "netstat", "ss", "ip", "ifconfig"],
        "text_processing": ["echo", "sed", "awk", "sort", "uniq", "wc", "cut"],
        "development": ["git", "python", "node", "npm", "docker", "kubectl"],
    }

    category = "other"
    for cat, commands in command_categories.items():
        if main_command in commands:
            category = cat
            break

    return {
        "main_command": main_command,
        "category": category,
        "estimated_complexity": "low" if len(command.split()) <= 3 else "medium",
        "command_length": len(command),
    }
