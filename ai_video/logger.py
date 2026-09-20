from datetime import datetime
from threading import RLock
from typing import Callable


LogListener = Callable[[str], None]


class Logger:
    """AI-Video 專案統一 Logger。"""

    _listeners: list[LogListener] = []
    _lock = RLock()

    @classmethod
    def subscribe(cls, listener: LogListener):
        """訂閱 Logger 訊息。"""

        with cls._lock:
            if listener not in cls._listeners:
                cls._listeners.append(listener)

    @classmethod
    def unsubscribe(cls, listener: LogListener):
        """取消訂閱 Logger 訊息。"""

        with cls._lock:
            if listener in cls._listeners:
                cls._listeners.remove(listener)

    @classmethod
    def _log(cls, level: str, message: str):
        """輸出訊息並通知所有訂閱者。"""

        now = datetime.now().strftime("%H:%M:%S")
        formatted_message = (
            f"[{now}] [{level}] {message}"
        )

        # 保留 Terminal 輸出
        print(formatted_message, flush=True)

        with cls._lock:
            listeners = list(cls._listeners)

        for listener in listeners:
            try:
                listener(formatted_message)
            except Exception as error:
                print(
                    f"Logger listener error: {error}",
                    flush=True,
                )

    @classmethod
    def info(cls, message: str):
        cls._log("INFO", message)

    @classmethod
    def success(cls, message: str):
        cls._log("SUCCESS", message)

    @classmethod
    def warning(cls, message: str):
        cls._log("WARNING", message)

    @classmethod
    def error(cls, message: str):
        cls._log("ERROR", message)