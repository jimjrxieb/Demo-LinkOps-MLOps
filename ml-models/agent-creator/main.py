#!/usr/bin/env python3
"""
Agent Creator FastAPI Service
============================

FastAPI service for generating and managing AI agents and tools from natural language.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import uvicorn
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logic.agent_generator import AgentGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agent Creator",
    description="Generate AI agents and tools from natural language",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent generator
agent_generator = AgentGenerator()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Agent Creator",
        "status": "running",
        "version": "1.0.0",
        "endpoints": [
            "/agent/create",
            "/agent/list",
            "/agent/{tool_id}",
            "/categories",
            "/health",
        ],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        llm_available = agent_generator._initialize_llm()
        return {
            "status": "healthy" if llm_available else "degraded",
            "service": "agent-creator",
            "llm_available": llm_available,
        }
    except Exception as e:
        return {"status": "error", "service": "agent-creator", "error": str(e)}


@app.post("/agent/create")
async def create_agent(task: str = Form(...), category: str = Form(None)):
    """Create an AI agent/tool from a natural language task."""
    try:
        if not task.strip():
            raise HTTPException(status_code=400, detail="Task description is required")

        result = agent_generator.generate_tool(task, category)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except Exception as e:
        logger.error(f"Agent creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@app.get("/agent/list")
async def list_agents():
    """List all generated agents/tools."""
    try:
        tools = agent_generator.list_tools()
        return {"tools": tools, "count": len(tools)}
    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")


@app.get("/agent/{tool_id}")
async def get_agent(tool_id: str):
    """Get a specific agent/tool by ID."""
    try:
        result = agent_generator.get_tool(tool_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Failed to get agent: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agent: {str(e)}")


@app.delete("/agent/{tool_id}")
async def delete_agent(tool_id: str):
    """Delete an agent/tool by ID."""
    try:
        result = agent_generator.delete_tool(tool_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Failed to delete agent: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete agent: {str(e)}")


@app.get("/categories")
async def get_categories():
    """Get available tool categories and their descriptions."""
    try:
        return agent_generator.get_categories()
    except Exception as e:
        logger.error(f"Failed to get categories: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get categories: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8700, reload=True)
