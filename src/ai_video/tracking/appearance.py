import numpy as np


def cosine_similarity(
    embedding1: np.ndarray | None,
    embedding2: np.ndarray | None,
) -> float:
    """計算兩組人臉 embedding 的餘弦相似度。"""

    if embedding1 is None or embedding2 is None:
        return 0.0

    vector1 = np.asarray(embedding1, dtype=np.float32).reshape(-1)
    vector2 = np.asarray(embedding2, dtype=np.float32).reshape(-1)

    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = float(
        np.dot(vector1, vector2) / (norm1 * norm2)
    )

    # 避免浮點誤差超出合理範圍
    return max(-1.0, min(1.0, similarity))