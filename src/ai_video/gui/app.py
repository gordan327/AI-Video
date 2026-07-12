import sys

from PySide6.QtWidgets import QApplication

from ai_video.gui.controller import Controller
from ai_video.gui.main_window import MainWindow


def main():
    """啟動 AI-Video GUI。"""

    app = QApplication(sys.argv)

    window = MainWindow()
    controller = Controller(window)

    # 保留 Controller 的參照，避免被 Python 提前回收
    window.controller = controller

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()