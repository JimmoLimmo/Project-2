Object Detection Using YOLOv8






This project implements a deep-learning object detection system using Ultralytics YOLOv8.
The model detects the following classes:

Cats

Dogs

Daleks

Lightsabers

Persons

Table of Contents

Features

Repository Contents

Requirements

Installation

Usage

Video Detection

Live Webcam Detection

Dataset Structure

Retraining the Model

Validating the Model

Project Deliverables Notes

Features

✔ Real-time webcam object detection
✔ Video file detection and annotation
✔ Custom YOLOv8 model trained on a multi-class dataset
✔ Includes scripts to retrain, validate, and run inference
✔ Dataset provided in YOLOv8 format

Repository Contents
├── dataset_yolo/                # Training, validation, test sets + data.yaml
├── runs/detect/final_model/     # Trained YOLOv8 model weights
├── video_detect.py              # Video detection script
├── live_detect.py               # Webcam detection script
├── requirements.txt             # Python dependencies
├── test3.mp4                    # Example test video
└── README.md                    # Documentation

Requirements

You must have Python 3.10 or newer installed.

YOLOv8 requires:

torch

ultralytics

opencv-python

numpy

matplotlib

Installation

Install all required dependencies:

pip install -r requirements.txt


If YOLO is not installed, run:

pip install ultralytics

Usage
1. Video Detection

To run object detection on any video:

python video_detect.py input_video.mp4 output_video.mp4


The output video will contain bounding boxes and class labels.

2. Live Webcam Detection

Requires a webcam or OBS virtual camera:

python live_detect.py


Press Q to exit the live detection window.

Dataset Structure

The dataset is stored in dataset_yolo/ and follows YOLOv8 conventions:

dataset_yolo/
│
├── train/
│   ├── images/
│   └── labels/
│
├── valid/
│   ├── images/
│   └── labels/
│
├── test/
│   ├── images/
│   └── labels/
│
└── data.yaml


data.yaml contains:

train: dataset_yolo/train/images
val: dataset_yolo/valid/images
test: dataset_yolo/test/images

names:
  0: cat
  1: dog
  2: dalek
  3: lightsaber
  4: person
  5: sith_lightsaber

Retraining the Model

To retrain YOLOv8 from scratch:

yolo detect train model=yolov8n.pt data=dataset_yolo/data.yaml epochs=100 imgsz=640 batch=16 name=final_model


Training output will be saved to:

runs/detect/final_model/


This includes:

best.pt — best performing weights

last.pt — last epoch weights

results.png — training curves

confusion_matrix.png

Validating the Model
Validation on validation set
yolo detect val model=runs/detect/final_model/weights/best.pt data=dataset_yolo/data.yaml

Validation on test set
yolo detect val model=runs/detect/final_model/weights/best.pt data=dataset_yolo/data.yaml split=test


YOLO will produce:

Precision/Recall curves

mAP metrics

Confusion matrix

Stats in runs/detect/val*/
