from pathlib import Path
import sys

import cv2


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

from ai_video.config_manager import ConfigManager
from ai_video.detector.detector_factory import DetectorFactory
from ai_video.model_manager import ModelManager


def main():
    """讀取影片第一張影格，執行人臉偵測並輸出偵測框圖片。"""

    video_path = PROJECT_ROOT / "input" / "demo.mp4"
    output_dir = PROJECT_ROOT / "output" / "debug"

    original_output_path = output_dir / "frame_000001.jpg"
    detected_output_path = (
        output_dir / "frame_000001_detected.jpg"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise RuntimeError(
            f"Cannot open video: {video_path}"
        )

    success, frame = capture.read()

    capture.release()

    if not success or frame is None:
        raise RuntimeError(
            "Cannot read first frame."
        )

    if not cv2.imwrite(
        str(original_output_path),
        frame,
    ):
        raise RuntimeError(
            f"Cannot save image: {original_output_path}"
        )

    print(f"Saved: {original_output_path}")

    config = ConfigManager()
    model_manager = ModelManager(config)

    detector = DetectorFactory.create(
        detector_type=config.get(
            "detector.type",
            "scrfd",
        ),
        model_manager=model_manager,
        config=config,
    )

    detections = detector.detect(frame)

    faces_dir = output_dir / "faces"
    faces_dir.mkdir(exist_ok=True)
    
    detected_frame = frame.copy()

    detected_frame = frame.copy()

    height, width = frame.shape[:2]

    for index, face in enumerate(
        detections,
        start=1,
    ):
        x1 = max(face.x1, 0)
        y1 = max(face.y1, 0)
        x2 = min(face.x2, width)
        y2 = min(face.y2, height)

        #
        # 儲存裁切的人臉
        #
        face_image = frame[y1:y2, x1:x2]

        face_path = (
            faces_dir
            / f"face_{index:02d}.jpg"
        )

        cv2.imwrite(
            str(face_path),
            face_image,
        )

        #
        # 畫偵測框
        #
        cv2.rectangle(
            detected_frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            3,
        )

        cv2.putText(
            detected_frame,
            str(index),
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    if not cv2.imwrite(
        str(detected_output_path),
        detected_frame,
    ):
        raise RuntimeError(
            f"Cannot save image: {detected_output_path}"
        )

    print(f"Saved: {detected_output_path}")
    print(
        f"Detector         : "
        f"{type(detector).__name__}"
    )
    print(
        f"Detections type  : "
        f"{type(detections)}"
    )
    print(
        f"Detected faces   : "
        f"{len(detections)}"
    )

    print(f"Saved faces      : {faces_dir}")
    
    for index, face in enumerate(
        detections,
        start=1,
    ):
        print(
            f"Face {index}: "
            f"bbox=({face.x1}, {face.y1}, "
            f"{face.x2}, {face.y2}), "
            f"confidence={face.confidence:.4f}"
        )


if __name__ == "__main__":
    main()