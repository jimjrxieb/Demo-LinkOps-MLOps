#!/usr/bin/env python3
"""
Status API Routes
================

API endpoints for system monitoring and tenant data summary.
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()

# Database path
DB_PATH = Path("db/sqlite/tenants.db")


# Pydantic models for response validation
class TenantSummary(BaseModel):
    tenant_name: str
    unit: Optional[str]
    lease_end: Optional[str]
    status: Optional[str]


class FileSummary(BaseModel):
    file: str
    count: int


class SyncLogEntry(BaseModel):
    file_name: str
    status: str
    records_processed: int
    synced_at: str


class SystemStatus(BaseModel):
    tenant_count: int
    file_count: int
    active_tenants: int
    expiring_leases: int
    total_rent: Optional[float]
    last_sync: Optional[str]


@router.get("/status/summary")
async def get_summary():
    """Get comprehensive system status summary."""
    try:
        if not DB_PATH.exists():
            return {
                "tenant_count": 0,
                "file_count": 0,
                "active_tenants": 0,
                "expiring_leases": 0,
                "total_rent": 0,
                "source_files": [],
                "expiring_leases": [],
                "recent_syncs": [],
                "system_status": "no_data",
            }

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Get basic counts
        cur.execute("SELECT COUNT(*) FROM tenants")
        tenant_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(DISTINCT source_file) FROM tenants")
        file_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM tenants WHERE status = 'active'")
        active_tenants = cur.fetchone()[0]

        # Get expiring leases (within 30 days)
        thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime(
            "%Y-%m-%d"
        )
        cur.execute(
            """
            SELECT COUNT(*) FROM tenants 
            WHERE lease_end <= ? AND status = 'active'
        """,
            (thirty_days_from_now,),
        )
        expiring_leases = cur.fetchone()[0]

        # Get total rent
        cur.execute("SELECT SUM(rent_amount) FROM tenants WHERE status = 'active'")
        total_rent_result = cur.fetchone()[0]
        total_rent = float(total_rent_result) if total_rent_result else 0

        # Get source files summary
        cur.execute(
            """
            SELECT source_file, COUNT(*) 
            FROM tenants 
            GROUP BY source_file 
            ORDER BY COUNT(*) DESC
        """
        )
        source_files = [{"file": row[0], "count": row[1]} for row in cur.fetchall()]

        # Get expiring leases details
        cur.execute(
            """
            SELECT tenant_name, unit, lease_end, status 
            FROM tenants 
            WHERE lease_end <= ? AND status = 'active'
            ORDER BY lease_end ASC 
            LIMIT 10
        """,
            (thirty_days_from_now,),
        )
        expiring_leases_details = [
            {"name": row[0], "unit": row[1], "lease_end": row[2], "status": row[3]}
            for row in cur.fetchall()
        ]

        # Get recent sync operations
        cur.execute(
            """
            SELECT file_name, status, records_processed, synced_at 
            FROM sync_log 
            ORDER BY synced_at DESC 
            LIMIT 5
        """
        )
        recent_syncs = [
            {
                "file_name": row[0],
                "status": row[1],
                "records_processed": row[2],
                "synced_at": row[3],
            }
            for row in cur.fetchall()
        ]

        # Get last sync time
        last_sync = None
        if recent_syncs:
            last_sync = recent_syncs[0]["synced_at"]

        conn.close()

        return {
            "tenant_count": tenant_count,
            "file_count": file_count,
            "active_tenants": active_tenants,
            "expiring_leases": expiring_leases,
            "total_rent": total_rent,
            "source_files": source_files,
            "expiring_leases": expiring_leases_details,
            "recent_syncs": recent_syncs,
            "last_sync": last_sync,
            "system_status": "operational" if tenant_count > 0 else "no_data",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to get summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/tenants")
async def get_tenants(status: Optional[str] = None, limit: int = 50, offset: int = 0):
    """Get tenant list with optional filtering."""
    try:
        if not DB_PATH.exists():
            return {"tenants": [], "total": 0}

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Build query based on filters
        query = "SELECT tenant_name, unit, status, lease_start, lease_end, rent_amount, email, phone FROM tenants"
        params = []

        if status:
            query += " WHERE status = ?"
            params.append(status)

        # Get total count
        count_query = query.replace(
            "SELECT tenant_name, unit, status, lease_start, lease_end, rent_amount, email, phone",
            "SELECT COUNT(*)",
        )
        cur.execute(count_query, params)
        total = cur.fetchone()[0]

        # Get paginated results
        query += " ORDER BY tenant_name LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cur.execute(query, params)
        tenants = [
            {
                "tenant_name": row[0],
                "unit": row[1],
                "status": row[2],
                "lease_start": row[3],
                "lease_end": row[4],
                "rent_amount": row[5],
                "email": row[6],
                "phone": row[7],
            }
            for row in cur.fetchall()
        ]

        conn.close()

        return {"tenants": tenants, "total": total, "limit": limit, "offset": offset}

    except Exception as e:
        logger.error(f"Failed to get tenants: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/sync-log")
async def get_sync_log(limit: int = 20):
    """Get recent sync operations log."""
    try:
        if not DB_PATH.exists():
            return {"sync_log": [], "total": 0}

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Get total count
        cur.execute("SELECT COUNT(*) FROM sync_log")
        total = cur.fetchone()[0]

        # Get recent sync log
        cur.execute(
            """
            SELECT file_name, file_hash, status, records_processed, error_message, synced_at 
            FROM sync_log 
            ORDER BY synced_at DESC 
            LIMIT ?
        """,
            (limit,),
        )

        sync_log = [
            {
                "file_name": row[0],
                "file_hash": row[1],
                "status": row[2],
                "records_processed": row[3],
                "error_message": row[4],
                "synced_at": row[5],
            }
            for row in cur.fetchall()
        ]

        conn.close()

        return {"sync_log": sync_log, "total": total, "limit": limit}

    except Exception as e:
        logger.error(f"Failed to get sync log: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/analytics")
async def get_analytics():
    """Get analytics and insights."""
    try:
        if not DB_PATH.exists():
            return {"analytics": {}, "status": "no_data"}

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        # Get status distribution
        cur.execute(
            """
            SELECT status, COUNT(*) 
            FROM tenants 
            GROUP BY status
        """
        )
        status_distribution = {row[0]: row[1] for row in cur.fetchall()}

        # Get monthly rent distribution
        cur.execute(
            """
            SELECT 
                CASE 
                    WHEN rent_amount < 1000 THEN 'Under $1K'
                    WHEN rent_amount < 2000 THEN '$1K-$2K'
                    WHEN rent_amount < 3000 THEN '$2K-$3K'
                    ELSE 'Over $3K'
                END as rent_range,
                COUNT(*) as count
            FROM tenants 
            WHERE rent_amount IS NOT NULL AND status = 'active'
            GROUP BY rent_range
        """
        )
        rent_distribution = {row[0]: row[1] for row in cur.fetchall()}

        # Get lease expiration timeline
        cur.execute(
            """
            SELECT 
                CASE 
                    WHEN lease_end <= date('now') THEN 'Expired'
                    WHEN lease_end <= date('now', '+30 days') THEN '30 days'
                    WHEN lease_end <= date('now', '+60 days') THEN '60 days'
                    WHEN lease_end <= date('now', '+90 days') THEN '90 days'
                    ELSE '90+ days'
                END as timeline,
                COUNT(*) as count
            FROM tenants 
            WHERE lease_end IS NOT NULL AND status = 'active'
            GROUP BY timeline
        """
        )
        lease_timeline = {row[0]: row[1] for row in cur.fetchall()}

        # Get average rent
        cur.execute(
            "SELECT AVG(rent_amount) FROM tenants WHERE rent_amount IS NOT NULL AND status = 'active'"
        )
        avg_rent_result = cur.fetchone()[0]
        avg_rent = float(avg_rent_result) if avg_rent_result else 0

        # Get occupancy rate
        cur.execute("SELECT COUNT(*) FROM tenants WHERE status = 'active'")
        active_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tenants")
        total_count = cur.fetchone()[0]
        occupancy_rate = (active_count / total_count * 100) if total_count > 0 else 0

        conn.close()

        return {
            "analytics": {
                "status_distribution": status_distribution,
                "rent_distribution": rent_distribution,
                "lease_timeline": lease_timeline,
                "average_rent": avg_rent,
                "occupancy_rate": occupancy_rate,
                "total_units": total_count,
                "occupied_units": active_count,
            },
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to get analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/health")
async def health_check():
    """Health check endpoint."""
    try:
        health_status = {
            "status": "healthy",
            "database": "connected" if DB_PATH.exists() else "not_found",
            "timestamp": datetime.now().isoformat(),
            "service": "tenant-sync-api",
        }

        if DB_PATH.exists():
            try:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM tenants")
                tenant_count = cur.fetchone()[0]
                conn.close()
                health_status["tenant_count"] = tenant_count
            except Exception as e:
                health_status["database"] = "error"
                health_status["error"] = str(e)

        return health_status

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
