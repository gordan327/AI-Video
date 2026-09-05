import sys
import os
import multiprocessing

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
)

from ai_video.config.configuration_error import (
    ConfigurationError,
)
from ai_video.gui.controller import Controller
from ai_video.gui.main_window import MainWindow


def main():
    """啟動 AI-Video GUI。"""

    # 防止打包成視窗版時 tqdm 因為沒有終端機而崩潰
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")

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

    # 保留 Controller 的參照，避免被 Python 提前回收
    window.controller = controller

    window.show()

    return app.exec()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.exit(main())