from dataclasses import dataclass
import cv2


@dataclass
class Detection:
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float = 0.0


class OpenCVPlateDetector:

    def detect(self, frame):

        gray = cv2.cvtColor(
            frame, cv2.COLOR_BGR2GRAY
        )

        gray = cv2.bilateralFilter(
            gray, 11, 17, 17
        )

        edges = cv2.Canny(
            gray, 30, 200
        )

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        contours = sorted(
            contours,
            key=cv2.contourArea,
            reverse=True
        )[:30]

        h, w = frame.shape[:2]

        results = []

        for contour in contours:

            x, y, cw, ch = cv2.boundingRect(contour)

            if ch == 0:
                continue

            ratio = cw / float(ch)
            area = cw * ch

            if 2.0 <= ratio <= 6.5 and area >= w * h * 0.0005:

                results.append(
                    Detection(
                        x,
                        y,
                        x + cw,
                        y + ch,
                        0.35
                    )
                )

        return results[:10]


class YOLOPlateDetector:

    def __init__(
        self,
        weights,
        confidence=0.25
    ):

        from ultralytics import YOLO

        self.model = YOLO(weights)
        self.confidence = confidence

    def detect(self, frame):

        results = self.model.predict(
            frame,
            conf=self.confidence,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                confidence = float(box.conf[0])

                detections.append(
                    Detection(
                        x1,
                        y1,
                        x2,
                        y2,
                        confidence
                    )
                )

        return detections
