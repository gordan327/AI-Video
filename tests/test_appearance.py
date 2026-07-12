import numpy as np
import pytest

from ai_video.appearance import cosine_similarity


def test_same_embedding():
    e = np.array([1.0, 0.0, 0.0])

    assert cosine_similarity(e, e) == pytest.approx(1.0)


def test_orthogonal_embedding():
    e1 = np.array([1.0, 0.0, 0.0])
    e2 = np.array([0.0, 1.0, 0.0])

    assert cosine_similarity(e1, e2) == pytest.approx(0.0)


def test_opposite_embedding():
    e1 = np.array([1.0, 0.0, 0.0])
    e2 = np.array([-1.0, 0.0, 0.0])

    assert cosine_similarity(e1, e2) == pytest.approx(-1.0)


def test_none_embedding():
    e = np.array([1.0, 0.0, 0.0])

    assert cosine_similarity(None, e) == 0.0
    assert cosine_similarity(e, None) == 0.0


def test_zero_vector():
    e1 = np.array([0.0, 0.0, 0.0])
    e2 = np.array([1.0, 0.0, 0.0])

    assert cosine_similarity(e1, e2) == 0.0