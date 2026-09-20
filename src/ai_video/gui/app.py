import sys
import os
import multiprocessing
from pathlib import Path
# 強制宣告引入，確保 PyInstaller 絕對不會漏掉這些子模組
import ai_video.detector.scrfd
import ai_video.renderer.blur
import ai_video.renderer.pixelate
import ai_video.renderer.solid
import ai_video.image.image_processor

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
    """確保 Windows 使用者桌面上擁有捷徑（透過內建 PowerShell 建立）。"""
    if os.name != "nt":
        return
    try:
        import subprocess
        
        # 取得目前執行的 .exe 路徑
        target = Path(sys.executable).resolve()
        
        # 取得桌面路徑
        desktop = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
        shortcut_path = desktop / "AI-Video.lnk"
        
        if not shortcut_path.exists():
            # 使用 PowerShell 建立捷徑，完全不需要額外安裝套件
            ps_script = f"""
            $WshShell = New-Object -ComObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
            $Shortcut.TargetPath = "{target}"
            $Shortcut.WorkingDirectory = "{target.parent}"
            $Shortcut.IconLocation = "{target}"
            $Shortcut.Save()
            """
            subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
    except Exception:
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