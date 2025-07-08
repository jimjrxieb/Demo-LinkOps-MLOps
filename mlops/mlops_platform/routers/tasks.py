from datetime import datetime

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
