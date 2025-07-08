"""
LinkOps Shared Settings Configuration

Centralized configuration management using Pydantic for all LinkOps microservices.
Supports environment variables, .env files, and Kubernetes secrets.
"""

from functools import lru_cache
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, Field, validator
from pydantic.types import SecretStr


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    url: str = Field(default="postgresql://mlops:password@localhost:5432/mlops")
    pool_size: int = Field(default=10, ge=1, le=50)
    max_overflow: int = Field(default=20, ge=0, le=100)
    echo: bool = Field(default=False)

    class Config:
        env_prefix = "DB_"


class RedisSettings(BaseSettings):
    """Redis configuration settings."""

    url: str = Field(default="redis://localhost:6379")
    db: int = Field(default=0, ge=0, le=15)
    password: Optional[SecretStr] = Field(default=None)
    max_connections: int = Field(default=10, ge=1, le=100)

    class Config:
        env_prefix = "REDIS_"


class APISettings(BaseSettings):
    """API configuration settings."""

    title: str = Field(default="LinkOps MLOps Platform")
    version: str = Field(default="1.0.0")
    description: str = Field(default="LinkOps MLOps Platform API")
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    cors_origins: List[str] = Field(default=["*"])
    cors_allow_credentials: bool = Field(default=True)

    class Config:
        env_prefix = "API_"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""

    secret_key: SecretStr = Field(default="your-secret-key-here")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1440)
    refresh_token_expire_days: int = Field(default=7, ge=1, le=365)

    # API Keys
    openai_api_key: Optional[SecretStr] = Field(default=None)
    gitguardian_api_key: Optional[SecretStr] = Field(default=None)
    snyk_token: Optional[SecretStr] = Field(default=None)

    class Config:
        env_prefix = "SECURITY_"


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""

    level: str = Field(default="INFO")
    format: str = Field(default="json")
    date_format: str = Field(default="%Y-%m-%d %H:%M:%S")
    file_path: Optional[str] = Field(default=None)
    max_size: int = Field(default=10 * 1024 * 1024)  # 10MB
    backup_count: int = Field(default=5)

    @validator("level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()

    class Config:
        env_prefix = "LOG_"


class MonitoringSettings(BaseSettings):
    """Monitoring configuration settings."""

    prometheus_enabled: bool = Field(default=True)
    prometheus_port: int = Field(default=9090, ge=1, le=65535)
    metrics_path: str = Field(default="/metrics")

    # Health check settings
    health_check_enabled: bool = Field(default=True)
    health_check_path: str = Field(default="/health")
    health_check_interval: int = Field(default=30, ge=1, le=300)

    class Config:
        env_prefix = "MONITORING_"


class WhisSettings(BaseSettings):
    """Whis services configuration settings."""

    # Data processing
    max_file_size: int = Field(default=100 * 1024 * 1024)  # 100MB
    allowed_extensions: List[str] = Field(
        default=[".txt", ".md", ".json", ".yaml", ".yml"]
    )
    temp_dir: str = Field(default="/tmp/whis")

    # AI/ML settings
    model_cache_dir: str = Field(default="/app/models")
    batch_size: int = Field(default=32, ge=1, le=512)
    max_tokens: int = Field(default=4096, ge=1, le=8192)

    class Config:
        env_prefix = "WHIS_"


class AuditSettings(BaseSettings):
    """Audit services configuration settings."""

    # Security scanners
    gitguardian_enabled: bool = Field(default=True)
    snyk_enabled: bool = Field(default=True)
    trivy_enabled: bool = Field(default=True)
    semgrep_enabled: bool = Field(default=True)

    # Scoring weights
    security_weight: float = Field(default=0.4, ge=0.0, le=1.0)
    compliance_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    best_practices_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    documentation_weight: float = Field(default=0.1, ge=0.0, le=1.0)

    # Report settings
    report_format: str = Field(default="json")
    report_output_dir: str = Field(default="/app/reports")

    class Config:
        env_prefix = "AUDIT_"


class Settings(BaseSettings):
    """Main application settings combining all configuration sections."""

    # Environment
    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    # Service identification
    service_name: str = Field(default="linkops-service")
    service_version: str = Field(default="1.0.0")

    # Configuration sections
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    api: APISettings = Field(default_factory=APISettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    whis: WhisSettings = Field(default_factory=WhisSettings)
    audit: AuditSettings = Field(default_factory=AuditSettings)

    # Kubernetes settings
    namespace: str = Field(default="linkops")
    pod_name: Optional[str] = Field(default=None)
    node_name: Optional[str] = Field(default=None)

    @validator("environment")
    def validate_environment(cls, v):
        valid_envs = ["development", "staging", "production", "testing"]
        if v.lower() not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v.lower()

    @validator("service_name")
    def validate_service_name(cls, v):
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError(
                "Service name must be alphanumeric with hyphens or underscores only"
            )
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

        # Allow environment variables to override nested settings
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.

    Returns:
        Settings: Application configuration settings

    Note:
        This function is cached to avoid reloading settings on every call.
        Use get_settings.cache_clear() to clear the cache if needed.
    """
    return Settings()


def get_service_settings(service_name: str) -> Dict[str, Any]:
    """
    Get service-specific settings.

    Args:
        service_name: Name of the service requesting settings

    Returns:
        Dict containing service-specific configuration
    """
    settings = get_settings()

    # Set service name if not already set
    if not settings.service_name or settings.service_name == "linkops-service":
        settings.service_name = service_name

    return {
        "service_name": settings.service_name,
        "service_version": settings.service_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "database": settings.database.dict(),
        "redis": settings.redis.dict(),
        "api": settings.api.dict(),
        "security": {
            k: v.get_secret_value() if hasattr(v, "get_secret_value") else v
            for k, v in settings.security.dict().items()
        },
        "logging": settings.logging.dict(),
        "monitoring": settings.monitoring.dict(),
        "whis": settings.whis.dict(),
        "audit": settings.audit.dict(),
    }


def validate_settings() -> bool:
    """
    Validate that all required settings are properly configured.

    Returns:
        bool: True if settings are valid, False otherwise
    """
    try:
        settings = get_settings()

        # Validate database URL
        if not settings.database.url:
            raise ValueError("Database URL is required")

        # Validate Redis URL
        if not settings.redis.url:
            raise ValueError("Redis URL is required")

        # Validate security settings
        if settings.security.secret_key.get_secret_value() == "your-secret-key-here":
            raise ValueError("Security secret key must be set")

        return True

    except Exception as e:
        print(f"Settings validation failed: {e}")
        return False


# Convenience functions for common settings
def get_database_url() -> str:
    """Get database URL from settings."""
    return get_settings().database.url


def get_redis_url() -> str:
    """Get Redis URL from settings."""
    return get_settings().redis.url


def get_secret_key() -> str:
    """Get secret key from settings."""
    return get_settings().security.secret_key.get_secret_value()


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from settings."""
    key = get_settings().security.openai_api_key
    return key.get_secret_value() if key else None


def get_gitguardian_api_key() -> Optional[str]:
    """Get GitGuardian API key from settings."""
    key = get_settings().security.gitguardian_api_key
    return key.get_secret_value() if key else None


def get_snyk_token() -> Optional[str]:
    """Get Snyk token from settings."""
    token = get_settings().security.snyk_token
    return token.get_secret_value() if token else None
