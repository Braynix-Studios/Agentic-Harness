"""Provider-neutral retrieval query and evidence contracts."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from core.contracts.common import JsonValue


@dataclass(frozen=True, slots=True)
class RetrievalQuery:
    query: str
    top_k: int = 5
    namespace: str | None = None
    metadata_filters: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.query.strip():
            raise ValueError("RetrievalQuery.query must not be empty")
        if self.top_k <= 0:
            raise ValueError("RetrievalQuery.top_k must be positive")


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    chunk_id: str
    source_id: str
    text: str
    relevance_score: float
    metadata: Mapping[str, JsonValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.chunk_id.strip() or not self.source_id.strip():
            raise ValueError("RetrievedChunk chunk_id and source_id must not be empty")
        if not math.isfinite(self.relevance_score):
            raise ValueError("RetrievedChunk.relevance_score must be finite")


@runtime_checkable
class Retriever(Protocol):
    """Async retrieval boundary; results should be ordered by relevance descending."""

    async def retrieve(self, query: RetrievalQuery) -> Sequence[RetrievedChunk]:
        """Return up to query.top_k evidence chunks with source provenance."""
        ...
