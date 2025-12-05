"""
shorten_filenames.py

Utility to shorten overly long filenames in the YOLO dataset directories.

Long filenames can cause:
- Filesystem limitations
- Issues with tools that assume shorter paths

This script trims base names and avoids collisions by appending counters.
"""

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAX_LEN = 80  # Maximum allowed filename length (including extension)
DATASET_DIRS = [
    os.path.join(ROOT_DIR, "dataset_yolo", "train", "images"),
    os.path.join(ROOT_DIR, "dataset_yolo", "valid", "images"),
    os.path.join(ROOT_DIR, "dataset_yolo", "test", "images"),
]


def shorten_dir(path: str) -> None:
    """
    Shorten filenames in a single directory if they exceed MAX_LEN characters.

    Args:
        path: Directory containing images.
    """
    if not os.path.exists(path):
        return

    print(f"\nScanning: {path}")
    for file_name in os.listdir(path):
        if len(file_name) <= MAX_LEN:
            continue

        name, ext = os.path.splitext(file_name)
        trimmed = name[:60]  # base name trim length
        new_file = trimmed + ext

        final_name = new_file
        counter = 1
        while os.path.exists(os.path.join(path, final_name)):
            final_name = f"{trimmed}_{counter}{ext}"
            counter += 1

        src = os.path.join(path, file_name)
        dst = os.path.join(path, final_name)
        os.rename(src, dst)
        print(f"Renamed: {file_name} → {final_name}")


def shorten_all() -> None:
    """
    Apply filename shortening to all configured dataset image directories.
    """
    for directory in DATASET_DIRS:
        shorten_dir(directory)

    print("\nFilename shortening complete.")


if __name__ == "__main__":
    shorten_all()
