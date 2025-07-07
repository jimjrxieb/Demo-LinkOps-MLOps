"""
LinkOps Rune Schema

Rune represents an executable task, script, or automation that can be performed
by the LinkOps platform. Runes are the execution layer of the system.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from pydantic import Field, validator, root_validator

from .base import BaseEntity


class RuneType(str, Enum):
    """Types of Runes based on their execution context."""
    
    # Infrastructure Runes
    KUBERNETES_DEPLOY = "kubernetes_deploy"
    KUBERNETES_SCALE = "kubernetes_scale"
    KUBERNETES_ROLLBACK = "kubernetes_rollback"
    KUBERNETES_CLEANUP = "kubernetes_cleanup"
    
    # GitOps Runes
    GIT_PUSH = "git_push"
    GIT_PULL = "git_pull"
    GIT_MERGE = "git_merge"
    GIT_TAG = "git_tag"
    ARGOCD_SYNC = "argocd_sync"
    ARGOCD_ROLLBACK = "argocd_rollback"
    
    # Security Runes
    SECURITY_SCAN = "security_scan"
    VULNERABILITY_SCAN = "vulnerability_scan"
    COMPLIANCE_CHECK = "compliance_check"
    SECRET_SCAN = "secret_scan"
    
    # Monitoring Runes
    METRICS_COLLECT = "metrics_collect"
    ALERT_CHECK = "alert_check"
    LOG_ANALYSIS = "log_analysis"
    HEALTH_CHECK = "health_check"
    
    # Data Processing Runes
    DATA_TRANSFORM = "data_transform"
    DATA_VALIDATE = "data_validate"
    DATA_CLEAN = "data_clean"
    DATA_EXPORT = "data_export"
    
    # System Runes
    SYSTEM_INFO = "system_info"
    SYSTEM_CLEANUP = "system_cleanup"
    BACKUP_CREATE = "backup_create"
    BACKUP_RESTORE = "backup_restore"
    
    # Custom Runes
    CUSTOM_SCRIPT = "custom_script"
    CUSTOM_COMMAND = "custom_command"
    CUSTOM_API = "custom_api"


class RuneStatus(str, Enum):
    """Status of a Rune."""
    
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    DISABLED = "disabled"


class RuneExecutionStatus(str, Enum):
    """Status of Rune execution."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class RunePriority(str, Enum):
    """Priority levels for Rune execution."""
    
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class RuneStep(BaseEntity):
    """A single step within a Rune."""
    
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Name of the step"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Description of what the step does"
    )
    command: str = Field(
        description="Command or action to execute"
    )
    args: List[str] = Field(
        default_factory=list,
        description="Arguments for the command"
    )
    env: Dict[str, str] = Field(
        default_factory=dict,
        description="Environment variables for the step"
    )
    timeout: int = Field(
        default=300,
        ge=1,
        le=3600,
        description="Timeout in seconds"
    )
    retries: int = Field(
        default=0,
        ge=0,
        le=10,
        description="Number of retries on failure"
    )
    condition: Optional[str] = Field(
        default=None,
        description="Condition for step execution"
    )
    on_failure: Optional[str] = Field(
        default=None,
        description="Action to take on failure"
    )
    on_success: Optional[str] = Field(
        default=None,
        description="Action to take on success"
    )


class Rune(BaseEntity):
    """
    Rune represents an executable task or automation in the LinkOps platform.
    
    Runes can contain:
    - Shell commands
    - API calls
    - Kubernetes operations
    - Git operations
    - Custom scripts
    - Workflow steps
    """
    
    # Core fields
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Name of the Rune"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Description of what the Rune does"
    )
    type: RuneType = Field(
        description="Type of the Rune"
    )
    status: RuneStatus = Field(
        default=RuneStatus.DRAFT,
        description="Status of the Rune"
    )
    
    # Execution configuration
    steps: List[RuneStep] = Field(
        default_factory=list,
        description="Steps to execute"
    )
    timeout: int = Field(
        default=1800,
        ge=1,
        le=7200,
        description="Total timeout in seconds"
    )
    retries: int = Field(
        default=0,
        ge=0,
        le=5,
        description="Number of retries on failure"
    )
    priority: RunePriority = Field(
        default=RunePriority.NORMAL,
        description="Execution priority"
    )
    
    # Requirements and dependencies
    requirements: Dict[str, str] = Field(
        default_factory=dict,
        description="Requirements for execution (tools, permissions, etc.)"
    )
    dependencies: List[str] = Field(
        default_factory=list,
        description="IDs of Runes that must complete before this one"
    )
    
    # Input and output
    input_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON schema for input validation"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON schema for output validation"
    )
    default_input: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Default input values"
    )
    
    # Execution tracking
    execution_count: int = Field(
        default=0,
        ge=0,
        description="Number of times this Rune has been executed"
    )
    success_count: int = Field(
        default=0,
        ge=0,
        description="Number of successful executions"
    )
    failure_count: int = Field(
        default=0,
        ge=0,
        description="Number of failed executions"
    )
    last_executed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last execution"
    )
    last_success_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last successful execution"
    )
    last_failure_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last failed execution"
    )
    
    # Performance metrics
    avg_execution_time: float = Field(
        default=0.0,
        ge=0.0,
        description="Average execution time in seconds"
    )
    min_execution_time: float = Field(
        default=0.0,
        ge=0.0,
        description="Minimum execution time in seconds"
    )
    max_execution_time: float = Field(
        default=0.0,
        ge=0.0,
        description="Maximum execution time in seconds"
    )
    
    # Safety and validation
    safe_mode: bool = Field(
        default=True,
        description="Whether the Rune runs in safe mode"
    )
    dry_run: bool = Field(
        default=False,
        description="Whether to perform a dry run"
    )
    validated: bool = Field(
        default=False,
        description="Whether the Rune has been validated"
    )
    validated_by: Optional[str] = Field(
        default=None,
        description="User or service that validated the Rune"
    )
    validated_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the Rune was validated"
    )
    
    # Related resources
    orb_ids: List[str] = Field(
        default_factory=list,
        description="IDs of related Orbs"
    )
    
    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the Rune"
    )
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name is not empty and properly formatted."""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
    
    @validator('steps')
    def validate_steps(cls, v):
        """Validate that steps list is not empty for active Runes."""
        if not v:
            raise ValueError("Rune must have at least one step")
        return v
    
    @validator('dependencies')
    def validate_dependencies(cls, v):
        """Validate that dependency IDs are valid UUIDs."""
        for id_str in v:
            try:
                from uuid import UUID
                UUID(id_str)
            except ValueError:
                raise ValueError(f"Invalid UUID format: {id_str}")
        return v
    
    @validator('orb_ids')
    def validate_orb_ids(cls, v):
        """Validate that Orb IDs are valid UUIDs."""
        for id_str in v:
            try:
                from uuid import UUID
                UUID(id_str)
            except ValueError:
                raise ValueError(f"Invalid UUID format: {id_str}")
        return v
    
    @root_validator
    def validate_execution_counts(cls, values):
        """Validate that execution counts are consistent."""
        execution_count = values.get('execution_count', 0)
        success_count = values.get('success_count', 0)
        failure_count = values.get('failure_count', 0)
        
        if success_count + failure_count > execution_count:
            raise ValueError("Success and failure counts cannot exceed execution count")
        
        return values
    
    def add_step(self, step: RuneStep):
        """Add a step to the Rune."""
        self.steps.append(step)
        self.update_timestamp()
    
    def remove_step(self, step_index: int):
        """Remove a step from the Rune."""
        if 0 <= step_index < len(self.steps):
            del self.steps[step_index]
            self.update_timestamp()
    
    def add_dependency(self, rune_id: str):
        """Add a dependency Rune ID."""
        if rune_id not in self.dependencies:
            self.dependencies.append(rune_id)
            self.update_timestamp()
    
    def remove_dependency(self, rune_id: str):
        """Remove a dependency Rune ID."""
        if rune_id in self.dependencies:
            self.dependencies.remove(rune_id)
            self.update_timestamp()
    
    def add_orb(self, orb_id: str):
        """Add a related Orb ID."""
        if orb_id not in self.orb_ids:
            self.orb_ids.append(orb_id)
            self.update_timestamp()
    
    def remove_orb(self, orb_id: str):
        """Remove a related Orb ID."""
        if orb_id in self.orb_ids:
            self.orb_ids.remove(orb_id)
            self.update_timestamp()
    
    def record_execution(self, success: bool, execution_time: float):
        """Record execution results."""
        self.execution_count += 1
        self.last_executed_at = datetime.utcnow()
        
        if success:
            self.success_count += 1
            self.last_success_at = datetime.utcnow()
        else:
            self.failure_count += 1
            self.last_failure_at = datetime.utcnow()
        
        # Update execution time metrics
        if self.avg_execution_time == 0.0:
            self.avg_execution_time = execution_time
            self.min_execution_time = execution_time
            self.max_execution_time = execution_time
        else:
            total_time = self.avg_execution_time * (self.execution_count - 1) + execution_time
            self.avg_execution_time = total_time / self.execution_count
            self.min_execution_time = min(self.min_execution_time, execution_time)
            self.max_execution_time = max(self.max_execution_time, execution_time)
        
        self.update_timestamp()
    
    def validate_rune(self, validated_by: str):
        """Mark the Rune as validated."""
        self.validated = True
        self.validated_by = validated_by
        self.validated_at = datetime.utcnow()
        self.update_timestamp()
    
    def get_success_rate(self) -> float:
        """Calculate success rate."""
        if self.execution_count == 0:
            return 0.0
        return self.success_count / self.execution_count
    
    def is_active(self) -> bool:
        """Check if the Rune is active."""
        return self.status == RuneStatus.ACTIVE and not self.deleted
    
    def can_be_executed(self) -> bool:
        """Check if the Rune can be executed."""
        return self.is_active() and self.validated and len(self.steps) > 0
    
    def get_estimated_duration(self) -> float:
        """Get estimated execution duration."""
        if self.avg_execution_time > 0:
            return self.avg_execution_time
        return sum(step.timeout for step in self.steps)


class RuneCreate(BaseEntity):
    """Schema for creating a new Rune."""
    
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Name of the Rune"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Description of what the Rune does"
    )
    type: RuneType = Field(
        description="Type of the Rune"
    )
    steps: List[RuneStep] = Field(
        description="Steps to execute"
    )
    timeout: int = Field(
        default=1800,
        ge=1,
        le=7200,
        description="Total timeout in seconds"
    )
    retries: int = Field(
        default=0,
        ge=0,
        le=5,
        description="Number of retries on failure"
    )
    priority: RunePriority = Field(
        default=RunePriority.NORMAL,
        description="Execution priority"
    )
    requirements: Dict[str, str] = Field(
        default_factory=dict,
        description="Requirements for execution"
    )
    input_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON schema for input validation"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON schema for output validation"
    )
    default_input: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Default input values"
    )
    safe_mode: bool = Field(
        default=True,
        description="Whether the Rune runs in safe mode"
    )
    tags: Dict[str, str] = Field(
        default_factory=dict,
        description="Tags for categorization"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata"
    )


class RuneUpdate(BaseEntity):
    """Schema for updating an existing Rune."""
    
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Name of the Rune"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Description of what the Rune does"
    )
    type: Optional[RuneType] = Field(
        default=None,
        description="Type of the Rune"
    )
    status: Optional[RuneStatus] = Field(
        default=None,
        description="Status of the Rune"
    )
    steps: Optional[List[RuneStep]] = Field(
        default=None,
        description="Steps to execute"
    )
    timeout: Optional[int] = Field(
        default=None,
        ge=1,
        le=7200,
        description="Total timeout in seconds"
    )
    retries: Optional[int] = Field(
        default=None,
        ge=0,
        le=5,
        description="Number of retries on failure"
    )
    priority: Optional[RunePriority] = Field(
        default=None,
        description="Execution priority"
    )
    requirements: Optional[Dict[str, str]] = Field(
        default=None,
        description="Requirements for execution"
    )
    input_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON schema for input validation"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON schema for output validation"
    )
    default_input: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Default input values"
    )
    safe_mode: Optional[bool] = Field(
        default=None,
        description="Whether the Rune runs in safe mode"
    )
    tags: Optional[Dict[str, str]] = Field(
        default=None,
        description="Tags for categorization"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata"
    )


class RuneExecution(BaseEntity):
    """Schema for Rune execution tracking."""
    
    rune_id: str = Field(
        description="ID of the Rune being executed"
    )
    status: RuneExecutionStatus = Field(
        default=RuneExecutionStatus.PENDING,
        description="Execution status"
    )
    input_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Input data for the execution"
    )
    output_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Output data from the execution"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if execution failed"
    )
    started_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when execution started"
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when execution completed"
    )
    execution_time: float = Field(
        default=0.0,
        ge=0.0,
        description="Execution time in seconds"
    )
    logs: List[str] = Field(
        default_factory=list,
        description="Execution logs"
    )
    step_results: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Results from individual steps"
    )


# Utility functions
def create_rune_from_steps(
    name: str,
    steps: List[RuneStep],
    rune_type: RuneType,
    created_by: str,
    **kwargs
) -> Rune:
    """Create a new Rune from steps."""
    return Rune(
        name=name,
        steps=steps,
        type=rune_type,
        created_by=created_by,
        **kwargs
    )


def validate_rune_steps(steps: List[RuneStep]) -> bool:
    """Validate Rune steps."""
    if not steps:
        return False
    
    for step in steps:
        if not step.name or not step.command:
            return False
        if step.timeout <= 0:
            return False
        if step.retries < 0:
            return False
    
    return True


def calculate_rune_complexity(rune: Rune) -> int:
    """Calculate complexity score for a Rune."""
    complexity = 0
    
    # Base complexity from number of steps
    complexity += len(rune.steps) * 10
    
    # Additional complexity from step types
    for step in rune.steps:
        if "kubectl" in step.command.lower():
            complexity += 5
        if "helm" in step.command.lower():
            complexity += 5
        if "git" in step.command.lower():
            complexity += 3
        if step.retries > 0:
            complexity += step.retries * 2
        if step.condition:
            complexity += 10
    
    # Complexity from dependencies
    complexity += len(rune.dependencies) * 5
    
    # Complexity from requirements
    complexity += len(rune.requirements) * 3
    
    return complexity 