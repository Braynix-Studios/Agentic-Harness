"""Public, provider-neutral interfaces and schemas for the P3 Agentic Harness."""

from core.contracts.errors import ErrorCode, ErrorInfo, P3Error
from core.contracts.llm import (
    FinishReason,
    LLMMessage,
    LLMProvider,
    LLMRequest,
    LLMResponse,
    MessageRole,
    TokenUsage,
)
from core.contracts.mcp import ToolCallRequest, ToolCallResult, ToolDescriptor, ToolProvider
from core.contracts.memory import MemoryKind, MemoryQuery, MemoryRecord, MemoryStore
from core.contracts.policy import PolicyDecision, PolicyRequest, PolicyResult, PolicyVerifier
from core.contracts.rag import RetrievalQuery, RetrievedChunk, Retriever

__all__ = [
    "ErrorCode",
    "ErrorInfo",
    "FinishReason",
    "LLMMessage",
    "LLMProvider",
    "LLMRequest",
    "LLMResponse",
    "MemoryKind",
    "MemoryQuery",
    "MemoryRecord",
    "MemoryStore",
    "MessageRole",
    "P3Error",
    "PolicyDecision",
    "PolicyRequest",
    "PolicyResult",
    "PolicyVerifier",
    "RetrievedChunk",
    "RetrievalQuery",
    "Retriever",
    "TokenUsage",
    "ToolCallRequest",
    "ToolCallResult",
    "ToolDescriptor",
    "ToolProvider",
]
