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
Version Control for Whis Enhancement System.
Handles versioning, backups, and change tracking for runes and orbs.
"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Base paths
BASE_PATH = Path(__file__).parent.parent.parent / "mlops_platform" / "data"
VERSIONS_DIR = BASE_PATH / "versions"
BACKUP_DIR = BASE_PATH / "backups"


def ensure_directories():
    """Ensure version and backup directories exist."""
    VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def save_version(item_type: str, item_id: str, item_data: Dict[str, Any]) -> str:
    """
    Save a version of an item (rune or orb).

    Args:
        item_type: Type of item ('runes' or 'orbs')
        item_id: Unique identifier for the item
        item_data: The item data to save

    Returns:
        Version identifier
    """
    ensure_directories()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_id = f"{item_type}_{item_id}_{timestamp}"

    try:
        # Create version file
        version_file = VERSIONS_DIR / f"{version_id}.json"

        version_data = {
            "version_id": version_id,
            "item_type": item_type,
            "item_id": item_id,
            "timestamp": datetime.now().isoformat(),
            "data": item_data,
            "metadata": {
                "created_by": "whis_enhance_loopback",
                "enhancement_type": "loopback_refinement",
            },
        }

        with open(version_file, "w", encoding="utf-8") as f:
            json.dump(version_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved version {version_id} for {item_type} {item_id}")
        return version_id

    except Exception as e:
        logger.error(f"Error saving version {version_id}: {str(e)}")
        raise


def get_version_history(item_type: str, item_id: str) -> List[Dict[str, Any]]:
    """
    Get version history for a specific item.

    Args:
        item_type: Type of item ('runes' or 'orbs')
        item_id: Unique identifier for the item

    Returns:
        List of version data sorted by timestamp (newest first)
    """
    ensure_directories()

    versions = []

    try:
        # Find all version files for this item
        pattern = f"{item_type}_{item_id}_*.json"
        version_files = list(VERSIONS_DIR.glob(pattern))

        for version_file in version_files:
            with open(version_file, "r", encoding="utf-8") as f:
                version_data = json.load(f)
                versions.append(version_data)

        # Sort by timestamp (newest first)
        versions.sort(key=lambda x: x["timestamp"], reverse=True)

        logger.info(f"Found {len(versions)} versions for {item_type} {item_id}")

    except Exception as e:
        logger.error(f"Error getting version history: {str(e)}")

    return versions


def restore_version(version_id: str) -> Optional[Dict[str, Any]]:
    """
    Restore a specific version.

    Args:
        version_id: The version identifier to restore

    Returns:
        The restored item data or None if not found
    """
    ensure_directories()

    try:
        version_file = VERSIONS_DIR / f"{version_id}.json"

        if not version_file.exists():
            logger.warning(f"Version file not found: {version_file}")
            return None

        with open(version_file, "r", encoding="utf-8") as f:
            version_data = json.load(f)

        logger.info(f"Restored version {version_id}")
        return version_data["data"]

    except Exception as e:
        logger.error(f"Error restoring version {version_id}: {str(e)}")
        return None


def create_backup(file_path: Path) -> str:
    """
    Create a backup of a file.

    Args:
        file_path: Path to the file to backup

    Returns:
        Backup file path
    """
    ensure_directories()

    if not file_path.exists():
        logger.warning(f"File not found for backup: {file_path}")
        return ""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    backup_path = BACKUP_DIR / backup_name

    try:
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return str(backup_path)

    except Exception as e:
        logger.error(f"Error creating backup: {str(e)}")
        return ""


def list_backups(file_pattern: str = "*") -> List[Dict[str, Any]]:
    """
    List available backups.

    Args:
        file_pattern: Pattern to filter backup files

    Returns:
        List of backup information
    """
    ensure_directories()

    backups = []

    try:
        backup_files = list(BACKUP_DIR.glob(f"{file_pattern}"))

        for backup_file in backup_files:
            stat = backup_file.stat()
            backups.append(
                {
                    "filename": backup_file.name,
                    "path": str(backup_file),
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )

        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x["created"], reverse=True)

    except Exception as e:
        logger.error(f"Error listing backups: {str(e)}")

    return backups


def cleanup_old_versions(max_versions: int = 10) -> int:
    """
    Clean up old versions, keeping only the most recent ones.

    Args:
        max_versions: Maximum number of versions to keep per item

    Returns:
        Number of versions cleaned up
    """
    ensure_directories()

    cleaned_count = 0

    try:
        # Group versions by item
        item_versions = {}

        for version_file in VERSIONS_DIR.glob("*.json"):
            with open(version_file, "r", encoding="utf-8") as f:
                version_data = json.load(f)

            item_key = f"{version_data['item_type']}_{version_data['item_id']}"
            if item_key not in item_versions:
                item_versions[item_key] = []
            item_versions[item_key].append((version_file, version_data))

        # Clean up old versions for each item
        for item_key, versions in item_versions.items():
            # Sort by timestamp (newest first)
            versions.sort(key=lambda x: x[1]["timestamp"], reverse=True)

            # Remove old versions
            for version_file, _ in versions[max_versions:]:
                version_file.unlink()
                cleaned_count += 1
                logger.info(f"Cleaned up old version: {version_file.name}")

        logger.info(f"Cleaned up {cleaned_count} old versions")

    except Exception as e:
        logger.error(f"Error cleaning up old versions: {str(e)}")

    return cleaned_count


def get_version_statistics() -> Dict[str, Any]:
    """
    Get statistics about version control system.

    Returns:
        Dictionary with version statistics
    """
    ensure_directories()

    stats = {
        "total_versions": 0,
        "total_backups": 0,
        "versions_by_type": {},
        "oldest_version": None,
        "newest_version": None,
        "storage_size": 0,
    }

    try:
        # Count versions
        version_files = list(VERSIONS_DIR.glob("*.json"))
        stats["total_versions"] = len(version_files)

        # Count backups
        backup_files = list(BACKUP_DIR.glob("*"))
        stats["total_backups"] = len(backup_files)

        # Group versions by type
        for version_file in version_files:
            with open(version_file, "r", encoding="utf-8") as f:
                version_data = json.load(f)
                item_type = version_data["item_type"]
                stats["versions_by_type"][item_type] = (
                    stats["versions_by_type"].get(item_type, 0) + 1
                )

        # Calculate storage size
        for file_path in VERSIONS_DIR.rglob("*"):
            if file_path.is_file():
                stats["storage_size"] += file_path.stat().st_size

        # Find oldest and newest versions
        if version_files:
            timestamps = []
            for version_file in version_files:
                with open(version_file, "r", encoding="utf-8") as f:
                    version_data = json.load(f)
                    timestamps.append(version_data["timestamp"])

            if timestamps:
                stats["oldest_version"] = min(timestamps)
                stats["newest_version"] = max(timestamps)

    except Exception as e:
        logger.error(f"Error getting version statistics: {str(e)}")

    return stats
