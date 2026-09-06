import sys
import os
import multiprocessing
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)

from ai_video.config.configuration_error import (
    ConfigurationError,
)
from ai_video.gui.controller import Controller
from ai_video.gui.main_window import MainWindow


def create_desktop_shortcut():
    """確保 Windows 使用者桌面上擁有捷徑（自動補救機制）。"""
    if os.name != "nt":
        return
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = Path(winshell.desktop())
        shortcut_path = desktop / "AI-Video.lnk"
        
        if not shortcut_path.exists():
            target = Path(sys.executable).resolve()
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortcut(str(shortcut_path))
            shortcut.TargetPath = str(target)
            shortcut.WorkingDirectory = str(target.parent)
            shortcut.IconLocation = str(target)
            shortcut.Save()
    except Exception:
        # 如果缺少 win32com 或 winshell 庫則靜默略過，不影響主程式運作
        pass


def main():
    """啟動 AI-Video GUI。"""

    # 防止打包成視窗版時 tqdm 因為沒有終端機而崩潰
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")

    # 自動檢查並建立桌面捷徑
    create_desktop_shortcut()

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

    window.controller = controller
    window.show()

    return app.exec()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.exit(main())