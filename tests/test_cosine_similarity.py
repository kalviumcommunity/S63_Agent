

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.similarity_utils import cosine_similarity
import math

def test_identical_vectors():
    v1 = [1, 2, 3]
    v2 = [1, 2, 3]
    assert math.isclose(cosine_similarity(v1, v2), 1.0, rel_tol=1e-9)

def test_orthogonal_vectors():
    v1 = [1, 0]
    v2 = [0, 1]
    assert math.isclose(cosine_similarity(v1, v2), 0.0, rel_tol=1e-9)

def test_opposite_vectors():
    v1 = [1, 0]
    v2 = [-1, 0]
    assert math.isclose(cosine_similarity(v1, v2), -1.0, rel_tol=1e-9)

def test_length_mismatch():
    try:
        cosine_similarity([1, 2], [1])
    except ValueError as e:
        assert "same length" in str(e)
    else:
        assert False, "Expected ValueError for length mismatch"

def test_empty_vector():
    try:
        cosine_similarity([], [])
    except ValueError as e:
        assert "non-empty" in str(e)
    else:
        assert False, "Expected ValueError for empty vectors"

if __name__ == "__main__":
    test_identical_vectors()
    test_orthogonal_vectors()
    test_opposite_vectors()
    test_length_mismatch()
    test_empty_vector()
    print("Cosine similarity tests passed!")