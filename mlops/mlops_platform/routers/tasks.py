from datetime import datetime


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


from fastapi import APIRouter, Body
from logic import storage

router = APIRouter()

TASKS_FILE = "tasks.json"
HISTORY_FILE = "history.csv"


@router.get("/")
def list_tasks():
    tasks = storage.read_json(TASKS_FILE)
    return {"tasks": tasks}


@router.post("/")
def add_task(task: dict = Body(...)):
    # Store in tasks.json
    storage.append_to_json(TASKS_FILE, task)

    # Also log to history.csv
    storage.append_to_csv(
        HISTORY_FILE,
        {
            "timestamp": datetime.utcnow().isoformat(),
            "input_type": "task",
            "source": "manual_input",
            "content": task.get("description", str(task)),
            "intent": task.get("intent", "unknown"),
        },
    )

    return {"message": "Task submitted successfully.", "task": task}
