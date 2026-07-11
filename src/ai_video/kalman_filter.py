import numpy as np


class KalmanFilter:
    """簡化版 2D Kalman Filter"""

    def __init__(self):

        # 狀態：
        # x, y, vx, vy
        self.state = np.zeros((4, 1))

        # 共變異矩陣
        self.P = np.eye(4)

        # 狀態轉移矩陣
        self.F = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ], dtype=float)

        # 觀測矩陣
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ], dtype=float)

        # Process Noise
        self.Q = np.eye(4) * 0.01

        # Measurement Noise
        self.R = np.eye(2) * 5

    def initiate(
        self,
        x,
        y,
    ):
        """初始化位置"""

        self.state = np.array([
            [x],
            [y],
            [0],
            [0],
        ], dtype=float)

    def predict(self):
        """預測下一個位置"""

        self.state = self.F @ self.state

        self.P = (
            self.F
            @ self.P
            @ self.F.T
            + self.Q
        )

        return (
            self.state[0, 0],
            self.state[1, 0],
        )

    def update(
        self,
        x,
        y,
    ):
        """利用觀測值修正"""

        z = np.array([
            [x],
            [y],
        ])

        y_residual = (
            z
            - self.H @ self.state
        )

        S = (
            self.H
            @ self.P
            @ self.H.T
            + self.R
        )

        K = (
            self.P
            @ self.H.T
            @ np.linalg.inv(S)
        )

        self.state = (
            self.state
            + K @ y_residual
        )

        I = np.eye(4)

        self.P = (
            I
            - K @ self.H
        ) @ self.P