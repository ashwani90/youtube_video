def generate_srt(text, duration, output_file="subtitles.srt"):
    lines = text.split(". ")
    time_per_line = duration / len(lines)

    with open(output_file, "w") as f:
        for i, line in enumerate(lines):
            start_time = i * time_per_line
            end_time = (i + 1) * time_per_line
            f.write(f"{i+1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{line.strip()}\n\n")
    
    print("✔ Subtitles (SRT) file created!")

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02},{millis:03}"

# Example Usage
generate_srt(TEXT_CONTENT, 30)  # 30-second video

#  add subtitles to youtube

def upload_subtitles(video_id, subtitle_file="subtitles.srt"):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    request = youtube.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "language": "en",
                "name": "English Subtitles",
                "isDraft": False
            }
        },
        media_body=MediaFileUpload(subtitle_file)
    )
    
    response = request.execute()
    print("✔ Subtitles uploaded successfully!")
