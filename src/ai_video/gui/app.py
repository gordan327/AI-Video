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
        # 確保 error 轉化為字串時不會觸發 ASCII 編碼失敗
        error_msg = str(error)
        if isinstance(error_msg, bytes):
            error_msg = error_msg.decode('utf-8', errors='ignore')
            
        QMessageBox.critical(
            None,
            "啟動錯誤",
            f"應用程式啟動失敗：\n{error_msg}",
        )
        return 1

    window.controller = controller

    setup_responsive_window(window)

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())