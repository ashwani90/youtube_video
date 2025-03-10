import cv2
import dlib
import numpy as np
import pyttsx3
import time
from moviepy.editor import *

# Load facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def generate_voiceover(text, output_audio):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio)
    engine.runAndWait()

def animate_lips(image_path, audio_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    for face in faces:
        landmarks = predictor(gray, face)
        for i in range(48, 61):  # Mouth region
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

    cv2.imshow("Lip-Sync Animation", image)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    
    # Combine with audio
    clip = ImageSequenceClip([image], fps=1)
    audio = AudioFileClip(audio_path)
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile("lip_sync_video.mp4", fps=24)

# Example usage
text = "This is a political satire cartoon"
audio_file = "voiceover.mp3"
generate_voiceover(text, audio_file)
animate_lips("cartoon_face.png", audio_file)


def add_speech_bubble(image, text, position=(50, 50), bubble_size=(300, 150)):
    img = cv2.imread(image)
    x, y = position
    w, h = bubble_size

    # Draw bubble
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), -1)
    cv2.putText(img, text, (x+10, y+40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    cv2.imshow("Speech Bubble", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example Usage
add_speech_bubble("cartoon_scene.png", "This is satire!")
def animate_character_movement(image_path, start, end, frames=30, easing="linear"):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    overlay = img.copy()
    
    x1, y1 = start
    x2, y2 = end

    for i in range(frames):
        alpha = i / frames
        if easing == "ease-in":
            alpha = alpha ** 2
        elif easing == "ease-out":
            alpha = 1 - (1 - alpha) ** 2

        x = int(x1 + alpha * (x2 - x1))
        y = int(y1 + alpha * (y2 - y1))

        frame = overlay.copy()
        cv2.circle(frame, (x, y), 30, (0, 0, 255), -1)

        cv2.imshow("Movement Animation", frame)
        cv2.waitKey(50)

    cv2.destroyAllWindows()

# Example Usage
animate_character_movement("background.png", (50, 100), (400, 100), frames=50, easing="ease-in")

def animate_background(image_path, layers=3, shift=10):
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    for i in range(30):
        shifted_img = img.copy()
        for layer in range(layers):
            dx = int(layer * shift * (i / 30))
            shifted_img[:, dx:] = img[:, :-dx]

        cv2.imshow("Parallax Effect", shifted_img)
        cv2.waitKey(50)

    cv2.destroyAllWindows()

# Example Usage
animate_background("background_scene.png", layers=3, shift=5)

def flash_effect(image_path, flashes=3, delay=200):
    img = cv2.imread(image_path)

    for _ in range(flashes):
        cv2.imshow("Flash Effect", img)
        cv2.waitKey(delay)
        cv2.imshow("Flash Effect", np.zeros_like(img))
        cv2.waitKey(delay)

    cv2.destroyAllWindows()

# Example Usage
flash_effect("dramatic_scene.png")

def add_hand_gesture(image_path, position):
    img = cv2.imread(image_path)
    hand = cv2.imread("hand.png", cv2.IMREAD_UNCHANGED)

    x, y = position
    img[y:y+hand.shape[0], x:x+hand.shape[1]] = hand

    cv2.imshow("Hand Gesture", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example Usage
add_hand_gesture("political_scene.png", (200, 300))

