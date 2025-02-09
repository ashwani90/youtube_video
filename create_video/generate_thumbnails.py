from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

INPUT_FILE = "images/abcd.jpeg"
THUMBNAIL_FILE = "images/thumbnail.jpg"

'''
This creates a thumbnail using an image file
'''

def generate_thumbnail(text):
    # Download background image
    img = Image.open(INPUT_FILE)
    img = img.resize((1280, 720))  # Resize to YouTube thumbnail size

    # Add text overlay
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype("fonts/arial.ttf", 80)
    text_position = (100, 550)  # Adjust as needed
    draw.text(text_position, text, font_size=80, fill="white")

    # Save thumbnail
    img.save(THUMBNAIL_FILE)
    print(f"✔ Thumbnail created: {THUMBNAIL_FILE}")

# Example Usage
thumbnail_text = "Stock Market Hits Record High!"
background_image_url = "https://source.unsplash.com/1280x720/?stock,finance"
generate_thumbnail(thumbnail_text)
