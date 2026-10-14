# Tests

- `contracts/`: prove mock and real implementations follow shared interface semantics.
- `unit/`: test an individual module without external services.
- `integration/`: test adapters and adjacent subsystems together.
- `e2e/`: validate complete workflows, including policy and failure paths.

Tests must be deterministic where practical and must not use live credentials or production data.
