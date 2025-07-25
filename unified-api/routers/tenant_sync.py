#!/usr/bin/env python3
"""
Tenant CSV Sync Engine
======================

Secure tenant data synchronization from CSV files to SQLite database.
Watches for new CSV files and automatically processes them.
"""

import csv
import hashlib
import logging
import sqlite3
import threading
import time
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
WATCH_DIR = Path("db/watch/tenants")
DB_PATH = Path("db/sqlite/tenants.db")
LOG_PATH = Path("db/logs/sync.log")
POLL_INTERVAL = 5  # seconds
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create necessary directories
WATCH_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


class TenantSyncEngine:
    """Secure tenant data synchronization engine."""

    def __init__(self):
        self.processed_files = set()
        self.file_hashes = {}
        self.running = False
        self.lock = threading.Lock()

        # Initialize database
        self.init_db()

        # Load processed files from disk
        self.load_processed_files()

        logger.info("🔄 Tenant sync engine initialized")
        logger.info(f"   Watch directory: {WATCH_DIR}")
        logger.info(f"   Database: {DB_PATH}")
        logger.info(f"   Poll interval: {POLL_INTERVAL}s")

    def init_db(self):
        """Initialize SQLite database with tenant table."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            # Create tenants table
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tenants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_name TEXT NOT NULL,
                    unit TEXT,
                    status TEXT,
                    lease_start TEXT,
                    lease_end TEXT,
                    rent_amount REAL,
                    email TEXT,
                    phone TEXT,
                    source_file TEXT NOT NULL,
                    file_hash TEXT,
                    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create index for better performance
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tenant_name ON tenants(tenant_name)
            """
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_unit ON tenants(unit)
            """
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_lease_end ON tenants(lease_end)
            """
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_source_file ON tenants(source_file)
            """
            )

            # Create sync log table
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS sync_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    file_hash TEXT,
                    status TEXT NOT NULL,
                    records_processed INTEGER DEFAULT 0,
                    error_message TEXT,
                    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()
            conn.close()
            logger.info("✅ Database initialized successfully")

        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise

    def load_processed_files(self):
        """Load list of processed files from database."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute("SELECT DISTINCT source_file FROM tenants")
            files = cur.fetchall()

            with self.lock:
                self.processed_files = {file[0] for file in files}

            conn.close()
            logger.info(f"📋 Loaded {len(self.processed_files)} processed files")

        except Exception as e:
            logger.error(f"❌ Failed to load processed files: {e}")

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file content."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"❌ Failed to calculate file hash: {e}")
            return ""

    def validate_csv_file(self, file_path: Path) -> bool:
        """Validate CSV file format and content."""
        try:
            # Check file size
            if file_path.stat().st_size > MAX_FILE_SIZE:
                logger.warning(f"⚠️ File too large: {file_path.name}")
                return False

            # Check file extension
            if file_path.suffix.lower() != ".csv":
                logger.warning(f"⚠️ Not a CSV file: {file_path.name}")
                return False

            # Validate CSV structure
            with open(file_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)

                # Check required columns
                required_columns = {"tenant_name"}
                if not required_columns.issubset(set(reader.fieldnames or [])):
                    logger.warning(f"⚠️ Missing required columns in {file_path.name}")
                    return False

                # Check if file has data
                row_count = 0
                for _row in reader:
                    row_count += 1
                    if row_count > 1:  # Just check first few rows
                        break

                if row_count == 0:
                    logger.warning(f"⚠️ Empty CSV file: {file_path.name}")
                    return False

            return True

        except Exception as e:
            logger.error(f"❌ CSV validation failed for {file_path.name}: {e}")
            return False

    def parse_csv_data(self, file_path: Path) -> list[dict]:
        """Parse CSV file and return structured data."""
        try:
            data = []
            with open(file_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
                    try:
                        # Clean and validate data
                        tenant_data = {
                            "tenant_name": row.get("tenant_name", "").strip(),
                            "unit": row.get("unit", "").strip(),
                            "status": row.get("status", "active").strip().lower(),
                            "lease_start": row.get("lease_start", "").strip(),
                            "lease_end": row.get("lease_end", "").strip(),
                            "rent_amount": self.parse_rent_amount(
                                row.get("rent_amount", "")
                            ),
                            "email": row.get("email", "").strip(),
                            "phone": row.get("phone", "").strip(),
                            "source_file": file_path.name,
                            "file_hash": self.calculate_file_hash(file_path),
                        }

                        # Validate required fields
                        if not tenant_data["tenant_name"]:
                            logger.warning(f"⚠️ Row {row_num}: Missing tenant name")
                            continue

                        data.append(tenant_data)

                    except Exception as e:
                        logger.warning(f"⚠️ Row {row_num}: Parse error - {e}")
                        continue

            return data

        except Exception as e:
            logger.error(f"❌ CSV parsing failed for {file_path.name}: {e}")
            return []

    def parse_rent_amount(self, rent_str: str) -> Optional[float]:
        """Parse rent amount string to float."""
        try:
            if not rent_str:
                return None

            # Remove currency symbols and commas
            cleaned = rent_str.replace("$", "").replace(",", "").strip()
            return float(cleaned) if cleaned else None

        except ValueError:
            return None

    def sync_file(self, file_path: Path) -> bool:
        """Sync a single CSV file to the database."""
        logger.info(f"🔄 Processing: {file_path.name}")

        try:
            # Validate file
            if not self.validate_csv_file(file_path):
                return False

            # Parse CSV data
            tenant_data = self.parse_csv_data(file_path)
            if not tenant_data:
                logger.warning(f"⚠️ No valid data found in {file_path.name}")
                return False

            # Insert data into database
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            # Prepare data for insertion
            rows = [
                (
                    data["tenant_name"],
                    data["unit"],
                    data["status"],
                    data["lease_start"],
                    data["lease_end"],
                    data["rent_amount"],
                    data["email"],
                    data["phone"],
                    data["source_file"],
                    data["file_hash"],
                )
                for data in tenant_data
            ]

            # Insert data
            cur.executemany(
                """
                INSERT INTO tenants (
                    tenant_name, unit, status, lease_start, lease_end,
                    rent_amount, email, phone, source_file, file_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                rows,
            )

            # Log sync operation
            cur.execute(
                """
                INSERT INTO sync_log (
                    file_name, file_hash, status, records_processed
                ) VALUES (?, ?, ?, ?)
            """,
                (
                    file_path.name,
                    tenant_data[0]["file_hash"],
                    "success",
                    len(tenant_data),
                ),
            )

            conn.commit()
            conn.close()

            # Update processed files set
            with self.lock:
                self.processed_files.add(file_path.name)

            logger.info(f"✅ Synced {len(tenant_data)} records from {file_path.name}")
            return True

        except Exception as e:
            logger.error(f"❌ Sync failed for {file_path.name}: {e}")

            # Log error
            try:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO sync_log (
                        file_name, file_hash, status, error_message
                    ) VALUES (?, ?, ?, ?)
                """,
                    (file_path.name, "", "error", str(e)),
                )
                conn.commit()
                conn.close()
            except:
                pass

            return False

    def watch_loop(self):
        """Main watch loop for new CSV files."""
        logger.info("👀 Starting file watch loop...")

        while self.running:
            try:
                # Scan for new CSV files
                for file_path in WATCH_DIR.glob("*.csv"):
                    with self.lock:
                        if file_path.name not in self.processed_files:
                            # Process new file
                            success = self.sync_file(file_path)
                            if success:
                                logger.info(
                                    f"✅ Successfully processed {file_path.name}"
                                )
                            else:
                                logger.error(f"❌ Failed to process {file_path.name}")

                # Sleep before next scan
                time.sleep(POLL_INTERVAL)

            except Exception as e:
                logger.error(f"❌ Watch loop error: {e}")
                time.sleep(POLL_INTERVAL)

    def start(self):
        """Start the sync engine."""
        self.running = True
        logger.info("🚀 Starting tenant sync engine...")

        # Start watch loop in a separate thread
        watch_thread = threading.Thread(target=self.watch_loop, daemon=True)
        watch_thread.start()

        logger.info("✅ Tenant sync engine started")

    def stop(self):
        """Stop the sync engine."""
        self.running = False
        logger.info("🛑 Tenant sync engine stopped")

    def get_stats(self) -> dict:
        """Get sync engine statistics."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            # Get tenant count
            cur.execute("SELECT COUNT(*) FROM tenants")
            tenant_count = cur.fetchone()[0]

            # Get file count
            cur.execute("SELECT COUNT(DISTINCT source_file) FROM tenants")
            file_count = cur.fetchone()[0]

            # Get recent syncs
            cur.execute(
                """
                SELECT file_name, status, records_processed, synced_at
                FROM sync_log
                ORDER BY synced_at DESC
                LIMIT 10
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

            conn.close()

            return {
                "tenant_count": tenant_count,
                "file_count": file_count,
                "recent_syncs": recent_syncs,
                "watch_directory": str(WATCH_DIR),
                "database_path": str(DB_PATH),
                "running": self.running,
            }

        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}


def main():
    """Main function to run the sync engine."""
    try:
        # Create and start sync engine
        sync_engine = TenantSyncEngine()
        sync_engine.start()

        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Received interrupt signal")
            sync_engine.stop()

    except Exception as e:
        logger.error(f"❌ Sync engine failed: {e}")
        raise


if __name__ == "__main__":
    main()
