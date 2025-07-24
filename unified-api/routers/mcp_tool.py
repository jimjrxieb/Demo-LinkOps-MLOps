import json
import os
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

MCP_DIR = "db/mcp_tools"
os.makedirs(MCP_DIR, exist_ok=True)


class MCPTool(BaseModel):
    name: str
    description: str
    task_type: str
    command: str
    tags: Optional[List[str]] = []


@router.post("/mcp-tool")
def save_mcp_tool(tool: MCPTool):
    try:
        path = os.path.join(MCP_DIR, f"{tool.name}.json")
        with open(path, "w") as f:
            json.dump(tool.dict(), f, indent=2)
        return {"message": f"MCP Tool '{tool.name}' saved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mcp-tool/list")
def list_mcp_tools():
    tools = []
    for filename in os.listdir(MCP_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(MCP_DIR, filename)) as f:
                tools.append(json.load(f))
    return tools


@router.delete("/mcp-tool/{tool_name}")
def delete_mcp_tool(tool_name: str):
    path = os.path.join(MCP_DIR, f"{tool_name}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Tool not found")
    os.remove(path)
    return {"message": f"MCP Tool '{tool_name}' deleted."}
