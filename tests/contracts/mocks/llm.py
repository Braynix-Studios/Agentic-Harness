"""Deterministic fake LLM provider for tests without network access."""

from __future__ import annotations

from core.contracts.llm import (
    FinishReason,
    LLMMessage,
    LLMRequest,
    LLMResponse,
    MessageRole,
    TokenUsage,
)


class MockLLMProvider:
    async def generate(self, request: LLMRequest) -> LLMResponse:
        prompt = " ".join(message.content for message in request.messages)
        last_user_message = next(
            (
                message.content
                for message in reversed(request.messages)
                if message.role is MessageRole.USER
            ),
            "mock response",
        )
        return LLMResponse(
            request_id="mock-llm-request",
            model=request.model or "mock-model",
            message=LLMMessage(role=MessageRole.ASSISTANT, content=f"mock:{last_user_message}"),
            finish_reason=FinishReason.STOP,
            usage=TokenUsage(
                input_tokens=len(prompt.split()),
                output_tokens=len(last_user_message.split()) + 1,
            ),
            provider_metadata={"provider": "mock"},
        )
