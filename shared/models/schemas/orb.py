"""
LinkOps Orb Schema

Orb represents knowledge, insights, and information that can be learned from
and used by the LinkOps platform. Orbs are the foundation of the learning system.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import Field, validator

from .base import BaseEntity


class OrbCategory(str, Enum):
    """Categories for organizing Orbs."""

    # Platform categories
    PLATFORM_ENGINEER = "platform_engineer"
    GITOPS = "gitops"
    KUBERNETES = "kubernetes"
    DEVOPS = "devops"
    MLOPS = "mlops"

    # Technology categories
    DOCKER = "docker"
    HELM = "helm"
    ARGOCD = "argocd"
    PROMETHEUS = "prometheus"
    GRAFANA = "grafana"

    # Process categories
    CI_CD = "ci_cd"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    MONITORING = "monitoring"
    AUTOMATION = "automation"

    # Domain categories
    INFRASTRUCTURE = "infrastructure"
    NETWORKING = "networking"
    STORAGE = "storage"
    DATABASE = "database"
    CACHE = "cache"

    # Custom categories
    CUSTOM = "custom"
    TEMPLATE = "template"
    BEST_PRACTICE = "best_practice"
    TROUBLESHOOTING = "troubleshooting"


class OrbStatus(str, Enum):
    """Status of an Orb."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class Orb(BaseEntity):
    """
    Orb represents a piece of knowledge or insight in the LinkOps platform.

    Orbs can contain:
    - Configuration templates
    - Best practices
    - Troubleshooting guides
    - Process documentation
    - Code snippets
    - Architecture patterns
    """

    # Core fields
    title: str = Field(min_length=1, max_length=200, description="Title of the Orb")
    content: str = Field(min_length=1, description="Main content of the Orb")
    category: OrbCategory = Field(description="Category of the Orb")
    status: OrbStatus = Field(default=OrbStatus.DRAFT, description="Status of the Orb")

    # Description and summary
    description: Optional[str] = Field(
        default=None, max_length=500, description="Brief description of the Orb"
    )
    summary: Optional[str] = Field(
        default=None, max_length=1000, description="Detailed summary of the Orb"
    )

    # Content metadata
    content_type: str = Field(
        default="markdown", description="Type of content (markdown, yaml, json, etc.)"
    )
    content_hash: Optional[str] = Field(
        default=None, description="Hash of the content for change detection"
    )

    # Related resources
    related_orb_ids: List[str] = Field(
        default_factory=list, description="IDs of related Orbs"
    )
    rune_ids: List[str] = Field(
        default_factory=list, description="IDs of related Runes"
    )

    # Usage tracking
    usage_count: int = Field(
        default=0, ge=0, description="Number of times this Orb has been used"
    )
    last_used_at: Optional[datetime] = Field(
        default=None, description="Timestamp of last usage"
    )

    # Quality and validation
    quality_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Quality score of the Orb (0.0 to 1.0)"
    )
    validated: bool = Field(
        default=False, description="Whether the Orb has been validated"
    )
    validated_by: Optional[str] = Field(
        default=None, description="User or service that validated the Orb"
    )
    validated_at: Optional[datetime] = Field(
        default=None, description="Timestamp when the Orb was validated"
    )

    # Source information
    source_url: Optional[str] = Field(
        default=None, description="URL where the Orb content originated"
    )
    source_type: Optional[str] = Field(
        default=None, description="Type of source (documentation, blog, etc.)"
    )

    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the Orb"
    )

    @validator("title")
    def validate_title(cls, v):
        """Validate title is not empty and properly formatted."""
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @validator("content")
    def validate_content(cls, v):
        """Validate content is not empty."""
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()

    @validator("related_orb_ids", "rune_ids")
    def validate_ids(cls, v):
        """Validate that IDs are valid UUIDs."""
        for id_str in v:
            try:
                from uuid import UUID

                UUID(id_str)
            except ValueError:
                raise ValueError(f"Invalid UUID format: {id_str}")
        return v

    def increment_usage(self):
        """Increment usage count and update last used timestamp."""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()
        self.update_timestamp()

    def add_related_orb(self, orb_id: str):
        """Add a related Orb ID."""
        if orb_id not in self.related_orb_ids:
            self.related_orb_ids.append(orb_id)
            self.update_timestamp()

    def remove_related_orb(self, orb_id: str):
        """Remove a related Orb ID."""
        if orb_id in self.related_orb_ids:
            self.related_orb_ids.remove(orb_id)
            self.update_timestamp()

    def add_rune(self, rune_id: str):
        """Add a related Rune ID."""
        if rune_id not in self.rune_ids:
            self.rune_ids.append(rune_id)
            self.update_timestamp()

    def remove_rune(self, rune_id: str):
        """Remove a related Rune ID."""
        if rune_id in self.rune_ids:
            self.rune_ids.remove(rune_id)
            self.update_timestamp()

    def validate_orb(self, validated_by: str):
        """Mark the Orb as validated."""
        self.validated = True
        self.validated_by = validated_by
        self.validated_at = datetime.utcnow()
        self.update_timestamp()

    def update_quality_score(self, score: float):
        """Update the quality score."""
        if not 0.0 <= score <= 1.0:
            raise ValueError("Quality score must be between 0.0 and 1.0")
        self.quality_score = score
        self.update_timestamp()

    def get_content_preview(self, max_length: int = 200) -> str:
        """Get a preview of the content."""
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "..."

    def is_active(self) -> bool:
        """Check if the Orb is active."""
        return self.status == OrbStatus.ACTIVE and not self.deleted

    def can_be_used(self) -> bool:
        """Check if the Orb can be used (active and validated)."""
        return self.is_active() and self.validated


class OrbCreate(BaseEntity):
    """Schema for creating a new Orb."""

    title: str = Field(min_length=1, max_length=200, description="Title of the Orb")
    content: str = Field(min_length=1, description="Main content of the Orb")
    category: OrbCategory = Field(description="Category of the Orb")
    description: Optional[str] = Field(
        default=None, max_length=500, description="Brief description of the Orb"
    )
    summary: Optional[str] = Field(
        default=None, max_length=1000, description="Detailed summary of the Orb"
    )
    content_type: str = Field(default="markdown", description="Type of content")
    source_url: Optional[str] = Field(
        default=None, description="URL where the Orb content originated"
    )
    source_type: Optional[str] = Field(default=None, description="Type of source")
    tags: Dict[str, str] = Field(
        default_factory=dict, description="Tags for categorization"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class OrbUpdate(BaseEntity):
    """Schema for updating an existing Orb."""

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=200, description="Title of the Orb"
    )
    content: Optional[str] = Field(
        default=None, min_length=1, description="Main content of the Orb"
    )
    category: Optional[OrbCategory] = Field(
        default=None, description="Category of the Orb"
    )
    status: Optional[OrbStatus] = Field(default=None, description="Status of the Orb")
    description: Optional[str] = Field(
        default=None, max_length=500, description="Brief description of the Orb"
    )
    summary: Optional[str] = Field(
        default=None, max_length=1000, description="Detailed summary of the Orb"
    )
    content_type: Optional[str] = Field(default=None, description="Type of content")
    quality_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Quality score"
    )
    source_url: Optional[str] = Field(
        default=None, description="URL where the Orb content originated"
    )
    source_type: Optional[str] = Field(default=None, description="Type of source")
    tags: Optional[Dict[str, str]] = Field(
        default=None, description="Tags for categorization"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class OrbSearch(BaseEntity):
    """Schema for searching Orbs."""

    query: Optional[str] = Field(default=None, description="Search query")
    category: Optional[OrbCategory] = Field(
        default=None, description="Filter by category"
    )
    status: Optional[OrbStatus] = Field(default=None, description="Filter by status")
    content_type: Optional[str] = Field(
        default=None, description="Filter by content type"
    )
    validated: Optional[bool] = Field(
        default=None, description="Filter by validation status"
    )
    min_quality_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Minimum quality score"
    )
    tags: Optional[Dict[str, str]] = Field(default=None, description="Filter by tags")
    created_after: Optional[datetime] = Field(
        default=None, description="Filter by creation date (after)"
    )
    created_before: Optional[datetime] = Field(
        default=None, description="Filter by creation date (before)"
    )
    limit: int = Field(
        default=50, ge=1, le=1000, description="Maximum number of results"
    )
    offset: int = Field(default=0, ge=0, description="Number of results to skip")
    sort_by: str = Field(default="created_at", description="Field to sort by")
    sort_order: str = Field(default="desc", description="Sort order (asc or desc)")


# Utility functions
def create_orb_from_content(
    title: str, content: str, category: OrbCategory, created_by: str, **kwargs
) -> Orb:
    """Create a new Orb from content."""
    return Orb(
        title=title, content=content, category=category, created_by=created_by, **kwargs
    )


def validate_orb_content(content: str, content_type: str = "markdown") -> bool:
    """Validate Orb content based on content type."""
    if not content.strip():
        return False

    if content_type == "markdown":
        # Basic markdown validation
        return len(content) > 10
    elif content_type == "yaml":
        # Basic YAML validation
        try:
            import yaml

            yaml.safe_load(content)
            return True
        except yaml.YAMLError:
            return False
    elif content_type == "json":
        # Basic JSON validation
        try:
            import json

            json.loads(content)
            return True
        except json.JSONDecodeError:
            return False

    return True


def calculate_orb_quality_score(orb: Orb) -> float:
    """Calculate quality score for an Orb."""
    score = 0.0

    # Content length (0-20 points)
    content_length = len(orb.content)
    if content_length > 1000:
        score += 20
    elif content_length > 500:
        score += 15
    elif content_length > 200:
        score += 10
    elif content_length > 100:
        score += 5

    # Description presence (0-10 points)
    if orb.description:
        score += 10

    # Summary presence (0-10 points)
    if orb.summary:
        score += 10

    # Tags presence (0-10 points)
    if orb.tags:
        score += min(len(orb.tags) * 2, 10)

    # Related resources (0-10 points)
    if orb.related_orb_ids or orb.rune_ids:
        score += 10

    # Usage count (0-20 points)
    if orb.usage_count > 100:
        score += 20
    elif orb.usage_count > 50:
        score += 15
    elif orb.usage_count > 10:
        score += 10
    elif orb.usage_count > 0:
        score += 5

    # Validation status (0-20 points)
    if orb.validated:
        score += 20

    return min(score / 100.0, 1.0)
