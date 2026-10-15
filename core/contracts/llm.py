"""Provider-neutral text generation contracts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol, runtime_checkable

from core.contracts.common import JsonValue


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class FinishReason(StrEnum):
    STOP = "stop"
    LENGTH = "length"
    TOOL_CALL = "tool_call"
    CONTENT_FILTER = "content_filter"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class LLMMessage:
    role: MessageRole
    content: str


@dataclass(frozen=True, slots=True)
class LLMRequest:
    messages: tuple[LLMMessage, ...]
    model: str | None = None
    temperature: float | None = None
    max_output_tokens: int | None = None
    metadata: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.messages:
            raise ValueError("LLMRequest.messages must contain at least one message")
        if self.model is not None and not self.model.strip():
            raise ValueError("LLMRequest.model must not be empty when provided")
        if self.temperature is not None and not 0.0 <= self.temperature <= 2.0:
            raise ValueError("LLMRequest.temperature must be between 0.0 and 2.0")
        if self.max_output_tokens is not None and self.max_output_tokens <= 0:
            raise ValueError("LLMRequest.max_output_tokens must be positive")


@dataclass(frozen=True, slots=True)
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0

    def __post_init__(self) -> None:
        if self.input_tokens < 0 or self.output_tokens < 0:
            raise ValueError("Token counts must not be negative")


@dataclass(frozen=True, slots=True)
class LLMResponse:
    request_id: str
    model: str
    message: LLMMessage
    finish_reason: FinishReason
    usage: TokenUsage = field(default_factory=TokenUsage)
    provider_metadata: Mapping[str, JsonValue] = field(default_factory=dict)


@runtime_checkable
class LLMProvider(Protocol):
    """Async generation boundary implemented by model-provider adapters."""

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate one assistant message; raise P3Error for normalized failures."""
        ...
