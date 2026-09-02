from ai_video.kalman_filter import KalmanFilter


kf = KalmanFilter()

print("初始化")

kf.initiate(100, 200)

print("State =", kf.state.ravel())

print()

print("Prediction 1")

print(kf.predict())

print()

print("Update")

kf.update(102, 201)

print(kf.state.ravel())

print()

print("Prediction 2")

print(kf.predict())