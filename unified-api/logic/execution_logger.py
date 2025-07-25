#!/usr/bin/env python3
"""
SQLite Execution Logger
======================

This module provides SQLite-based logging for MCP tool executions,
replacing the JSON file-based system with better performance and querying capabilities.
"""

import logging
import os
import sqlite3
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Database path
DB_PATH = os.path.join("db", "execution_logs.db")

# Ensure database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def init_logger():
    """Initialize the SQLite database and create tables if they don't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create execution logs table
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT,
                command TEXT NOT NULL,
                stdout TEXT,
                stderr TEXT,
                returncode INTEGER NOT NULL,
                duration_ms INTEGER NOT NULL,
                success BOOLEAN NOT NULL,
                timestamp TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Create indexes for better query performance
        c.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_tool_name
            ON execution_logs(tool_name)
        """
        )

        c.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_timestamp
            ON execution_logs(timestamp)
        """
        )

        c.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_success
            ON execution_logs(success)
        """
        )

        conn.commit()
        conn.close()

        logger.info(f"✅ SQLite execution logger initialized: {DB_PATH}")

    except Exception as e:
        logger.error(f"❌ Failed to initialize SQLite logger: {str(e)}")
        raise


def log_execution(
    tool_name: Optional[str],
    command: str,
    stdout: str,
    stderr: str,
    returncode: int,
    duration_ms: int,
    success: bool = None,
) -> bool:
    """
    Log an execution to the SQLite database.

    Args:
        tool_name: Name of the tool (optional)
        command: Command that was executed
        stdout: Standard output
        stderr: Standard error
        returncode: Return code from execution
        duration_ms: Execution duration in milliseconds
        success: Whether execution was successful (auto-calculated if None)

    Returns:
        True if logging was successful, False otherwise
    """
    try:
        # Auto-calculate success if not provided
        if success is None:
            success = returncode == 0

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute(
            """
            INSERT INTO execution_logs (
                tool_name, command, stdout, stderr, returncode,
                duration_ms, success, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                tool_name,
                command,
                stdout,
                stderr,
                returncode,
                duration_ms,
                success,
                datetime.utcnow().isoformat(),
            ),
        )

        conn.commit()
        conn.close()

        logger.info(f"📝 Execution logged: {tool_name or 'custom'} ({duration_ms}ms)")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to log execution: {str(e)}")
        return False


def get_logs(limit: int = 100, tool_name: Optional[str] = None) -> list[dict[str, Any]]:
    """
    Retrieve execution logs from the database.

    Args:
        limit: Maximum number of logs to return
        tool_name: Filter by tool name (optional)

    Returns:
        List of execution log dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        c = conn.cursor()

        if tool_name:
            c.execute(
                """
                SELECT * FROM execution_logs
                WHERE tool_name = ?
                ORDER BY id DESC
                LIMIT ?
            """,
                (tool_name, limit),
            )
        else:
            c.execute(
                """
                SELECT * FROM execution_logs
                ORDER BY id DESC
                LIMIT ?
            """,
                (limit,),
            )

        rows = c.fetchall()
        conn.close()

        # Convert to list of dictionaries
        logs = []
        for row in rows:
            logs.append(dict(row))

        return logs

    except Exception as e:
        logger.error(f"❌ Failed to retrieve logs: {str(e)}")
        return []


def get_execution_stats() -> dict[str, Any]:
    """
    Get execution statistics from the database.

    Returns:
        Dictionary with execution statistics
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Total executions
        c.execute("SELECT COUNT(*) FROM execution_logs")
        total_executions = c.fetchone()[0]

        # Successful executions
        c.execute("SELECT COUNT(*) FROM execution_logs WHERE success = 1")
        successful_executions = c.fetchone()[0]

        # Failed executions
        c.execute("SELECT COUNT(*) FROM execution_logs WHERE success = 0")
        failed_executions = c.fetchone()[0]

        # Average execution time
        c.execute("SELECT AVG(duration_ms) FROM execution_logs")
        avg_duration = c.fetchone()[0] or 0

        # Most used tools
        c.execute(
            """
            SELECT tool_name, COUNT(*) as count
            FROM execution_logs
            WHERE tool_name IS NOT NULL
            GROUP BY tool_name
            ORDER BY count DESC
            LIMIT 5
        """
        )
        most_used_tools = c.fetchall()

        # Recent activity (last 10 executions)
        c.execute(
            """
            SELECT * FROM execution_logs
            ORDER BY id DESC
            LIMIT 10
        """
        )
        recent_activity = []
        for row in c.fetchall():
            recent_activity.append(
                {
                    "id": row[0],
                    "tool_name": row[1],
                    "command": row[2],
                    "returncode": row[5],
                    "duration_ms": row[6],
                    "success": bool(row[7]),
                    "timestamp": row[8],
                }
            )

        conn.close()

        # Calculate success rate
        success_rate = (
            round((successful_executions / total_executions) * 100, 2)
            if total_executions > 0
            else 0
        )

        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": success_rate,
            "average_execution_time_ms": round(avg_duration, 2),
            "most_used_tools": most_used_tools,
            "recent_activity": recent_activity,
        }

    except Exception as e:
        logger.error(f"❌ Failed to get execution stats: {str(e)}")
        return {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "success_rate": 0,
            "average_execution_time_ms": 0,
            "most_used_tools": [],
            "recent_activity": [],
        }


def cleanup_old_logs(days_to_keep: int = 30) -> int:
    """
    Clean up old execution logs.

    Args:
        days_to_keep: Number of days of logs to keep

    Returns:
        Number of logs deleted
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Delete logs older than specified days
        cutoff_date = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days_to_keep)

        c.execute(
            """
            DELETE FROM execution_logs
            WHERE timestamp < ?
        """,
            (cutoff_date.isoformat(),),
        )

        deleted_count = c.rowcount
        conn.commit()
        conn.close()

        if deleted_count > 0:
            logger.info(f"🧹 Cleaned up {deleted_count} old execution logs")

        return deleted_count

    except Exception as e:
        logger.error(f"❌ Failed to cleanup old logs: {str(e)}")
        return 0


def get_tool_performance(tool_name: str, limit: int = 50) -> dict[str, Any]:
    """
    Get performance statistics for a specific tool.

    Args:
        tool_name: Name of the tool
        limit: Number of recent executions to analyze

    Returns:
        Dictionary with tool performance statistics
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Tool-specific statistics
        c.execute(
            """
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                AVG(duration_ms) as avg_duration,
                MIN(duration_ms) as min_duration,
                MAX(duration_ms) as max_duration
            FROM execution_logs
            WHERE tool_name = ?
        """,
            (tool_name,),
        )

        stats = c.fetchone()

        # Recent executions
        c.execute(
            """
            SELECT * FROM execution_logs
            WHERE tool_name = ?
            ORDER BY id DESC
            LIMIT ?
        """,
            (tool_name, limit),
        )

        recent_executions = []
        for row in c.fetchall():
            recent_executions.append(
                {
                    "id": row[0],
                    "command": row[2],
                    "returncode": row[5],
                    "duration_ms": row[6],
                    "success": bool(row[7]),
                    "timestamp": row[8],
                }
            )

        conn.close()

        if stats[0] == 0:
            return {
                "tool_name": tool_name,
                "total_executions": 0,
                "successful_executions": 0,
                "success_rate": 0,
                "average_duration_ms": 0,
                "min_duration_ms": 0,
                "max_duration_ms": 0,
                "recent_executions": [],
            }

        success_rate = round((stats[1] / stats[0]) * 100, 2)

        return {
            "tool_name": tool_name,
            "total_executions": stats[0],
            "successful_executions": stats[1],
            "success_rate": success_rate,
            "average_duration_ms": round(stats[2] or 0, 2),
            "min_duration_ms": stats[3] or 0,
            "max_duration_ms": stats[4] or 0,
            "recent_executions": recent_executions,
        }

    except Exception as e:
        logger.error(f"❌ Failed to get tool performance: {str(e)}")
        return {
            "tool_name": tool_name,
            "total_executions": 0,
            "successful_executions": 0,
            "success_rate": 0,
            "average_duration_ms": 0,
            "min_duration_ms": 0,
            "max_duration_ms": 0,
            "recent_executions": [],
        }


# Initialize the logger when module is imported
init_logger()
