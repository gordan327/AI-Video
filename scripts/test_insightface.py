from insightface.app import FaceAnalysis

app = FaceAnalysis(
    name="buffalo_sc",
    root="models/downloads"
)

app.prepare(ctx_id=0)

print("InsightFace 載入成功！")