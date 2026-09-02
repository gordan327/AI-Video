import cv2

from insightface.app import FaceAnalysis

app = FaceAnalysis(
    name="buffalo_sc",
    root="models/downloads",
)

app.prepare(ctx_id=0)

image = cv2.imread("videos/test.jpg")

faces = app.get(image)

print(f"偵測到 {len(faces)} 張人臉")

if len(faces) > 0:
    print(type(faces[0]))
    print(dir(faces[0]))