#!/usr/bin/env python3
"""
Agent Builder Router
===================

Router for Agent Builder service endpoints.
Proxies requests to the agent-builder service.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter()

# Agent Builder service configuration
AGENT_BUILDER_BASE_URL = "http://agent-builder:8700"
AGENT_BUILDER_TIMEOUT = 120  # 2 minutes for tool generation


@router.get("/health")
async def health_check():
    """Health check for Agent Builder service."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{AGENT_BUILDER_BASE_URL}/health")
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "service": "agent-builder",
                    "timestamp": datetime.now().isoformat(),
                    "details": response.json(),
                }
            else:
                return {
                    "status": "degraded",
                    "service": "agent-builder",
                    "timestamp": datetime.now().isoformat(),
                    "error": f"Service returned status {response.status_code}",
                }
    except Exception as e:
        logger.error(f"Agent Builder health check failed: {e}")
        return {
            "status": "error",
            "service": "agent-builder",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@router.post("/agent/create")
async def create_agent(task: str = Form(...), category: str = Form(None)):
    """
    Create an AI agent/tool from a natural language task.

    Args:
        task: Natural language description of the task
        category: Optional category override

    Returns:
        Generated tool information
    """
    try:
        async with httpx.AsyncClient(timeout=AGENT_BUILDER_TIMEOUT) as client:
            data = {"task": task}
            if category:
                data["category"] = category

            response = await client.post(
                f"{AGENT_BUILDER_BASE_URL}/agent/create", data=data
            )

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Tool generation timeout")
    except Exception as e:
        logger.error(f"Agent creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Creation failed: {str(e)}")


@router.get("/agent/list")
async def list_agents():
    """
    List all generated agents/tools.

    Returns:
        List of tool information
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{AGENT_BUILDER_BASE_URL}/agent/list")

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")


@router.get("/agent/{tool_id}")
async def get_agent(tool_id: str):
    """
    Get a specific agent/tool by ID.

    Args:
        tool_id: Tool ID to retrieve

    Returns:
        Tool information and content
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{AGENT_BUILDER_BASE_URL}/agent/{tool_id}")

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Failed to get agent: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agent: {str(e)}")


@router.delete("/agent/{tool_id}")
async def delete_agent(tool_id: str):
    """
    Delete an agent/tool by ID.

    Args:
        tool_id: Tool ID to delete

    Returns:
        Deletion confirmation
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(f"{AGENT_BUILDER_BASE_URL}/agent/{tool_id}")

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Failed to delete agent: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete agent: {str(e)}")


@router.get("/categories")
async def get_categories():
    """
    Get available tool categories and their descriptions.

    Returns:
        Category information
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{AGENT_BUILDER_BASE_URL}/categories")

            if response.status_code == 200:
                return response.json()
            else:
                error_detail = (
                    response.json()
                    if response.headers.get("content-type") == "application/json"
                    else response.text
                )
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )

    except Exception as e:
        logger.error(f"Failed to get categories: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get categories: {str(e)}"
        )


@router.get("/stats")
async def get_agent_builder_stats():
    """
    Get Agent Builder service statistics.

    Returns:
        Service statistics and status
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get tools list for stats
            tools_response = await client.get(f"{AGENT_BUILDER_BASE_URL}/agent/list")
            tools_data = (
                tools_response.json()
                if tools_response.status_code == 200
                else {"tools": [], "count": 0}
            )

            # Get categories
            categories_response = await client.get(
                f"{AGENT_BUILDER_BASE_URL}/categories"
            )
            categories_data = (
                categories_response.json()
                if categories_response.status_code == 200
                else {}
            )

            return {
                "service": "agent-builder",
                "timestamp": datetime.now().isoformat(),
                "tools": {
                    "total_count": tools_data.get("count", 0),
                    "by_category": {},
                    "by_complexity": {"simple": 0, "moderate": 0, "complex": 0},
                },
                "categories": categories_data,
                "status": "operational",
            }

    except Exception as e:
        logger.error(f"Failed to get Agent Builder stats: {e}")
        return {
            "service": "agent-builder",
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "error": str(e),
        }
