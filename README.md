This project implements a deep-learning object detection system using Ultralytics YOLOv8.
The model is trained to detect:
• Cats
• Dogs
• Daleks
• Lightsabers
• Person

The repository includes:
• A trained YOLOv8 model (runs/detect/final_model/weights/best.pt)
• Scripts for video detection and live webcam detection
• Dataset in YOLOv8 format
• All utilities needed to retrain or re-run detection

REQUIREMENTS
You need Python 3.10 or newer
To install the required dependencies run:
pip install -r requirements.txt

USAGE INSTRUCTIONS
Video Detection
Run object detection on any video:
python video_detect.py input_video.mpy output_video.mp4
The output will contain bounding boxes and labels

Live Webcam Detection
Requires a webcam or OBS virtual camera is required. Run:
python live_detect.py
Press Q to exit the script

(Note: You must change the model path at the top of either script if you retrain)

DATASET LOCATION (for retraining)
The dataset is stored in dataset_yolo

RETRAINING THE MODEL
yolo detect train model=yolov8n.pt data=dataset_yolo/data.yaml epochs=100 imgsz=640 batch=16 name=<Name>

The output will appear in:
runs/detect/<Name>/
It will include:
• best.pt - best performing weights
• last.pt = final epoch weights
• results.png - training curves
• confusion_matrix.png

VALIDATING THE MODEL
Validation on validation set
yolo detect val model=runs/detect/final_model/weights/best.pt data=dataset_yolo/data.yaml

Validation on test set
yolo detect val model=runs/detect/final_model/weights/best.pt data=dataset_yolo/data.yaml split=test


YOLO produces:
• Precision/Recall curves
• mAP metrics
• Confusion matrix
• Stats saved under runs/detect/val*/