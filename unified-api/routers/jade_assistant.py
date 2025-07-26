import re
from typing import Dict, List, Optional

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rag.search import semantic_search

router = APIRouter(prefix="/jade", tags=["Jade Assistant"])


class ChatQuery(BaseModel):
    message: str


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


@router.post("/chat", response_model=ChatResponse)
async def chat(query: ChatQuery):
    try:
        # Check for tool invocation command
        tool_name = detect_tool_command(query.message)
        if tool_name:
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.post(
                        f"http://localhost:8000/mcp-tool/execute/{tool_name}",
                        timeout=30.0,
                    )
                    if res.status_code == 200:
                        return ChatResponse(
                            answer=f"✅ Successfully ran tool `{tool_name}`",
                            tool_run={
                                "tool": tool_name,
                                "status": "success",
                                "result": res.json(),
                            },
                        )
                    else:
                        return ChatResponse(
                            answer=f"❌ Failed to run tool `{tool_name}`: {res.text}",
                            tool_run={
                                "tool": tool_name,
                                "status": "error",
                                "error": res.text,
                            },
                        )
            except Exception as e:
                return ChatResponse(
                    answer=f"❌ Error executing tool `{tool_name}`: {str(e)}",
                    tool_run={"tool": tool_name, "status": "error", "error": str(e)},
                )

        # Perform semantic search if not a tool command
        results = semantic_search(query.message)

        if not results:
            return ChatResponse(
                answer="I couldn't find any relevant information in the documents.",
                sources=[],
            )

        # Format the response using the best match
        top_result = results[0]
        answer = top_result["content"]

        # Format sources with highlights
        sources = [
            Source(
                content=r["content"],
                file=r["source"],
                score=round(r["score"], 3),
                highlight=r["highlight"],
            )
            for r in results
        ]

        return ChatResponse(answer=answer, sources=sources)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )
