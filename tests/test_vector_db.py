

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.retrieval_agent import RetrievalAgent
from core.vector_store import InMemoryVectorStore
from agents.embedding_agent import EmbeddingAgent
from core.embedding_client import MockEmbeddingClient

def test_vector_db_end_to_end():
    embed_agent = EmbeddingAgent(client=MockEmbeddingClient(), model="mock-embedding")
    vdb = InMemoryVectorStore()
    agent = RetrievalAgent(embed_agent=embed_agent, vector_store=vdb)

    corpus = [
        "Paris is the capital of France.",
        "The Eiffel Tower is in Paris.",
        "Berlin is the capital of Germany.",
        "Delhi is the capital of India.",
        "The Colosseum is in Rome.",
    ]
    agent.index(corpus)

    results = agent.search("Where is Eiffel Tower located?", k=3)
    assert len(results) == 3, "Should return top-k results"
    texts_in_results = [payload["text"] for _, payload in results]
    assert any("Eiffel Tower" in text for text in texts_in_results), \
        "At least one of the top results should mention Eiffel Tower"

def test_vector_db_scalability_small():
    embed_agent = EmbeddingAgent(client=MockEmbeddingClient(), model="mock-embedding")
    vdb = InMemoryVectorStore()
    agent = RetrievalAgent(embed_agent=embed_agent, vector_store=vdb)

    docs = [f"Doc {i} about topic {i%10}" for i in range(500)]
    agent.index(docs)
    assert vdb.count() == 500

    res = agent.search("topic 7", k=5)
    assert len(res) == 5

if __name__ == "__main__":
    test_vector_db_end_to_end()
    test_vector_db_scalability_small()
    print("Vector DB tests passed!")