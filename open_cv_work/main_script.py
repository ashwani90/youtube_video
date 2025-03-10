import cv2
import numpy as np
import moviepy.editor as mp
from gtts import gTTS
from moviepy.video.fx import fadein, fadeout
from moviepy.video.fx.all import resize

# Cartoonize Image
def cartoonize_image(img_path, style="pencil"):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if style == "pencil":
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        return sketch
    
    elif style == "oil_paint":
        return cv2.stylization(img, sigma_s=150, sigma_r=0.25)

    elif style == "comic":
        edges = cv2.Canny(gray, 100, 200)
        colored = cv2.bitwise_and(img, img, mask=edges)
        return colored

    return img

# Generate Speech Audio
def generate_speech(text, output_file="speech.mp3"):
    tts = gTTS(text, lang="en")
    tts.save(output_file)

# Create Speech Bubble
def add_speech_bubble(img, text, position=(50, 50)):
    h, w, _ = img.shape
    overlay = img.copy()
    cv2.rectangle(overlay, position, (w - 50, position[1] + 100), (255, 255, 255), -1)
    cv2.putText(overlay, text, (position[0] + 10, position[1] + 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    
    return cv2.addWeighted(overlay, 0.6, img, 0.4, 0)

# Apply Scene Transition Effects
def apply_transitions(video_path, output_path):
    clip = mp.VideoFileClip(video_path)
    fade_in = fadein.fadein(clip, 1)
    fade_out = fadeout.fadeout(fade_in, 1)
    final_clip = resize(fade_out, 0.8)  # Apply zoom effect
    final_clip.write_videofile(output_path, fps=24)

# Main Execution
if __name__ == "__main__":
    img_path = "input.jpg"
    text = "We must take action now!"
    
    cartoon_style = "comic"  # Options: "pencil", "oil_paint", "comic"
    
    cartoonized_img = cartoonize_image(img_path, style=cartoon_style)
    bubble_img = add_speech_bubble(cartoonized_img, text)
    
    cv2.imwrite("cartoon_output.jpg", bubble_img)
    generate_speech(text, "speech.mp3")

    print("Cartoon and speech bubble generated successfully!")

from moviepy.editor import ImageSequenceClip, AudioFileClip

def create_animated_cartoon(images, audio_path, output_video="cartoon_video.mp4"):
    clip = ImageSequenceClip(images, fps=12)
    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_video, fps=24)

image_files = ["cartoon_output.jpg"] * 30  # 30 frames for animation
create_animated_cartoon(image_files, "speech.mp3")
