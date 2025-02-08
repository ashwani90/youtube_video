import os
import requests
import random
from gtts import gTTS
from moviepy.editor import *
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuration
TEXT_CONTENT = "Breaking News! Stock markets have hit an all-time high. Experts predict further growth in the upcoming months."
AUDIO_FILE = "audio.mp3"
VIDEO_FILE = "output.mp4"
FONT_PATH = "arial.ttf"

# Step 1: Convert Text to Speech
def generate_audio(text, output_file):
    tts = gTTS(text, lang='en')
    tts.save(output_file)
    print("✔ Audio file generated!")

# Step 2: Download Multiple Background Images
def download_images(search_term, num_images=5):
    images = []
    for i in range(num_images):
        API_URL = f"https://source.unsplash.com/1280x720/?{search_term}&random={random.randint(1, 1000)}"
        image_file = f"image_{i}.jpg"
        response = requests.get(API_URL)
        with open(image_file, "wb") as f:
            f.write(response.content)
        images.append(image_file)
    print(f"✔ {num_images} images downloaded!")
    return images

# Step 3: Generate Video with Image Transitions
def generate_video(image_files):
    clips = []
    for img in image_files:
        img_clip = ImageClip(img).set_duration(3)  # Each image lasts 3 seconds
        clips.append(img_clip)

    video_clip = concatenate_videoclips(clips, method="compose")
    audio_clip = AudioFileClip(AUDIO_FILE)
    
    text_clip = TextClip(TEXT_CONTENT, fontsize=40, color='white', font=FONT_PATH)
    text_clip = text_clip.set_position(('center', 'bottom')).set_duration(video_clip.duration)

    final_video = CompositeVideoClip([video_clip, text_clip])
    final_video = final_video.set_audio(audio_clip)
    final_video.write_videofile(VIDEO_FILE, fps=24, codec="libx264")
    print("✔ Video with multiple images generated!")

# Step 4: Upload Video to YouTube
def upload_to_youtube():
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    CLIENT_SECRETS_FILE = "client_secrets.json"  # Get this from Google Cloud Console

    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey="YOUR_YOUTUBE_API_KEY")

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Breaking News - Stock Market Update",
                "description": "Automated news update on stock markets.",
                "tags": ["news", "stock market", "finance"],
                "categoryId": "25"  # News & Politics category
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True)
    )

    response = request.execute()
    print(f"✔ Video uploaded successfully! Video ID: {response['id']}")

# Run all steps
generate_audio(TEXT_CONTENT, AUDIO_FILE)
image_files = download_images("stock market", num_images=5)
generate_video(image_files)
upload_to_youtube()
