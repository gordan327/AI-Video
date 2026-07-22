import os
import subprocess
import sys
from pathlib import Path


def open_folder(path: str | Path) -> None:
    """使用作業系統的檔案管理器開啟指定資料夾。"""

    folder_path = Path(path).expanduser().resolve()

    if not folder_path.exists():
        raise FileNotFoundError(
            f"找不到指定的資料夾：{folder_path}"
        )

    if not folder_path.is_dir():
        raise NotADirectoryError(
            f"指定路徑不是資料夾：{folder_path}"
        )

    if sys.platform == "darwin":
        command = [
            "open",
            str(folder_path),
        ]
    elif os.name == "nt":
        command = [
            "explorer",
            str(folder_path),
        ]
    else:
        command = [
            "xdg-open",
            str(folder_path),
        ]

    try:
        subprocess.run(
            command,
            check=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            "找不到作業系統的資料夾開啟工具。"
        ) from error
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"無法開啟資料夾：{folder_path}"
        ) from error