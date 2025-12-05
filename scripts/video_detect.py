"""
video_detect.py

Runs YOLOv8 object detection on a video file and writes an annotated output
video with bounding boxes and class labels.

Usage:
    python scripts/video_detect.py input_video.mp4 output_video.mp4

Notes:
- Paths may be absolute or relative to the project root.
- The model path is fixed to runs/detect/final/weights/best.pt by default.
"""

import os
import sys
import cv2
from ultralytics import YOLO


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT_DIR, "runs", "detect", "final", "weights", "best.pt")


def annotate_video(input_path: str, output_path: str) -> None:
    """
    Run object detection on a video and save an annotated copy.

    Args:
        input_path: Path to input video file.
        output_path: Path to output annotated video file.
    """
    # Load YOLO model
    model = YOLO(MODEL_PATH)

    # Open input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open input video: {input_path}")

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    print(f"Processing video: {input_path}")
    print(f"Saving annotated video to: {output_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO on this frame
        results = model(frame, imgsz=640, conf=0.5, verbose=False)
        result = results[0]

        # Draw all detections
        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cls_id = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())
                label = f"{model.names[cls_id]} {conf:.2f}"

                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2,
                )

                (tw, th), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
                )
                cv2.rectangle(
                    frame,
                    (int(x1), int(y1) - th - 4),
                    (int(x1) + tw, int(y1)),
                    (0, 255, 0),
                    -1,
                )
                cv2.putText(
                    frame,
                    label,
                    (int(x1), int(y1) - 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )

        out.write(frame)
        frame_idx += 1
        if frame_idx % 30 == 0:
            print(f"Processed {frame_idx} frames...")

    cap.release()
    out.release()
    print("Done!")


def main() -> None:
    """
    CLI entry point for the script.
    """
    if len(sys.argv) != 3:
        print("Usage: python scripts/video_detect.py input.mp4 output.mp4")
        sys.exit(1)

    input_video = sys.argv[1]
    output_video = sys.argv[2]

    if not os.path.exists(input_video):
        print(f"Input video not found: {input_video}")
        sys.exit(1)

    annotate_video(input_video, output_video)


if __name__ == "__main__":
    main()
