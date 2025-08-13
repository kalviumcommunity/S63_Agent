

import math
from typing import List

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    Formula: (v1 ⋅ v2) / (||v1|| * ||v2||)
    Returns value in [-1, 1] where 1 means identical direction.
    """
    if not vec1 or not vec2:
        raise ValueError("Vectors must be non-empty")
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must be of same length")

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1)) or 1e-12
    norm2 = math.sqrt(sum(b * b for b in vec2)) or 1e-12

    return dot_product / (norm1 * norm2)


if __name__ == "__main__":
    v1 = [1, 0, 0]
    v2 = [1, 0, 0]
    v3 = [0, 1, 0]

    print("cos(v1, v2) =", cosine_similarity(v1, v2))  # Expect 1.0
    print("cos(v1, v3) =", cosine_similarity(v1, v3))  # Expect 0.0