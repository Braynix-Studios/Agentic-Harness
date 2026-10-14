# P3 — Agentic Harness

P3 is a modular engineering harness for composing agentic workflows from replaceable capability providers. The target architecture connects MCP tools, memory, retrieval-augmented generation (RAG), provider-neutral LLM access, agent orchestration, policy enforcement, and evaluation.

> **Project status:** early foundation. This repository scaffold is not a claim that the target subsystems are implemented. Shared contracts and mocks are the immediate engineering priority.

## Goals

- **Contract-first development:** agree on typed interfaces, schemas, events, and error types before deep parallel implementation.
- **Replaceable providers:** keep MCP, memory, retrieval, and LLM implementations behind stable interfaces.
- **Observable execution:** make tool calls, agent steps, checkpoints, and failures inspectable.
- **Controlled execution:** apply policy and approval checks at capability-execution boundaries.
- **Testability:** use mocks and contract tests so modules can be developed independently.
- **Integrate, don't rebuild:** treat the existing `dev-mcp` subsystem as the first MCP provider; do not duplicate its functionality.

## Architecture overview

```text
Application / Workflow
        |
Agent Runtime + Planner + Checkpoints
        |
Agentic Loop / Orchestration
        |
Policy + Approval -------- Unified Evaluation
        |
Shared Contracts (schemas, interfaces, events, errors)
        |
+-------------+-------------+-------------+-------------+
| MCP Runtime | Memory      | RAG          | LLM Gateway |
| dev-mcp     | Store       | Retriever    | Providers   |
+-------------+-------------+-------------+-------------+
        |
Storage, adapters, telemetry, and test infrastructure
```

This is the **target architecture**, not a statement that each box is already implemented.

## Version roadmap

| Version | Milestone | Focus |
|---|---|---|
| v0.1.0 | Foundation | Repository and project-control baseline |
| v0.2.0 | Contracts | Shared schemas, interfaces, mocks, errors, events, and contract tests |
| v0.3.0 | MCP Runtime | MCP client/registry and `dev-mcp` provider adapter |
| v0.4.0 | Memory Engine | Memory interfaces, persistence, retrieval, and lifecycle |
| v0.5.0 | RAG + LLM Gateway | Provider-neutral retrieval and model access |
| v0.6.0 | Agent Runtime | Agent state, planner, runtime adapter, and checkpoints |
| v0.7.0 | Agentic Loop | Bounded end-to-end tool-using workflow |
| v0.8.0 | Policy + Evaluation | Permission/approval enforcement and unified evaluation |
| v0.9.0 | Integrated Beta | Cross-component integration and reliability hardening |
| v1.0.0 | Stable Harness | Versioned interfaces, documented operations, and release checks |

See [ROADMAP.md](ROADMAP.md) and [docs/architecture/system-overview.md](docs/architecture/system-overview.md).

## Repository layout

```text
.
├── core/contracts/        # Shared, versioned contracts — v0.2.0 priority
├── p3/
│   ├── mcp_runtime/        # MCP client, registry, and provider adapters
│   ├── memory/             # Memory interfaces and persistence adapters
│   ├── rag/                # Indexing, retrieval, and context assembly
│   ├── llm_gateway/        # Provider-neutral model access
│   ├── agent_runtime/      # Agent state, planner, and checkpoints
│   ├── orchestration/      # Agentic loop and workflow control
│   ├── policy/             # Rules, permissions, and approvals
│   ├── evaluation/         # Evaluators and evaluation schemas
│   └── observability/      # Events, traces, and structured logging
├── integrations/dev_mcp/   # Adapter to the existing dev-mcp subsystem
├── tests/                  # Contract, unit, integration, and E2E tests
├── docs/                   # Architecture, ADRs, and development guides
├── examples/               # Small, documented examples
├── scripts/                # Developer and maintenance scripts
└── .github/                # Issue/PR templates and CI workflows
```

## Team ownership

| Owner | Primary area |
|---|---|
| **Pranjal** | MCP runtime, Memory Engine, `dev-mcp` integration, capability infrastructure, shared runtime/storage/safety primitives |
| **Prasant** | Agent runtime, planning/re-planning, orchestration, checkpoints, agentic loop, evaluation orchestration |
| **Praveen** | RAG, LLM Gateway, embeddings/vector-store abstraction, indexing, retrieval, and context assembly |

Shared contracts and cross-cutting changes should be reviewed by each affected owner.

## Development principles

1. Freeze shared interfaces in `core/contracts/` before deep parallel implementation.
2. Keep framework-specific types out of shared contracts wherever practical.
3. Use interfaces and mocks to keep subsystem implementations replaceable and testable.
4. Add unit tests for local behavior and contract tests for cross-module compatibility.
5. Enforce policy at tool-execution boundaries; approval-sensitive actions must not bypass it.
6. Never commit credentials, tokens, production secrets, or real user data.
7. Record significant architecture decisions under `docs/decisions/`.
8. Keep all implementation claims aligned with actual code and passing tests.

## Working agreement

- GitHub is used for code, branches, commits, pull requests, code review, and CI.
- Jira remains the delivery-status source of truth unless the team explicitly decides to migrate. Avoid maintaining a duplicate task backlog in GitHub Issues.
- Reference the tracking issue in branch names, commits, and pull requests where applicable.
- Keep pull requests focused and document scope, testing, risks, and contract changes.

## Getting started

This is an initial scaffold. It does not yet provide a fully operational agent runtime or service. The initial Python package configuration is deliberately minimal until the team agrees on dependency and framework choices.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
ruff check .
pytest
```

The immediate milestone is **v0.2.0 — Contracts**. Start with the shared contract package, mocks, versioning policy, and contract-test suite. Do not build subsystem internals against unreviewed interfaces.
