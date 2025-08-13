

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Any, Dict, List, Optional, Tuple
from agents.embedding_agent import EmbeddingAgent
from core.embedding_client import MockEmbeddingClient, GeminiEmbeddingClient
from core.vector_store import InMemoryVectorStore
from core.token_utils import log_tokens

class RetrievalAgent:
    """
    Thin wrapper that:
      1) Creates embeddings for texts
      2) Stores them in a vector DB
      3) Lets you query by semantic similarity
    """

    def __init__(
        self,
        embed_agent: Optional[EmbeddingAgent] = None,
        vector_store: Optional[InMemoryVectorStore] = None,
        use_mock: bool = True,
    ):
        if embed_agent is None:
            client = MockEmbeddingClient() if use_mock else GeminiEmbeddingClient()
            embed_agent = EmbeddingAgent(client=client, model="mock-embedding" if use_mock else "text-embedding-004")
        self.embed_agent = embed_agent
        self.vdb = vector_store or InMemoryVectorStore()

    def index(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> int:
        """Embed and store texts. Returns total count in DB."""
        resp = self.embed_agent.embed(texts)
        log_tokens(resp)
        vectors = resp["embeddings"]
        self.vdb.upsert_embeddings(texts, vectors, metadatas)
        return self.vdb.count()

    def search(self, query: str, k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
        """Embed query and run cosine similarity search."""
        resp = self.embed_agent.embed([query])
        log_tokens(resp)
        qvec = resp["embeddings"][0]
        return self.vdb.similarity_search(qvec, k=k)

if __name__ == "__main__":
    agent = RetrievalAgent(use_mock=True)
    agent.index(
        [
            "Paris is the capital of France.",
            "The Eiffel Tower is in Paris.",
            "Berlin is the capital of Germany.",
            "Taj Mahal is located in Agra, India.",
        ],
        metadatas=[
            {"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}
        ]
    )
    results = agent.search("Where is the Eiffel Tower?", k=2)
    for score, payload in results:
        print(f"{score:.3f} :: {payload}")