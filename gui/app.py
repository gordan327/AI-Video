import sys

from PySide6.QtWidgets import QApplication

from ai_video.gui.main_window import MainWindow


def main():
    """啟動 AI-Video GUI。"""

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()