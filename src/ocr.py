class PlateOCR:

    def __init__(self, languages=None, gpu=False):

        import easyocr

        self.reader = easyocr.Reader(
            languages or ["en"],
            gpu=gpu
        )

    def read(self, image):

        if image is None or image.size == 0:
            return "", 0.0

        results = self.reader.readtext(image)

        if not results:
            return "", 0.0

        best = max(
            results,
            key=lambda item: float(item[2])
        )

        text = "".join(
            char for char in best[1].upper()
            if char.isalnum()
        )

        confidence = float(best[2])

        return text, confidence
