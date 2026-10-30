# ANPR Dataset

This directory stores vehicle images
and number plate annotations.

## Dataset Structure

dataset/
|
|-- images/
|   |-- train/
|   |-- val/
|
|-- labels/
    |-- train/
    |-- val/

## Annotation Format

YOLO annotation format:

class_id x_center y_center width height

All coordinates must be normalized
between 0 and 1.

## Dataset Usage

The dataset is used to train
the YOLO license plate detection model.

## Important

Use legally permitted images and
properly annotated license plates.

No dataset is included currently.
