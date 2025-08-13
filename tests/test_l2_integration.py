import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.vector_store import InMemoryVectorStore
from core.similarity_utils import l2_distance, cosine_similarity

def test_l2_and_cosine_integration():
    store = InMemoryVectorStore()

    # Add some dummy embeddings
    store.upsert_embeddings(
        ["Vector A", "Vector B", "Vector C"],
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.9, 0.1]
        ],
        [
            {"text": "Vector A"},
            {"text": "Vector B"},
            {"text": "Vector C"}
        ]
    )

    query = [1.0, 0.0]

    cosine_results = store.similarity_search(query, k=3, metric="cosine")
    l2_results = store.similarity_search(query, k=3, metric="l2")

    print("Cosine similarity results:", cosine_results)
    print("L2 distance results:", l2_results)

    # First cosine similarity result should be Vector A
    assert cosine_results[0][1]["text"] == "Vector A"

    # First L2 similarity result should also be Vector A
    assert l2_results[0][1]["text"] == "Vector A"

if __name__ == "__main__":
    test_l2_and_cosine_integration()
    print("L2 integration tests passed!")
