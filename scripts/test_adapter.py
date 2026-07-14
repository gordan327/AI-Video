from ai_video.face import Face
from ai_video.detector.face_detection_adapter import FaceDetectionAdapter

adapter = FaceDetectionAdapter()

faces = [
    Face(
        x1=10,
        y1=20,
        x2=100,
        y2=150,
        confidence=0.95,
    )
]

detections = adapter.to_detections(faces)

print(detections)
print(detections.xyxy)
print(detections.confidence)
print(detections.class_id)