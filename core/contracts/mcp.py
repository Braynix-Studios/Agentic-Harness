"""Provider-neutral tool and MCP capability contracts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from core.contracts.common import JsonValue
from core.contracts.errors import ErrorInfo


@dataclass(frozen=True, slots=True)
class ToolDescriptor:
    name: str
    description: str
    input_schema: Mapping[str, JsonValue]
    annotations: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("ToolDescriptor.name must not be empty")


@dataclass(frozen=True, slots=True)
class ToolCallRequest:
    request_id: str
    tool_name: str
    arguments: Mapping[str, JsonValue] = field(default_factory=dict)
    timeout_seconds: float | None = None

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("ToolCallRequest.request_id must not be empty")
        if not self.tool_name.strip():
            raise ValueError("ToolCallRequest.tool_name must not be empty")
        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            raise ValueError("ToolCallRequest.timeout_seconds must be positive")


@dataclass(frozen=True, slots=True)
class ToolCallResult:
    request_id: str
    tool_name: str
    result: JsonValue | None = None
    error: ErrorInfo | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None


@runtime_checkable
class ToolProvider(Protocol):
    """Async boundary for discovering and invoking tool capabilities."""

    async def list_tools(self) -> Sequence[ToolDescriptor]:
        """Return the provider's currently available tool descriptors."""
        ...

    async def call_tool(self, request: ToolCallRequest) -> ToolCallResult:
        """Invoke a tool and return either a result or normalized error data."""
        ...
