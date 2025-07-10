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
Daily Router - Manages daily logs and digests
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter()


class DailyLogCreate(BaseModel):
    date: str
    summary: str
    tasks_completed: List[str] = []
    tasks_pending: List[str] = []
    challenges: List[str] = []
    achievements: List[str] = []
    notes: str = ""
    mood: Optional[str] = None  # great, good, okay, bad
    hours_worked: Optional[float] = None


class DailyLogUpdate(BaseModel):
    summary: Optional[str] = None
    tasks_completed: Optional[List[str]] = None
    tasks_pending: Optional[List[str]] = None
    challenges: Optional[List[str]] = None
    achievements: Optional[List[str]] = None
    notes: Optional[str] = None
    mood: Optional[str] = None
    hours_worked: Optional[float] = None


class DailyLogResponse(BaseModel):
    id: str
    date: str
    summary: str
    tasks_completed: List[str]
    tasks_pending: List[str]
    challenges: List[str]
    achievements: List[str]
    notes: str
    mood: Optional[str]
    hours_worked: Optional[float]
    created_at: str
    updated_at: str


def get_daily_logs_file():
    """Get the daily logs data file path."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir / "daily_logs.json"


def load_daily_logs() -> List[Dict]:
    """Load daily logs from JSON file."""
    logs_file = get_daily_logs_file()
    if logs_file.exists():
        try:
            with open(logs_file, "r") as f:
                return json.load(f)
        except BaseException:
            return []
    return []


def save_daily_logs(logs: List[Dict]):
    """Save daily logs to JSON file."""
    logs_file = get_daily_logs_file()
    with open(logs_file, "w") as f:
        json.dump(logs, f, indent=2)


@router.post("/", response_model=DailyLogResponse)
async def create_daily_log(log: DailyLogCreate):
    """Create a new daily log."""
    logs = load_daily_logs()

    log_id = f"daily_{log.date}_{datetime.now().strftime('%H%M%S')}"

    new_log = {
        "id": log_id,
        "date": log.date,
        "summary": log.summary,
        "tasks_completed": log.tasks_completed,
        "tasks_pending": log.tasks_pending,
        "challenges": log.challenges,
        "achievements": log.achievements,
        "notes": log.notes,
        "mood": log.mood,
        "hours_worked": log.hours_worked,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    logs.append(new_log)
    save_daily_logs(logs)

    return DailyLogResponse(**new_log)


@router.get("/", response_model=List[DailyLogResponse])
async def get_daily_logs(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    mood: Optional[str] = None,
):
    """Get daily logs with optional filtering."""
    logs = load_daily_logs()

    # Apply filters
    if start_date:
        logs = [log for log in logs if log.get("date") >= start_date]
    if end_date:
        logs = [log for log in logs if log.get("date") <= end_date]
    if mood:
        logs = [log for log in logs if log.get("mood") == mood]

    # Sort by date (newest first)
    logs.sort(key=lambda x: x.get("date", ""), reverse=True)

    return [DailyLogResponse(**log) for log in logs]


@router.get("/{log_id}", response_model=DailyLogResponse)
async def get_daily_log(log_id: str):
    """Get a specific daily log by ID."""
    logs = load_daily_logs()

    for log in logs:
        if log["id"] == log_id:
            return DailyLogResponse(**log)

    raise HTTPException(status_code=404, detail="Daily log not found")


@router.put("/{log_id}", response_model=DailyLogResponse)
async def update_daily_log(log_id: str, log_update: DailyLogUpdate):
    """Update a daily log."""
    logs = load_daily_logs()

    for log in logs:
        if log["id"] == log_id:
            # Update fields
            update_data = log_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                log[key] = value

            log["updated_at"] = datetime.now().isoformat()
            save_daily_logs(logs)

            return DailyLogResponse(**log)

    raise HTTPException(status_code=404, detail="Daily log not found")


@router.delete("/{log_id}")
async def delete_daily_log(log_id: str):
    """Delete a daily log."""
    logs = load_daily_logs()

    for i, log in enumerate(logs):
        if log["id"] == log_id:
            logs.pop(i)
            save_daily_logs(logs)
            return {"message": "Daily log deleted successfully"}

    raise HTTPException(status_code=404, detail="Daily log not found")


@router.get("/today/summary")
async def get_today_summary():
    """Get today's summary and statistics."""
    today = datetime.now().strftime("%Y-%m-%d")
    logs = load_daily_logs()

    today_logs = [log for log in logs if log.get("date") == today]

    if not today_logs:
        return {"date": today, "has_log": False, "message": "No log found for today"}

    # Get the most recent log for today
    today_log = max(today_logs, key=lambda x: x.get("created_at", ""))

    return {
        "date": today,
        "has_log": True,
        "summary": today_log.get("summary", ""),
        "tasks_completed_count": len(today_log.get("tasks_completed", [])),
        "tasks_pending_count": len(today_log.get("tasks_pending", [])),
        "achievements_count": len(today_log.get("achievements", [])),
        "challenges_count": len(today_log.get("challenges", [])),
        "mood": today_log.get("mood"),
        "hours_worked": today_log.get("hours_worked"),
    }


@router.get("/stats/weekly")
async def get_weekly_stats():
    """Get weekly statistics."""
    today = datetime.now()
    week_ago = today - timedelta(days=7)

    logs = load_daily_logs()
    weekly_logs = [
        log
        for log in logs
        if week_ago.strftime("%Y-%m-%d")
        <= log.get("date", "")
        <= today.strftime("%Y-%m-%d")
    ]

    if not weekly_logs:
        return {
            "period": f"{week_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}",
            "total_logs": 0,
            "message": "No logs found for this week",
        }

    total_tasks_completed = sum(
        len(log.get("tasks_completed", [])) for log in weekly_logs
    )
    total_tasks_pending = sum(len(log.get("tasks_pending", [])) for log in weekly_logs)
    total_achievements = sum(len(log.get("achievements", [])) for log in weekly_logs)
    total_hours = sum(log.get("hours_worked", 0) for log in weekly_logs)

    # Mood distribution
    mood_counts = {}
    for log in weekly_logs:
        mood = log.get("mood", "unknown")
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

    return {
        "period": f"{week_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}",
        "total_logs": len(weekly_logs),
        "total_tasks_completed": total_tasks_completed,
        "total_tasks_pending": total_tasks_pending,
        "total_achievements": total_achievements,
        "total_hours_worked": round(total_hours, 2),
        "average_tasks_per_day": round(total_tasks_completed / len(weekly_logs), 2),
        "mood_distribution": mood_counts,
    }


@router.get("/stats/monthly")
async def get_monthly_stats():
    """Get monthly statistics."""
    today = datetime.now()
    month_ago = today - timedelta(days=30)

    logs = load_daily_logs()
    monthly_logs = [
        log
        for log in logs
        if month_ago.strftime("%Y-%m-%d")
        <= log.get("date", "")
        <= today.strftime("%Y-%m-%d")
    ]

    if not monthly_logs:
        return {
            "period": f"{month_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}",
            "total_logs": 0,
            "message": "No logs found for this month",
        }

    total_tasks_completed = sum(
        len(log.get("tasks_completed", [])) for log in monthly_logs
    )
    total_tasks_pending = sum(len(log.get("tasks_pending", [])) for log in monthly_logs)
    total_achievements = sum(len(log.get("achievements", [])) for log in monthly_logs)
    total_hours = sum(log.get("hours_worked", 0) for log in monthly_logs)

    # Most common challenges
    all_challenges = []
    for log in monthly_logs:
        all_challenges.extend(log.get("challenges", []))

    challenge_counts = {}
    for challenge in all_challenges:
        challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1

    top_challenges = sorted(challenge_counts.items(), key=lambda x: x[1], reverse=True)[
        :5
    ]

    return {
        "period": f"{month_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}",
        "total_logs": len(monthly_logs),
        "total_tasks_completed": total_tasks_completed,
        "total_tasks_pending": total_tasks_pending,
        "total_achievements": total_achievements,
        "total_hours_worked": round(total_hours, 2),
        "average_tasks_per_day": round(total_tasks_completed / len(monthly_logs), 2),
        "top_challenges": top_challenges,
    }


@router.post("/export")
async def export_daily_logs(request: Request):
    """Export daily logs to CSV."""
    data = await request.json()
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    logs = load_daily_logs()

    # Apply date filters
    if start_date:
        logs = [log for log in logs if log.get("date") >= start_date]
    if end_date:
        logs = [log for log in logs if log.get("date") <= end_date]

    # Sort by date
    logs.sort(key=lambda x: x.get("date", ""))

    # Create CSV content
    csv_content = []
    headers = [
        "date",
        "summary",
        "tasks_completed",
        "tasks_pending",
        "challenges",
        "achievements",
        "notes",
        "mood",
        "hours_worked",
    ]
    csv_content.append(headers)

    for log in logs:
        row = [
            log.get("date", ""),
            log.get("summary", ""),
            "; ".join(log.get("tasks_completed", [])),
            "; ".join(log.get("tasks_pending", [])),
            "; ".join(log.get("challenges", [])),
            "; ".join(log.get("achievements", [])),
            log.get("notes", ""),
            log.get("mood", ""),
            str(log.get("hours_worked", "")),
        ]
        csv_content.append(row)

    return {
        "message": "Daily logs exported successfully",
        "total_logs": len(logs),
        "csv_content": csv_content,
    }
