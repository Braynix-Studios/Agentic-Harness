# System Overview

## Design intent

P3 is an orchestration harness whose subsystems communicate through explicit contracts. Provider choices remain replaceable, and the existing `dev-mcp` subsystem is integrated through an adapter rather than rebuilt.

## Logical layers

1. **Application/workflow layer** — requests a run and supplies execution context.
2. **Agent runtime** — owns agent state, planning, re-planning, and checkpoints.
3. **Orchestration loop** — bounds iterations, manages tool calls, and handles retries/cancellation.
4. **Policy and approval** — authorizes sensitive capabilities before execution and records decisions.
5. **Capability subsystems** — MCP/tools, memory, retrieval, and LLM gateway.
6. **Shared contracts** — types, schemas, events, errors, and compatibility policy.
7. **Adapters and infrastructure** — persistence, provider SDKs, telemetry, and test fakes.

## Dependency rules

- Shared contracts should not import application frameworks or provider SDKs.
- Runtime modules depend inward on contracts; adapters translate provider-specific shapes at the edges.
- Policy checks must be enforced at capability-execution boundaries.
- Retrieved content and tool results are untrusted input.
- State, memory, and telemetry need explicit retention and redaction rules before production use.

## Initial sequence

The v0.2.0 contract milestone precedes deep subsystem implementations. Use mocks to enable parallel work while keeping interface changes reviewable.
