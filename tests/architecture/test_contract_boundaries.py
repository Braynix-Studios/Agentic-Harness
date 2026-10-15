"""Guard the contract layer against dependencies on runtime/provider implementations."""

from __future__ import annotations

import ast
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_ROOT = REPOSITORY_ROOT / "core" / "contracts"
FORBIDDEN_IMPORT_ROOTS = {
    "p3",
    "integrations",
    "langchain",
    "langchain_core",
    "langgraph",
    "openai",
    "anthropic",
    "chromadb",
    "qdrant_client",
    "sentence_transformers",
}


def _imported_modules(source: str) -> list[str]:
    tree = ast.parse(source)
    modules: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)

    return modules


def test_contract_package_exists() -> None:
    assert CONTRACT_ROOT.is_dir(), "Create the shared core/contracts package first"
    assert list(CONTRACT_ROOT.rglob("*.py")), "Contract package should contain Python modules"


def test_contracts_do_not_import_runtime_or_provider_packages() -> None:
    violations: list[str] = []

    for source_path in sorted(CONTRACT_ROOT.rglob("*.py")):
        source = source_path.read_text(encoding="utf-8")
        for module in _imported_modules(source):
            root_name = module.split(".", maxsplit=1)[0]
            if root_name in FORBIDDEN_IMPORT_ROOTS:
                relative_path = source_path.relative_to(REPOSITORY_ROOT)
                violations.append(f"{relative_path}: imports forbidden module '{module}'")

    assert not violations, (
        "Shared contracts must remain framework/provider neutral. Move concrete implementation "
        "imports to p3/ or integrations/ instead:\n" + "\n".join(violations)
    )
