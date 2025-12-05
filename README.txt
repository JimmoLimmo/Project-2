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
To run Video Processed Object Detection script, the syntax required is:
python video_detect.py input_video.mpy output_video.mp4

To run Live Webcam Detection script, a webcam or OBS virtual camera is required. Run:
python live_detect.py

DATASET LOCATION (for retraining)
The dataset is stored in dataset_yolo

RETRAINING THE MODEL
yolo detect train model=yolov8n.pt data=dataset_yolo/data.yaml epochs=100 imgsz=640 batch=16 name=final_model

The output will appear in:
runs/detect/final_model/

