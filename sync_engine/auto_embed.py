#!/usr/bin/env python3
"""
Auto-Embed Processing Module

This module handles the automatic processing of new files:
1. Sanitization (PII redaction, text normalization)
2. Embedding into the RAG vector store
3. Metadata tracking and logging
"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Import existing modules (adjust paths as needed)
try:
    from rag.embed import embed_document
    from rag.sanitize import sanitize_document
except ImportError:
    # Fallback for development/testing
    def embed_document(path: str) -> bool:
        logging.info(f"Mock embedding: {path}")
        return True

    def sanitize_document(path: str) -> str:
        logging.info(f"Mock sanitization: {path}")
        return path


logger = logging.getLogger(__name__)

# Processing directories
PROCESSING_DIR = Path(__file__).parent / "processing"
PROCESSED_DIR = Path(__file__).parent / "processed"
FAILED_DIR = Path(__file__).parent / "failed"
LOGS_DIR = Path(__file__).parent / "logs"

# Create directories
for dir_path in [PROCESSING_DIR, PROCESSED_DIR, FAILED_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def process_file(path: Path) -> Dict[str, Any]:
    """
    Process a file through the complete pipeline:
    1. Sanitize (redact PII, normalize text)
    2. Embed into vector store
    3. Track metadata and results

    Args:
        path: Path to the file to process

    Returns:
        Dict containing processing results and metadata
    """
    start_time = datetime.now()
    original_name = path.name

    # Create processing record
    processing_record = {
        "original_file": str(path),
        "original_name": original_name,
        "start_time": start_time.isoformat(),
        "status": "processing",
        "steps": [],
    }

    try:
        logger.info(f"Starting processing: {original_name}")

        # Step 1: Copy to processing directory
        processing_path = (
            PROCESSING_DIR
            / f"processing_{start_time.strftime('%Y%m%d_%H%M%S')}_{original_name}"
        )
        shutil.copy2(path, processing_path)
        processing_record["steps"].append(
            {
                "step": "copy_to_processing",
                "status": "success",
                "path": str(processing_path),
            }
        )

        # Step 2: Sanitize the document
        logger.info(f"Sanitizing: {original_name}")
        sanitized_path = sanitize_document(str(processing_path))
        processing_record["steps"].append(
            {
                "step": "sanitize",
                "status": "success",
                "original_path": str(processing_path),
                "sanitized_path": sanitized_path,
            }
        )

        # Step 3: Embed into vector store
        logger.info(f"Embedding: {original_name}")
        embed_success = embed_document(sanitized_path)

        if embed_success:
            processing_record["steps"].append(
                {"step": "embed", "status": "success", "path": sanitized_path}
            )

            # Move to processed directory
            processed_path = (
                PROCESSED_DIR
                / f"processed_{start_time.strftime('%Y%m%d_%H%M%S')}_{original_name}"
            )
            shutil.move(processing_path, processed_path)

            processing_record["status"] = "completed"
            processing_record["processed_path"] = str(processed_path)
            processing_record["end_time"] = datetime.now().isoformat()

            logger.info(f"Successfully processed: {original_name}")

        else:
            raise Exception("Embedding failed")

    except Exception as e:
        logger.error(f"Error processing {original_name}: {e}")

        # Move to failed directory
        failed_path = (
            FAILED_DIR
            / f"failed_{start_time.strftime('%Y%m%d_%H%M%S')}_{original_name}"
        )
        if processing_path.exists():
            shutil.move(processing_path, failed_path)

        processing_record["status"] = "failed"
        processing_record["error"] = str(e)
        processing_record["end_time"] = datetime.now().isoformat()
        processing_record["failed_path"] = str(failed_path)

        # Add failed step
        processing_record["steps"].append(
            {"step": "embed", "status": "failed", "error": str(e)}
        )

    # Save processing log
    save_processing_log(processing_record)

    return processing_record


def save_processing_log(record: Dict[str, Any]):
    """Save processing record to log file"""
    log_file = LOGS_DIR / f"processing_log_{datetime.now().strftime('%Y%m%d')}.jsonl"

    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        logger.error(f"Failed to save processing log: {e}")


def get_processing_stats() -> Dict[str, Any]:
    """Get processing statistics"""
    try:
        # Count files in each directory
        stats = {
            "processing": len(list(PROCESSING_DIR.glob("*"))),
            "processed": len(list(PROCESSED_DIR.glob("*"))),
            "failed": len(list(FAILED_DIR.glob("*"))),
            "logs": len(list(LOGS_DIR.glob("*.jsonl"))),
        }

        # Get recent processing history
        today_log = (
            LOGS_DIR / f"processing_log_{datetime.now().strftime('%Y%m%d')}.jsonl"
        )
        if today_log.exists():
            with open(today_log) as f:
                lines = f.readlines()
                stats["today_processed"] = len(
                    [l for l in lines if '"status": "completed"' in l]
                )
                stats["today_failed"] = len(
                    [l for l in lines if '"status": "failed"' in l]
                )
        else:
            stats["today_processed"] = 0
            stats["today_failed"] = 0

        return stats

    except Exception as e:
        logger.error(f"Failed to get processing stats: {e}")
        return {"error": str(e)}


def cleanup_old_files(days_to_keep: int = 7):
    """Clean up old processed and failed files"""
    cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)

    for directory in [PROCESSED_DIR, FAILED_DIR]:
        for file_path in directory.glob("*"):
            if file_path.stat().st_mtime < cutoff_date:
                try:
                    file_path.unlink()
                    logger.info(f"Cleaned up old file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to clean up {file_path}: {e}")


def process_batch(file_paths: list) -> list:
    """Process multiple files in batch"""
    results = []

    for file_path in file_paths:
        path = Path(file_path)
        if path.exists():
            result = process_file(path)
            results.append(result)
        else:
            logger.warning(f"File not found: {file_path}")
            results.append(
                {
                    "original_file": str(file_path),
                    "status": "failed",
                    "error": "File not found",
                }
            )

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: auto_embed.py <path-to-file> [path-to-file2 ...]")
        sys.exit(1)

    # Process each file provided as argument
    for file_path in sys.argv[1:]:
        path = Path(file_path)
        if path.exists():
            result = process_file(path)
            print(f"Processed {path.name}: {result['status']}")
        else:
            print(f"File not found: {file_path}")
