
import sys
import os
import cv2
from ultralytics import YOLO

#path to model
MODEL_PATH = "runs/detect/final_model/weights/best.pt"

def annotate_video(input_path, output_path):
    #load model
    model = YOLO(MODEL_PATH)

    #open input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open input video: {input_path}")

    #get video properties
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # output codec

    #create VideoWriter for output
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    print(f"Processing video: {input_path}")
    print(f"Saving annotated video to: {output_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #run YOLO on this frame
        results = model(frame, imgsz=640, conf=0.5, verbose=False)
        result = results[0]

        #draw all detections (this is where multi-object happens)
        if result.boxes is not None:
            for box in result.boxes:
                # xyxy = [x1, y1, x2, y2]
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cls_id = int(box.cls[0].cpu().numpy())
                conf   = float(box.conf[0].cpu().numpy())

                label = f"{model.names[cls_id]} {conf:.2f}"

                #draw rectangle
                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )

                #draw label background
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                cv2.rectangle(
                    frame,
                    (int(x1), int(y1) - th - 4),
                    (int(x1) + tw, int(y1)),
                    (0, 255, 0),
                    -1
                )

                #draw label text
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
    print("Done!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python video_detect.py input.mp4 output.mp4")
        sys.exit(1)

    input_video = sys.argv[1]
    output_video = sys.argv[2]

    if not os.path.exists(input_video):
        print(f"Input video not found: {input_video}")
        sys.exit(1)

    annotate_video(input_video, output_video)
