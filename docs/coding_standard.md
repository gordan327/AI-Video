# AI-Video Coding Standard

Version: 1.0

---

# 1. Python Version

Python 3.14+

---

# 2. Type Hint

所有公開函式必須加入 Type Hint。

例如：

def detect(frame: np.ndarray) -> list[Face]:

---

# 3. Docstring

所有 Class 與 public function 必須有 Docstring。

格式：

class Face:
    """代表一張人臉。"""

---

# 4. Import 順序

1. Python Standard Library

2. Third-party Library

3. ai_video Package

例如：

import os

import cv2
import numpy as np

from ai_video.face import Face

---

# 5. 命名規範

Class：

PascalCase

FaceDetector

ModelManager

Variable：

snake_case

track_id

frame_index

Constant：

UPPER_CASE

MAX_TRACK_AGE

---

# 6. 每個 Class 單一責任

一個 Class 只負責一件事情。

例如：

KalmanFilter

只負責：

Predict

Update

不得：

Create Track

Match Face

Renderer

---

# 7. 每個 Module 只放相關 Class

例如：

geometry.py

只放 Geometry Function。

不要放 Tracker。

---

# 8. 測試

每增加一個重要 Module，

至少建立一個 scripts/test_xxx.py。