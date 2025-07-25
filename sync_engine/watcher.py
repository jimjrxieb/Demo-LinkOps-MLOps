#!/usr/bin/env python3
"""
File Watcher for Auto-Embedding Documents

This module watches a designated directory for new files and automatically
processes them through the sanitization and embedding pipeline.
"""

import logging
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from sync_engine.auto_embed import process_file
from sync_engine.config import get_sync_config

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Folder to watch for new docs
WATCH_DIR = Path(__file__).parent / "watch"
WATCH_DIR.mkdir(parents=True, exist_ok=True)

# Supported file extensions
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".md", ".csv"}


class NewFileHandler(FileSystemEventHandler):
    """Handles file system events for new file detection"""

    def __init__(self):
        self.processing_files = set()
        self.sync_config = get_sync_config()

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        path = Path(event.src_path)

        # Check if auto-sync is enabled
        if not self.sync_config.get("auto_sync_enabled", False):
            logger.info(f"Auto-sync disabled, skipping: {path.name}")
            return

        # Check file extension
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            logger.info(f"Unsupported file type, skipping: {path.name}")
            return

        # Prevent duplicate processing
        if path in self.processing_files:
            logger.info(f"File already being processed, skipping: {path.name}")
            return

        logger.info(f"[watcher] New file detected: {path}")

        # Add to processing set
        self.processing_files.add(path)

        try:
            # Wait a moment for file to be fully written
            time.sleep(1)

            # Process the file
            result = process_file(path)
            logger.info(f"[watcher] Successfully embedded: {path.name} -> {result}")

        except Exception as e:
            logger.error(f"[watcher] ERROR embedding {path.name}: {e}")
        finally:
            # Remove from processing set
            self.processing_files.discard(path)

    def on_moved(self, event):
        """Handle file move events (rename)"""
        if not event.is_directory:
            path = Path(event.dest_path)
            logger.info(f"[watcher] File moved/renamed: {path}")
            # Treat as new file
            self.on_created(event)

    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory:
            path = Path(event.src_path)
            logger.debug(f"[watcher] File modified: {path}")
            # Could implement incremental updates here


def start_watcher():
    """Start the file watcher service"""
    observer = Observer()
    event_handler = NewFileHandler()

    # Schedule the watcher
    observer.schedule(event_handler, str(WATCH_DIR), recursive=False)

    logger.info(f"[watcher] Starting file watcher for: {WATCH_DIR}")
    logger.info(f"[watcher] Supported extensions: {SUPPORTED_EXTENSIONS}")
    logger.info(
        f"[watcher] Auto-sync enabled: {get_sync_config().get('auto_sync_enabled', False)}"
    )

    observer.start()
    return observer


def stop_watcher(observer):
    """Stop the file watcher service"""
    if observer:
        observer.stop()
        observer.join()
        logger.info("[watcher] File watcher stopped")


def main():
    """Main function to run the watcher as a standalone service"""
    try:
        observer = start_watcher()

        # Keep the watcher running
        while True:
            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("[watcher] Received interrupt signal")
    except Exception as e:
        logger.error(f"[watcher] Unexpected error: {e}")
    finally:
        stop_watcher(observer)


if __name__ == "__main__":
    main()
