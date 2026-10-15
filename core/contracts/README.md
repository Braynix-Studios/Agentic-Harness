# Shared Contracts — v0.2.0

This package is the shared boundary between parallel P3 workstreams. The initial provider-neutral protocols and data models are now defined for:

- `llm.py` — text generation request/response, messages, usage, and `LLMProvider`.
- `mcp.py` — tool descriptors, tool-call requests/results, and `ToolProvider`.
- `memory.py` — namespaced memory records/queries and `MemoryStore`.
- `rag.py` — retrieval queries, provenance-carrying chunks, and `Retriever`.
- `policy.py` — policy requests, allow/deny/approval decisions, and `PolicyVerifier`.
- `errors.py` — stable error codes, safe error data, and `P3Error`.
- `common.py` — JSON-compatible types shared by contract models.

Deterministic fakes live in `tests/contracts/mocks/` and the contract suite lives in `tests/contracts/test_provider_contracts.py`. Fakes are test-only and are not production providers.

## Compatibility rules

1. Keep models typed and documented; do not expose framework or provider SDK objects.
2. Protocols use async methods for boundaries that may perform I/O.
3. Namespace memory lookups explicitly. A missing record returns `None`; deletion returns whether anything was removed.
4. Tool failures are returned as `ErrorInfo`; provider methods may raise `P3Error` for normalized transport/runtime failures.
5. Policy evaluation is fail-closed: the caller must not execute an action after a verifier failure, `DENY`, or unresolved approval requirement.
6. Retrieved chunks must preserve source identifiers. Relevance scores are ranking signals, not probabilities unless an adapter documents that interpretation.
7. Add behavior and edge-case contract tests when changing any public schema/protocol. Cross-owner review is expected for breaking changes.

The agent-state, checkpoint, events, and evaluation contracts are still pending; they are not implied to exist by these initial interfaces.
