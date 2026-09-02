"""AI-Video 版本資訊。"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version


try:
    __version__ = version("ai-video")
except PackageNotFoundError:
    __version__ = "unknown"

__build__ = ""
__codename__ = ""