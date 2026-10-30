import argparse
from pathlib import Path
import yaml

from src.pipeline import ANPRPipeline


def main():

    parser = argparse.ArgumentParser(
        description="Automatic Number Plate Recognition"
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Image, video path or webcam index"
    )

    parser.add_argument(
        "--mode",
        choices=["opencv", "yolo"],
        default=None
    )

    parser.add_argument(
        "--weights",
        default=None
    )

    parser.add_argument(
        "--languages",
        nargs="+",
        default=None
    )

    parser.add_argument(
        "--show",
        action="store_true"
    )

    parser.add_argument(
        "--config",
        default="config.yaml"
    )

    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    detection = config.get("detection", {})
    ocr = config.get("ocr", {})
    output = config.get("output", {})

    mode = args.mode or detection.get("mode", "opencv")

    weights = (
        args.weights or
        detection.get(
            "weights",
            "models/license_plate_detector.pt"
        )
    )

    pipeline = ANPRPipeline(
        mode=mode,
        weights=weights,
        confidence=detection.get("confidence", 0.25),
        languages=args.languages or ["en"],
        gpu=ocr.get("gpu", False),
        output_dir=output.get("directory", "output"),
        csv_file=output.get("csv_file", "detections.csv")
    )

    source = args.source

    suffix = (
        Path(source).suffix.lower()
        if not source.isdigit()
        else ""
    )

    image_extensions = [
        ".jpg", ".jpeg", ".png", ".bmp", ".webp"
    ]

    if suffix in image_extensions:
        result = pipeline.process_image(source)
    else:
        result = pipeline.process_video(
            source,
            show=args.show
        )

    print("ANPR Processing Completed!")
    print("Output:", result)


if __name__ == "__main__":
    main()
