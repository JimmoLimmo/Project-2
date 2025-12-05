"""
scrape_images.py

Google Images scraping utility for building the raw dataset.

Features:
- Uses Google Custom Search API to download images for each class
- Avoids duplicates via perceptual hashing (imagehash)
- Organizes downloads in dataset_raw/<class>/<timestamp>/ folders

Environment variables required (in a .env file at project root):
    GOOGLE_API_KEY
    GOOGLE_CX_ID
"""

import os
import time
import imagehash
from typing import Dict, List

from PIL import Image
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch


# -------------------------------------------------------------------------
# Paths and global configuration
# -------------------------------------------------------------------------

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT_DIR, "dataset_raw")
os.makedirs(RAW_DIR, exist_ok=True)

# Load API credentials
load_dotenv(os.path.join(ROOT_DIR, ".env"))
API_KEY = os.getenv("GOOGLE_API_KEY")
CX_ID = os.getenv("GOOGLE_CX_ID")

if not API_KEY or not CX_ID:
    raise ValueError("Missing GOOGLE_API_KEY or GOOGLE_CX_ID in .env file at project root.")

gis = GoogleImagesSearch(API_KEY, CX_ID)

# Search categories per class
CATEGORIES: Dict[str, List[str]] = {
    "dalek": [
        "dalek doctor who",
        "gold dalek",
        "black dalek",
    ],
    "lightsaber": [
        "lightsaber",
        "blue lightsaber",
        "green lightsaber",
        "star wars lightsaber",
        "lightsaber duel",
    ],
    "sith_lightsaber": [
        "sith lightsaber",
        "red lightsaber",
        "double bladed lightsaber",
        "dark side lightsaber",
        "darth maul lightsaber",
    ],
    "cat": [
        "cat close-up",
        "kitten",
        "cat outdoors",
        "tabby cat",
        "cat sitting",
    ],
    "dog": [
        "dog close-up",
        "puppy",
        "dog running",
        "dog outdoors",
        "dog portrait",
    ],
    "person": [
        "person portrait",
        "people walking",
        "person standing",
        "man woman walking",
        "human face",
    ],
}

RUN_NAME = time.strftime("%Y-%m-%d_%H-%M-%S")
EXISTING_HASHES = set()


# -------------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------------


def load_existing_hashes(root: str = RAW_DIR) -> None:
    """
    Populate EXISTING_HASHES with hashes of all images already in dataset_raw.

    Args:
        root: Root directory to scan (defaults to RAW_DIR).
    """
    for class_folder in os.listdir(root):
        class_path = os.path.join(root, class_folder)
        if not os.path.isdir(class_path):
            continue

        for file_name in os.listdir(class_path):
            fp = os.path.join(class_path, file_name)
            try:
                img = Image.open(fp).convert("RGB")
                h = imagehash.average_hash(img)
                EXISTING_HASHES.add(h)
            except Exception:
                # Ignore unreadable files
                continue


def is_duplicate(img: Image.Image, threshold: int = 5) -> bool:
    """
    Determine whether an image is a near-duplicate of one already in the dataset.

    Args:
        img: PIL Image object.
        threshold: Hamming distance threshold for considering two hashes duplicates.

    Returns:
        True if duplicate, False otherwise.
    """
    h = imagehash.average_hash(img)
    return any(abs(h - old) < threshold for old in EXISTING_HASHES)


def scrape_category(class_name: str, search_terms: List[str]) -> None:
    """
    Scrape images for a single class using several search terms.

    Args:
        class_name: Name of the class (e.g., 'dog', 'person').
        search_terms: List of search query strings for that class.
    """
    output_dir = os.path.join(RAW_DIR, class_name, RUN_NAME)
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nDownloading images for category '{class_name}'")
    for term in search_terms:
        print(f" → Searching '{term}' ...")

        params = {
            "q": term,
            "num": 10,
            "fileType": "jpg|png",
            "safe": "off",
            "imgType": "photo",
        }

        try:
            temp_dir = os.path.join(output_dir, "_temp")
            os.makedirs(temp_dir, exist_ok=True)

            gis.search(search_params=params, path_to_dir=temp_dir)

            for fname in os.listdir(temp_dir):
                fp = os.path.join(temp_dir, fname)
                try:
                    img = Image.open(fp).convert("RGB")
                    if is_duplicate(img):
                        os.remove(fp)
                        continue

                    final_path = os.path.join(output_dir, fname)
                    img.save(final_path)
                    EXISTING_HASHES.add(imagehash.average_hash(img))
                except Exception:
                    # skip bad file
                    continue

            # Clean up temp directory
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)

        except Exception as exc:  # noqa: BLE001
            print(f"Skipped '{term}' due to error: {exc}")


def scrape_all() -> None:
    """
    Main entry point for scraping images for all defined categories.
    """
    print("Run folder:", RUN_NAME)
    load_existing_hashes()
    print(f"Loaded {len(EXISTING_HASHES)} existing image hashes.")

    for class_name, terms in CATEGORIES.items():
        scrape_category(class_name, terms)

    print("\nImage scraping complete! All images saved in 'dataset_raw/'.")


if __name__ == "__main__":
    scrape_all()
