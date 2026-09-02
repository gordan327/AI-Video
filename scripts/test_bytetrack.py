import supervision as sv

print("Supervision:", sv.__version__)

tracker = sv.ByteTrack()

print(type(tracker))

print(dir(tracker))