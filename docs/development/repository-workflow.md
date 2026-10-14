# Repository Workflow

1. Confirm scope and owner in Jira before starting.
2. Create a short branch named with the Jira key when applicable.
3. Keep interface changes separate from provider implementations when feasible.
4. Add tests and update docs in the same PR as the behavior they describe.
5. Explain the test results, limitations, contract impact, and security implications in the PR description.
6. Merge only after required checks and owner reviews pass.

GitHub is for source collaboration; Jira remains the delivery-status source of truth unless the team formally changes that policy.
