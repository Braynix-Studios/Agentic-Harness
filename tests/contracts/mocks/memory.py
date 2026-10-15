"""In-memory MemoryStore fake with deterministic namespace isolation."""

from __future__ import annotations

from collections.abc import Sequence

from core.contracts.memory import MemoryQuery, MemoryRecord


class MockMemoryStore:
    def __init__(self, records: Sequence[MemoryRecord] = ()) -> None:
        self._records: dict[tuple[str, str], MemoryRecord] = {
            (record.namespace, record.memory_id): record for record in records
        }

    async def upsert(self, record: MemoryRecord) -> MemoryRecord:
        self._records[(record.namespace, record.memory_id)] = record
        return record

    async def get(self, memory_id: str, namespace: str) -> MemoryRecord | None:
        return self._records.get((namespace, memory_id))

    async def search(self, query: MemoryQuery) -> Sequence[MemoryRecord]:
        text_filter = query.text_contains.casefold() if query.text_contains else None
        results = [
            record
            for (namespace, _), record in self._records.items()
            if namespace == query.namespace
            and (query.kind is None or record.kind is query.kind)
            and (text_filter is None or text_filter in record.content.casefold())
            and all(
                record.metadata.get(key) == value
                for key, value in query.metadata_filters.items()
            )
        ]
        results.sort(key=lambda record: (-record.updated_at.timestamp(), record.memory_id))
        return tuple(results[: query.limit])

    async def delete(self, memory_id: str, namespace: str) -> bool:
        return self._records.pop((namespace, memory_id), None) is not None
