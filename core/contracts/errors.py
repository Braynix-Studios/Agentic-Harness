"""Provider-neutral errors shared across P3 subsystem boundaries."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum


class ErrorCode(StrEnum):
    """Stable machine-readable error categories."""

    INVALID_ARGUMENT = "invalid_argument"
    NOT_FOUND = "not_found"
    TIMEOUT = "timeout"
    UNAVAILABLE = "unavailable"
    PERMISSION_DENIED = "permission_denied"
    APPROVAL_REQUIRED = "approval_required"
    CONFLICT = "conflict"
    PROVIDER_ERROR = "provider_error"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True, slots=True)
class ErrorInfo:
    """Safe error data suitable for returning across a subsystem boundary."""

    code: ErrorCode
    message: str
    retryable: bool = False
    details: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.message.strip():
            raise ValueError("ErrorInfo.message must not be empty")


class P3Error(Exception):
    """Typed exception for failures that should be normalized at subsystem edges."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        *,
        retryable: bool = False,
        details: Mapping[str, str] | None = None,
    ) -> None:
        if not message.strip():
            raise ValueError("P3Error.message must not be empty")
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.details = dict(details or {})

    def to_info(self) -> ErrorInfo:
        """Convert this exception into safe, serializable boundary data."""

        return ErrorInfo(
            code=self.code,
            message=self.message,
            retryable=self.retryable,
            details=self.details,
        )
