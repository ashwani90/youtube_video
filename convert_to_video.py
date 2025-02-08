from moviepy.editor import *  

# Load background image & audio  
image = ImageClip("background.jpg").set_duration(10)  
audio = AudioFileClip("audio.mp3")  

# Add subtitles  
txt = TextClip("Breaking News!", fontsize=70, color='white')  
txt = txt.set_position('bottom').set_duration(10)  

# Combine everything  
video = CompositeVideoClip([image, txt])  
video = video.set_audio(audio)  
video.write_videofile("output.mp4", fps=24)  
