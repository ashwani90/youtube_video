from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, concatenate_videoclips, vfx
from moviepy.video.fx import FadeIn, FadeOut

VIDEO_FILE = "output/output3.mp4"
FONT_PATH = "arial.ttf"
AUDIO_FILE = "audio_files/audio.mp3"
TEXT_CONTENT = "Breaking News! Stock markets have hit an all-time high. Experts predict further growth in the upcoming months."

# duration = 3

'''
This creates the video file with the text and audio
also has zoom effects and fade effect
'''

def resize_func(t):
    duration = 2
    if t < 4:
        return 1 + 0.2*t  # Zoom-in.
    elif 4 <= t <= 6:
        return 1 + 0.2*4  # Stay.
    else: # 6 < t
        return 1 + 0.2*(duration-t)  # Zoom-out.

def generate_video_with_ai_voice(image_files, music_file="background_music.mp3"):
    clips = []
    for img in image_files:
        img_clip = ImageClip(img).with_duration(3).resized(resize_func)
        fade_duration = 3  # Duration of fade effect in seconds
        FadeIn(img_clip, fade_duration)  
        FadeOut(img_clip, 1)
        # img_clip = img_clip.crossfadein(1)
        # image_clip = img_clip.fx(vfx.fadein, 1) 
        # .fadein(1).fadeout(1)  # Smooth fade effect
        clips.append(img_clip)

    video_clip = concatenate_videoclips(clips, method="compose")
    audio_clip = AudioFileClip(AUDIO_FILE)
    # music = AudioFileClip(music_file)  # Reduce music volume

    # Sync voice and background music
    final_audio = CompositeAudioClip([audio_clip])
    final_video = video_clip.with_audio(final_audio)

    # Add subtitles
    # text_clip = TextClip(TEXT_CONTENT, font_size=40, color='white')
    # text_clip = text_clip.with_position(('center', 'bottom')).with_duration(video_clip.duration)

    final_video = CompositeVideoClip([final_video])
    final_video.write_videofile(VIDEO_FILE, fps=24, codec="libx264")
    print("✔ Video with AI voice, music & effects created!")

# Run enhanced video generation
image_files = ["images/image1.jpeg", "images/image2.jpeg", "images/image3.jpeg"]  # Example images
generate_video_with_ai_voice(image_files, music_file=AUDIO_FILE)
