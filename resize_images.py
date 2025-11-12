import os
from PIL import Image

root_dir = "dataset_raw"
output_dir = "dataset_resized"
size = (416, 416)
valid_exts = (".jpg", ".jpeg", ".png", ".pjpeg")

for class_name in os.listdir(root_dir):
    src = os.path.join(root_dir, class_name)
    dst = os.path.join(output_dir, class_name)
    os.makedirs(dst, exist_ok=True)
    
    for img_name in os.listdir(src):
        try:
            # Skip files that don't have a valid extension
            if not img_name.lower().endswith(valid_exts):
                continue
            
            img_path = os.path.join(src, img_name)
            
            # Normalize .pjpeg to .jpg 
            out_name = os.path.splitext(img_name)[0] + ".jpg"
            
            img = Image.open(img_path).convert("RGB")
            img = img.resize(size)
            img.save(os.path.join(dst, out_name), "JPEG")
        except Exception as e:
            print(f"Skipping {img_name}: {e}")

print("Resized and saved images to", output_dir)
