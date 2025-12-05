"""
live_detect.py

Runs live webcam object detection using a trained YOLOv8 model.
"""

import os
import cv2
from ultralytics import YOLO


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT_DIR, "runs", "detect", "final", "weights", "best.pt")


def run_realtime(camera_index: int = 0):
    """
    Run webcam inference using YOLOv8.

    Args:
        camera_index (int): Camera device index.
    """
    model = YOLO(MODEL_PATH)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {camera_index}")

    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, imgsz=416, conf=0.5, verbose=False)
        result = results[0]

        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cls_id = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())
                label = f"{model.names[cls_id]} {conf:.2f}"

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(frame, (int(x1), int(y1) - th - 4), (int(x1) + tw, int(y1)), (0, 255, 0), -1)
                cv2.putText(frame, label, (int(x1), int(y1) - 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        cv2.imshow("YOLOv8 Live Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_realtime()
