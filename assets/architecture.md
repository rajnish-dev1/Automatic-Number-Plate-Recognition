# ANPR System Architecture

```mermaid
flowchart TD
    A[Input Image / Video / Webcam]
    B[Frame Extraction]
    C[Image Preprocessing]
    D{Detection Mode}
    E[OpenCV Detection]
    F[YOLO Detection]
    G[Number Plate Localization]
    H[Plate Cropping]
    I[Image Enhancement]
    J[EasyOCR Recognition]
    K[Text Processing]
    L[Recognized Vehicle Number]
    M[Annotated Output]
    N[CSV Result Storage]

    A --> B
    B --> C
    C --> D
    D -->|Mode 1| E
    D -->|Mode 2| F
    E --> G
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    L --> N
