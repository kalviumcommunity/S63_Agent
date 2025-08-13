

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.similarity_utils import l2_distance
import math

def test_identical_vectors():
    v1 = [1, 2, 3]
    v2 = [1, 2, 3]
    assert math.isclose(l2_distance(v1, v2), 0.0, rel_tol=1e-9)

def test_simple_distance():
    v1 = [0, 0]
    v2 = [3, 4]
    assert math.isclose(l2_distance(v1, v2), 5.0, rel_tol=1e-9)

def test_length_mismatch():
    try:
        l2_distance([1, 2], [1])
    except ValueError as e:
        assert "same length" in str(e)
    else:
        assert False, "Expected ValueError for length mismatch"

def test_empty_vector():
    try:
        l2_distance([], [])
    except ValueError as e:
        assert "non-empty" in str(e)
    else:
        assert False, "Expected ValueError for empty vectors"

if __name__ == "__main__":
    test_identical_vectors()
    test_simple_distance()
    test_length_mismatch()
    test_empty_vector()
    print("L2 distance tests passed!")