import sys
import os
import cv2
import subprocess
from ultralytics import YOLO

# Path to the trained YOLO weights
MODEL_PATH = "runs/detect/train7/weights/best.pt"

def annotate_video(input_path, output_path):
    temp_video_no_audio = "temp_no_audio.mp4"

    # Load YOLO model
    model = YOLO(MODEL_PATH)

    # Open input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open input video: {input_path}")

    # Get video properties
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Create writer for frame output (no audio)
    out = cv2.VideoWriter(temp_video_no_audio, fourcc, fps, (width, height))

    print(f"Processing video: {input_path}")

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO detection on this frame
        results = model(frame, imgsz=640, conf=0.5, verbose=False)
        result = results[0]

        # Draw detection boxes
        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cls_id = int(box.cls[0].cpu().numpy())
                conf   = float(box.conf[0].cpu().numpy())

                label = f"{model.names[cls_id]} {conf:.2f}"

                # Rectangle (green)
                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )

                # Text label
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(
                    frame,
                    (int(x1), int(y1) - th - 4),
                    (int(x1) + tw, int(y1)),
                    (0, 255, 0),
                    -1
                )
                cv2.putText(
                    frame,
                    label,
                    (int(x1), int(y1) - 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA
                )

        out.write(frame)
        frame_idx += 1
        if frame_idx % 30 == 0:
            print(f"Processed {frame_idx} frames...")

    cap.release()
    out.release()
    print("Frame annotation complete, restoring audio...")

    # Merge original audio back into final output
    cmd = [
        "ffmpeg", "-i", input_path, "-i", temp_video_no_audio,
        "-c:a", "copy", "-c:v", "copy", output_path, "-y"
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(temp_video_no_audio)

    print("Done! Output video has original audio.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python video_detect.py input.mp4 output.mp4")
        sys.exit(1)

    input_video  = sys.argv[1]
    output_video = sys.argv[2]

    if not os.path.exists(input_video):
        print(f"Input video not found: {input_video}")
        sys.exit(1)

    annotate_video(input_video, output_video)
