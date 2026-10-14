# P3 Roadmap

This roadmap records the intended sequence. A version is complete only when its acceptance criteria are met and the release is reviewed; directory placeholders do not count as implementation.

| Version | Milestone | Core deliverables | Depends on |
|---|---|---|---|
| v0.1.0 | Foundation | Repository baseline, team workflow, project structure | — |
| v0.2.0 | Contracts | Shared schemas/interfaces, version policy, mocks, events/errors, contract tests | v0.1.0 |
| v0.3.0 | MCP Runtime | MCP client, registry, permissions boundary, `dev-mcp` provider | v0.2.0 |
| v0.4.0 | Memory Engine | Memory interface, store abstraction, lifecycle/retention semantics | v0.2.0 |
| v0.5.0 | RAG + LLM Gateway | Retriever/index interfaces, context assembly, provider-neutral model gateway | v0.2.0 |
| v0.6.0 | Agent Runtime | Framework-neutral state, planner/re-planner contract, checkpoints | v0.2.0 and subsystem contracts |
| v0.7.0 | Agentic Loop | Bounded execution loop, tool-call flow, retry/stop conditions | v0.3.0–v0.6.0 |
| v0.8.0 | Policy + Evaluation | Policy checks, approval boundaries, evaluator protocols and test sets | v0.7.0 |
| v0.9.0 | Integrated Beta | End-to-end scenarios, failure recovery, telemetry, security/reliability review | v0.8.0 |
| v1.0.0 | Stable Harness | Compatibility policy, docs, release checklist, supported interfaces | v0.9.0 |
| v1.1+ | Expansion | Multi-agent capabilities and additional providers only when justified | v1.0.0 |

## Release gate

A version may be marked complete when:

- required interfaces and behavioral expectations are documented;
- unit and contract tests pass;
- integration tests cover its boundary with adjacent components;
- errors, timeouts, cancellation, and retry behavior are explicit where relevant;
- security/policy implications are reviewed;
- README and operational documentation match the actual implementation;
- a reviewer who owns the affected subsystem has approved the change.
