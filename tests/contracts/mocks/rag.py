"""Deterministic substring/token fake retriever for contract tests."""

from __future__ import annotations

import re
from collections.abc import Sequence

from core.contracts.rag import RetrievalQuery, RetrievedChunk


class MockRetriever:
    def __init__(self, chunks: Sequence[RetrievedChunk] = ()) -> None:
        self._chunks = tuple(chunks)

    async def retrieve(self, query: RetrievalQuery) -> Sequence[RetrievedChunk]:
        terms = set(re.findall(r"\w+", query.query.casefold()))
        matches = [
            chunk
            for chunk in self._chunks
            if terms.intersection(set(re.findall(r"\w+", chunk.text.casefold())))
            and all(
                chunk.metadata.get(key) == value for key, value in query.metadata_filters.items()
            )
            and (query.namespace is None or chunk.metadata.get("namespace") == query.namespace)
        ]
        matches.sort(key=lambda chunk: (-chunk.relevance_score, chunk.chunk_id))
        return tuple(matches[: query.top_k])
