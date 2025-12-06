# Project 2

This project implements a deep-learning object detection system using **Ultralytics YOLOv8**.

## Supported Classes
- Cats  
- Dogs  
- Daleks  
- Lightsabers  
- Person  

---

# Repository Contents
- `runs/detect/final_model/weights/best.pt` — trained YOLOv8 model  
- `video_detect.py` — video inference  
- `live_detect.py` — webcam inference  
- Dataset in YOLOv8 format (`dataset_yolo/`)  
- Scripts/utilities for retraining and evaluation  

---

# Requirements
You need **Python 3.10 or newer**.

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Usage Instructions
## Video Detection
Run object detection on any video:
```bash
python video_detect.py input_video.mp4 output_video.mp4
```
The output video will contain bounding boxes and labels.

## Live Webcam Detection
Requires a webcam or OBS Virtual Camera:
```bash
python live_detect.py
```
Press Q to exit the script.

Note: Update the model path inside the script if you retrain the model.

---

# Dataset Location (for Retraining)
The dataset is stored in:
```bash
dataset_yolo/
```
Be sure the dataset you use is in YoloV8 format

# Retraining the Model
To retrain YOLOv8:
```bash
yolo detect train model=yolov8n.pt data=dataset_yolo/data.yaml epochs=100 imgsz=640 batch=16 name=<model_name>
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

---

# Validating the Model

## Validation on validation set
```bash
yolo detect val model=runs/detect/<model_name>/weights/best.pt data=dataset_yolo/data.yaml
```

## Validation on test set
```bash
yolo detect val model=runs/detect/<model_name>/weights/best.pt data=dataset_yolo/data.yaml split=test
```

YOLO generates:
- Precision/Recall curves
- mAP metrics
- Confusion matrix
- Validation stats under runs/detect/val*/

---

# Dataset Preparation & Utilities
You can prepare your dataset anyway you want. I created image scraping and processing scripts if you'd like to use them. You can edit the categories to fit the needs of your model.

Here is what is required if you'd like to use my scripts.

### Create a .env file for Google Images API (REQUIRED FOR SCRAPING)
Inside the root folder:
```bash
GOOGLE_API_KEY=YOUR_API_KEY_HERE
GOOGLE_CX_ID=YOUR_CX_ID_HERE
```
This is required for image_scraper.py to work.

### Create a Google Cloud Project
1. Go to: https://console.cloud.google.com/
2. Sign in with your Google account.
3. Click Select Project → New Project
4. Name it anything (e.g., YOLO-Scraper).

### Enable the Custom Search API
1. Open the API Library: https://console.cloud.google.com/apis/library
2. Search for Custom Search API
3. Click Enable

### Create an API Key
1. Go to Credentials: https://console.cloud.google.com/apis/credentials
2. Click Create Credentials → API Key
3. Copy the generated key — this is your:
```bash
GOOGLE_API_KEY=your_key_here
```
Note that Google has a limit for the free tier. 

### Create a Custom Search Engine (CSE)
1. Go to the CSE dashboard: https://cse.google.com/cse/all
2. Click Add
3. For "Sites to search", enter: 
```bash
www.google.com
```
4. Click Create

From here you can change your search engine settings

### Enable Image Search for your CSE
1. Open your CSE 
2. Go to Setup 
3. Go to Basics
4. Toggle Image Search
5. Save

### Get Your CX ID
While still in your CSE settings:
1. Go to Setup
2. Under Details, you'll see something like: 
```bash
Search engine ID: 1234567890abcdef:xyz123abc
```
This goes in your 
```bash
GOOGLE_CX_ID=your_cx_here
```
---
If everything works your images will be downloaded into 
```bash
dataset_raw/<class>/<timestamp>/
```
## Recommended Workflow

### **Step 1 — Scrape images**  
```bash
python scripts/image_scraper.py
```

### **Step 2 - Clean Dataset**
```bash
python scripts/dataset_cleaner.py
```

### **Step 3 - Resize Images**
```bash
python scripts/dataset_resizer.py
```


### **Step 4 - Normalize Filename Length**
```bash
python scripts/filename_shortener.py
```

### **Step 5 - Import Images to Roboflow and Start Labeling!** 