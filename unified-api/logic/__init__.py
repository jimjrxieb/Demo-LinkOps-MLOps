"""
Logic Module
===========

This module contains business logic for the unified API.
"""

__version__ = "1.0.0"
__author__ = "LinkOps Team"
__description__ = "Business logic for secure AI platform"

from .execution_logger import (
    cleanup_old_logs,
    get_execution_stats,
    get_logs,
    get_tool_performance,
    init_logger,
    log_execution,
)
from .executor import get_command_info, run_tool_command, validate_command

__all__ = [
    "run_tool_command",
    "validate_command",
    "get_command_info",
    "log_execution",
    "get_logs",
    "get_execution_stats",
    "get_tool_performance",
    "cleanup_old_logs",
    "init_logger",
]
