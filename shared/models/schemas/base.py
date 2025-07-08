"""
LinkOps Base Schema

Base Pydantic model with shared configuration for all LinkOps schemas.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    """
    Base model for all LinkOps schemas with shared configuration.

    Features:
    - JSON serialization/deserialization
    - Field validation
    - Automatic type conversion
    - Extra field handling
    - UUID generation
    - Timestamp handling
    """

    model_config = ConfigDict(
        # JSON configuration
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        },
        # Validation configuration
        validate_assignment=True,
        validate_default=True,
        # Extra field handling
        extra="forbid",  # Reject extra fields
        # Field configuration
        populate_by_name=True,
        # Serialization configuration
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            }
        },
    )


class TimestampedModel(BaseModel):
    """
    Base model with timestamp fields for tracking creation and updates.
    """

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the record was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the record was last updated",
    )

    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()


class IdentifiedModel(BaseModel):
    """
    Base model with UUID identifier.
    """

    id: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the record"
    )


class BaseEntity(TimestampedModel, IdentifiedModel):
    """
    Base entity model combining timestamps and UUID identifier.
    """

    # Metadata fields
    version: int = Field(default=1, description="Version number for optimistic locking")
    deleted: bool = Field(default=False, description="Soft delete flag")

    # Audit fields
    created_by: Optional[str] = Field(
        default=None, description="User or service that created the record"
    )
    updated_by: Optional[str] = Field(
        default=None, description="User or service that last updated the record"
    )

    # Tags and labels
    tags: Dict[str, str] = Field(
        default_factory=dict, description="Key-value tags for categorization"
    )
    labels: Dict[str, str] = Field(
        default_factory=dict, description="Key-value labels for organization"
    )

    def add_tag(self, key: str, value: str):
        """Add a tag to the entity."""
        self.tags[key] = value
        self.update_timestamp()

    def remove_tag(self, key: str):
        """Remove a tag from the entity."""
        if key in self.tags:
            del self.tags[key]
            self.update_timestamp()

    def add_label(self, key: str, value: str):
        """Add a label to the entity."""
        self.labels[key] = value
        self.update_timestamp()

    def remove_label(self, key: str):
        """Remove a label from the entity."""
        if key in self.labels:
            del self.labels[key]
            self.update_timestamp()

    def soft_delete(self, deleted_by: str = None):
        """Soft delete the entity."""
        self.deleted = True
        self.updated_by = deleted_by
        self.update_timestamp()

    def restore(self, restored_by: str = None):
        """Restore a soft-deleted entity."""
        self.deleted = False
        self.updated_by = restored_by
        self.update_timestamp()


class PaginatedResponse(BaseModel):
    """
    Base model for paginated API responses.
    """

    items: list = Field(description="List of items in the current page")
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    size: int = Field(description="Number of items per page")
    pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_prev: bool = Field(description="Whether there is a previous page")


class ErrorResponse(BaseModel):
    """
    Base model for error responses.
    """

    error: str = Field(description="Error message")
    code: str = Field(description="Error code")
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional error details"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp when the error occurred"
    )


class SuccessResponse(BaseModel):
    """
    Base model for success responses.
    """

    message: str = Field(description="Success message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of the response"
    )


class HealthCheckResponse(BaseModel):
    """
    Base model for health check responses.
    """

    status: str = Field(description="Health status (healthy, unhealthy, degraded)")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of the health check"
    )
    version: str = Field(description="Service version")
    checks: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Individual health check results"
    )


# Utility functions for common operations
def generate_uuid() -> UUID:
    """Generate a new UUID."""
    return uuid4()


def get_current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.utcnow()


def format_timestamp(dt: datetime) -> str:
    """Format timestamp as ISO string."""
    return dt.isoformat() + "Z"


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO timestamp string."""
    return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))


# Common field validators
def validate_uuid(v: str) -> UUID:
    """Validate and convert string to UUID."""
    try:
        return UUID(v)
    except ValueError:
        raise ValueError("Invalid UUID format")


def validate_timestamp(v: str) -> datetime:
    """Validate and convert string to datetime."""
    try:
        return parse_timestamp(v)
    except ValueError:
        raise ValueError("Invalid timestamp format")


def validate_tags(v: Dict[str, str]) -> Dict[str, str]:
    """Validate tags dictionary."""
    if not isinstance(v, dict):
        raise ValueError("Tags must be a dictionary")

    for key, value in v.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Tags must be string key-value pairs")
        if len(key) > 50 or len(value) > 100:
            raise ValueError("Tag key/value too long")

    return v
