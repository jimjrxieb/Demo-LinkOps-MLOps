#!/usr/bin/env python3
"""
Agent Creator Router
===================

Router for AI agent creation service endpoints.
Integrates with the actual agent-creator service.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import FileResponse

# Add the agent creator service to the path
sys.path.append("/app/ml-models/agent-creator")

try:
    from logic.agent_generator import generate_agent_code, validate_agent_parameters
except ImportError:
    # Fallback for when service is not available
    generate_agent_code = None
    validate_agent_parameters = None

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check for agent creator service."""
    try:
        if generate_agent_code:
            return {
                "status": "healthy",
                "service": "agent_creator",
                "timestamp": datetime.now().isoformat(),
                "details": {"agent_generator": "available", "validation": "available"},
            }
        else:
            return {
                "status": "degraded",
                "service": "agent_creator",
                "timestamp": datetime.now().isoformat(),
                "error": "Agent generator not available",
            }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "service": "agent_creator",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@router.post("/generate-agent")
async def generate_agent(
    agent_name: str = Form(...),
    agent_type: str = Form(...),
    description: str = Form(""),
    security_level: str = Form("medium"),
    capabilities: str = Form(""),
    workflow_steps: str = Form("[]"),
):
    """Generate an AI agent with specified configuration."""
    try:
        if not generate_agent_code:
            raise HTTPException(
                status_code=503, detail="Agent generator service not available"
            )

        # Parse capabilities and workflow steps
        import json

        try:
            capabilities_list = [
                cap.strip() for cap in capabilities.split(",") if cap.strip()
            ]
            workflow_steps_list = json.loads(workflow_steps) if workflow_steps else []
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="Invalid JSON in workflow_steps"
            )

        # Validate parameters
        if validate_agent_parameters:
            validate_agent_parameters(
                agent_type, agent_name, capabilities_list, security_level
            )

        # Generate agent using the actual service
        output_path = generate_agent_code(
            agent_type=agent_type,
            agent_name=agent_name,
            tools=capabilities_list,
            capabilities=capabilities_list,
            security_level=security_level,
            description=description,
        )

        # Read generated code
        with open(output_path, "r") as f:
            generated_code = f.read()

        return {
            "status": "success",
            "message": "Agent generated successfully",
            "agent_name": agent_name,
            "agent_type": agent_type,
            "description": description,
            "security_level": security_level,
            "capabilities": capabilities_list,
            "workflow_steps": workflow_steps_list,
            "output_path": output_path,
            "agent_code": generated_code,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Agent generation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Agent generation failed: {str(e)}"
        )


@router.post("/generate-workflow-agent")
async def generate_workflow_agent(
    workflow_name: str = Form(...),
    steps: str = Form(...),
    triggers: str = Form(""),
    error_handling: str = Form("retry"),
):
    """Generate a workflow agent for orchestrating multiple tasks."""
    try:
        if not generate_agent_code:
            raise HTTPException(
                status_code=503, detail="Agent generator service not available"
            )

        # Parse steps and triggers
        import json

        try:
            steps_list = json.loads(steps)
            triggers_list = [
                trigger.strip() for trigger in triggers.split(",") if trigger.strip()
            ]
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in steps")

        # Generate workflow agent
        output_path = generate_agent_code(
            agent_type="workflow",
            agent_name=workflow_name,
            tools=triggers_list,
            capabilities=["workflow_orchestration", "error_handling"],
            security_level="medium",
            description=f"Workflow agent for {workflow_name}",
        )

        # Read generated code
        with open(output_path, "r") as f:
            generated_code = f.read()

        return {
            "status": "success",
            "message": "Workflow agent generated successfully",
            "workflow_name": workflow_name,
            "steps": steps_list,
            "triggers": triggers_list,
            "error_handling": error_handling,
            "output_path": output_path,
            "agent_code": generated_code,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Workflow agent generation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Workflow agent generation failed: {str(e)}"
        )


@router.get("/templates")
async def get_templates():
    """Get available agent templates."""
    templates = [
        {
            "type": "taskbot",
            "name": "TaskBot",
            "description": "Execute specific tasks and workflows",
            "capabilities": ["data_processing", "file_operations", "validation"],
            "security_levels": ["low", "medium", "high"],
        },
        {
            "type": "commandbot",
            "name": "CommandBot",
            "description": "Execute system commands safely",
            "capabilities": [
                "command_execution",
                "file_operations",
                "network_requests",
            ],
            "security_levels": ["medium", "high"],
        },
        {
            "type": "assistant",
            "name": "Assistant",
            "description": "Conversational AI assistant",
            "capabilities": ["conversation", "information_retrieval", "task_planning"],
            "security_levels": ["low", "medium", "high"],
        },
        {
            "type": "workflow",
            "name": "Workflow",
            "description": "Orchestrate complex workflows",
            "capabilities": ["workflow_orchestration", "error_handling", "monitoring"],
            "security_levels": ["medium", "high"],
        },
    ]

    return {"templates": templates, "timestamp": datetime.now().isoformat()}


@router.get("/capabilities")
async def get_capabilities():
    """Get available agent capabilities."""
    capabilities = [
        {
            "id": "data_processing",
            "name": "Data Processing",
            "description": "Process and transform data",
            "security_level": "low",
        },
        {
            "id": "file_operations",
            "name": "File Operations",
            "description": "Read, write, and manage files",
            "security_level": "medium",
        },
        {
            "id": "network_requests",
            "name": "Network Requests",
            "description": "Make HTTP requests to APIs",
            "security_level": "medium",
        },
        {
            "id": "command_execution",
            "name": "Command Execution",
            "description": "Execute system commands",
            "security_level": "high",
        },
        {
            "id": "validation",
            "name": "Validation",
            "description": "Validate inputs and outputs",
            "security_level": "low",
        },
        {
            "id": "notification",
            "name": "Notification",
            "description": "Send notifications and alerts",
            "security_level": "low",
        },
        {
            "id": "conversation",
            "name": "Conversation",
            "description": "Handle natural language conversations",
            "security_level": "low",
        },
        {
            "id": "information_retrieval",
            "name": "Information Retrieval",
            "description": "Search and retrieve information",
            "security_level": "low",
        },
        {
            "id": "task_planning",
            "name": "Task Planning",
            "description": "Plan and organize tasks",
            "security_level": "low",
        },
        {
            "id": "workflow_orchestration",
            "name": "Workflow Orchestration",
            "description": "Coordinate complex workflows",
            "security_level": "medium",
        },
        {
            "id": "error_handling",
            "name": "Error Handling",
            "description": "Handle and recover from errors",
            "security_level": "low",
        },
        {
            "id": "monitoring",
            "name": "Monitoring",
            "description": "Monitor system and process status",
            "security_level": "low",
        },
    ]

    return {"capabilities": capabilities, "timestamp": datetime.now().isoformat()}


@router.get("/download/{agent_path:path}")
async def download_agent(agent_path: str):
    """Download a generated agent file."""
    try:
        full_path = f"/app/ml-models/agent-creator/output/{agent_path}"

        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="Agent file not found")

        return FileResponse(
            path=full_path,
            filename=os.path.basename(full_path),
            media_type="text/plain",
        )

    except Exception as e:
        logger.error(f"Agent download failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent download failed: {str(e)}")


@router.get("/agents")
async def list_agents():
    """List all available agents."""
    try:
        agents_dir = "/app/ml-models/agent-creator/output"

        if not os.path.exists(agents_dir):
            return {"agents": [], "total": 0}

        agents = []
        for filename in os.listdir(agents_dir):
            if filename.endswith(".py"):
                file_path = os.path.join(agents_dir, filename)
                stat = os.stat(file_path)
                agents.append(
                    {
                        "name": filename,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    }
                )

        return {
            "agents": agents,
            "total": len(agents),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Agent listing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent listing failed: {str(e)}")


@router.get("/supported-agents")
async def get_supported_agents():
    """Get supported agent types."""
    agents = [
        {"value": "taskbot", "label": "TaskBot"},
        {"value": "commandbot", "label": "CommandBot"},
        {"value": "assistant", "label": "Assistant"},
        {"value": "workflow", "label": "Workflow"},
    ]

    return {"supported_agents": agents, "timestamp": datetime.now().isoformat()}


@router.post("/validate")
async def validate_agent_config(
    agent_name: str = Form(...),
    agent_type: str = Form(...),
    capabilities: str = Form("[]"),
    security_level: str = Form("medium"),
):
    """Validate agent configuration before generation."""
    try:
        import json

        capabilities_list = json.loads(capabilities) if capabilities else []

        # Validation rules
        errors = []

        if not agent_name or len(agent_name) < 3:
            errors.append("Agent name must be at least 3 characters long")

        valid_types = ["taskbot", "commandbot", "assistant", "workflow"]
        if agent_type not in valid_types:
            errors.append(f"Agent type must be one of: {', '.join(valid_types)}")

        valid_security_levels = ["low", "medium", "high"]
        if security_level not in valid_security_levels:
            errors.append(
                f"Security level must be one of: {', '.join(valid_security_levels)}"
            )

        # Check capability compatibility
        if agent_type == "commandbot" and security_level == "low":
            errors.append("CommandBot requires medium or high security level")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Agent validation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Agent validation failed: {str(e)}"
        )


@router.delete("/agents/{agent_name}")
async def delete_agent(agent_name: str):
    """Delete an agent file."""
    try:
        agent_path = f"/app/ml-models/agent-creator/output/{agent_name}"

        if not os.path.exists(agent_path):
            raise HTTPException(status_code=404, detail="Agent not found")

        os.remove(agent_path)

        return {
            "status": "success",
            "message": f"Agent {agent_name} deleted successfully",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Agent deletion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent deletion failed: {str(e)}")
