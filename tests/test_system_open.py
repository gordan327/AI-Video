from pathlib import Path
from unittest.mock import patch

from ai_video.utils.system_open import open_folder


def test_open_folder_on_macos(
    tmp_path: Path,
):
    """確認 macOS 使用 open 指令開啟資料夾。"""

    with (
        patch(
            "ai_video.utils.system_open.sys.platform",
            "darwin",
        ),
        patch(
            "ai_video.utils.system_open.subprocess.run",
        ) as mock_run,
    ):
        open_folder(tmp_path)

    mock_run.assert_called_once_with(
        [
            "open",
            str(tmp_path.resolve()),
        ],
        check=True,
    )