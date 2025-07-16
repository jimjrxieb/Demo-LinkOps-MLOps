import shlex


def sanitize_cmd(cmd):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {
        "ls",
        "echo",
        "kubectl",
        "helm",
        "python3",
        "cat",
        "go",
        "docker",
        "npm",
        "black",
        "ruff",
        "yamllint",
        "prettier",
        "flake8",
    }
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd


from fastapi import FastAPI
from orb_scoring import get_library_stats, score_task_against_orbs, search_orbs
from pydantic import BaseModel
from task_router import AutonomyEvaluation, Task, evaluate_task

app = FastAPI(title="FickNury Autonomy Evaluator")


class TaskItem(BaseModel):
    task_id: str
    task_description: str


class AutonomyResponse(BaseModel):
    task_id: str
    autonomous: bool
    confidence: float
    reasoning: str
    automation_feasibility: str
    recommendations: list[str]


@app.post("/api/evaluate-autonomy", response_model=AutonomyResponse)
async def evaluate_task_autonomy(task: Task) -> AutonomyResponse:
    """
    Evaluate if a task can be 100% completed autonomously using AI/ML, orbs, and runes.
    This works AFTER the 70% orb confidence check - only for tasks with <70% confidence.
    """
    evaluation = await evaluate_task(task)

    return AutonomyResponse(
        task_id=evaluation.task_id,
        autonomous=evaluation.autonomous,
        confidence=evaluation.confidence,
        reasoning=evaluation.reasoning,
        automation_feasibility=evaluation.automation_feasibility,
        recommendations=evaluation.recommendations,
    )


@app.post("/evaluate")
async def evaluate_single_task(task: Task) -> AutonomyEvaluation:
    """
    Evaluate a single task for autonomy (new system).
    """
    return await evaluate_task(task)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "ficknury-autonomy-evaluator"}


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "service": "ficknury_autonomy_evaluator",
        "purpose": "Evaluates if tasks can be 100% completed autonomously",
        "note": "Works with 70% orb confidence system - evaluates low-confidence tasks",
    }


# --- ORB SCORING ENDPOINTS (unchanged) ---


class OrbTaskInput(BaseModel):
    task: str


class OrbSearchInput(BaseModel):
    query: str


@app.post("/api/orb/score")
async def score_task_with_orbs(input_data: OrbTaskInput):
    """
    Score a task against the DevSecOps Orb library for automation evaluation
    """
    try:
        result = score_task_against_orbs(input_data.task)
        return result
    except Exception as e:
        return {"error": str(e), "task": input_data.task}


@app.post("/api/orb/search")
async def search_orb_library(input_data: OrbSearchInput):
    """
    Search the Orb library by title, keywords, or category
    """
    try:
        results = search_orbs(input_data.query)
        return {"query": input_data.query, "results": results, "total": len(results)}
    except Exception as e:
        return {"error": str(e), "query": input_data.query}


@app.get("/api/orb/stats")
async def get_orb_library_stats():
    """
    Get statistics about the Orb library
    """
    try:
        return get_library_stats()
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/orb/health")
async def orb_health_check():
    """
    Health check for Orb scoring functionality
    """
    try:
        stats = get_library_stats()
        return {
            "status": "healthy",
            "orb_scoring": "enabled",
            "library_loaded": stats["total_orbs"] > 0,
            "total_orbs": stats["total_orbs"],
            "categories": stats["categories"],
        }
    except Exception as e:
        return {"status": "unhealthy", "orb_scoring": "error", "error": str(e)}
