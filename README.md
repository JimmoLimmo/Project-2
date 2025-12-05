## Project 2

This project implements a deep-learning object detection system using **Ultralytics YOLOv8**.

## Supported Classes
- Cats  
- Dogs  
- Daleks  
- Lightsabers  
- Person  

---

## Repository Contents
- `runs/detect/final_model/weights/best.pt` — trained YOLOv8 model  
- `video_detect.py` — video inference  
- `live_detect.py` — webcam inference  
- Dataset in YOLOv8 format (`dataset_yolo/`)  
- Scripts/utilities for retraining and evaluation  

---

## Requirements
You need **Python 3.10 or newer**.

Install dependencies:

```bash
pip install -r requirements.txt
```
## Usage Instructions
# Video Detection
Run object detection on any video:
```bash
python video_detect.py input_video.mp4 output_video.mp4
```
The output video will contain bounding boxes and labels.

# Live Webcam Detection
Requires a webcam or OBS Virtual Camera:
```bash
python live_detect.py
```
Press Q to exit the script.

Note: Update the model path inside the script if you retrain the model.

### Dataset Location (for Retraining)
The dataset is stored in:
```bash
dataset_yolo/
```
### Retraining the Model
To retrain YOLOv8:
```bash
yolo detect train model=yolov8n.pt data=dataset_yolo/data.yaml epochs=100 imgsz=640 batch=16 name=<Name>
```
Training output will be saved in:
```bash
runs/detect/<Name>/
```
This includes:
- best.pt — best performing weights
- last.pt — final epoch weights
- results.png — training curves
- confusion_matrix.png

## Validating the Model
# Validation on validation set
```bash
yolo detect val model=runs/detect/final_model/weights/best.pt data=dataset_yolo/data.yaml
```

# Validation on test set
```bash
yolo detect val model=runs/detect/final_model/weights/best.pt data=dataset_yolo/data.yaml split=test
```

YOLO generates:
- Precision/Recall curves
- mAP metrics
- Confusion matrix
- Validation stats under runs/detect/val*/