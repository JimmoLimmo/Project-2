
import os
from PIL import Image

root_dir = "dataset_raw"
output_dir = "dataset_resized"
size = (416, 416)  

for class_name in os.listdir(root_dir):
    src = os.path.join(root_dir, class_name)
    dst = os.path.join(output_dir, class_name)
    os.makedirs(dst, exist_ok=True)
    
    for img_name in os.listdir(src):
        try:
            img_path = os.path.join(src, img_name)
            img = Image.open(img_path).convert("RGB")
            img = img.resize(size)
            img.save(os.path.join(dst, img_name))
        except Exception as e:
            print(f"Skipping {img_name}: {e}")

print(" Resized and saved images to", output_dir)
