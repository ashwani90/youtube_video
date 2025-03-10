import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from moviepy.editor import VideoFileClip, CompositeVideoClip, AudioFileClip, TextClip
import random

# Initialize canvas
WIDTH, HEIGHT = 800, 600
background = np.full((HEIGHT, WIDTH, 3), (255, 255, 255), dtype=np.uint8)  # White canvas

# Define multiple character properties
characters = [
    {"name": "Politician A", "pos": [50, 400], "face": "face1.png", "speech": "I promise change!"},
    {"name": "Politician B", "pos": [600, 400], "face": "face2.png", "speech": "More taxes incoming!"},
]

# Load character faces
for char in characters:
    face = cv2.imread(char["face"])
    if face is not None:
        face = cv2.resize(face, (100, 100))
        char["face_img"] = face

# Function for smooth movement
def move_character(start, end, frames=60, ease="linear"):
    points = []
    for i in range(frames):
        t = i / (frames - 1)
        if ease == "ease-in":
            t = t**2
        elif ease == "ease-out":
            t = 1 - (1 - t)**2
        x = int(start[0] + (end[0] - start[0]) * t)
        y = int(start[1] + (end[1] - start[1]) * t)
        points.append((x, y))
    return points

# Define motion paths
characters[0]["path"] = move_character(characters[0]["pos"], [300, 400], ease="ease-out")
characters[1]["path"] = move_character(characters[1]["pos"], [450, 400], ease="ease-in")

# Speech bubble function
def draw_speech_bubble(img, text, pos):
    x, y = pos
    bubble_w, bubble_h = 200, 100
    bubble = np.full((bubble_h, bubble_w, 3), (255, 255, 255), dtype=np.uint8)
    cv2.rectangle(bubble, (0, 0), (bubble_w, bubble_h), (0, 0, 0), 2)
    
    # Add text
    cv2.putText(bubble, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Attach speech tail dynamically
    tail_pts = np.array([[bubble_w // 2, bubble_h], [bubble_w // 2 + 20, bubble_h + 30], [bubble_w // 2 - 20, bubble_h + 30]], np.int32)
    cv2.fillPoly(bubble, [tail_pts], (255, 255, 255))
    cv2.polylines(bubble, [tail_pts], True, (0, 0, 0), 2)
    
    img[y-100:y, x:x+200] = bubble

# Animation function
def animate(frame):
    global background
    img = background.copy()
    
    for char in characters:
        if frame < len(char["path"]):
            x, y = char["path"][frame]
            img[y:y+100, x:x+100] = char["face_img"]
            draw_speech_bubble(img, char["speech"], (x, y))
    
    return img

# Create animation
frames = []
for i in range(60):
    frames.append(animate(i))

# Convert frames to video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('political_satire.avi', fourcc, 30, (WIDTH, HEIGHT))

for frame in frames:
    out.write(frame)
out.release()

# Add narration and effects using moviepy
clip = VideoFileClip("political_satire.avi")
audio = AudioFileClip("speech_narration.mp3")  # Pre-recorded narration
final_clip = CompositeVideoClip([clip.set_audio(audio)])

# Save final video
final_clip.write_videofile("final_political_satire.mp4", codec="libx264", fps=30)

