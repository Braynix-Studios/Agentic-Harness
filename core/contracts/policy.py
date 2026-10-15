"""Provider-neutral policy verification and human-approval decision contracts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable

from core.contracts.common import JsonValue


class PolicyDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRES_APPROVAL = "requires_approval"


@dataclass(frozen=True, slots=True)
class PolicyRequest:
    request_id: str
    run_id: str
    actor_id: str
    action: str
    resource: str
    attributes: Mapping[str, JsonValue] = field(default_factory=dict)
    requires_approval: bool = False

    def __post_init__(self) -> None:
        required_fields = ("request_id", "run_id", "actor_id", "action", "resource")
        for field_name in required_fields:
            if not getattr(self, field_name).strip():
                raise ValueError(f"PolicyRequest.{field_name} must not be empty")


@dataclass(frozen=True, slots=True)
class PolicyResult:
    decision: PolicyDecision
    reason: str
    policy_id: str
    evaluated_at: datetime
    obligations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.reason.strip() or not self.policy_id.strip():
            raise ValueError("PolicyResult.reason and policy_id must not be empty")
        if self.evaluated_at.tzinfo is None or self.evaluated_at.utcoffset() is None:
            raise ValueError("PolicyResult.evaluated_at must be timezone-aware")


@runtime_checkable
class PolicyVerifier(Protocol):
    """Async authorization boundary; callers must fail closed on verifier failure."""

    async def evaluate(self, request: PolicyRequest) -> PolicyResult:
        """Evaluate an action before capability execution."""
        ...
