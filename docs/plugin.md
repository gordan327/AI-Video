# Renderer Plugin Development

本文件說明如何為 AI-Video 新增一種隱私處理 Renderer。

目前內建：

- BlurRenderer
- PixelateRenderer

所有 Renderer 都需繼承 `BaseRenderer`，並實作統一的 `render()` 方法。

---

## 1. Renderer 介面

檔案：

```text
src/ai_video/renderer/base_renderer.py
```

共同介面：

```python
from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    """所有隱私呈現方式的共同介面。"""

    @abstractmethod
    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        """對指定矩形區域進行隱私處理。"""

        raise NotImplementedError
```

Renderer 只負責處理指定區域，不需要知道：

- 人臉如何偵測
- 人臉如何追蹤
- GUI 如何運作
- 影片如何讀取或輸出

---

## 2. 建立新的 Renderer

例如建立純色遮罩：

```text
src/ai_video/renderer/solid_renderer.py
```

內容：

```python
from ai_video.renderer.base_renderer import BaseRenderer


class SolidRenderer(BaseRenderer):
    """使用純色遮蔽指定區域。"""

    def __init__(
        self,
        color: tuple[int, int, int] = (0, 0, 0),
    ):
        self.color = color

    def render(
        self,
        frame,
        box: tuple[int, int, int, int],
    ):
        frame_height, frame_width = frame.shape[:2]

        x1, y1, x2, y2 = box

        x1 = max(0, min(frame_width, int(x1)))
        y1 = max(0, min(frame_height, int(y1)))
        x2 = max(0, min(frame_width, int(x2)))
        y2 = max(0, min(frame_height, int(y2)))

        if x2 <= x1 or y2 <= y1:
            return

        frame[y1:y2, x1:x2] = self.color
```

---

## 3. 註冊到 RendererFactory

修改：

```text
src/ai_video/renderer/renderer_factory.py
```

加入匯入：

```python
from ai_video.renderer.solid_renderer import SolidRenderer
```

加入 Registry：

```python
_RENDERERS = {
    "blur": BlurRenderer,
    "pixelate": PixelateRenderer,
    "solid": SolidRenderer,
}
```

並在 `create()` 中建立對應物件：

```python
if renderer_type == "solid":
    return renderer_class(
        color=kwargs.get(
            "color",
            (0, 0, 0),
        ),
    )
```

---

## 4. 加入 GUI 選項

修改：

```text
src/ai_video/gui/main_window.py
```

加入：

```python
self.renderer_combo.addItem(
    "純色遮罩",
    "solid",
)
```

第一個參數是使用者看到的名稱，第二個參數是程式內部使用的識別碼。

---

## 5. 加入設定

修改：

```text
src/ai_video/config/config.yaml
```

例如：

```yaml
renderer:
  type: solid
```

如 Renderer 有額外參數，也應放在相同區塊：

```yaml
renderer:
  type: solid
  color:
    - 0
    - 0
    - 0
```

---

## 6. 加入測試

新增：

```text
tests/test_solid_renderer.py
```

至少測試：

- 指定區域有被修改
- 區域外保持不變
- 超出畫面的座標可安全裁切
- 無效區域不會造成錯誤

Factory 也應加入建立新 Renderer 的測試。

---

## 7. 開發原則

新增 Renderer 時應遵循：

1. 繼承 `BaseRenderer`
2. 實作 `render(frame, box)`
3. 不直接操作 GUI
4. 不負責偵測或追蹤
5. 不讀寫影片檔案
6. 所有參數由設定系統傳入
7. 補上 pytest 測試
8. 更新 README、CHANGELOG 與本文件

---

## 8. 未來方向

未來規劃支援：

- Solid Color Renderer
- Emoji Renderer
- Mosaic Renderer
- Image Overlay Renderer
- AI Replacement Renderer
- 自動 Plugin Discovery
- 第三方 Renderer Plugin