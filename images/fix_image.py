from PIL import Image

image_path = "abcd.jpeg"

try:
    with Image.open(image_path) as img:
        print(f"✔ Image format: {img.format}, Mode: {img.mode}")
except Exception as e:
    print(f"❌ Error: {e}")