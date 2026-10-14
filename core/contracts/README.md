# Shared Contracts — v0.2.0 Priority

This package is the shared boundary between parallel workstreams. Freeze public interfaces and compatibility expectations here before implementations become deeply coupled.

Planned modules (add only after the shapes are agreed):

- `agent.py` — framework-neutral agent state and runtime request/result contracts.
- `memory.py` — memory records, query/write requests, and store protocol.
- `mcp.py` — capability/tool descriptors, invocation request/result, and runtime protocol.
- `rag.py` — document/chunk models, retrieval request/results, and retriever protocol.
- `llm.py` — provider-neutral generation request/response and gateway protocol.
- `policy.py` — execution context, decisions, approval requirements, and policy protocol.
- `evaluation.py` — evaluation case, metric, result, and report models.
- `events.py` — stable runtime event envelope and event types.
- `errors.py` — shared error taxonomy with actionable, non-secret messages.
- `version.py` — contract package version and compatibility policy.

## Rules

1. Keep public schemas typed and explicitly documented.
2. Do not leak framework- or provider-specific classes through these contracts.
3. Define timeout, cancellation, error, retry, and idempotency semantics where applicable.
4. Add contract tests and conforming mocks alongside each contract.
5. Breaking changes require an explicit versioning decision and migration notes.
