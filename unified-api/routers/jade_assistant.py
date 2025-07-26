import re
from typing import Dict, List, Optional, Any

import httpx
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from rag.search import semantic_search
from rag.logic.search import semantic_search as rag_semantic_search
from ..logic.executor import execute_tool_by_name

router = APIRouter()


class JadeQuery(BaseModel):
    query: str


class Source(BaseModel):
    content: str
    file: str
    score: float
    highlight: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    tool_run: Optional[Dict] = None


def detect_tool_command(message: str) -> Optional[str]:
    """Extract tool name from command like 'run tool X'."""
    pattern = r"run\s+tool\s+(\w+)"
    match = re.search(pattern, message.lower())
    return match.group(1) if match else None


@router.post("/jade/query")
async def jade_query(data: JadeQuery) -> Dict[str, Any]:
    """
    Process a query from Jade AI Assistant and execute matching tools.
    
    Args:
        data: JadeQuery containing the user's query
        
    Returns:
        Dict containing response, optional result, and optional error
    """
    query = data.query

    # Search memory for matching tools
    search_results = semantic_search(query, top_k=1)
    if not search_results:
        return {"response": "I couldn't find any matching tools for your request."}

    # Pick the best matching tool (top result)
    top_result = search_results[0]
    tool_name = top_result.get("metadata", {}).get("tool_name")

    if not tool_name:
        return {
            "response": "I found something, but it's missing a valid tool reference.",
            "highlight": top_result.get("matched_text", ""),
            "source": top_result.get("source")
        }

    # Execute the matched tool
    try:
        execution_result = execute_tool_by_name(tool_name)
        return {
            "response": f"✅ I ran the tool `{tool_name}` for you.",
            "result": execution_result,
            "highlight": top_result.get("matched_text", ""),
            "source": top_result.get("source"),
            "score": top_result.get("score")
        }
    except FileNotFoundError:
        return {
            "response": f"⚠️ I couldn't find the tool `{tool_name}` in our system.",
            "error": "Tool not found",
            "highlight": top_result.get("matched_text", ""),
            "source": top_result.get("source")
        }
    except Exception as e:
        return {
            "response": f"⚠️ I found `{tool_name}` but it failed to execute.",
            "error": str(e),
            "highlight": top_result.get("matched_text", ""),
            "source": top_result.get("source")
        }
