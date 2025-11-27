import os
import time
import imagehash
from PIL import Image
from dotenv import load_dotenv
from google_images_search import GoogleImagesSearch

# API Info
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
CX_ID = os.getenv("GOOGLE_CX_ID")

if not API_KEY or not CX_ID:
    raise ValueError("Missing GOOGLE_API_KEY or GOOGLE_CX_ID in .env file!")

gis = GoogleImagesSearch(API_KEY, CX_ID)
# Classes
categories = {
    # "dalek": [
    #     "dalek doctor who",
    #     # "dalek toy",
    #     # "dalek prop",
    #     # "gold dalek",
    #     # "black dalek"
    # ],
    # "lightsaber": [
    #     "lightsaber",
    #     "blue lightsaber",
    #     "green lightsaber",
    #     "star wars lightsaber",
    #     "lightsaber duel"
    # ],
    # "sith_lightsaber": [
    #     "sith lightsaber",
    #     "red lightsaber",
    #     "double bladed lightsaber",
    #     "dark side lightsaber",
    #     "darth maul lightsaber"
    # ],
    # "cat": [
    #     "cat close-up",
    #     "kitten",
    #     "cat outdoors",
    #     "tabby cat",
    #     "cat sitting"
    # ],
    "dog": [
        "dog close-up",
        "puppy",
        "dog running",
        "dog outdoors",
        "dog portrait"
    ],
    "person": [
        "person portrait",
        "people walking",
        "person standing",
        "man woman walking",
        "human face"
    ]
}

# Create a unique run folder
RUN_NAME = time.strftime("%Y-%m-%d_%H-%M-%S")
print("Run folder:", RUN_NAME)

# Prepare global hash list
existing_hashes = set()


def load_existing_hashes(root="dataset_raw"):
    """Load hashes of all images across entire dataset."""
    for class_folder in os.listdir(root):
        class_path = os.path.join(root, class_folder)
        if not os.path.isdir(class_path):
            continue

        for file in os.listdir(class_path):
            fp = os.path.join(class_path, file)
            try:
                img = Image.open(fp).convert("RGB")
                h = imagehash.average_hash(img)
                existing_hashes.add(h)
            except:
                pass

load_existing_hashes()
print(f"Loaded {len(existing_hashes)} existing image hashes.")


def is_duplicate(img):
    """Check if an image is a duplicate using perceptual hash."""
    h = imagehash.average_hash(img)
    return any(abs(h - old) < 5 for old in existing_hashes)

# Download Settings
for class_name, search_terms in categories.items():
    output_dir = f"dataset_raw/{class_name}/{RUN_NAME}"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n Downloading images for category '{class_name}'")

    for term in search_terms:
        print(f" → Searching '{term}' ...")

        params = {
            'q': term,
            'num': 10,
            'fileType': 'jpg|png',
            'safe': 'off',
            'imgType': 'photo'
        }

        try:
            temp_dir = output_dir + "/_temp"
            os.makedirs(temp_dir, exist_ok=True)

            gis.search(search_params=params, path_to_dir=temp_dir)

            # Filter duplicates before final save
            for fname in os.listdir(temp_dir):
                fp = os.path.join(temp_dir, fname)
                try:
                    img = Image.open(fp).convert("RGB")
                    if is_duplicate(img):
                        os.remove(fp)
                        continue

                    # Save & store hash
                    final_path = os.path.join(output_dir, fname)
                    img.save(final_path)
                    existing_hashes.add(imagehash.average_hash(img))

                except:
                    pass

            # Removing temp folder contents
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)

        except Exception as e:
            print(f"Skipped '{term}' due to error: {e}")

print("\n Image scraping complete! All images saved in 'dataset_raw/'")
