import os

MAX_LEN = 80  # target max filename length (without collision suffix)

DATASET_DIRS = [
    "dataset_yolo/train/images",
    "dataset_yolo/valid/images",
    "dataset_yolo/test/images"
]

for dataset in DATASET_DIRS:
    if not os.path.exists(dataset):
        continue

    print("\nScanning:", dataset)

    for file in os.listdir(dataset):
        if len(file) > MAX_LEN:
            name, ext = os.path.splitext(file)
            trimmed = name[:60]  # trim main name to 60 chars
            new_file = trimmed + ext

            # handle collisions safely
            counter = 1
            final_name = new_file
            while os.path.exists(os.path.join(dataset, final_name)):
                final_name = f"{trimmed}_{counter}{ext}"
                counter += 1

            os.rename(os.path.join(dataset, file), os.path.join(dataset, final_name))
            print("Renamed:", file, "→", final_name)

print("\nFilename shortening complete")
