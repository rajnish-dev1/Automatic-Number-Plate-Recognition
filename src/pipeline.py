from pathlib import Path
import cv2

from .detection import (
    OpenCVPlateDetector,
    YOLOPlateDetector
)

from .ocr import PlateOCR
from .preprocessing import enhance_plate

from .utils import (
    clamp_box,
    annotate,
    append_csv
)


class ANPRPipeline:

    def __init__(
        self,
        mode="opencv",
        weights="models/license_plate_detector.pt",
        confidence=0.25,
        languages=None,
        gpu=False,
        output_dir="output",
        csv_file="detections.csv"
    ):

        if mode == "opencv":
            self.detector = OpenCVPlateDetector()

        elif mode == "yolo":
            self.detector = YOLOPlateDetector(
                weights,
                confidence
            )

        else:
            raise ValueError("Invalid detection mode")

        self.ocr = PlateOCR(languages, gpu)

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.csv_path = self.output_dir / csv_file

    def process_frame(self, frame):

        annotated = frame.copy()

        height, width = frame.shape[:2]

        for detection in self.detector.detect(frame):

            box = clamp_box(
                detection,
                width,
                height
            )

            x1, y1, x2, y2 = box

            plate = frame[y1:y2, x1:x2]

            enhanced = enhance_plate(plate)

            text, confidence = self.ocr.read(enhanced)

            annotate(
                annotated,
                box,
                text,
                confidence
            )

            if text:
                append_csv(
                    self.csv_path,
                    text,
                    confidence,
                    box
                )

        return annotated

    def process_image(self, source):

        frame = cv2.imread(str(source))

        if frame is None:
            raise FileNotFoundError(
                f"Image not found: {source}"
            )

        result = self.process_frame(frame)

        output = (
            self.output_dir /
            f"annotated_{Path(source).stem}.jpg"
        )

        cv2.imwrite(str(output), result)

        return output

    def process_video(self, source, show=False):

        cap = cv2.VideoCapture(
            int(source) if str(source).isdigit()
            else str(source)
        )

        if not cap.isOpened():
            raise RuntimeError("Cannot open video")

        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

        width = int(
            cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        output = (
            self.output_dir /
            "annotated_video.mp4"
        )

        writer = cv2.VideoWriter(
            str(output),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        try:
            while True:

                success, frame = cap.read()

                if not success:
                    break

                result = self.process_frame(frame)

                writer.write(result)

                if show:

                    cv2.imshow(
                        "ANPR System",
                        result
                    )

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

        finally:
            cap.release()
            writer.release()
            cv2.destroyAllWindows()

        return output
