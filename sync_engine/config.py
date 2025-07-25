#!/usr/bin/env python3
"""
Sync Engine Configuration Module

Manages configuration settings for the auto-sync functionality including:
- Auto-sync enable/disable
- File type filters
- Processing preferences
- Directory paths
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Configuration file path
CONFIG_FILE = Path(__file__).parent / "sync_config.json"

# Default configuration
DEFAULT_CONFIG = {
    "auto_sync_enabled": False,
    "supported_extensions": [".pdf", ".txt", ".docx", ".md", ".csv"],
    "watch_directory": str(Path(__file__).parent / "watch"),
    "processing": {
        "max_file_size_mb": 50,
        "enable_sanitization": True,
        "enable_embedding": True,
        "cleanup_old_files": True,
        "days_to_keep": 7,
    },
    "notifications": {
        "enable_email": False,
        "enable_webhook": False,
        "webhook_url": "",
    },
    "logging": {"level": "INFO", "save_logs": True, "log_retention_days": 30},
}


def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return merge_configs(DEFAULT_CONFIG, config)
        else:
            # Create default config file
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        return False


def merge_configs(default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    """Merge user config with defaults"""
    result = default.copy()

    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result


def get_sync_config() -> Dict[str, Any]:
    """Get current sync configuration"""
    return load_config()


def update_sync_config(updates: Dict[str, Any]) -> bool:
    """Update sync configuration"""
    config = load_config()
    config = merge_configs(config, updates)
    return save_config(config)


def toggle_auto_sync(enabled: bool) -> bool:
    """Toggle auto-sync on/off"""
    return update_sync_config({"auto_sync_enabled": enabled})


def is_auto_sync_enabled() -> bool:
    """Check if auto-sync is enabled"""
    config = get_sync_config()
    return config.get("auto_sync_enabled", False)


def get_supported_extensions() -> List[str]:
    """Get list of supported file extensions"""
    config = get_sync_config()
    return config.get("supported_extensions", DEFAULT_CONFIG["supported_extensions"])


def get_watch_directory() -> Path:
    """Get the directory to watch for new files"""
    config = get_sync_config()
    watch_dir = Path(config.get("watch_directory", DEFAULT_CONFIG["watch_directory"]))
    watch_dir.mkdir(parents=True, exist_ok=True)
    return watch_dir


def get_processing_config() -> Dict[str, Any]:
    """Get processing configuration"""
    config = get_sync_config()
    return config.get("processing", DEFAULT_CONFIG["processing"])


def get_notification_config() -> Dict[str, Any]:
    """Get notification configuration"""
    config = get_sync_config()
    return config.get("notifications", DEFAULT_CONFIG["notifications"])


def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration"""
    config = get_sync_config()
    return config.get("logging", DEFAULT_CONFIG["logging"])


def reset_config() -> bool:
    """Reset configuration to defaults"""
    return save_config(DEFAULT_CONFIG)


def validate_config(config: Dict[str, Any]) -> List[str]:
    """Validate configuration and return list of errors"""
    errors = []

    # Check required fields
    required_fields = ["auto_sync_enabled", "supported_extensions", "watch_directory"]
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")

    # Validate file extensions
    if "supported_extensions" in config:
        extensions = config["supported_extensions"]
        if not isinstance(extensions, list):
            errors.append("supported_extensions must be a list")
        else:
            for ext in extensions:
                if not ext.startswith("."):
                    errors.append(f"File extension must start with '.': {ext}")

    # Validate watch directory
    if "watch_directory" in config:
        try:
            Path(config["watch_directory"])
        except Exception:
            errors.append("Invalid watch_directory path")

    # Validate processing config
    if "processing" in config:
        processing = config["processing"]
        if "max_file_size_mb" in processing:
            try:
                size = float(processing["max_file_size_mb"])
                if size <= 0:
                    errors.append("max_file_size_mb must be positive")
            except (ValueError, TypeError):
                errors.append("max_file_size_mb must be a number")

    return errors


if __name__ == "__main__":
    # Test configuration functions
    print("Testing sync engine configuration...")

    # Load config
    config = get_sync_config()
    print(f"Current config: {json.dumps(config, indent=2)}")

    # Test toggle
    print(f"Auto-sync enabled: {is_auto_sync_enabled()}")
    toggle_auto_sync(True)
    print(f"After toggle: {is_auto_sync_enabled()}")

    # Test validation
    errors = validate_config(config)
    if errors:
        print(f"Config validation errors: {errors}")
    else:
        print("Config validation passed")

    # Reset to defaults
    reset_config()
    print("Config reset to defaults")
