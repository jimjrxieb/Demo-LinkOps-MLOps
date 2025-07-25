#!/usr/bin/env python3
"""
MCP Tool Schema Validator
========================

This module provides Pydantic-based schema validation for MCP tool submissions,
ensuring data integrity and proper formatting before saving to the database.
"""

import re
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator


class MCPTool(BaseModel):
    """
    MCP Tool Schema with comprehensive validation.

    This schema validates all aspects of MCP tool submissions including:
    - Name format and uniqueness
    - Command syntax and security
    - Tag validation and formatting
    - Auto-execution configuration
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique name for the MCP tool",
        example="restart_apache",
    )

    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Human-readable description of what the tool does",
        example="Restart Apache web server gracefully",
    )

    task_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Type/category of the task (e.g., sysadmin, monitoring, backup)",
        example="sysadmin",
    )

    command: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Command or script to execute",
        example="sudo systemctl restart apache2",
    )

    tags: list[str] = Field(
        default_factory=list,
        description="List of tags for categorizing and filtering tools",
        example=["linux", "apache", "restart"],
    )

    auto: bool = Field(
        default=False,
        description="Whether this tool should be executed automatically by the Auto Runner",
        example=True,
    )

    @validator("name")
    def validate_name(cls, v):
        """Validate tool name format and content."""
        if not v:
            raise ValueError("Tool name cannot be empty")

        # Check for valid characters (alphanumeric, hyphens, underscores)
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Tool name must contain only letters, numbers, hyphens, and underscores"
            )

        # Check for reserved names
        reserved_names = ["system", "admin", "root", "sudo", "exec", "run", "test"]
        if v.lower() in reserved_names:
            raise ValueError(f'Tool name "{v}" is reserved and cannot be used')

        return v.lower()  # Normalize to lowercase

    @validator("description")
    def validate_description(cls, v):
        """Validate tool description."""
        if v is not None:
            # Remove extra whitespace
            v = " ".join(v.split())
            if len(v) > 500:
                raise ValueError("Description must be 500 characters or less")
        return v

    @validator("task_type")
    def validate_task_type(cls, v):
        """Validate task type format."""
        if not v:
            raise ValueError("Task type cannot be empty")

        # Check for valid characters
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Task type must contain only letters, numbers, hyphens, and underscores"
            )

        return v.lower()  # Normalize to lowercase

    @validator("command")
    def validate_command(cls, v):
        """Validate command syntax and security."""
        if not v:
            raise ValueError("Command cannot be empty")

        # Check for potentially dangerous commands
        dangerous_patterns = [
            r"\brm\s+-rf\b",  # rm -rf
            r"\bdd\s+if=/dev/",  # dd with device input
            r"\b:\(\)\s*\{\s*:\s*\|:\s*&\s*\}",  # fork bomb
            r"\bchmod\s+777\b",  # overly permissive chmod
            r"\bchown\s+root\b",  # changing ownership to root
            r"\b>\s*/\w+",  # output redirection to system files
            r"\b\|\s*bash\b",  # piping to bash
            r"\b\|\s*sh\b",  # piping to sh
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError(
                    f"Command contains potentially dangerous pattern: {pattern}"
                )

        # Check for basic command structure
        if len(v.strip()) < 2:
            raise ValueError("Command is too short")

        # Check for maximum length
        if len(v) > 2000:
            raise ValueError("Command is too long (max 2000 characters)")

        return v.strip()

    @validator("tags")
    def validate_tags(cls, v):
        """Validate and normalize tags."""
        if not isinstance(v, list):
            raise ValueError("Tags must be a list")

        validated_tags = []
        for tag in v:
            if not isinstance(tag, str):
                raise ValueError("All tags must be strings")

            # Clean and validate tag
            tag = tag.strip().lower()
            if not tag:
                continue  # Skip empty tags

            # Check tag format - allow spaces and hyphens
            if not re.match(r"^[a-zA-Z0-9\s_-]+$", tag):
                raise ValueError(f'Tag "{tag}" contains invalid characters')

            # Remove spaces and normalize
            tag = re.sub(r"\s+", "-", tag)

            # Check tag length
            if len(tag) > 50:
                raise ValueError(f'Tag "{tag}" is too long (max 50 characters)')

            validated_tags.append(tag)

        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in validated_tags:
            if tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)

        return unique_tags

    @validator("auto")
    def validate_auto(cls, v):
        """Validate auto-execution setting."""
        if not isinstance(v, bool):
            raise ValueError("Auto-execution setting must be a boolean")
        return v

    @root_validator(skip_on_failure=True)
    def validate_tool_integrity(cls, values):
        """Validate overall tool integrity and consistency."""
        name = values.get("name")
        command = values.get("command")
        auto = values.get("auto", False)

        # Check for name-command consistency
        if name and command:
            # If auto-enabled, ensure command is appropriate
            if auto:
                # Check if command looks like it could be run automatically
                if any(
                    keyword in command.lower()
                    for keyword in ["interactive", "prompt", "confirm", "y/n"]
                ):
                    raise ValueError(
                        "Auto-enabled tools should not contain interactive prompts"
                    )

        return values

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "name": "restart_apache",
                "description": "Restart Apache web server gracefully",
                "task_type": "sysadmin",
                "command": "sudo systemctl restart apache2",
                "tags": ["linux", "apache", "restart"],
                "auto": True,
            }
        }

        # Additional validation examples
        examples = [
            {
                "name": "check_disk_space",
                "description": "Check available disk space on all mounted filesystems",
                "task_type": "monitoring",
                "command": "df -h",
                "tags": ["disk", "space", "monitoring"],
                "auto": True,
            },
            {
                "name": "backup_database",
                "description": "Create a backup of the main database",
                "task_type": "backup",
                "command": "pg_dump mydb > backup_$(date +%Y%m%d_%H%M%S).sql",
                "tags": ["database", "backup", "postgresql"],
                "auto": False,
            },
            {
                "name": "system_status",
                "description": "Display system status and resource usage",
                "task_type": "monitoring",
                "command": "uptime && free -h && df -h .",
                "tags": ["system", "status", "monitoring"],
                "auto": True,
            },
        ]


class MCPToolUpdate(BaseModel):
    """
    Schema for updating existing MCP tools.
    All fields are optional for partial updates.
    """

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Updated name for the MCP tool"
    )

    description: Optional[str] = Field(
        None, max_length=500, description="Updated description of what the tool does"
    )

    task_type: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Updated task type/category"
    )

    command: Optional[str] = Field(
        None,
        min_length=1,
        max_length=2000,
        description="Updated command or script to execute",
    )

    tags: Optional[list[str]] = Field(None, description="Updated list of tags")

    auto: Optional[bool] = Field(None, description="Updated auto-execution setting")

    # Reuse the same validators as MCPTool
    @validator("name")
    def validate_name(cls, v):
        if v is not None:
            return MCPTool.validate_name(cls, v)
        return v

    @validator("description")
    def validate_description(cls, v):
        if v is not None:
            return MCPTool.validate_description(cls, v)
        return v

    @validator("task_type")
    def validate_task_type(cls, v):
        if v is not None:
            return MCPTool.validate_task_type(cls, v)
        return v

    @validator("command")
    def validate_command(cls, v):
        if v is not None:
            return MCPTool.validate_command(cls, v)
        return v

    @validator("tags")
    def validate_tags(cls, v):
        if v is not None:
            return MCPTool.validate_tags(cls, v)
        return v

    @validator("auto")
    def validate_auto(cls, v):
        if v is not None:
            return MCPTool.validate_auto(cls, v)
        return v


class MCPToolResponse(BaseModel):
    """
    Schema for MCP tool responses (what gets returned to the client).
    """

    name: str
    description: Optional[str]
    task_type: str
    command: str
    tags: list[str]
    auto: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "restart_apache",
                "description": "Restart Apache web server gracefully",
                "task_type": "sysadmin",
                "command": "sudo systemctl restart apache2",
                "tags": ["linux", "apache", "restart"],
                "auto": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
            }
        }


# Validation utility functions
def validate_mcp_tool_data(data: dict) -> MCPTool:
    """
    Utility function to validate MCP tool data.

    Args:
        data: Dictionary containing MCP tool data

    Returns:
        Validated MCPTool instance

    Raises:
        ValueError: If validation fails
    """
    try:
        return MCPTool(**data)
    except Exception as e:
        raise ValueError(f"MCP tool validation failed: {str(e)}")


def validate_mcp_tool_update(data: dict) -> MCPToolUpdate:
    """
    Utility function to validate MCP tool update data.

    Args:
        data: Dictionary containing MCP tool update data

    Returns:
        Validated MCPToolUpdate instance

    Raises:
        ValueError: If validation fails
    """
    try:
        return MCPToolUpdate(**data)
    except Exception as e:
        raise ValueError(f"MCP tool update validation failed: {str(e)}")
