import pytest

from ai_video.tracking.kalman_filter import KalmanFilter


def test_initiate_sets_position_and_zero_velocity():
    kalman = KalmanFilter()

    kalman.initiate(100, 200)

    assert kalman.state[0, 0] == pytest.approx(100.0)
    assert kalman.state[1, 0] == pytest.approx(200.0)
    assert kalman.state[2, 0] == pytest.approx(0.0)
    assert kalman.state[3, 0] == pytest.approx(0.0)


def test_first_prediction_keeps_same_position():
    kalman = KalmanFilter()
    kalman.initiate(100, 200)

    predicted_x, predicted_y = kalman.predict()

    assert predicted_x == pytest.approx(100.0)
    assert predicted_y == pytest.approx(200.0)


def test_update_moves_state_toward_measurement():
    kalman = KalmanFilter()
    kalman.initiate(100, 200)
    kalman.predict()

    kalman.update(102, 201)

    assert 100.0 < kalman.state[0, 0] < 102.0
    assert 200.0 < kalman.state[1, 0] < 201.0


def test_update_estimates_positive_velocity():
    kalman = KalmanFilter()
    kalman.initiate(100, 200)
    kalman.predict()

    kalman.update(102, 201)

    assert kalman.state[2, 0] > 0
    assert kalman.state[3, 0] > 0


def test_second_prediction_uses_estimated_velocity():
    kalman = KalmanFilter()
    kalman.initiate(100, 200)
    kalman.predict()
    kalman.update(102, 201)

    current_x = kalman.state[0, 0]
    current_y = kalman.state[1, 0]

    predicted_x, predicted_y = kalman.predict()

    assert predicted_x > current_x
    assert predicted_y > current_y