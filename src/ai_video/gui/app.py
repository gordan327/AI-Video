import os
import sys

# ----------------- 1. 強制 macOS/Windows 全域 UTF-8 語系編碼修復 -----------------
# 解決 macOS Finder 雙擊開啟時 LANG / LC_ALL 預設為 C/ASCII 導致中文路徑崩潰問題
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

if sys.version_info[0] == 3:
    import importlib
    importlib.reload(sys)

try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

if getattr(sys, 'frozen', False) or "__compiled__" in globals():
    try:
        raw_path = sys.executable if hasattr(sys, 'executable') else sys.argv[0]
        if isinstance(raw_path, bytes):
            raw_path = raw_path.decode(sys.getfilesystemencoding() or 'utf-8', errors='ignore')
        
        executable_path = os.path.realpath(raw_path)
        bundle_dir = os.path.dirname(executable_path)
        os.chdir(bundle_dir)
    except Exception:
        pass
# --------------------------------------------------------------------------------

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
    """動態調整視窗大小以適應目前螢幕解析度，並包覆捲軸保護低解析度螢幕。"""
    screen = QApplication.primaryScreen().availableGeometry()
    screen_width = screen.width()
    screen_height = screen.height()

    default_width = int(screen_width * 0.8)
    default_height = int(screen_height * 0.8)

    central_widget = window.centralWidget()
    if central_widget and not isinstance(central_widget, QScrollArea):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        
        window.setCentralWidget(scroll_area)

    window.resize(default_width, default_height)
    window.setMinimumSize(800, 600)


import traceback
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from ai_video.gui.main_window import MainWindow
from ai_video.gui.controller import Controller

def main():
    """啟動 AI-Video GUI。"""
    app = QApplication(sys.argv)

    try:
        window = MainWindow()
        controller = Controller(window)
        window.controller = controller
        
        # 載入自適應視窗設定
        setup_responsive_window(window)
        
        window.show()
        return app.exec()

    except Exception as error:
        # 捕捉所有初始化時的崩潰，並以視窗彈窗強制印出 Traceback
        error_details = traceback.format_exc()
        QMessageBox.critical(
            None,
            "程式啟動崩潰",
            f"AI-Video 在啟動時發生嚴重錯誤：\n\n{error_details}"
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())