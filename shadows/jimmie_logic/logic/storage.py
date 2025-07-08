"""
Storage Helper - JSON read/write operations for jimmie_logic
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class StorageManager:
    """Manages JSON file storage for jimmie_logic data."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def _get_file_path(self, filename: str) -> Path:
        """Get the full path for a data file."""
        return self.data_dir / f"{filename}.json"

    def read_json(self, filename: str) -> List[Dict]:
        """Read data from a JSON file."""
        file_path = self._get_file_path(filename)

        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {file_path}: {e}")
            return []

    def write_json(self, filename: str, data: List[Dict]) -> bool:
        """Write data to a JSON file."""
        file_path = self._get_file_path(filename)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (json.JSONEncodeError, IOError) as e:
            print(f"Error writing {file_path}: {e}")
            return False

    def append_json(self, filename: str, item: Dict) -> bool:
        """Append a single item to a JSON file."""
        data = self.read_json(filename)
        data.append(item)
        return self.write_json(filename, data)

    def update_json(self, filename: str, item_id: str, updates: Dict) -> bool:
        """Update a specific item in a JSON file."""
        data = self.read_json(filename)

        for i, item in enumerate(data):
            if item.get("id") == item_id:
                data[i].update(updates)
                data[i]["updated_at"] = datetime.now().isoformat()
                return self.write_json(filename, data)

        return False

    def delete_json(self, filename: str, item_id: str) -> bool:
        """Delete a specific item from a JSON file."""
        data = self.read_json(filename)

        for i, item in enumerate(data):
            if item.get("id") == item_id:
                data.pop(i)
                return self.write_json(filename, data)

        return False

    def find_json(self, filename: str, **filters) -> List[Dict]:
        """Find items in a JSON file that match the given filters."""
        data = self.read_json(filename)

        if not filters:
            return data

        filtered_data = []
        for item in data:
            matches = True
            for key, value in filters.items():
                if key not in item or item[key] != value:
                    matches = False
                    break
            if matches:
                filtered_data.append(item)

        return filtered_data

    def get_json_stats(self, filename: str) -> Dict[str, Any]:
        """Get statistics for a JSON file."""
        data = self.read_json(filename)

        if not data:
            return {"filename": filename, "count": 0, "message": "No data found"}

        # Get unique values for common fields
        stats = {
            "filename": filename,
            "count": len(data),
            "categories": {},
            "tags": {},
            "authors": {},
            "recent_updates": 0,
        }

        # Count categories, tags, authors
        for item in data:
            # Categories
            category = item.get("category", "unknown")
            stats["categories"][category] = stats["categories"].get(category, 0) + 1

            # Tags
            tags = item.get("tags", [])
            for tag in tags:
                stats["tags"][tag] = stats["tags"].get(tag, 0) + 1

            # Authors
            author = item.get("author", "unknown")
            stats["authors"][author] = stats["authors"].get(author, 0) + 1

            # Recent updates (last 7 days)
            updated_at = item.get("updated_at")
            if updated_at:
                try:
                    update_date = datetime.fromisoformat(updated_at)
                    if (datetime.now() - update_date).days <= 7:
                        stats["recent_updates"] += 1
                except BaseException:
                    pass

        return stats

    def backup_data(self, backup_dir: str = "backups") -> bool:
        """Create a backup of all data files."""
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"jimmie_logic_backup_{timestamp}"
        backup_dir_path = backup_path / backup_name
        backup_dir_path.mkdir(exist_ok=True)

        try:
            # Copy all JSON files
            for json_file in self.data_dir.glob("*.json"):
                backup_file = backup_dir_path / json_file.name
                with open(json_file, "r") as src, open(backup_file, "w") as dst:
                    dst.write(src.read())

            # Create backup metadata
            metadata = {
                "backup_timestamp": datetime.now().isoformat(),
                "files_backed_up": [f.name for f in self.data_dir.glob("*.json")],
                "total_files": len(list(self.data_dir.glob("*.json"))),
            }

            with open(backup_dir_path / "backup_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)

            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def restore_data(self, backup_dir: str) -> bool:
        """Restore data from a backup."""
        backup_path = Path(backup_dir)

        if not backup_path.exists():
            print(f"Backup directory {backup_dir} does not exist")
            return False

        try:
            # Find the most recent backup
            backup_dirs = [
                d
                for d in backup_path.iterdir()
                if d.is_dir() and d.name.startswith("jimmie_logic_backup_")
            ]
            if not backup_dirs:
                print("No backup directories found")
                return False

            latest_backup = max(backup_dirs, key=lambda x: x.name)

            # Restore JSON files
            for json_file in latest_backup.glob("*.json"):
                if json_file.name != "backup_metadata.json":
                    restore_file = self.data_dir / json_file.name
                    with open(json_file, "r") as src, open(restore_file, "w") as dst:
                        dst.write(src.read())

            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False


# Global storage manager instance
storage = StorageManager()
