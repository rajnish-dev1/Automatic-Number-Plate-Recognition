import numpy as np

from src.detection import OpenCVPlateDetector
from src.preprocessing import enhance_plate


def test_detector():

    image = np.zeros(
        (240, 640, 3),
        dtype=np.uint8
    )

    detector = OpenCVPlateDetector()

    result = detector.detect(image)

    assert isinstance(result, list)


def test_preprocessing():

    image = np.zeros(
        (30, 100, 3),
        dtype=np.uint8
    )

    result = enhance_plate(image)

    assert result is not None

    assert result.shape[0] > 0
