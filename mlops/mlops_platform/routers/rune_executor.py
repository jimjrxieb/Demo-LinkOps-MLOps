import asyncio
import json
import os
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/rune", tags=["rune-executor"])


# Models
class RuneExecutionRequest(BaseModel):
    commands: List[str]
    name: str
    description: Optional[str] = "API-generated rune"
    timeout_seconds: Optional[int] = 300
    stop_on_failure: Optional[bool] = True
    allowed_commands: Optional[List[str]] = None
    denied_commands: Optional[List[str]] = None


class RuneExecutionResponse(BaseModel):
    execution_id: str
    status: str
    message: str
    results_file: Optional[str] = None


class RuneStatus(BaseModel):
    execution_id: str
    status: str
    progress: int
    total_commands: int
    completed_commands: int
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


# Storage for execution status
execution_status = {}


class RuneExecutor:
    def __init__(self):
        self.agent_path = self._find_agent_path()
        self.results_dir = Path("rune_results")
        self.results_dir.mkdir(exist_ok=True)

    def _find_agent_path(self) -> str:
        """Find the platform agent binary"""
        possible_paths = [
            "tools/agents/platform_agent",
            "tools/agents/build/platform_agent",
            "/usr/local/bin/platform_agent",
            "./platform_agent",
        ]

        for path in possible_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path

        # Try to build if not found
        build_script = "tools/agents/build.sh"
        if os.path.exists(build_script):
            try:
                subprocess.run([build_script], check=True, capture_output=True)
                if os.path.exists("tools/agents/build/platform_agent"):
                    return "tools/agents/build/platform_agent"
            except subprocess.CalledProcessError:
                pass

        raise FileNotFoundError("Platform agent not found. Please build it first.")

    def create_rune_file(self, request: RuneExecutionRequest) -> str:
        """Create a temporary rune configuration file"""
        rune_config = {
            "name": request.name,
            "description": request.description,
            "commands": request.commands,
            "validation": {
                "allowed_commands": request.allowed_commands or [],
                "denied_commands": request.denied_commands or [],
                "timeout_seconds": request.timeout_seconds,
                "stop_on_failure": request.stop_on_failure,
            },
        }

        # Create temporary file
        rune_file = self.results_dir / f"rune_{uuid.uuid4().hex}.json"
        with open(rune_file, "w") as f:
            json.dump(rune_config, f, indent=2)

        return str(rune_file)

    async def execute_rune_async(self, execution_id: str, rune_file: str):
        """Execute rune asynchronously"""
        try:
            # Update status
            execution_status[execution_id].status = "running"
            execution_status[execution_id].progress = 0

            # Execute the rune
            process = await asyncio.create_subprocess_exec(
                self.agent_path,
                "--rune",
                rune_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            # Parse results
            results_file = rune_file.replace(".json", "_results.json")
            results = []

            if os.path.exists(results_file):
                with open(results_file, "r") as f:
                    results = json.load(f)

            # Update status
            execution_status[execution_id].status = "completed"
            execution_status[execution_id].progress = 100
            execution_status[execution_id].completed_commands = len(results)
            execution_status[execution_id].results = results
            execution_status[execution_id].completed_at = datetime.now()

            # Clean up rune file
            if os.path.exists(rune_file):
                os.remove(rune_file)

        except Exception as e:
            execution_status[execution_id].status = "failed"
            execution_status[execution_id].error = str(e)
            execution_status[execution_id].completed_at = datetime.now()


# Global executor instance
executor = None


@router.on_event("startup")
async def startup_event():
    global executor
    try:
        executor = RuneExecutor()
    except FileNotFoundError as e:
        print(f"Warning: {e}")


@router.post("/execute", response_model=RuneExecutionResponse)
async def execute_rune(
    request: RuneExecutionRequest, background_tasks: BackgroundTasks
):
    """Execute a rune with the given commands"""
    if executor is None:
        raise HTTPException(status_code=503, detail="Rune executor not available")

    # Generate execution ID
    execution_id = uuid.uuid4().hex

    # Create rune file
    try:
        rune_file = executor.create_rune_file(request)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create rune file: {str(e)}"
        )

    # Initialize status
    execution_status[execution_id] = RuneStatus(
        execution_id=execution_id,
        status="queued",
        progress=0,
        total_commands=len(request.commands),
        completed_commands=0,
        created_at=datetime.now(),
    )

    # Start execution in background
    background_tasks.add_task(executor.execute_rune_async, execution_id, rune_file)

    return RuneExecutionResponse(
        execution_id=execution_id,
        status="queued",
        message="Rune execution started",
        results_file=rune_file.replace(".json", "_results.json"),
    )


@router.get("/status/{execution_id}", response_model=RuneStatus)
async def get_execution_status(execution_id: str):
    """Get the status of a rune execution"""
    if execution_id not in execution_status:
        raise HTTPException(status_code=404, detail="Execution not found")

    return execution_status[execution_id]


@router.get("/list")
async def list_executions():
    """List all rune executions"""
    return {
        "executions": [
            {
                "execution_id": status.execution_id,
                "status": status.status,
                "progress": status.progress,
                "total_commands": status.total_commands,
                "completed_commands": status.completed_commands,
                "created_at": status.created_at,
                "completed_at": status.completed_at,
            }
            for status in execution_status.values()
        ]
    }


@router.delete("/{execution_id}")
async def delete_execution(execution_id: str):
    """Delete an execution record"""
    if execution_id not in execution_status:
        raise HTTPException(status_code=404, detail="Execution not found")

    del execution_status[execution_id]
    return {"message": "Execution deleted"}


@router.post("/execute-simple")
async def execute_simple_command(command: str):
    """Execute a single command directly"""
    if executor is None:
        raise HTTPException(status_code=503, detail="Rune executor not available")

    try:
        # Create a simple rune with one command
        request = RuneExecutionRequest(
            commands=[command],
            name=f"Simple command: {command[:50]}",
            description="Single command execution",
        )

        rune_file = executor.create_rune_file(request)

        # Execute synchronously for simple commands
        process = await asyncio.create_subprocess_exec(
            executor.agent_path,
            "--rune",
            rune_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        # Parse results
        results_file = rune_file.replace(".json", "_results.json")
        results = []

        if os.path.exists(results_file):
            with open(results_file, "r") as f:
                results = json.load(f)

        # Clean up
        if os.path.exists(rune_file):
            os.remove(rune_file)

        return {
            "command": command,
            "success": process.returncode == 0,
            "output": stdout.decode() if stdout else "",
            "error": stderr.decode() if stderr else "",
            "results": results,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Command execution failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check for the rune executor"""
    if executor is None:
        return {
            "status": "unhealthy",
            "message": "Rune executor not available",
            "agent_path": None,
        }

    return {
        "status": "healthy",
        "message": "Rune executor ready",
        "agent_path": executor.agent_path,
        "results_directory": str(executor.results_dir),
    }
