import cv2


def enhance_plate(plate):

    if plate is None or plate.size == 0:
        return plate

    gray = cv2.cvtColor(
        plate,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.bilateralFilter(
        gray,
        9,
        75,
        75
    )

    return gray
