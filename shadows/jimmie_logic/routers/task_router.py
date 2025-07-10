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


"""
Task Router - Manages MLOps tasks, audit flows, and work items
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: str
    category: str  # mlops, kubernetes, infrastructure, audit, other
    priority: str = "medium"  # low, medium, high, critical
    tags: List[str] = []
    assignee: Optional[str] = None
    estimated_hours: Optional[float] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    assignee: Optional[str] = None
    estimated_hours: Optional[float] = None
    status: Optional[str] = None  # pending, in_progress, completed, blocked


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    priority: str
    tags: List[str]
    assignee: Optional[str]
    estimated_hours: Optional[float]
    status: str
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None


def get_tasks_file():
    """Get the tasks data file path."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir / "tasks.json"


def load_tasks() -> List[Dict]:
    """Load tasks from JSON file."""
    tasks_file = get_tasks_file()
    if tasks_file.exists():
        try:
            with open(tasks_file, "r") as f:
                return json.load(f)
        except BaseException:
            return []
    return []


def save_tasks(tasks: List[Dict]):
    """Save tasks to JSON file."""
    tasks_file = get_tasks_file()
    with open(tasks_file, "w") as f:
        json.dump(tasks, f, indent=2)


def log_to_history(action: str, task_id: str, details: Dict):
    """Log task activity to history CSV."""
    history_file = Path("data") / "history.csv"
    history_file.parent.mkdir(exist_ok=True)

    # Create CSV file with headers if it doesn't exist
    if not history_file.exists():
        with open(history_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "action", "task_id", "category", "details"])

    with open(history_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                datetime.now().isoformat(),
                action,
                task_id,
                details.get("category", ""),
                json.dumps(details),
            ]
        )


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """Create a new task."""
    tasks = load_tasks()

    task_id = f"task_{len(tasks) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    new_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "category": task.category,
        "priority": task.priority,
        "tags": task.tags,
        "assignee": task.assignee,
        "estimated_hours": task.estimated_hours,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "completed_at": None,
    }

    tasks.append(new_task)
    save_tasks(tasks)

    # Log to history
    log_to_history(
        "create",
        task_id,
        {"category": task.category, "priority": task.priority, "title": task.title},
    )

    return TaskResponse(**new_task)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    category: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
):
    """Get all tasks with optional filtering."""
    tasks = load_tasks()

    # Apply filters
    if category:
        tasks = [t for t in tasks if t.get("category") == category]
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    if priority:
        tasks = [t for t in tasks if t.get("priority") == priority]
    if assignee:
        tasks = [t for t in tasks if t.get("assignee") == assignee]

    return [TaskResponse(**task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a specific task by ID."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            return TaskResponse(**task)

    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate):
    """Update a task."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            # Update fields
            update_data = task_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                task[key] = value

            task["updated_at"] = datetime.now().isoformat()

            # Set completed_at if status is completed
            if task_update.status == "completed" and not task.get("completed_at"):
                task["completed_at"] = datetime.now().isoformat()

            save_tasks(tasks)

            # Log to history
            log_to_history(
                "update",
                task_id,
                {
                    "category": task.get("category"),
                    "status": task.get("status"),
                    "changes": update_data,
                },
            )

            return TaskResponse(**task)

    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a task."""
    tasks = load_tasks()

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(i)
            save_tasks(tasks)

            # Log to history
            log_to_history(
                "delete",
                task_id,
                {
                    "category": deleted_task.get("category"),
                    "title": deleted_task.get("title"),
                },
            )

            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")


@router.get("/stats/summary")
async def get_task_stats():
    """Get task statistics."""
    tasks = load_tasks()

    stats = {
        "total": len(tasks),
        "by_category": {},
        "by_status": {},
        "by_priority": {},
        "recent_completed": 0,
    }

    for task in tasks:
        # Category stats
        category = task.get("category", "unknown")
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

        # Status stats
        status = task.get("status", "unknown")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

        # Priority stats
        priority = task.get("priority", "unknown")
        stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1

        # Recent completed (last 7 days)
        if task.get("status") == "completed" and task.get("completed_at"):
            completed_date = datetime.fromisoformat(task["completed_at"])
            if (datetime.now() - completed_date).days <= 7:
                stats["recent_completed"] += 1

    return stats
