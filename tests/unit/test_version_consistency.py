"""Keep package metadata and the public Python package version in sync."""

from __future__ import annotations

import tomllib
from pathlib import Path

from p3 import __version__

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_pyproject_version_matches_python_package_version() -> None:
    project_metadata = tomllib.loads(
        (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert project_metadata["project"]["version"] == __version__
