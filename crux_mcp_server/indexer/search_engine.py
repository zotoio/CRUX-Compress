"""Search engine with TF-IDF fallback and optional sentence-transformers."""

from __future__ import annotations

import logging
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

from crux_mcp_server.utils.frontmatter import extract_searchable_text

if TYPE_CHECKING:
    from crux_mcp_server.indexer.scanner import MemoryEntry, MemoryIndex

logger = logging.getLogger(__name__)

_sentence_transformers = None
_embedder_model = None


def _try_load_embedder() -> bool:
    """Attempt to import sentence-transformers and load a model."""
    global _sentence_transformers, _embedder_model
    if _embedder_model is not None:
        return True
    try:
        import sentence_transformers  # type: ignore[import-untyped]
        _sentence_transformers = sentence_transformers
        _embedder_model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Loaded sentence-transformers for semantic search")
        return True
    except ImportError:
        logger.info("sentence-transformers not available; using TF-IDF fallback")
        return False


@dataclass
class SearchResult:
    entry: MemoryEntry
    score: float


class SearchEngine:
    """Hybrid search: sentence-transformers when available, TF-IDF otherwise."""

    def __init__(self) -> None:
        self._documents: list[tuple[MemoryEntry, str]] = []
        self._idf: dict[str, float] = {}
        self._tf_vectors: list[dict[str, float]] = []
        self._embeddings: object | None = None
        self._use_embeddings = False

    def build(self, index: MemoryIndex) -> None:
        """Build search structures from the memory index."""
        self._documents = []
        for entry in index.entries:
            text = extract_searchable_text(
                {"title": entry.title, "description": entry.description, "tags": entry.tags},
                entry.body,
            )
            self._documents.append((entry, text))

        self._build_tfidf()

        if _try_load_embedder():
            self._build_embeddings()

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        if not self._documents:
            return []

        if self._use_embeddings and _embedder_model is not None:
            return self._search_embeddings(query, limit)
        return self._search_tfidf(query, limit)

    def _build_tfidf(self) -> None:
        n = len(self._documents)
        if n == 0:
            return

        doc_freq: Counter[str] = Counter()
        self._tf_vectors = []

        for _, text in self._documents:
            tokens = _tokenize(text)
            tf = Counter(tokens)
            total = len(tokens) or 1
            self._tf_vectors.append({t: c / total for t, c in tf.items()})
            doc_freq.update(set(tokens))

        self._idf = {
            term: math.log((n + 1) / (df + 1)) + 1
            for term, df in doc_freq.items()
        }

    def _search_tfidf(self, query: str, limit: int) -> list[SearchResult]:
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        query_tf = Counter(query_tokens)
        total_q = len(query_tokens)

        results: list[SearchResult] = []
        for i, (entry, _) in enumerate(self._documents):
            score = 0.0
            for token, count in query_tf.items():
                qtf = count / total_q
                idf = self._idf.get(token, 0)
                dtf = self._tf_vectors[i].get(token, 0)
                score += qtf * idf * dtf
            if score > 0:
                results.append(SearchResult(entry=entry, score=score))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:limit]

    def _build_embeddings(self) -> None:
        if not self._documents or _embedder_model is None:
            return
        texts = [text for _, text in self._documents]
        try:
            self._embeddings = _embedder_model.encode(texts, convert_to_tensor=False)
            self._use_embeddings = True
        except Exception:
            logger.warning("Failed to build embeddings; falling back to TF-IDF", exc_info=True)
            self._use_embeddings = False

    def _search_embeddings(self, query: str, limit: int) -> list[SearchResult]:
        if _embedder_model is None or self._embeddings is None:
            return self._search_tfidf(query, limit)

        try:
            import numpy as np  # type: ignore[import-untyped]
            query_emb = _embedder_model.encode([query], convert_to_tensor=False)
            scores = np.dot(self._embeddings, query_emb.T).flatten()
            top_indices = np.argsort(scores)[::-1][:limit]
            results = []
            for idx in top_indices:
                if scores[idx] > 0:
                    results.append(SearchResult(
                        entry=self._documents[idx][0],
                        score=float(scores[idx]),
                    ))
            return results
        except Exception:
            logger.warning("Embedding search failed; falling back to TF-IDF", exc_info=True)
            return self._search_tfidf(query, limit)


_WORD_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())
