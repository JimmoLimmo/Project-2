"""
clean_dataset.py

Utility script for cleaning the raw dataset before training.
Removes:
- Tiny images
- Low-contrast images
- Blank images
- Perceptual duplicates using image hashing

"""

import os
import sys
import cv2
import numpy as np
from PIL import Image
import imagehash
from tqdm import tqdm

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(ROOT_DIR, "dataset_raw")

MIN_SIZE = 128
HASH_THRESHOLD = 5


def is_low_contrast(image, threshold: int = 10) -> bool:
    """
    Return True if the image has very low contrast.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray.std() < threshold


def is_blank(image, ratio_threshold: float = 0.98) -> bool:
    """
    Return True if an image is almost a single solid color.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    dominant_ratio = hist.max() / hist.sum()
    return dominant_ratio > ratio_threshold


def collect_all_images(root: str):
    """
    Recursively yield all image file paths under a given directory.
    """
    for r, _, files in os.walk(root):
        for file in files:
            yield os.path.join(r, file)


def clean_dataset():
    """
    Main dataset cleanup function.
    Removes unusable images and prints summary.
    """
    print("\nStarting dataset cleanup...")

    global_hashes = set()
    removed = 0

    all_files = list(collect_all_images(INPUT_DIR))
    print(f"Found {len(all_files)} total images\n")

    for file_path in tqdm(all_files):
        try:
            img = Image.open(file_path)
            img.verify()  # quick validation
            img = Image.open(file_path).convert("RGB")

            # Remove very small images
            if img.width < MIN_SIZE or img.height < MIN_SIZE:
                os.remove(file_path)
                removed += 1
                continue

            # Duplicate detection
            h = imagehash.average_hash(img)
            if any(abs(h - old) < HASH_THRESHOLD for old in global_hashes):
                os.remove(file_path)
                removed += 1
                continue
            global_hashes.add(h)

            # Convert to numpy for OpenCV checks
            arr = np.array(img)

            if is_low_contrast(arr) or is_blank(arr):
                os.remove(file_path)
                removed += 1
                continue

        except Exception:
            # Fallback: file unreadable → delete
            try:
                os.remove(file_path)
                removed += 1
            except Exception:
                pass

    print(f"\nCleanup complete! Removed {removed} unusable images.\n")


if __name__ == "__main__":
    clean_dataset()
