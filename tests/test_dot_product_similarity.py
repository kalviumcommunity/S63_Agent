import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.vector_store import InMemoryVectorStore

def test_dot_product_similarity():
    store = InMemoryVectorStore()
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
    results = store.similarity_search(query, k=2, metric="dot") 

    assert results[0][1]["text"] == "Vector A", "Top result should be Vector A"
    assert results[1][1]["text"] == "Vector C", "Second result should be Vector C"

if __name__ == "__main__":
    test_dot_product_similarity()
    print("Dot product similarity tests passed!") 