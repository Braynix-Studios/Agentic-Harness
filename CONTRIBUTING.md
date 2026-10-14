# Contributing to P3

## Before starting

1. Check the Jira delivery board and confirm the scope and owner of the work.
2. Read the applicable contract and architecture notes.
3. For changes that alter a shared interface or dependency direction, agree on the change with affected owners before implementation.

## Branch and commit conventions

Use short branches with a tracking key when available, for example:

- `SCRUM-6/freeze-contract-package`
- `SCRUM-7/mcp-runtime-contract`

Use Conventional Commit-style messages where practical:

- `feat(contracts): define memory interface`
- `test(contracts): add mock compatibility tests`
- `docs(architecture): clarify provider boundaries`

Include the tracking key in the branch, commit, or PR when a tracked issue exists.

## Pull requests

Every pull request should state:

- the problem and intended behavior;
- key design decisions and contract changes;
- tests and commands run;
- risk, migration, and compatibility notes;
- any follow-up work or intentionally deferred scope.

Do not bundle unrelated refactors with contract changes. Shared contract changes need review from affected subsystem owners.

## Quality checks

Run locally before opening a PR:

```bash
ruff check .
pytest
```

Add tests at the right level: unit tests for local behavior, contract tests for compatibility between implementations, integration tests for actual adapters, and end-to-end tests for complete workflows.

## Contract-first rule

Treat `core/contracts/` as the common boundary. Mocks should conform to the same contracts as real providers. Avoid importing provider-specific SDKs or agent-framework objects into shared contracts.
