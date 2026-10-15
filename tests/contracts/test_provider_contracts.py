"""Contract tests for P3's initial provider-neutral interfaces and fakes."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest

from core.contracts import (
    ErrorCode,
    LLMMessage,
    LLMProvider,
    LLMRequest,
    MemoryKind,
    MemoryQuery,
    MemoryRecord,
    MemoryStore,
    MessageRole,
    PolicyDecision,
    PolicyRequest,
    PolicyVerifier,
    RetrievedChunk,
    RetrievalQuery,
    Retriever,
    ToolCallRequest,
    ToolDescriptor,
    ToolProvider,
)
from core.contracts.errors import P3Error
from tests.contracts.mocks import (
    MockLLMProvider,
    MockMemoryStore,
    MockPolicyVerifier,
    MockRetriever,
    MockToolProvider,
)
from tests.contracts.mocks.tools import echo_handler


def _now() -> datetime:
    return datetime.now(timezone.utc)


def test_mocks_conform_to_runtime_checkable_protocols() -> None:
    assert isinstance(MockLLMProvider(), LLMProvider)
    assert isinstance(MockMemoryStore(), MemoryStore)
    assert isinstance(MockPolicyVerifier(), PolicyVerifier)
    assert isinstance(MockRetriever(), Retriever)
    assert isinstance(MockToolProvider(), ToolProvider)


def test_llm_mock_returns_provider_neutral_response() -> None:
    async def scenario() -> None:
        provider = MockLLMProvider()
        response = await provider.generate(
            LLMRequest(messages=(LLMMessage(role=MessageRole.USER, content="hello p3"),))
        )
        assert response.model == "mock-model"
        assert response.message.role is MessageRole.ASSISTANT
        assert response.message.content == "mock:hello p3"
        assert response.usage.input_tokens == 2

    asyncio.run(scenario())


def test_tool_mock_lists_tools_and_normalizes_missing_tool_error() -> None:
    async def scenario() -> None:
        tool = ToolDescriptor(
            name="echo",
            description="Echo input arguments",
            input_schema={"type": "object"},
        )
        provider = MockToolProvider((tool,), {"echo": echo_handler})
        assert [item.name for item in await provider.list_tools()] == ["echo"]
        result = await provider.call_tool(
            ToolCallRequest(request_id="call-1", tool_name="echo", arguments={"value": "p3"})
        )
        assert result.succeeded
        assert result.result == {"echo": {"value": "p3"}}

        missing = await provider.call_tool(
            ToolCallRequest(request_id="call-2", tool_name="missing")
        )
        assert not missing.succeeded
        assert missing.error is not None
        assert missing.error.code is ErrorCode.NOT_FOUND

    asyncio.run(scenario())


def test_memory_mock_scopes_search_and_deletion_by_namespace() -> None:
    async def scenario() -> None:
        now = _now()
        first = MemoryRecord(
            memory_id="m-1",
            namespace="team-a",
            content="P3 contracts are shared",
            kind=MemoryKind.SEMANTIC,
            created_at=now,
            updated_at=now,
            metadata={"owner": "Pranjal"},
        )
        second = MemoryRecord(
            memory_id="m-1",
            namespace="team-b",
            content="Separate namespace record",
            kind=MemoryKind.WORKING,
            created_at=now,
            updated_at=now,
        )
        store = MockMemoryStore((first, second))
        results = await store.search(MemoryQuery(namespace="team-a", text_contains="CONTRACT"))
        assert results == (first,)
        assert await store.get("m-1", "team-b") == second
        assert await store.delete("m-1", "team-a")
        assert await store.get("m-1", "team-a") is None
        assert not await store.delete("missing", "team-a")

    asyncio.run(scenario())


def test_retriever_returns_relevant_chunks_ranked_and_limited() -> None:
    async def scenario() -> None:
        chunks = (
            RetrievedChunk("c-low", "doc-1", "P3 contract basics", 0.3),
            RetrievedChunk("c-high", "doc-2", "Contract review standards", 0.9),
            RetrievedChunk("c-other", "doc-3", "Independent module", 0.8),
        )
        retriever = MockRetriever(chunks)
        results = await retriever.retrieve(RetrievalQuery(query="contract", top_k=1))
        assert [chunk.chunk_id for chunk in results] == ["c-high"]

    asyncio.run(scenario())


def test_policy_mock_defaults_to_deny_and_supports_approval_gate() -> None:
    async def scenario() -> None:
        verifier = MockPolicyVerifier(
            allowed_actions={"read_file"},
            approval_actions={"delete_file"},
        )
        common = {"request_id": "r-1", "run_id": "run-1", "actor_id": "agent"}
        allowed = await verifier.evaluate(
            PolicyRequest(**common, action="read_file", resource="workspace/readme.md")
        )
        denied = await verifier.evaluate(
            PolicyRequest(**common, action="shell_exec", resource="workspace")
        )
        approval = await verifier.evaluate(
            PolicyRequest(**common, action="delete_file", resource="workspace/data.txt")
        )
        assert allowed.decision is PolicyDecision.ALLOW
        assert denied.decision is PolicyDecision.DENY
        assert approval.decision is PolicyDecision.REQUIRES_APPROVAL

    asyncio.run(scenario())


def test_contract_inputs_reject_invalid_limits_and_empty_queries() -> None:
    with pytest.raises(ValueError, match="top_k"):
        RetrievalQuery(query="find evidence", top_k=0)
    with pytest.raises(ValueError, match="at least one message"):
        LLMRequest(messages=())
    with pytest.raises(ValueError, match="limit"):
        MemoryQuery(namespace="default", limit=0)


def test_p3_error_converts_to_boundary_error_info() -> None:
    error = P3Error(
        ErrorCode.TIMEOUT,
        "Tool call timed out",
        retryable=True,
        details={"request_id": "call-123"},
    )
    info = error.to_info()
    assert info.code is ErrorCode.TIMEOUT
    assert info.retryable
    assert info.details["request_id"] == "call-123"
