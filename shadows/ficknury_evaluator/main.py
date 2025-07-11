from typing import dict, list


def sanitize_cmd(cmd):
    import shlex

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


from fastapi import FastAPI, Request
from pydantic import BaseModel
from scorer import score_task
from selector import select_agent_for_task
from task_router import Task, TaskEvaluation, evaluate_task

app = FastAPI(title="FickNury Evaluator")


class TaskItem(BaseModel):
    task_id: str
    task_description: str


class EvaluationResponse(BaseModel):
    automatable: list[str]
    non_automatable: list[str]
    score_map: dict[str, float]
    suggestions: dict[str, str]


@app.post("/api/evaluate", response_model=EvaluationResponse)
async def evaluate_tasks(request: Request):
    data = await request.json()
    tasks = data.get("tasks", [])

    auto_ids = []
    non_auto_ids = []
    score_map = {}
    suggestions = {}

    for task in tasks:
        task_id = task.get("task_id")
        description = task.get("task_description")
        score_data = score_task(task)
        agent = select_agent_for_task(description, {})

        score_map[task_id] = score_data["score"]
        suggestions[task_id] = agent

        if score_data["automatable"]:
            auto_ids.append(task_id)
        else:
            non_auto_ids.append(task_id)

    return EvaluationResponse(
        automatable=auto_ids,
        non_automatable=non_auto_ids,
        score_map=score_map,
        suggestions=suggestions,
    )


@app.post("/evaluate")
async def evaluate_single_task(task: Task) -> TaskEvaluation:
    """
    Evaluate a single task using the new task router.
    """
    return await evaluate_task(task)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "ficknury-evaluator"}


@app.get("/")
def read_root():
    return {"status": "ok", "service": "ficknury_evaluator"}
