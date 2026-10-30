import csv
from pathlib import Path
from datetime import datetime
import cv2


def clamp_box(box, width, height):

    x1 = max(0, min(int(box.x1), width - 1))
    y1 = max(0, min(int(box.y1), height - 1))

    x2 = max(x1 + 1, min(int(box.x2), width))
    y2 = max(y1 + 1, min(int(box.y2), height))

    return x1, y1, x2, y2


def annotate(frame, box, text, confidence):

    x1, y1, x2, y2 = box

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 220, 80),
        2
    )

    label = f"{text or 'PLATE'} | OCR {confidence:.2f}"

    cv2.putText(
        frame,
        label,
        (x1, max(25, y1 - 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 220, 80),
        2
    )


def append_csv(csv_path, text, confidence, box):

    path = Path(csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    exists = path.exists()

    with path.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not exists:
            writer.writerow([
                "timestamp",
                "plate_text",
                "ocr_confidence",
                "x1", "y1", "x2", "y2"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            text,
            confidence,
            *box
        ])
