"""
LinkOps Shared Logging Configuration

Centralized logging setup for all LinkOps microservices with structured logging,
file rotation, and Prometheus metrics integration.
"""

import logging
import logging.handlers
import sys
import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from .settings import get_settings


class StructuredFormatter(logging.Formatter):
    """Structured JSON formatter for consistent log output."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": getattr(record, "service_name", "unknown"),
            "version": getattr(record, "service_version", "unknown"),
            "environment": getattr(record, "environment", "unknown"),
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in [
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "getMessage",
                "exc_info",
                "exc_text",
                "stack_info",
                "service_name",
                "service_version",
                "environment",
            ]:
                log_entry[key] = value

        return json.dumps(log_entry, default=str)


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for development."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]

        # Add color to level name
        record.levelname = f"{color}{record.levelname}{reset}"

        # Format the message
        formatted = super().format(record)

        # Add service info
        service_name = getattr(record, "service_name", "unknown")
        service_version = getattr(record, "service_version", "unknown")
        environment = getattr(record, "environment", "unknown")

        return f"[{service_name}:{service_version}:{environment}] {formatted}"


class LinkOpsLogger(logging.Logger):
    """Custom logger with additional context."""

    def __init__(
        self,
        name: str,
        service_name: str = None,
        service_version: str = None,
        environment: str = None,
    ):
        super().__init__(name)
        self.service_name = service_name or "linkops-service"
        self.service_version = service_version or "1.0.0"
        self.environment = environment or "development"

    def _log(
        self,
        level: int,
        msg: str,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        **kwargs,
    ):
        """Override _log to add service context."""
        if extra is None:
            extra = {}

        extra.update(
            {
                "service_name": self.service_name,
                "service_version": self.service_version,
                "environment": self.environment,
            }
        )

        super()._log(level, msg, args, exc_info, extra, stack_info, **kwargs)


def setup_logging(
    service_name: str = None,
    service_version: str = None,
    environment: str = None,
    log_level: str = None,
    log_format: str = None,
    file_path: str = None,
) -> logging.Logger:
    """
    Setup logging configuration for a LinkOps service.

    Args:
        service_name: Name of the service
        service_version: Version of the service
        environment: Environment (development, staging, production)
        log_level: Logging level
        log_format: Log format (json, console)
        file_path: Path to log file

    Returns:
        Configured logger instance
    """
    settings = get_settings()
    logging_config = settings.logging

    # Use provided values or defaults from settings
    service_name = service_name or settings.service_name
    service_version = service_version or settings.service_version
    environment = environment or settings.environment
    log_level = log_level or logging_config.level
    log_format = log_format or logging_config.format
    file_path = file_path or logging_config.file_path

    # Create custom logger
    logger = LinkOpsLogger(
        name=service_name,
        service_name=service_name,
        service_version=service_version,
        environment=environment,
    )

    # Set log level
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))

    if log_format.lower() == "json":
        console_formatter = StructuredFormatter()
    else:
        console_formatter = ColoredFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if file path is specified)
    if file_path:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=file_path,
            maxBytes=logging_config.max_size,
            backupCount=logging_config.backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))

        # Always use JSON format for file logging
        file_formatter = StructuredFormatter()
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance for the current service.

    Args:
        name: Logger name (defaults to service name)

    Returns:
        Logger instance
    """
    settings = get_settings()
    logger_name = name or settings.service_name

    # Check if logger already exists
    if logger_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(logger_name)

    # Setup new logger
    return setup_logging(
        service_name=settings.service_name,
        service_version=settings.service_version,
        environment=settings.environment,
    )


def log_function_call(func):
    """Decorator to log function calls with parameters and timing."""

    def wrapper(*args, **kwargs):
        logger = get_logger()

        # Log function entry
        logger.debug(
            f"Entering {func.__name__}",
            extra={
                "function": func.__name__,
                "module": func.__module__,
                "args_count": len(args),
                "kwargs_count": len(kwargs),
                "kwargs_keys": list(kwargs.keys()) if kwargs else [],
            },
        )

        try:
            result = func(*args, **kwargs)
            logger.debug(
                f"Exiting {func.__name__} successfully",
                extra={"function": func.__name__, "result_type": type(result).__name__},
            )
            return result
        except Exception as e:
            logger.error(
                f"Error in {func.__name__}: {str(e)}",
                extra={
                    "function": func.__name__,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
            )
            raise

    return wrapper


def log_performance(func):
    """Decorator to log function performance metrics."""
    import time

    def wrapper(*args, **kwargs):
        logger = get_logger()
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time

            logger.info(
                f"Function {func.__name__} completed",
                extra={
                    "function": func.__name__,
                    "execution_time_ms": round(execution_time * 1000, 2),
                    "status": "success",
                },
            )

            return result
        except Exception as e:
            execution_time = time.time() - start_time

            logger.error(
                f"Function {func.__name__} failed",
                extra={
                    "function": func.__name__,
                    "execution_time_ms": round(execution_time * 1000, 2),
                    "status": "error",
                    "error": str(e),
                },
            )
            raise

    return wrapper


class LogContext:
    """Context manager for adding context to log messages."""

    def __init__(self, **context):
        self.context = context
        self.logger = get_logger()

    def __enter__(self):
        # Store original extra
        self.original_extra = getattr(self.logger, "_extra", {})
        # Add new context
        self.logger._extra = {**self.original_extra, **self.context}
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original extra
        self.logger._extra = self.original_extra


def log_context(**context):
    """Decorator to add context to all log messages in a function."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            with LogContext(**context):
                return func(*args, **kwargs)

        return wrapper

    return decorator


# Convenience functions for common logging patterns
def log_service_start(service_name: str, version: str, environment: str):
    """Log service startup information."""
    logger = get_logger(service_name)
    logger.info(
        "Service starting",
        extra={
            "event": "service_start",
            "service_name": service_name,
            "version": version,
            "environment": environment,
        },
    )


def log_service_stop(service_name: str):
    """Log service shutdown information."""
    logger = get_logger(service_name)
    logger.info(
        "Service stopping",
        extra={"event": "service_stop", "service_name": service_name},
    )


def log_health_check(service_name: str, status: str, details: Dict[str, Any] = None):
    """Log health check results."""
    logger = get_logger(service_name)
    logger.info(
        "Health check",
        extra={
            "event": "health_check",
            "service_name": service_name,
            "status": status,
            "details": details or {},
        },
    )


def log_api_request(
    service_name: str,
    method: str,
    path: str,
    status_code: int,
    response_time_ms: float,
    user_agent: str = None,
    client_ip: str = None,
):
    """Log API request information."""
    logger = get_logger(service_name)
    logger.info(
        "API request",
        extra={
            "event": "api_request",
            "method": method,
            "path": path,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "user_agent": user_agent,
            "client_ip": client_ip,
        },
    )


def log_database_operation(
    service_name: str,
    operation: str,
    table: str,
    duration_ms: float,
    success: bool,
    error: str = None,
):
    """Log database operation information."""
    logger = get_logger(service_name)
    log_level = logging.INFO if success else logging.ERROR

    logger.log(
        log_level,
        "Database operation",
        extra={
            "event": "database_operation",
            "operation": operation,
            "table": table,
            "duration_ms": duration_ms,
            "success": success,
            "error": error,
        },
    )


def log_external_api_call(
    service_name: str,
    api_name: str,
    endpoint: str,
    method: str,
    status_code: int,
    duration_ms: float,
    success: bool,
    error: str = None,
):
    """Log external API call information."""
    logger = get_logger(service_name)
    log_level = logging.INFO if success else logging.ERROR

    logger.log(
        log_level,
        "External API call",
        extra={
            "event": "external_api_call",
            "api_name": api_name,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "success": success,
            "error": error,
        },
    )
