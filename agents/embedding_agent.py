
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import List, Optional
from core.embedding_client import MockEmbeddingClient, GeminiEmbeddingClient
from core.token_utils import log_tokens

class EmbeddingAgent:
    def __init__(self, client=None, model: str = "text-embedding-004"):
        self.client = client or GeminiEmbeddingClient()
        self.model = model

    def embed(self, texts: List[str], model: Optional[str] = None):
        resp = self.client.embed(texts, model=model or self.model)
        # Log token usage if available
        if "usage" in resp:
            log_tokens(resp)
        return resp

if __name__ == "__main__":
    agent = EmbeddingAgent(client=MockEmbeddingClient(), model="mock-embedding")
    out = agent.embed(["Hello world", "Embeddings are vectors"])
    print("Embeddings:", out["embeddings"])