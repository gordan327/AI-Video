import subprocess
import sys
import time
from pathlib import Path

import cv2

from ai_video.config_manager import ConfigManager


def read_video_info(video_path: str) -> tuple[int, float]:
    """讀取影片總影格數與原始 FPS。"""

    capture = cv2.VideoCapture(video_path)

    if not capture.isOpened():
        raise RuntimeError(f"無法開啟影片：{video_path}")

    frame_count = int(
        capture.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    source_fps = float(
        capture.get(cv2.CAP_PROP_FPS)
    )

    capture.release()

    return frame_count, source_fps


def main():
    config = ConfigManager()

    input_path = config.get("video.input")

    if not input_path:
        raise ValueError("config.yaml 缺少 video.input")

    if not Path(input_path).exists():
        raise FileNotFoundError(
            f"找不到測試影片：{input_path}"
        )

    frame_count, source_fps = read_video_info(
        input_path
    )

    print("=" * 50)
    print("AI-Video Pipeline Benchmark")
    print("=" * 50)
    print(f"Input       : {input_path}")
    print(f"Frames      : {frame_count}")
    print(f"Source FPS  : {source_fps:.2f}")
    print("開始執行完整處理流程……")

    start_time = time.perf_counter()

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_video.cli",
        ],
        check=False,
    )

    elapsed_time = time.perf_counter() - start_time

    if result.returncode != 0:
        raise RuntimeError(
            "AI-Video CLI 執行失敗，"
            f"返回碼：{result.returncode}"
        )

    processing_fps = (
        frame_count / elapsed_time
        if elapsed_time > 0
        else 0.0
    )

    realtime_ratio = (
        processing_fps / source_fps
        if source_fps > 0
        else 0.0
    )

    print()
    print("=" * 50)
    print("Benchmark Result")
    print("=" * 50)
    print(f"Elapsed Time : {elapsed_time:.2f} sec")
    print(f"Processing FPS: {processing_fps:.2f}")
    print(f"Realtime Ratio: {realtime_ratio:.2f}x")


if __name__ == "__main__":
    main()