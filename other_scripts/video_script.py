import os
import requests
import random
from gtts import gTTS
from moviepy.editor import *
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

'''
Upload code on youtube
'''

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

upload_to_youtube()
