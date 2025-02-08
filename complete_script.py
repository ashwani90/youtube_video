import os
import requests
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

# Configuration
TEXT_CONTENT = "Breaking News! Stock markets have hit an all-time high. Experts predict further growth in the upcoming months."
AUDIO_FILE = "audio.mp3"
IMAGE_FILE = "background.jpg"
VIDEO_FILE = "output.mp4"
FONT_PATH = "arial.ttf"  # Use a valid font path

# Step 1: Convert Text to Speech (TTS)
def generate_audio(text, output_file):
    tts = gTTS(text, lang='en')
    tts.save(output_file)
    print("✔ Audio file generated!")

# Step 2: Fetch Background Image (Optional: Download from Unsplash/Pexels)
def download_image(search_term, output_file):
    API_URL = f"https://source.unsplash.com/1280x720/?{search_term}"
    response = requests.get(API_URL)
    with open(output_file, "wb") as f:
        f.write(response.content)
    print("✔ Background image downloaded!")

# Step 3: Generate Subtitle Image
def create_subtitle_image(text, output_file):
    img = Image.open(IMAGE_FILE)
    draw = ImageDraw.Draw(img)
    
    # Load font
    font_size = 40
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except:
        font = ImageFont.load_default()

    # Text position
    text_width, text_height = draw.textsize(text, font=font)
    position = ((img.width - text_width) // 2, img.height - 100)
    
    # Draw text
    draw.text(position, text, fill="white", font=font)
    img.save(output_file)
    print("✔ Subtitle image created!")

# Step 4: Create Video with Subtitles and Audio
def generate_video():
    # Load assets
    image_clip = ImageClip(IMAGE_FILE).set_duration(10)
    audio_clip = AudioFileClip(AUDIO_FILE)
    
    # Add subtitles
    text_clip = TextClip(TEXT_CONTENT, fontsize=40, color='white', font=FONT_PATH)
    text_clip = text_clip.set_position(('center', 'bottom')).set_duration(10)
    
    # Merge everything
    video = CompositeVideoClip([image_clip, text_clip])
    video = video.set_audio(audio_clip)
    
    # Save video
    video.write_videofile(VIDEO_FILE, fps=24, codec="libx264")
    print("✔ Video generated successfully!")

# Run all steps
generate_audio(TEXT_CONTENT, AUDIO_FILE)
download_image("stock market", IMAGE_FILE)
create_subtitle_image(TEXT_CONTENT, IMAGE_FILE)
generate_video()
