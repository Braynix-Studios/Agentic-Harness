"""Provider-neutral memory records, queries, and storage protocol."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable

from core.contracts.common import JsonValue


class MemoryKind(StrEnum):
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    namespace: str
    content: str
    kind: MemoryKind
    created_at: datetime
    updated_at: datetime
    metadata: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.memory_id.strip():
            raise ValueError("MemoryRecord.memory_id must not be empty")
        if not self.namespace.strip():
            raise ValueError("MemoryRecord.namespace must not be empty")
        for field_name, value in (("created_at", self.created_at), ("updated_at", self.updated_at)):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"MemoryRecord.{field_name} must be timezone-aware")
        if self.updated_at < self.created_at:
            raise ValueError("MemoryRecord.updated_at must not precede created_at")


@dataclass(frozen=True, slots=True)
class MemoryQuery:
    namespace: str
    text_contains: str | None = None
    kind: MemoryKind | None = None
    metadata_filters: Mapping[str, JsonValue] = field(default_factory=dict)
    limit: int = 20

    def __post_init__(self) -> None:
        if not self.namespace.strip():
            raise ValueError("MemoryQuery.namespace must not be empty")
        if self.limit <= 0:
            raise ValueError("MemoryQuery.limit must be positive")


@runtime_checkable
class MemoryStore(Protocol):
    """Async persistence boundary; implementations must isolate namespaces."""

    async def upsert(self, record: MemoryRecord) -> MemoryRecord:
        """Insert or replace a record identified by namespace and memory_id."""
        ...

    async def get(self, memory_id: str, namespace: str) -> MemoryRecord | None:
        """Return one record, or None when it does not exist in this namespace."""
        ...

    async def search(self, query: MemoryQuery) -> Sequence[MemoryRecord]:
        """Return matching records, never more than query.limit results."""
        ...

    async def delete(self, memory_id: str, namespace: str) -> bool:
        """Delete one record and report whether a record was removed."""
        ...
