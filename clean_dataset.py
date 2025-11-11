
import os
import cv2
import numpy as np
from PIL import Image
import imagehash
from tqdm import tqdm

# Paths
INPUT_DIR = "dataset_raw"     
MIN_SIZE = 128                 
HASH_THRESHOLD = 5           

#Check if image has low contrast.
def is_low_contrast(image, threshold=10):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray.std() < threshold

#Detect if image is mostly one color.
def is_blank(image, ratio_threshold=0.98):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    dominant_ratio = hist.max() / hist.sum()
    return dominant_ratio > ratio_threshold

def clean_folder(folder_path):
    print(f"\nCleaning folder: {folder_path}")
    seen_hashes = set()
    removed = 0

    for file_name in tqdm(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        try:
            # Load 
            with Image.open(file_path) as img:
                img.verify()  # verify no corruption

            img = Image.open(file_path).convert("RGB")
            w, h = img.size

            # Remove too small --
            if w < MIN_SIZE or h < MIN_SIZE:
                os.remove(file_path)
                removed += 1
                continue

            # Compute hash for duplicates
            hash_val = imagehash.average_hash(img)
            if any(hash_val - h2 < HASH_THRESHOLD for h2 in seen_hashes):
                os.remove(file_path)
                removed += 1
                continue
            seen_hashes.add(hash_val)

            # Check for blank/low-contrast
            arr = np.array(img)
            if is_blank(arr) or is_low_contrast(arr):
                os.remove(file_path)
                removed += 1
                continue

        except Exception as e:
            # Remove
            try:
                os.remove(file_path)
                removed += 1
            except:
                pass

    print(f"Done. Removed {removed} unusable images from '{folder_path}'.")

def main():
    print("Starting dataset cleanup...")
    for subfolder in os.listdir(INPUT_DIR):
        full_path = os.path.join(INPUT_DIR, subfolder)
        if os.path.isdir(full_path):
            clean_folder(full_path)
    print("\nDataset cleaning complete!")

if __name__ == "__main__":
    main()
