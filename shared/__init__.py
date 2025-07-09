"""
LinkOps MLOps Platform - Shared Components

This package provides shared utilities, schemas, and components used across
all LinkOps microservices including Whis, Audit, Shadows, and Frontend.

Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "LinkOps Team"
__email__ = "team@linkops.com"

from .config.logging import get_logger, setup_logging
# Import commonly used components for easy access
from .config.settings import Settings, get_settings
from .constants.tags import AUDIT_SEVERITIES, ORB_CATEGORIES, RUNE_TYPES
from .models.schemas.base import BaseModel
from .models.schemas.orb import Orb, OrbCreate, OrbUpdate
from .models.schemas.repo_audit import AuditScore, RepoAuditResult
from .models.schemas.rune import Rune, RuneCreate, RuneUpdate
from .utils.file_io import read_json, read_yaml, write_json, write_yaml
from .utils.sanitizer import sanitize_filename, sanitize_text
from .utils.yaml_tools import dump_yaml, load_yaml, validate_yaml

__all__ = [
    # Config
    "Settings",
    "get_settings",
    "setup_logging",
    "get_logger",
    # Models
    "BaseModel",
    "Orb",
    "OrbCreate",
    "OrbUpdate",
    "Rune",
    "RuneCreate",
    "RuneUpdate",
    "RepoAuditResult",
    "AuditScore",
    # Utils
    "load_yaml",
    "dump_yaml",
    "validate_yaml",
    "read_json",
    "write_json",
    "read_yaml",
    "write_yaml",
    "sanitize_text",
    "sanitize_filename",
    # Constants
    "ORB_CATEGORIES",
    "RUNE_TYPES",
    "AUDIT_SEVERITIES",
]
