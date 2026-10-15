"""Fail-closed policy verifier fake for tests."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone

from core.contracts.policy import PolicyDecision, PolicyRequest, PolicyResult


class MockPolicyVerifier:
    def __init__(
        self,
        *,
        allowed_actions: Iterable[str] = (),
        approval_actions: Iterable[str] = (),
        policy_id: str = "mock-policy-v1",
    ) -> None:
        self._allowed_actions = frozenset(allowed_actions)
        self._approval_actions = frozenset(approval_actions)
        self._policy_id = policy_id

    async def evaluate(self, request: PolicyRequest) -> PolicyResult:
        if request.requires_approval or request.action in self._approval_actions:
            decision = PolicyDecision.REQUIRES_APPROVAL
            reason = "The action requires explicit human approval"
        elif request.action in self._allowed_actions:
            decision = PolicyDecision.ALLOW
            reason = "The action is explicitly allowlisted by the mock policy"
        else:
            decision = PolicyDecision.DENY
            reason = "The action is not allowlisted; default deny applies"
        return PolicyResult(
            decision=decision,
            reason=reason,
            policy_id=self._policy_id,
            evaluated_at=datetime.now(timezone.utc),
        )
