from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

THUMBNAIL_FILE = "thumbnail.jpg"

def generate_thumbnail(text, background_image_url):
    # Download background image
    response = requests.get(background_image_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((1280, 720))  # Resize to YouTube thumbnail size

    # Add text overlay
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 80)
    text_position = (100, 550)  # Adjust as needed
    draw.text(text_position, text, font=font, fill="white")

    # Save thumbnail
    img.save(THUMBNAIL_FILE)
    print(f"✔ Thumbnail created: {THUMBNAIL_FILE}")

# Example Usage
thumbnail_text = "Stock Market Hits Record High!"
background_image_url = "https://source.unsplash.com/1280x720/?stock,finance"
generate_thumbnail(thumbnail_text, background_image_url)
