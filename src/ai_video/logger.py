from datetime import datetime


class Logger:
    """AI-Video 專案統一 Logger"""

    @staticmethod
    def _log(level: str, message: str):

        now = datetime.now().strftime("%H:%M:%S")

        print(f"[{now}] [{level}] {message}")

    @staticmethod
    def info(message: str):
        Logger._log("INFO", message)

    @staticmethod
    def success(message: str):
        Logger._log("SUCCESS", message)

    @staticmethod
    def warning(message: str):
        Logger._log("WARNING", message)

    @staticmethod
    def error(message: str):
        Logger._log("ERROR", message)