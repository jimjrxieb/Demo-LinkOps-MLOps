import json
import logging
import os
from datetime import datetime

# Import auto runner for execution
from executor.auto_runner import get_execution_history, get_tool_executions, run_tool
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

# Import our comprehensive schema
from schemas.mcp_tool_schema import (
    MCPTool,
    MCPToolResponse,
    MCPToolUpdate,
)

router = APIRouter()
logger = logging.getLogger(__name__)

MCP_DIR = "db/mcp_tools"
os.makedirs(MCP_DIR, exist_ok=True)


@router.post("/mcp-tool", response_model=MCPToolResponse)
async def save_mcp_tool(tool: MCPTool):
    """
    Create a new MCP tool with comprehensive validation.

    This endpoint validates all aspects of the tool submission including:
    - Name format and security
    - Command syntax and safety
    - Tag validation and normalization
    - Auto-execution configuration
    """
    try:
        # Additional validation: check if tool already exists
        path = os.path.join(MCP_DIR, f"{tool.name}.json")
        if os.path.exists(path):
            raise HTTPException(
                status_code=409,
                detail=f"MCP Tool '{tool.name}' already exists. Use PUT to update or choose a different name.",
            )

        # Add metadata
        tool_data = tool.dict()
        tool_data["created_at"] = datetime.utcnow().isoformat() + "Z"
        tool_data["updated_at"] = tool_data["created_at"]

        # Save the validated tool
        with open(path, "w") as f:
            json.dump(tool_data, f, indent=2)

        logger.info(f"✅ MCP Tool '{tool.name}' created successfully")

        return MCPToolResponse(**tool_data)

    except ValidationError as e:
        logger.error(f"❌ MCP Tool validation failed: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating MCP Tool '{tool.name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/mcp-tool/list", response_model=list[MCPToolResponse])
async def list_mcp_tools():
    """
    List all MCP tools with validation and proper formatting.
    """
    try:
        tools = []
        for filename in os.listdir(MCP_DIR):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(MCP_DIR, filename)) as f:
                        tool_data = json.load(f)
                        # Ensure all tools have the required fields
                        if "auto" not in tool_data:
                            tool_data["auto"] = False
                        if "tags" not in tool_data:
                            tool_data["tags"] = []
                        tools.append(MCPToolResponse(**tool_data))
                except Exception as e:
                    logger.warning(f"⚠️ Error loading tool {filename}: {str(e)}")
                    continue

        logger.info(f"📋 Listed {len(tools)} MCP tools")
        return tools

    except Exception as e:
        logger.error(f"❌ Error listing MCP tools: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/mcp-tool/{tool_name}")
async def delete_mcp_tool(tool_name: str):
    """
    Delete an MCP tool by name.
    """
    try:
        path = os.path.join(MCP_DIR, f"{tool_name}.json")
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        os.remove(path)
        logger.info(f"🗑️ MCP Tool '{tool_name}' deleted successfully")
        return {"message": f"MCP Tool '{tool_name}' deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting MCP Tool '{tool_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/mcp-tool/{tool_name}", response_model=MCPToolResponse)
async def update_mcp_tool(tool_name: str, tool_update: MCPToolUpdate):
    """
    Update an existing MCP tool with validation.
    """
    try:
        path = os.path.join(MCP_DIR, f"{tool_name}.json")
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        # Load existing tool
        with open(path) as f:
            existing_data = json.load(f)

        # Update with new data (only provided fields)
        update_data = tool_update.dict(exclude_unset=True)
        existing_data.update(update_data)
        existing_data["updated_at"] = datetime.utcnow().isoformat() + "Z"

        # Validate the updated tool
        try:
            MCPTool(**existing_data)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")

        # Save updated tool
        with open(path, "w") as f:
            json.dump(existing_data, f, indent=2)

        logger.info(f"✅ MCP Tool '{tool_name}' updated successfully")
        return MCPToolResponse(**existing_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating MCP Tool '{tool_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/mcp-tool/{tool_name}", response_model=MCPToolResponse)
async def get_mcp_tool(tool_name: str):
    """
    Get a specific MCP tool by name.
    """
    try:
        path = os.path.join(MCP_DIR, f"{tool_name}.json")
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        with open(path) as f:
            tool_data = json.load(f)

        # Ensure all required fields are present
        if "auto" not in tool_data:
            tool_data["auto"] = False
        if "tags" not in tool_data:
            tool_data["tags"] = []

        return MCPToolResponse(**tool_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting MCP Tool '{tool_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/mcp-tool/execute/{tool_name}")
async def execute_mcp_tool(tool_name: str):
    """
    Execute an MCP tool with full validation and logging.

    This endpoint:
    - Loads and validates the tool
    - Checks auto-execution setting
    - Performs runtime security validation
    - Executes the command with timeout protection
    - Logs the execution result
    """
    try:
        logger.info(f"🚀 API request to execute tool: {tool_name}")

        # Execute the tool using the auto runner
        result = run_tool(tool_name)

        # Determine HTTP status code based on execution result
        if result["success"]:
            logger.info(f"✅ Tool '{tool_name}' executed successfully")
        else:
            logger.warning(
                f"❌ Tool '{tool_name}' execution failed: {result['error_message']}"
            )

        return {
            "status": "success" if result["success"] else "error",
            "message": f"Tool '{tool_name}' execution completed",
            "result": result,
        }

    except Exception as e:
        logger.error(f"❌ Error executing tool '{tool_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")


@router.get("/mcp-tool/executions")
async def list_executions(limit: int = 50):
    """
    Get recent execution history.
    """
    try:
        executions = get_execution_history(limit=limit)
        logger.info(f"📋 Retrieved {len(executions)} execution records")

        return {"executions": executions, "count": len(executions), "limit": limit}

    except Exception as e:
        logger.error(f"❌ Error retrieving execution history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/mcp-tool/executions/{tool_name}")
async def get_tool_execution_history(tool_name: str, limit: int = 20):
    """
    Get execution history for a specific tool.
    """
    try:
        executions = get_tool_executions(tool_name, limit=limit)
        logger.info(
            f"📋 Retrieved {len(executions)} execution records for tool '{tool_name}'"
        )

        return {
            "tool_name": tool_name,
            "executions": executions,
            "count": len(executions),
            "limit": limit,
        }

    except Exception as e:
        logger.error(
            f"❌ Error retrieving execution history for tool '{tool_name}': {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/mcp-tool/status")
async def get_system_status():
    """
    Get overall system status including tool counts and recent activity.
    """
    try:
        # Count available tools
        tool_count = len([f for f in os.listdir(MCP_DIR) if f.endswith(".json")])

        # Get recent executions
        recent_executions = get_execution_history(limit=5)

        # Count auto-enabled tools
        auto_tools = []
        for filename in os.listdir(MCP_DIR):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(MCP_DIR, filename)) as f:
                        tool_data = json.load(f)
                        if tool_data.get("auto", False):
                            auto_tools.append(tool_data["name"])
                except:
                    continue

        status = {
            "total_tools": tool_count,
            "auto_enabled_tools": len(auto_tools),
            "auto_tools": auto_tools,
            "recent_executions": len(recent_executions),
            "system_status": "operational",
        }

        logger.info(
            f"📊 System status: {tool_count} tools, {len(auto_tools)} auto-enabled"
        )
        return status

    except Exception as e:
        logger.error(f"❌ Error getting system status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
