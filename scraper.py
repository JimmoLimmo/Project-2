import os
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
    "cat": [
        "cat close-up",
        "kitten",
        "cat outdoors",
        "tabby cat",
        "cat sitting"
    ],
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

# Download Settings
for class_name, search_terms in categories.items():
    output_dir = f"dataset_raw/{class_name}"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nDownloading images for '{class_name}'")

    for term in search_terms:
        print(f" Searching '{term}' ...")
        params = {
            'q': term,
            'num': 10,  
            'fileType': 'jpg|png',
            'safe': 'off',
            'imgType': 'photo'
        }

        try:
            gis.search(search_params=params, path_to_dir=output_dir)
        except Exception as e:
            print(f"Skipped '{term}' due to error: {e}")

print("\n Image scraping complete! All images saved in 'dataset_raw/'")
