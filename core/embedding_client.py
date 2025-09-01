

from typing import Any, Dict, List, Optional

class BaseEmbeddingClient:
    def embed(
        self,
        texts: List[str],
        model: str = "text-embedding-004",
        **kwargs
    ) -> Dict[str, Any]:
        raise NotImplementedError

class MockEmbeddingClient(BaseEmbeddingClient):
    """
    Returns deterministic small vectors so tests don't need network/API.
    """
    def embed(self, texts: List[str], model: str = "mock-embedding", **kwargs) -> Dict[str, Any]:
        vectors = []
        for t in texts:
            # toy 8-dim embedding: lengths + simple hashes (stable for tests)
            base = len(t)
            vec = [
                float(base),
                float(sum(ord(c) for c in t) % 97),
                float(len(t.split())),
                float(base % 13),
                float(base % 17),
                float(base % 19),
                float(base % 23),
                float(base % 29),
            ]
            vectors.append(vec)
        usage = {"prompt_tokens": sum(len(t.split()) for t in texts), "embedding_tokens": len(texts)}
        return {"model": model, "embeddings": vectors, "usage": usage}

class GeminiEmbeddingClient(BaseEmbeddingClient):
    """
    Uses Google Generative AI embeddings. Requires GEMINI_API_KEY in env.
    Default model: text-embedding-004
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-004"):
        import os
        import google.generativeai as genai
        default_key = "AIzaSyAn-EwrEIjRK9SlZWCSpL9m7VdEZg3fx-w"
        genai.configure(api_key=api_key or os.getenv("GEMINI_API_KEY") or default_key)
        self._genai = genai
        self._model = model

    def embed(self, texts: List[str], model: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        m = model or self._model
        # google.generativeai API expects {"content": "..."} objects
        inputs = [{"content": t} for t in texts]
        resp = self._genai.embed_content(model=m, content=inputs, task_type="retrieval_document", **kwargs)
        # resp could be a list or object depending on SDK version; normalize:
        vectors = resp.get("embedding", {}).get("values") if isinstance(resp, dict) else None
        # If batch returns list-of-embeddings (newer SDKs), collect them:
        if vectors is None and hasattr(resp, "embeddings"):
            vectors = [e.values for e in resp.embeddings]
        elif vectors is None:
            # fallback: single
            vectors = [resp.embedding.values]  # type: ignore
        usage = {"prompt_tokens": sum(len(t.split()) for t in texts), "embedding_tokens": len(texts)}
        return {"model": m, "embeddings": vectors, "usage": usage}