"""
resize_images.py

Resizes all raw dataset images to a standard resolution and preserves the
timestamp folder structure.

Outputs normalized .jpg files in dataset_resized/.
"""

import os
from PIL import Image


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT_DIR, "dataset_raw")
OUT_DIR = os.path.join(ROOT_DIR, "dataset_resized")

TARGET_SIZE = (416, 416)
VALID_EXT = (".jpg", ".jpeg", ".png", ".pjpeg")

os.makedirs(OUT_DIR, exist_ok=True)


def resize_all():
    """
    Resize images to TARGET_SIZE while preserving the directory structure.
    """
    print("Resizing dataset...")

    for root, _, files in os.walk(RAW_DIR):
        for file in files:
            if not file.lower().endswith(VALID_EXT):
                continue

            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, RAW_DIR)
            out_dir = os.path.join(OUT_DIR, rel_path)
            os.makedirs(out_dir, exist_ok=True)

            base = os.path.splitext(file)[0]
            out_file = base + ".jpg"
            out_path = os.path.join(out_dir, out_file)

            counter = 1
            while os.path.exists(out_path):
                out_file = f"{base}_{counter}.jpg"
                out_path = os.path.join(out_dir, out_file)
                counter += 1

            try:
                img = Image.open(src_path).convert("RGB")
                img = img.resize(TARGET_SIZE)
                img.save(out_path, "JPEG")
            except Exception as e:
                print(f"Skipping {src_path}: {e}")

    print("Resize complete.")


if __name__ == "__main__":
    resize_all()
