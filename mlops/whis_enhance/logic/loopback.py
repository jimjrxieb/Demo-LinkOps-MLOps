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
Whis Loopback Logic - Processes repeated tasks and improves runes based on feedback.
This module implements the feedback loop for continuous improvement of the Whis system.
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .enhancer import enhance_content

logger = logging.getLogger(__name__)

# File paths
HISTORY_FILE = (
    Path(__file__).parent.parent.parent / "mlops_platform" / "data" / "history.csv"
)
RUNES_FILE = (
    Path(__file__).parent.parent.parent / "mlops_platform" / "data" / "runes.json"
)
ORBS_FILE = (
    Path(__file__).parent.parent.parent / "mlops_platform" / "data" / "orbs.json"
)
FEEDBACK_DIR = (
    Path(__file__).parent.parent.parent / "mlops_platform" / "data" / "feedback"
)


def load_repeat_tasks(threshold: int = 2) -> List[Dict[str, Any]]:
    """
    Find tasks that appear more than threshold times in history.

    Args:
        threshold: Minimum number of occurrences to consider a task as repeated

    Returns:
        List of repeated tasks with their metadata
    """
    if not HISTORY_FILE.exists():
        logger.warning(f"History file not found: {HISTORY_FILE}")
        return []

    counts = {}
    task_details = {}

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                content = row.get("content", "").strip()
                if content:
                    counts[content] = counts.get(content, 0) + 1
                    if content not in task_details:
                        task_details[content] = {
                            "content": content,
                            "first_seen": row.get("timestamp", ""),
                            "last_seen": row.get("timestamp", ""),
                            "status": row.get("status", ""),
                            "agent": row.get("agent", ""),
                            "confidence": float(row.get("confidence", 0.0)),
                            "occurrences": 1,
                        }
                    else:
                        task_details[content]["last_seen"] = row.get("timestamp", "")
                        task_details[content]["occurrences"] = counts[content]
    except Exception as e:
        logger.error(f"Error reading history file: {str(e)}")
        return []

    # Filter tasks that meet the threshold
    repeated_tasks = [
        task for task in task_details.values() if task["occurrences"] >= threshold
    ]

    logger.info(
        f"Found {len(repeated_tasks)} repeated tasks with threshold {threshold}"
    )
    return repeated_tasks


def load_failed_tasks() -> List[Dict[str, Any]]:
    """
    Load tasks that have failed or been marked as problematic.

    Returns:
        List of failed tasks
    """
    if not HISTORY_FILE.exists():
        return []

    failed_tasks = []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = row.get("status", "").lower()
                if status in ["failed", "error", "blocked", "timeout"]:
                    failed_tasks.append(
                        {
                            "content": row.get("content", ""),
                            "status": status,
                            "error_message": row.get("error_message", ""),
                            "timestamp": row.get("timestamp", ""),
                            "agent": row.get("agent", ""),
                            "confidence": float(row.get("confidence", 0.0)),
                        }
                    )
    except Exception as e:
        logger.error(f"Error reading failed tasks: {str(e)}")

    return failed_tasks


def find_matching_rune(
    task_content: str, runes: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Find a rune that matches the given task content.

    Args:
        task_content: The task content to match
        runes: List of available runes

    Returns:
        Matching rune or None if not found
    """
    for rune in runes:
        description = rune.get("description", "").lower()
        keywords = rune.get("keywords", [])

        # Check if task content contains rune description or keywords
        task_lower = task_content.lower()
        if description in task_lower:
            return rune

        for keyword in keywords:
            if keyword.lower() in task_lower:
                return rune

    return None


async def enhance_rune(
    rune: Dict[str, Any], task_feedback: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Enhance a rune based on task feedback and performance data.

    Args:
        rune: The rune to enhance
        task_feedback: Feedback data from repeated/failed tasks

    Returns:
        Enhanced rune
    """
    enhanced_rune = rune.copy()

    try:
        # Enhance rune description based on feedback
        if "description" in rune:
            enhanced_description, _ = await enhance_content(
                {"text": rune["description"]}, {"enhancement_type": "content"}
            )
            enhanced_rune["description"] = enhanced_description.get(
                "text", rune["description"]
            )

        # Enhance rune logic based on failure patterns
        if "logic" in rune and task_feedback.get("error_message"):
            enhanced_logic, _ = await enhance_content(
                {"text": rune["logic"]}, {"enhancement_type": "quality"}
            )
            enhanced_rune["logic"] = enhanced_logic.get("text", rune["logic"])

        # Add feedback-based improvements
        enhanced_rune["improvements"] = enhanced_rune.get("improvements", [])
        enhanced_rune["improvements"].append(
            {
                "type": "loopback_enhancement",
                "timestamp": datetime.now().isoformat(),
                "feedback_source": task_feedback.get("content", ""),
                "confidence_before": task_feedback.get("confidence", 0.0),
                "status": task_feedback.get("status", ""),
            }
        )

        # Update success rate if available
        if "success_rate" in enhanced_rune:
            current_rate = enhanced_rune["success_rate"]
            if task_feedback.get("status") == "completed":
                enhanced_rune["success_rate"] = min(1.0, current_rate + 0.01)
            else:
                enhanced_rune["success_rate"] = max(0.0, current_rate - 0.02)

        # Add version tracking
        enhanced_rune["version"] = enhanced_rune.get("version", 1) + 1
        enhanced_rune["last_enhanced"] = datetime.now().isoformat()

        logger.info(f"Enhanced rune {rune.get('id', 'unknown')} based on feedback")

    except Exception as e:
        logger.error(f"Error enhancing rune: {str(e)}")

    return enhanced_rune


async def loopback_refine(threshold: int = 2) -> Dict[str, Any]:
    """
    Main loopback refinement process.

    Args:
        threshold: Minimum occurrences for repeated tasks

    Returns:
        Summary of refinement results
    """
    results = {
        "enhanced_runes": [],
        "enhanced_orbs": [],
        "failed_tasks_processed": 0,
        "repeated_tasks_processed": 0,
        "total_improvements": 0,
        "timestamp": datetime.now().isoformat(),
    }

    try:
        # Load repeated tasks
        repeated_tasks = load_repeat_tasks(threshold)
        results["repeated_tasks_processed"] = len(repeated_tasks)

        # Load failed tasks
        failed_tasks = load_failed_tasks()
        results["failed_tasks_processed"] = len(failed_tasks)

        # Load runes
        if RUNES_FILE.exists():
            with open(RUNES_FILE, "r", encoding="utf-8") as f:
                runes = json.load(f)
        else:
            logger.warning(f"Runes file not found: {RUNES_FILE}")
            runes = []

        # Process repeated tasks
        for task in repeated_tasks:
            matching_rune = find_matching_rune(task["content"], runes)
            if matching_rune:
                enhanced_rune = await enhance_rune(matching_rune, task)
                results["enhanced_runes"].append(
                    {
                        "rune_id": matching_rune.get("id"),
                        "enhancements": enhanced_rune.get("improvements", []),
                    }
                )
                results["total_improvements"] += 1

        # Process failed tasks
        for task in failed_tasks:
            matching_rune = find_matching_rune(task["content"], runes)
            if matching_rune:
                enhanced_rune = await enhance_rune(matching_rune, task)
                results["enhanced_runes"].append(
                    {
                        "rune_id": matching_rune.get("id"),
                        "enhancements": enhanced_rune.get("improvements", []),
                    }
                )
                results["total_improvements"] += 1

        # Save enhanced runes back to file
        if results["enhanced_runes"]:
            await save_enhanced_runes(runes)

        logger.info(
            f"Loopback refinement completed: {results['total_improvements']} improvements made"
        )

    except Exception as e:
        logger.error(f"Error in loopback refinement: {str(e)}")
        results["error"] = str(e)

    return results


async def save_enhanced_runes(runes: List[Dict[str, Any]]) -> None:
    """
    Save enhanced runes back to the runes file.

    Args:
        runes: List of runes to save
    """
    try:
        # Create backup
        if RUNES_FILE.exists():
            backup_file = RUNES_FILE.with_suffix(
                f".backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            with open(RUNES_FILE, "r", encoding="utf-8") as f:
                with open(backup_file, "w", encoding="utf-8") as backup:
                    backup.write(f.read())

        # Save enhanced runes
        with open(RUNES_FILE, "w", encoding="utf-8") as f:
            json.dump(runes, f, indent=2, ensure_ascii=False)

        logger.info(f"Enhanced runes saved to {RUNES_FILE}")

    except Exception as e:
        logger.error(f"Error saving enhanced runes: {str(e)}")


def get_loopback_statistics() -> Dict[str, Any]:
    """
    Get statistics about loopback processing.

    Returns:
        Dictionary with loopback statistics
    """
    stats = {
        "repeated_tasks": len(load_repeat_tasks(2)),
        "failed_tasks": len(load_failed_tasks()),
        "total_history_entries": 0,
        "last_loopback_run": None,
    }

    # Count total history entries
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                stats["total_history_entries"] = sum(1 for _ in reader)
        except Exception as e:
            logger.error(f"Error counting history entries: {str(e)}")

    # Check for last loopback run in feedback directory
    if FEEDBACK_DIR.exists():
        feedback_files = list(FEEDBACK_DIR.glob("loopback_*.json"))
        if feedback_files:
            latest_file = max(feedback_files, key=lambda x: x.stat().st_mtime)
            stats["last_loopback_run"] = datetime.fromtimestamp(
                latest_file.stat().st_mtime
            ).isoformat()

    return stats
