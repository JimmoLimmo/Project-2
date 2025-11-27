import os
from PIL import Image

RAW_DIR = "dataset_raw"
OUT_DIR = "dataset_resized"
TARGET_SIZE = (416, 416)
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".pjpeg")

os.makedirs(OUT_DIR, exist_ok=True)

def resize_all():
    print("Resizing images and preserving timestamp folders...")

    for root, dirs, files in os.walk(RAW_DIR):
        for file in files:
            if not file.lower().endswith(VALID_EXTENSIONS):
                continue
            
            src_path = os.path.join(root, file)

            # Get relative path
            rel_path = os.path.relpath(root, RAW_DIR)
            parts = rel_path.split(os.sep)

            # Determine class and timestamp
            class_name = parts[0] if len(parts) > 0 else None
            timestamp = parts[1] if len(parts) > 1 else None

            if class_name is None:
                continue

            # Output directory preserves timestamp folder
            if timestamp:
                class_out_dir = os.path.join(OUT_DIR, class_name, timestamp)
            else:
                class_out_dir = os.path.join(OUT_DIR, class_name)

            os.makedirs(class_out_dir, exist_ok=True)

            # Normalize extension to .jpg
            base_name = os.path.splitext(file)[0]
            out_name = base_name + ".jpg"
            out_path = os.path.join(class_out_dir, out_name)

            # Prevent collisions
            counter = 1
            while os.path.exists(out_path):
                out_name = f"{base_name}_{counter}.jpg"
                out_path = os.path.join(class_out_dir, out_name)
                counter += 1

            try:
                img = Image.open(src_path).convert("RGB")
                img = img.resize(TARGET_SIZE)
                img.save(out_path, "JPEG")
            except Exception as e:
                print(f"Skipping {src_path}: {e}")

    print("\nResize complete! Files saved to:", OUT_DIR)


if __name__ == "__main__":
    resize_all()
