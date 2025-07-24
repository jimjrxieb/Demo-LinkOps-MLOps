#!/usr/bin/env python3
"""
MCP Tool Executor Router
=======================

This router provides endpoints for executing MCP tools and managing
tool execution history using SQLite database.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from logic.executor import run_tool_command, validate_command, get_command_info
from logic.execution_logger import log_execution, get_logs, get_execution_stats, get_tool_performance, cleanup_old_logs

logger = logging.getLogger(__name__)
router = APIRouter()


class ToolExecutionRequest(BaseModel):
    command: str
    timeout: Optional[int] = 30
    tool_name: Optional[str] = None


class ToolExecutionResponse(BaseModel):
    stdout: str
    stderr: str
    returncode: int
    execution_time: float
    success: bool
    command: str
    timestamp: str
    tool_name: Optional[str] = None


@router.post("/execute-tool", response_model=ToolExecutionResponse)
async def execute_tool(request: ToolExecutionRequest):
    """
    Execute a tool command and return the results.
    
    Args:
        request: ToolExecutionRequest containing the command to execute
    
    Returns:
        ToolExecutionResponse with execution results
    """
    try:
        # Validate command for security
        validation = validate_command(request.command)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["error"])
        
        # Get command information
        command_info = get_command_info(request.command)
        logger.info(f"🔍 Command analysis: {command_info}")
        
        # Execute the command
        result = run_tool_command(request.command, request.timeout)
        
        # Add timestamp and tool name
        result["timestamp"] = datetime.now().isoformat()
        result["tool_name"] = request.tool_name
        
        # Log execution to SQLite database
        duration_ms = int(result["execution_time"] * 1000)  # Convert to milliseconds
        log_execution(
            tool_name=request.tool_name,
            command=request.command,
            stdout=result["stdout"],
            stderr=result["stderr"],
            returncode=result["returncode"],
            duration_ms=duration_ms,
            success=result["success"]
        )
        
        return ToolExecutionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Tool execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@router.post("/execute-saved-tool/{tool_name}")
async def execute_saved_tool(tool_name: str, timeout: Optional[int] = 30):
    """
    Execute a saved MCP tool by name.
    
    Args:
        tool_name: Name of the saved tool to execute
        timeout: Optional timeout override
    
    Returns:
        ToolExecutionResponse with execution results
    """
    try:
        # Load the saved tool
        tool_path = f"db/mcp_tools/{tool_name}.json"
        if not os.path.exists(tool_path):
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
        
        with open(tool_path, 'r') as f:
            tool_data = json.load(f)
        
        # Create execution request
        request = ToolExecutionRequest(
            command=tool_data["command"],
            timeout=timeout,
            tool_name=tool_name
        )
        
        # Execute the tool
        return await execute_tool(request)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Saved tool execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@router.get("/execution-history")
async def get_execution_history(limit: int = 50, tool_name: Optional[str] = None):
    """
    Get execution history for tools from SQLite database.
    
    Args:
        limit: Maximum number of entries to return
        tool_name: Optional filter by tool name
    
    Returns:
        List of execution history entries
    """
    try:
        logs = get_logs(limit=limit, tool_name=tool_name)
        return logs
        
    except Exception as e:
        logger.error(f"❌ Failed to get execution history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")


@router.get("/tool-stats")
async def get_tool_statistics():
    """
    Get statistics about tool executions from SQLite database.
    
    Returns:
        Dictionary with execution statistics
    """
    try:
        stats = get_execution_stats()
        return stats
        
    except Exception as e:
        logger.error(f"❌ Failed to get tool statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")


@router.get("/tool-performance/{tool_name}")
async def get_tool_performance_stats(tool_name: str, limit: int = 50):
    """
    Get performance statistics for a specific tool.
    
    Args:
        tool_name: Name of the tool
        limit: Number of recent executions to analyze
    
    Returns:
        Dictionary with tool performance statistics
    """
    try:
        performance = get_tool_performance(tool_name, limit=limit)
        return performance
        
    except Exception as e:
        logger.error(f"❌ Failed to get tool performance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get performance: {str(e)}")


@router.delete("/cleanup-logs")
async def cleanup_execution_logs(days_to_keep: int = 30):
    """
    Clean up old execution logs.
    
    Args:
        days_to_keep: Number of days of logs to keep
    
    Returns:
        Dictionary with cleanup results
    """
    try:
        deleted_count = cleanup_old_logs(days_to_keep=days_to_keep)
        return {
            "message": f"Cleaned up {deleted_count} old execution logs",
            "deleted_count": deleted_count,
            "days_kept": days_to_keep
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to cleanup logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup logs: {str(e)}") 