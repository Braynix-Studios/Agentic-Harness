# P3 CI/CD and contract compatibility policy

## Purpose

CI is the merge gate for code quality and compatibility. A pull request must pass lint, formatting, type checking, tests, dependency checks, and the contract-layer architecture guard. Shared interfaces should be changed deliberately and reviewed by owners of every affected subsystem.

## Checks provided

- Python matrix on 3.11, 3.12, and 3.13.
- Ruff lint and formatting.
- Mypy strict type check for `core/` and `p3/`.
- Pytest suite including contract-boundary and version-consistency tests.
- `pip-audit` vulnerability scan of the installed runtime/development environment.
- On version tags, verify the tag matches `project.version`, build wheel and source distribution, validate metadata, and attach artifacts to a GitHub Release.
- Dependabot proposes weekly dependency and GitHub Actions updates.

## Rules for keeping contributors synchronized

1. Keep shared contracts in `core/contracts/` in this monorepo; do not copy interface definitions into each subsystem.
2. Contract changes must include contract tests, updated examples, and a note about backwards compatibility in the pull request.
3. Subsystems should depend on shared contracts, not on each other's private implementation modules.
4. Keep vendor/framework dependencies in provider adapters, not in the shared contract package. The architecture test enforces the currently known forbidden import roots; extend it when new providers/frameworks are adopted.
5. Every bug fix adds a regression test where practical. New behavior requires positive and relevant negative/edge-case tests.
6. Use feature branches and pull requests; do not push routine feature work directly to `main`.
7. Keep the package version in `pyproject.toml` and `p3.__version__` synchronized; a test checks this.
8. Tag a release as `vX.Y.Z` only when `project.version` in `pyproject.toml` is `X.Y.Z`. Tag pushes trigger tests and a GitHub Release build only after all checks pass.
9. The release workflow does not publish to PyPI or deploy a service. Add a destination-specific deployment only after an actual service/package distribution target has been chosen.

## Required manual GitHub settings

In the repository Settings, create a branch ruleset targeting `main`:

- Require pull requests before merging.
- Require the quality check for Python 3.11, 3.12, and 3.13 and the dependency audit status check.
- Require at least one approval, if the team can provide a reviewer.
- Require conversation resolution and prevent force pushes/deletion.
- Enable automatic merge only if reviewers explicitly approve it.

Run the workflow once before selecting check names in branch rules. GitHub displays the exact status-check names after the first run.

## If the team later splits into separate repositories

This repo is currently structured as a monorepo. If MCP, memory, agent runtime, or RAG are moved into separate repositories, extract `core/contracts` into a separately versioned package/repository. Consumers should pin a released contract version and run provider contract tests against that exact version. Add a coordinated upgrade pull request (or repository-dispatch workflow) when a new contract release becomes available. Copying files manually between repositories is not a reliable synchronization mechanism.
