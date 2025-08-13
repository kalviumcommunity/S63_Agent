

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.embedding_agent import EmbeddingAgent
from core.embedding_client import MockEmbeddingClient

def test_mock_embeddings_shape_and_stability():
    agent = EmbeddingAgent(client=MockEmbeddingClient(), model="mock-embedding")
    texts = ["hello", "hello world"]
    resp = agent.embed(texts)
    vecs = resp["embeddings"]

    assert len(vecs) == 2, "Should return an embedding per input"
    assert len(vecs[0]) == 8, "Mock embeddings should be 8-dimensional"

    # Deterministic: same input → same vector
    resp2 = agent.embed(["hello"])
    assert vecs[0] == resp2["embeddings"][0], "Mock embeddings must be deterministic"

    # Basic monotonicity: different inputs produce different vectors
    assert vecs[0] != vecs[1], "Different inputs should give different vectors"

if __name__ == "__main__":
    test_mock_embeddings_shape_and_stability()
    print("Embeddings test passed!")