# Contract Tests

Contract tests validate public data-model expectations and provider/mock conformance. They must run deterministically without network access, credentials, or vendor SDKs.

- `test_provider_contracts.py` exercises the initial LLM, tool/MCP, memory, retrieval, and policy interfaces.
- `mocks/` contains local deterministic fakes for parallel subsystem development.

Every new shared protocol should have tests for a normal case, an empty/not-found case, invalid inputs, and relevant error/approval behavior. Real provider adapters should run the same reusable contract tests where practical.

Run the suite with `pytest tests/contracts -ra`.
