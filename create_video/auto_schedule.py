from datetime import datetime, timedelta
import pytz

#  automaticallt schuled updates to youtube with video
# check this view if this is so easy

def upload_to_youtube_scheduled(publish_time):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Breaking News - Stock Market Update",
                "description": "Automated news update on stock markets.",
                "tags": ["news", "stock market", "finance"],
                "categoryId": "25"
            },
            "status": {
                "privacyStatus": "private",  # Keep private until scheduled time
                "publishAt": publish_time.isoformat()  # Scheduled time in ISO format
            }
        },
        media_body=MediaFileUpload(VIDEO_FILE, chunksize=-1, resumable=True)
    )

    response = request.execute()
    print(f"✔ Video scheduled for: {publish_time} (UTC) | Video ID: {response['id']}")

# Example: Schedule upload for 6 hours from now
publish_time = datetime.utcnow() + timedelta(hours=6)
publish_time = publish_time.replace(tzinfo=pytz.UTC)
upload_to_youtube_scheduled(publish_time)
