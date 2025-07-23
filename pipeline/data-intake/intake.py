#!/usr/bin/env python3
"""
Data Intake Component
====================

Handles file uploads and initial data processing.
"""

import hashlib
import logging
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class DataIntake:
    """
    Data intake component for handling file uploads and initial processing.
    """

    def __init__(self, upload_dir: str = "/tmp/uploads"):
        """
        Initialize the data intake component.

        Args:
            upload_dir: Directory to store uploaded files
        """
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        logger.info(
            f"📥 Data intake initialized with upload directory: {self.upload_dir}"
        )

    def save_upload(
        self, file_path: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save uploaded file to the intake directory.

        Args:
            file_path: Path to the uploaded file
            metadata: Optional metadata about the upload

        Returns:
            Path to the saved file

        Raises:
            FileNotFoundError: If the source file doesn't exist
            ValueError: If the file is invalid
        """
        source_path = Path(file_path)

        # Validate source file
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")

        if not source_path.is_file():
            raise ValueError(f"Source path is not a file: {file_path}")

        # Generate unique filename
        timestamp = int(time.time())
        file_hash = self._calculate_file_hash(source_path)
        file_extension = source_path.suffix
        filename = f"upload_{timestamp}_{file_hash[:8]}{file_extension}"

        # Create destination path
        dest_path = self.upload_dir / filename

        # Copy file
        try:
            shutil.copy2(source_path, dest_path)
            logger.info(f"📁 File uploaded: {source_path} -> {dest_path}")

            # Save metadata if provided
            if metadata:
                self._save_metadata(dest_path, metadata)

            return str(dest_path)

        except Exception as e:
            logger.error(f"❌ Failed to save upload: {e}")
            raise

    def save_upload_with_validation(
        self,
        file_path: str,
        allowed_extensions: Optional[list] = None,
        max_size_mb: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Save uploaded file with validation.

        Args:
            file_path: Path to the uploaded file
            allowed_extensions: List of allowed file extensions
            max_size_mb: Maximum file size in MB
            metadata: Optional metadata about the upload

        Returns:
            Path to the saved file

        Raises:
            ValueError: If file validation fails
        """
        source_path = Path(file_path)

        # Validate file extension
        if allowed_extensions:
            if source_path.suffix.lower() not in [
                ext.lower() for ext in allowed_extensions
            ]:
                raise ValueError(f"File extension not allowed: {source_path.suffix}")

        # Validate file size
        if max_size_mb:
            file_size_mb = source_path.stat().st_size / (1024 * 1024)
            if file_size_mb > max_size_mb:
                raise ValueError(
                    f"File too large: {file_size_mb:.2f}MB > {max_size_mb}MB"
                )

        # Save the file
        return self.save_upload(file_path, metadata)

    def get_upload_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get information about an uploaded file.

        Args:
            file_path: Path to the uploaded file

        Returns:
            Dictionary with file information
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        stat = path.stat()

        info = {
            "filename": path.name,
            "file_path": str(path),
            "file_size": stat.st_size,
            "file_size_mb": stat.st_size / (1024 * 1024),
            "file_extension": path.suffix,
            "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_hash": self._calculate_file_hash(path),
        }

        # Load metadata if available
        metadata_path = path.with_suffix(path.suffix + ".metadata.json")
        if metadata_path.exists():
            try:
                import json

                with open(metadata_path, "r") as f:
                    info["metadata"] = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load metadata: {e}")

        return info

    def list_uploads(self, limit: Optional[int] = None) -> list:
        """
        List uploaded files.

        Args:
            limit: Maximum number of files to return

        Returns:
            List of uploaded file information
        """
        files = []

        for file_path in self.upload_dir.iterdir():
            if file_path.is_file() and not file_path.name.endswith(".metadata.json"):
                try:
                    file_info = self.get_upload_info(str(file_path))
                    files.append(file_info)
                except Exception as e:
                    logger.warning(f"Failed to get info for {file_path}: {e}")

        # Sort by creation time (newest first)
        files.sort(key=lambda x: x["created_time"], reverse=True)

        # Apply limit
        if limit:
            files = files[:limit]

        return files

    def cleanup_old_uploads(self, days_old: int = 7) -> int:
        """
        Clean up old uploaded files.

        Args:
            days_old: Remove files older than this many days

        Returns:
            Number of files removed
        """
        import time

        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        removed_count = 0

        for file_path in self.upload_dir.iterdir():
            if file_path.is_file():
                if file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()

                        # Also remove metadata file if it exists
                        metadata_path = file_path.with_suffix(
                            file_path.suffix + ".metadata.json"
                        )
                        if metadata_path.exists():
                            metadata_path.unlink()

                        removed_count += 1
                        logger.info(f"🗑️ Removed old file: {file_path}")

                    except Exception as e:
                        logger.error(f"Failed to remove {file_path}: {e}")

        logger.info(f"🧹 Cleanup completed: {removed_count} files removed")
        return removed_count

    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate SHA-256 hash of a file.

        Args:
            file_path: Path to the file

        Returns:
            SHA-256 hash string
        """
        hash_sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)

        return hash_sha256.hexdigest()

    def _save_metadata(self, file_path: Path, metadata: Dict[str, Any]):
        """
        Save metadata for an uploaded file.

        Args:
            file_path: Path to the uploaded file
            metadata: Metadata to save
        """
        metadata_path = file_path.with_suffix(file_path.suffix + ".metadata.json")

        # Add timestamp to metadata
        metadata["upload_timestamp"] = datetime.now().isoformat()
        metadata["original_filename"] = file_path.name

        try:
            import json

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            logger.debug(f"📝 Metadata saved: {metadata_path}")

        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")


def save_upload(file_path: str) -> str:
    """
    Convenience function to save an uploaded file.

    Args:
        file_path: Path to the uploaded file

    Returns:
        Path to the saved file
    """
    intake = DataIntake()
    return intake.save_upload(file_path)


if __name__ == "__main__":
    # Example usage
    print("📥 Data Intake Demo")
    print("=" * 30)

    # Create example file
    example_file = "/tmp/test_upload.csv"
    with open(example_file, "w") as f:
        f.write("name,email,value\n")
        f.write("John,john@example.com,100\n")
        f.write("Jane,jane@example.com,200\n")

    # Test data intake
    intake = DataIntake()

    # Save upload
    saved_path = intake.save_upload(
        example_file, metadata={"source": "demo", "user": "test"}
    )
    print(f"✅ File saved: {saved_path}")

    # Get upload info
    info = intake.get_upload_info(saved_path)
    print(f"📊 File info: {info['filename']} ({info['file_size_mb']:.2f}MB)")

    # List uploads
    uploads = intake.list_uploads(limit=5)
    print(f"📋 Found {len(uploads)} uploads")

    print("🎉 Data intake demo completed!")
