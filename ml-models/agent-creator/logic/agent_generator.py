import os
import re
import tempfile
import uuid
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader

# Get template directory
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def generate_agent_code(
    agent_type: str,
    agent_name: str,
    tools: List[str] = None,
    capabilities: List[str] = None,
    security_level: str = "medium",
    description: str = "",
    workflow_steps: List[Dict] = None,
    triggers: List[str] = None,
    error_handling: str = "retry",
) -> str:
    """
    Generate AI agent code using Jinja2 templates.

    Args:
        agent_type: Type of agent (base, taskbot, commandbot, assistant, workflow)
        agent_name: Name for the agent
        tools: List of tools/commands the agent can use
        capabilities: List of agent capabilities
        security_level: Security level (low, medium, high)
        description: Agent description
        workflow_steps: List of workflow steps (for workflow agents)
        triggers: List of triggers (for workflow agents)
        error_handling: Error handling strategy

    Returns:
        Path to the generated agent file
    """
    try:
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

        # Map agent types to template names
        template_mapping = {
            "base": "base_agent.py.jinja",
            "taskbot": "taskbot.py.jinja",
            "commandbot": "commandbot.py.jinja",
            "assistant": "assistant.py.jinja",
            "workflow": "workflow.py.jinja",
        }

        template_name = template_mapping.get(agent_type, "base_agent.py.jinja")
        template = env.get_template(template_name)

        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", agent_name)
        output_filename = f"{safe_name}_{agent_type}_{unique_id}.py"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)

        # Prepare context for template rendering
        context = {
            "agent_name": agent_name,
            "agent_type": agent_type,
            "tools": tools or [],
            "capabilities": capabilities or [],
            "security_level": security_level,
            "description": description or f"{agent_name} {agent_type} agent",
            "tools_str": ", ".join(tools) if tools else "",
            "capabilities_str": ", ".join(capabilities) if capabilities else "",
            "workflow_steps": workflow_steps or [],
            "triggers": triggers or [],
            "error_handling": error_handling,
        }

        # Add security configurations based on level
        context.update(get_security_config(security_level))

        # Render template
        rendered_code = template.render(**context)

        # Write generated code to file
        with open(output_path, "w") as f:
            f.write(rendered_code)

        return output_path

    except Exception as e:
        raise Exception(f"Failed to generate agent code: {str(e)}")


def validate_agent_parameters(
    agent_type: str, agent_name: str, tools: List[str], security_level: str
) -> bool:
    """
    Validate agent generation parameters.

    Args:
        agent_type: Type of agent
        agent_name: Name for the agent
        tools: List of tools
        security_level: Security level

    Returns:
        True if valid, raises exception if invalid
    """
    # Validate agent type
    valid_types = ["base", "taskbot", "commandbot", "assistant", "workflow"]
    if agent_type not in valid_types:
        raise ValueError(
            f"Invalid agent type: {agent_type}. Must be one of {valid_types}"
        )

    # Validate agent name
    if not agent_name or not agent_name.strip():
        raise ValueError("Agent name is required")

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", agent_name):
        raise ValueError(
            "Agent name must start with a letter and contain only letters, numbers, and underscores"
        )

    # Validate security level
    valid_levels = ["low", "medium", "high"]
    if security_level not in valid_levels:
        raise ValueError(
            f"Invalid security level: {security_level}. Must be one of {valid_levels}"
        )

    # Validate tools for commandbot
    if agent_type == "commandbot":
        dangerous_commands = [
            "rm",
            "del",
            "format",
            "shutdown",
            "reboot",
            "kill",
            "sudo",
        ]
        for tool in tools:
            if any(dangerous in tool.lower() for dangerous in dangerous_commands):
                if security_level != "high":
                    raise ValueError(
                        f"Dangerous command '{tool}' requires high security level"
                    )

    return True


def get_security_config(security_level: str) -> Dict[str, Any]:
    """Get security configuration based on security level."""
    configs = {
        "low": {
            "input_validation": False,
            "output_sanitization": False,
            "command_whitelist": False,
            "logging_level": "INFO",
            "timeout_seconds": 30,
            "max_retries": 3,
        },
        "medium": {
            "input_validation": True,
            "output_sanitization": True,
            "command_whitelist": True,
            "logging_level": "WARNING",
            "timeout_seconds": 60,
            "max_retries": 2,
        },
        "high": {
            "input_validation": True,
            "output_sanitization": True,
            "command_whitelist": True,
            "logging_level": "ERROR",
            "timeout_seconds": 120,
            "max_retries": 1,
        },
    }

    return configs.get(security_level, configs["medium"])


def get_agent_metadata(agent_type: str) -> Dict[str, Any]:
    """Get metadata about agent types."""
    metadata = {
        "base": {
            "description": "Basic agent template with minimal functionality",
            "use_cases": ["Simple automation", "Learning", "Prototyping"],
            "complexity": "low",
            "security_requirements": "low",
        },
        "taskbot": {
            "description": "Task-oriented agent for handling specific tasks",
            "use_cases": ["Data processing", "File operations", "API interactions"],
            "complexity": "medium",
            "security_requirements": "medium",
        },
        "commandbot": {
            "description": "Command execution agent with security controls",
            "use_cases": [
                "System administration",
                "DevOps automation",
                "Shell scripting",
            ],
            "complexity": "medium",
            "security_requirements": "high",
        },
        "assistant": {
            "description": "AI assistant agent with conversation capabilities",
            "use_cases": [
                "Customer support",
                "Information retrieval",
                "Conversational AI",
            ],
            "complexity": "high",
            "security_requirements": "medium",
        },
        "workflow": {
            "description": "Workflow orchestration agent",
            "use_cases": [
                "Pipeline automation",
                "Process orchestration",
                "Multi-step tasks",
            ],
            "complexity": "high",
            "security_requirements": "high",
        },
    }

    return metadata.get(agent_type, {})


def get_recommended_tools(agent_type: str) -> List[str]:
    """Get recommended tools for different agent types."""
    recommendations = {
        "taskbot": [
            "pandas",
            "numpy",
            "requests",
            "json",
            "csv",
            "datetime",
            "os",
            "pathlib",
            "logging",
            "subprocess",
        ],
        "commandbot": [
            "ls",
            "pwd",
            "whoami",
            "echo",
            "cat",
            "grep",
            "find",
            "mkdir",
            "cp",
            "mv",
            "chmod",
            "ps",
            "top",
        ],
        "assistant": [
            "search",
            "calculate",
            "format",
            "translate",
            "summarize",
            "extract",
            "validate",
            "convert",
        ],
        "workflow": [
            "validate",
            "execute",
            "monitor",
            "notify",
            "rollback",
            "retry",
            "log",
            "report",
        ],
    }

    return recommendations.get(agent_type, [])


def get_capability_descriptions() -> Dict[str, str]:
    """Get descriptions for different capabilities."""
    return {
        "task_execution": "Execute predefined tasks and workflows",
        "command_execution": "Execute system commands with security controls",
        "data_processing": "Process and transform data",
        "file_operations": "Read, write, and manipulate files",
        "network_requests": "Make HTTP requests to external services",
        "workflow_orchestration": "Coordinate multi-step workflows",
        "error_handling": "Handle and recover from errors",
        "monitoring": "Monitor system and process status",
        "logging": "Log activities and events",
        "security_validation": "Validate inputs and enforce security policies",
    }


def generate_agent_documentation(
    agent_name: str,
    agent_type: str,
    tools: List[str],
    capabilities: List[str],
    description: str,
) -> str:
    """Generate documentation for the agent."""
    doc = f"""# {agent_name} Agent

## Overview
{description}

## Type
{agent_type}

## Tools
{chr(10).join(f"- {tool}" for tool in tools) if tools else "- No tools configured"}

## Capabilities
{chr(10).join(f"- {cap}" for cap in capabilities) if capabilities else "- No capabilities configured"}

## Usage
```python
from {agent_name.lower()}_agent import {agent_name}Agent

agent = {agent_name}Agent()
result = agent.handle("your input here")
```

## Security
This agent operates with security level: {get_security_config("medium")["logging_level"]}

## Examples
See the generated agent code for usage examples.
"""
    return doc
