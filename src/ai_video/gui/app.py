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

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)

from ai_video.config.configuration_error import ConfigurationError
from ai_video.gui.controller import Controller
from ai_video.gui.main_window import MainWindow


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

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())