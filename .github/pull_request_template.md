## Summary

<!-- What does this change do and why? Link the related GitHub issue, e.g. Closes #123. -->

## Change type

- [ ] Shared contract or schema change
- [ ] Runtime / adapter implementation
- [ ] Test or CI change
- [ ] Documentation / maintenance

## Validation

- [ ] Added or updated unit tests where behavior changed.
- [ ] Added or updated contract tests for shared-interface changes.
- [ ] Added or updated integration/E2E tests when a subsystem boundary changed.
- [ ] Ran `ruff check .`.
- [ ] Ran `ruff format --check .`.
- [ ] Ran `mypy core p3`.
- [ ] Ran `pytest`.
- [ ] Updated relevant documentation and examples.

## Compatibility and risk

- [ ] No unreviewed breaking change to `core/contracts/`.
- [ ] Provider/framework-specific dependencies remain behind adapters.
- [ ] Error, timeout, cancellation, and retry behavior were considered where relevant.
- [ ] No credentials, secrets, or real sensitive data are included.

**Risk / migration notes:**

<!-- Explain contract/API changes and any migration implications. -->
