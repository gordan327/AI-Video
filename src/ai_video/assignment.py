import numpy as np
from scipy.optimize import linear_sum_assignment


class HungarianAssignment:
    """使用 Hungarian Algorithm 尋找整體最佳配對。"""

    def assign(
        self,
        score_matrix: list[list[float]],
    ) -> list[tuple[int, int]]:
        """
        回傳配對索引：

        [(track_index, face_index), ...]
        """

        if not score_matrix:
            return []

        if not score_matrix[0]:
            return []

        scores = np.asarray(
            score_matrix,
            dtype=np.float32,
        )

        # linear_sum_assignment 尋找最低成本，
        # 因此把分數轉換成成本。
        cost_matrix = 1.0 - scores

        track_indexes, face_indexes = linear_sum_assignment(
            cost_matrix
        )

        return list(
            zip(
                track_indexes.tolist(),
                face_indexes.tolist(),
            )
        )