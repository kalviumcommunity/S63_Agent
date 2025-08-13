

from typing import Any, Dict, List, Optional, Tuple
import math

class BaseVectorStore:
    def upsert_embeddings(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        raise NotImplementedError

    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5,
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """Return list of (score, payload) sorted by descending score."""
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError


class InMemoryVectorStore(BaseVectorStore):
    """
    Simple, dependency-light in-memory vector DB using cosine similarity.
    Stores: vectors, texts, and optional metadata per record.
    """

    def __init__(self, normalize: bool = True):
        self._records: List[Dict[str, Any]] = []
        self._normalize = normalize

    def _normalize_vec(self, v: List[float]) -> List[float]:
        if not self._normalize:
            return v
        norm = math.sqrt(sum(x * x for x in v)) or 1e-12
        return [x / norm for x in v]

    def upsert_embeddings(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        if len(texts) != len(embeddings):
            raise ValueError("texts and embeddings must have the same length")
        if metadatas is not None and len(metadatas) != len(texts):
            raise ValueError("metadatas length must match texts length if provided")

        for i, (t, e) in enumerate(zip(texts, embeddings)):
            rec = {
                "text": t,
                "vector": self._normalize_vec(e),
                "metadata": (metadatas[i] if metadatas else {}),
            }
            self._records.append(rec)

    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5,
    ) -> List[Tuple[float, Dict[str, Any]]]:
        if not self._records:
            return []
        q = self._normalize_vec(query_embedding)

        results: List[Tuple[float, Dict[str, Any]]] = []
        for rec in self._records:
            v = rec["vector"]
            score = sum(a * b for a, b in zip(q, v))
            payload = {"text": rec["text"], "metadata": rec["metadata"]}
            results.append((float(score), payload))

        results.sort(key=lambda x: x[0], reverse=True)
        return results[: max(1, k)]

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()