#!/usr/bin/env python3
"""
Auto Runner API Router
=====================

This router provides API endpoints for the Auto Tool Runner status monitoring
and control functionality.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from logic.execution_logger import get_execution_stats, get_logs
from pydantic import BaseModel

router = APIRouter()

# Configuration
TOOLS_PATH = "db/mcp_tools"
AUTO_RUNNER_LOG = "auto_runner.log"


class AutoRunnerStatus(BaseModel):
    status: str
    auto_tools_count: int
    last_execution: str = None
    last_execution_tool: str = None
    uptime: str = None


class AutoRunnerExecution(BaseModel):
    id: int
    tool_name: str
    command: str
    stdout: str
    stderr: str
    returncode: int
    duration_ms: int
    success: bool
    timestamp: str


@router.get("/status", response_model=AutoRunnerStatus)
async def get_auto_runner_status():
    """Get the current status of the Auto Tool Runner."""
    try:
        # Check if auto runner process is running
        runner_status = "stopped"
        auto_tools_count = 0
        last_execution = None
        last_execution_tool = None

        # Count auto-enabled tools
        tools_dir = Path(TOOLS_PATH)
        if tools_dir.exists():
            for filename in os.listdir(tools_dir):
                if filename.endswith(".json"):
                    file_path = tools_dir / filename
                    try:
                        with open(file_path) as f:
                            tool = json.load(f)
                            if tool.get("auto", False):
                                auto_tools_count += 1
                    except Exception:
                        continue

        # Check if auto runner log file exists and has recent activity
        if os.path.exists(AUTO_RUNNER_LOG):
            try:
                # Check if log file was modified in the last 10 minutes
                stat = os.stat(AUTO_RUNNER_LOG)
                if (datetime.now().timestamp() - stat.st_mtime) < 600:  # 10 minutes
                    runner_status = "running"
            except Exception:
                pass

        # Get last execution from database
        try:
            logs = get_logs(limit=1)
            if logs:
                last_log = logs[0]
                last_execution = last_log.get("timestamp")
                last_execution_tool = last_log.get("tool_name")
        except Exception:
            pass

        return AutoRunnerStatus(
            status=runner_status,
            auto_tools_count=auto_tools_count,
            last_execution=last_execution,
            last_execution_tool=last_execution_tool,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")


@router.get("/executions", response_model=list[AutoRunnerExecution])
async def get_recent_executions(limit: int = 10):
    """Get recent tool executions."""
    try:
        logs = get_logs(limit=limit)
        return [
            AutoRunnerExecution(
                id=log.get("id", 0),
                tool_name=log.get("tool_name", "Unknown"),
                command=log.get("command", ""),
                stdout=log.get("stdout", ""),
                stderr=log.get("stderr", ""),
                returncode=log.get("returncode", -1),
                duration_ms=log.get("duration_ms", 0),
                success=log.get("success", False),
                timestamp=log.get("timestamp", ""),
            )
            for log in logs
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting executions: {str(e)}"
        )


@router.get("/auto-tools")
async def get_auto_enabled_tools():
    """Get list of auto-enabled tools."""
    try:
        auto_tools = []
        tools_dir = Path(TOOLS_PATH)

        if not tools_dir.exists():
            return auto_tools

        for filename in os.listdir(tools_dir):
            if filename.endswith(".json"):
                file_path = tools_dir / filename
                try:
                    with open(file_path) as f:
                        tool = json.load(f)
                        if tool.get("auto", False):
                            auto_tools.append(tool)
                except Exception:
                    continue

        return auto_tools

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting auto tools: {str(e)}"
        )


@router.post("/start")
async def start_auto_runner():
    """Start the Auto Tool Runner (placeholder - would need actual implementation)."""
    try:
        # This is a placeholder - in a real implementation, you would:
        # 1. Start the auto_runner.py process
        # 2. Return success/failure status

        return {"message": "Auto Runner start command sent", "status": "starting"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting runner: {str(e)}")


@router.post("/stop")
async def stop_auto_runner():
    """Stop the Auto Tool Runner (placeholder - would need actual implementation)."""
    try:
        # This is a placeholder - in a real implementation, you would:
        # 1. Stop the auto_runner.py process
        # 2. Return success/failure status

        return {"message": "Auto Runner stop command sent", "status": "stopping"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping runner: {str(e)}")


@router.get("/stats")
async def get_auto_runner_stats():
    """Get Auto Runner statistics."""
    try:
        stats = get_execution_stats()

        # Add auto runner specific stats
        auto_tools_count = 0
        tools_dir = Path(TOOLS_PATH)
        if tools_dir.exists():
            for filename in os.listdir(tools_dir):
                if filename.endswith(".json"):
                    file_path = tools_dir / filename
                    try:
                        with open(file_path) as f:
                            tool = json.load(f)
                            if tool.get("auto", False):
                                auto_tools_count += 1
                    except Exception:
                        continue

        stats["auto_tools_count"] = auto_tools_count
        stats["auto_runner_status"] = (
            "running" if os.path.exists(AUTO_RUNNER_LOG) else "stopped"
        )

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")
