import os
import cv2
import numpy as np
from PIL import Image
import imagehash
from tqdm import tqdm

INPUT_DIR = "dataset_raw"
MIN_SIZE = 128
HASH_THRESHOLD = 5


def is_low_contrast(image, threshold=10):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray.std() < threshold


def is_blank(image, ratio_threshold=0.98):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    dominant_ratio = hist.max() / hist.sum()
    return dominant_ratio > ratio_threshold


def collect_all_images(root):
    """Yield file paths for ALL images under root (recursive)."""
    for root, dirs, files in os.walk(root):
        for file in files:
            yield os.path.join(root, file)


def clean_dataset():
    print("\n Starting dataset cleanup...")
    global_hashes = set()
    removed = 0

    all_files = list(collect_all_images(INPUT_DIR))
    print(f"Found {len(all_files)} total images\n")

    for file_path in tqdm(all_files):
        try:
            img = Image.open(file_path)
            img.verify()
            img = Image.open(file_path).convert("RGB")

            # Check small resolution
            if img.width < MIN_SIZE or img.height < MIN_SIZE:
                os.remove(file_path)
                removed += 1
                continue

            # Hash check
            h = imagehash.average_hash(img)
            if any(abs(h - old) < HASH_THRESHOLD for old in global_hashes):
                os.remove(file_path)
                removed += 1
                continue
            global_hashes.add(h)

            # OpenCV checks
            arr = np.array(img)
            if is_low_contrast(arr) or is_blank(arr):
                os.remove(file_path)
                removed += 1
                continue

        except:
            # Unable to open -> delete
            try:
                os.remove(file_path)
                removed += 1
            except:
                pass

    print(f"\n Cleanup complete! Removed {removed} unusable images.\n")


if __name__ == "__main__":
    clean_dataset()
