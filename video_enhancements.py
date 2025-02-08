def generate_video_with_music(image_files, music_file="background_music.mp3"):
    clips = []
    for img in image_files:
        img_clip = ImageClip(img).set_duration(3).fadein(1).fadeout(1)  # Add fade effect
        clips.append(img_clip)

    video_clip = concatenate_videoclips(clips, method="compose")
    audio_clip = AudioFileClip(AUDIO_FILE)
    music = AudioFileClip(music_file).subclip(0, video_clip.duration).fx(volumex, 0.3)  # Reduce music volume

    # Merge video, voiceover, and background music
    final_audio = CompositeAudioClip([audio_clip, music])
    final_video = video_clip.set_audio(final_audio)

    # Add subtitles
    text_clip = TextClip(TEXT_CONTENT, fontsize=40, color='white', font=FONT_PATH)
    text_clip = text_clip.set_position(('center', 'bottom')).set_duration(video_clip.duration)

    final_video = CompositeVideoClip([final_video, text_clip])
    final_video.write_videofile(VIDEO_FILE, fps=24, codec="libx264")
    print("✔ Enhanced video with music & effects created!")

# Run enhanced video generation
generate_video_with_music(image_files)
