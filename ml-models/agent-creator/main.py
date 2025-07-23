import os
import tempfile
import uuid

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logic.agent_generator import generate_agent_code, validate_agent_parameters

app = FastAPI(title="Agent Creator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "agent-creator"}


@app.post("/generate-agent/")
async def generate_agent(
    agent_type: str = Form(
        ..., description="Type of agent: base, taskbot, commandbot, assistant, workflow"
    ),
    agent_name: str = Form(..., description="Name for the agent"),
    tools: str = Form("", description="Comma-separated list of tools/commands"),
    capabilities: str = Form("", description="Comma-separated list of capabilities"),
    security_level: str = Form(
        "medium", description="Security level: low, medium, high"
    ),
    description: str = Form("", description="Agent description"),
):
    """
    Generate AI agent code based on parameters.

    Args:
        agent_type: Type of agent (base, taskbot, commandbot, assistant, workflow)
        agent_name: Name for the agent
        tools: Comma-separated list of tools/commands
        capabilities: Comma-separated list of capabilities
        security_level: Security level (low, medium, high)
        description: Agent description

    Returns:
        Generated agent code and metadata
    """
    try:
        # Parse parameters
        tools_list = [tool.strip() for tool in tools.split(",") if tool.strip()]
        capabilities_list = [
            cap.strip() for cap in capabilities.split(",") if cap.strip()
        ]

        # Validate parameters
        validate_agent_parameters(agent_type, agent_name, tools_list, security_level)

        # Generate agent code
        output_path = generate_agent_code(
            agent_type=agent_type,
            agent_name=agent_name,
            tools=tools_list,
            capabilities=capabilities_list,
            security_level=security_level,
            description=description,
        )

        # Read generated code
        with open(output_path, "r") as f:
            generated_code = f.read()

        return {
            "message": "Agent created successfully",
            "agent_type": agent_type,
            "agent_name": agent_name,
            "tools": tools_list,
            "capabilities": capabilities_list,
            "security_level": security_level,
            "output_path": output_path,
            "agent_code": generated_code,
            "status": "success",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Agent generation failed: {str(e)}"
        )


@app.post("/generate-workflow-agent/")
async def generate_workflow_agent(
    workflow_name: str = Form(..., description="Name for the workflow agent"),
    steps: str = Form(..., description="JSON string of workflow steps"),
    triggers: str = Form("", description="Comma-separated list of triggers"),
    error_handling: str = Form(
        "retry", description="Error handling strategy: retry, skip, stop"
    ),
):
    """
    Generate a workflow agent for orchestrating multiple tasks.

    Args:
        workflow_name: Name for the workflow
        steps: JSON string defining workflow steps
        triggers: Comma-separated list of triggers
        error_handling: Error handling strategy

    Returns:
        Generated workflow agent code
    """
    try:
        import json

        # Parse workflow steps
        try:
            workflow_steps = json.loads(steps)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400, detail="Invalid JSON in steps parameter"
            )

        # Parse triggers
        triggers_list = [
            trigger.strip() for trigger in triggers.split(",") if trigger.strip()
        ]

        # Generate workflow agent
        output_path = generate_agent_code(
            agent_type="workflow",
            agent_name=workflow_name,
            tools=[],
            capabilities=["workflow_orchestration", "error_handling", "monitoring"],
            security_level="high",
            description=f"Workflow agent for {workflow_name}",
            workflow_steps=workflow_steps,
            triggers=triggers_list,
            error_handling=error_handling,
        )

        # Read generated code
        with open(output_path, "r") as f:
            generated_code = f.read()

        return {
            "message": "Workflow agent created successfully",
            "workflow_name": workflow_name,
            "steps": workflow_steps,
            "triggers": triggers_list,
            "error_handling": error_handling,
            "output_path": output_path,
            "agent_code": generated_code,
            "status": "success",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Workflow agent generation failed: {str(e)}"
        )


@app.get("/supported-agents")
async def get_supported_agents():
    """Get list of supported agent types and capabilities."""
    return {
        "agent_types": ["base", "taskbot", "commandbot", "assistant", "workflow"],
        "capabilities": [
            "task_execution",
            "command_execution",
            "data_processing",
            "file_operations",
            "network_requests",
            "workflow_orchestration",
            "error_handling",
            "monitoring",
            "logging",
            "security_validation",
        ],
        "security_levels": ["low", "medium", "high"],
        "error_handling_strategies": ["retry", "skip", "stop", "notify"],
    }


@app.get("/agent-templates")
async def get_agent_templates():
    """Get available agent templates with examples."""
    return {
        "base": {
            "description": "Basic agent template with minimal functionality",
            "example": {
                "agent_type": "base",
                "agent_name": "MyAgent",
                "tools": "",
                "capabilities": "",
            },
        },
        "taskbot": {
            "description": "Task-oriented agent for handling specific tasks",
            "example": {
                "agent_type": "taskbot",
                "agent_name": "DataProcessor",
                "tools": "pandas,numpy,matplotlib",
                "capabilities": "data_processing,visualization",
            },
        },
        "commandbot": {
            "description": "Command execution agent with security controls",
            "example": {
                "agent_type": "commandbot",
                "agent_name": "SecureShell",
                "tools": "ls,pwd,whoami,echo",
                "capabilities": "command_execution,security_validation",
            },
        },
        "assistant": {
            "description": "AI assistant agent with conversation capabilities",
            "example": {
                "agent_type": "assistant",
                "agent_name": "HelpBot",
                "tools": "search,calculate,format",
                "capabilities": "conversation,information_retrieval",
            },
        },
        "workflow": {
            "description": "Workflow orchestration agent",
            "example": {
                "agent_type": "workflow",
                "workflow_name": "DataPipeline",
                "steps": '[{"step": "extract", "action": "read_data"}, {"step": "transform", "action": "process_data"}]',
                "triggers": "schedule,manual,event",
            },
        },
    }


@app.post("/validate-agent/")
async def validate_agent_config(
    agent_type: str = Form(...),
    tools: str = Form(""),
    security_level: str = Form("medium"),
):
    """Validate agent configuration before generation."""
    try:
        tools_list = [tool.strip() for tool in tools.split(",") if tool.strip()]

        # Validate parameters
        validate_agent_parameters(agent_type, "test_agent", tools_list, security_level)

        return {
            "valid": True,
            "message": "Agent configuration is valid",
            "warnings": [],
            "recommendations": [],
        }

    except Exception as e:
        return {
            "valid": False,
            "message": str(e),
            "warnings": [],
            "recommendations": [],
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
