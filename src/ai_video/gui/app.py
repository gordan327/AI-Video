import os
import sys

# ----------------- 1. 強制 UTF-8 與非 ASCII 路徑修復 -----------------
# 確保在 macOS 雙擊時，包含中文的路徑不會觸發 UnicodeEncodeError
os.environ["PYTHONIOENCODING"] = "utf-8"

if getattr(sys, 'frozen', False) or "__compiled__" in globals():
    try:
        # 使用系統檔案編碼安全解碼路徑
        raw_path = sys.executable if hasattr(sys, 'executable') else sys.argv[0]
        if isinstance(raw_path, bytes):
            raw_path = raw_path.decode(sys.getfilesystemencoding() or 'utf-8')
        
        executable_path = os.path.realpath(raw_path)
        bundle_dir = os.path.dirname(executable_path)
        os.chdir(bundle_dir)
    except Exception:
        pass
# ------------------------------------------------------------------------

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QScrollArea,
    QWidget,
)

from ai_video.config.configuration_error import ConfigurationError
from ai_video.gui.controller import Controller
from ai_video.gui.main_window import MainWindow


def setup_responsive_window(window: MainWindow):
    """
    動態調整視窗大小以適應目前螢幕解析度，並包覆捲軸保護低解析度螢幕。
    """
    # 1. 取得主螢幕的可用區域大小 (扣除工作列/Taskbar)
    screen = QApplication.primaryScreen().availableGeometry()
    screen_width = screen.width()
    screen_height = screen.height()

    # 預設視窗大小設為螢幕寬高的 80% (避免超出螢幕)
    default_width = int(screen_width * 0.8)
    default_height = int(screen_height * 0.8)

    # 2. 為中央區塊加上 QScrollArea (當視窗縮小或螢幕太小時代替捲軸)
    central_widget = window.centralWidget()
    if central_widget and not isinstance(central_widget, QScrollArea):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 讓內容自動隨視窗縮放
        scroll_area.setWidget(central_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 移除 ScrollArea 的邊框外觀，保持介面簡潔
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        window.setCentralWidget(scroll_area)

    # 3. 設定預設大小與允許最低極限
    window.resize(default_width, default_height)
    window.setMinimumSize(800, 600)  # 設定最小可縮小尺寸，防止介面過度擠壓


def main():
    """啟動 AI-Video GUI。"""

    app = QApplication(sys.argv)

    window = MainWindow()

    try:
        controller = Controller(window)
    except ConfigurationError as error:
        QMessageBox.critical(
            window,
            "設定檔錯誤",
            str(error),
        )
        return 1
    except Exception as error:
        QMessageBox.critical(
            None,
            "啟動錯誤",
            f"應用程式啟動失敗：\n{str(error)}",
        )
        return 1

    window.controller = controller

    # 響應式螢幕自適應與捲軸防護
    setup_responsive_window(window)

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())