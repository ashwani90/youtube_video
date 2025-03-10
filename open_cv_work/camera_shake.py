
import random

def camera_shake(image, intensity=5, steps=10):
    """Applies a random shake effect to simulate camera movement."""
    h, w = image.shape[:2]
    frames = []
    
    for _ in range(steps):
        dx = random.randint(-intensity, intensity)
        dy = random.randint(-intensity, intensity)
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        shaken = cv2.warpAffine(image, M, (w, h))
        frames.append(shaken)
    
    return frames

def tilt_effect(image, angle=10, steps=20):
    """Simulates a smooth camera tilt."""
    h, w = image.shape[:2]
    frames = []

    for i in range(steps):
        rotation_angle = angle * (i / steps)
        M = cv2.getRotationMatrix2D((w//2, h//2), rotation_angle, 1)
        tilted = cv2.warpAffine(image, M, (w, h))
        frames.append(tilted)
    
    return frames

def animate_text_speech(image, text, position, progress):
    """Displays text in sync with AI-generated voice."""
    words = text.split()
    num_words = int(progress * len(words))
    displayed_text = " ".join(words[:num_words])

    cv2.putText(image, displayed_text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, (255, 255, 255), 2, cv2.LINE_AA)
    return image

def lip_sync_animation(image, frame_count):
    """Animates lip movements based on the frame count."""
    mouth_positions = [
        (100, 90, 30, 10),  # Closed
        (100, 95, 30, 15),  # Slightly Open
        (100, 100, 30, 20)  # Fully Open
    ]
    
    pos = mouth_positions[frame_count % len(mouth_positions)]
    cv2.ellipse(image, (pos[0], pos[1]), (pos[2], pos[3]), 0, 0, 180, (0, 0, 0), -1)
    
    return image

def generate_scene_from_script(script):
    """Takes a script and generates animated frames."""
    scenes = []
    for line in script.split("\n"):
        if line.startswith("Character:"):
            character_name = line.split(":")[1].strip()
        elif line.startswith("Emotion:"):
            emotion = line.split(":")[1].strip()
        elif line.startswith("Dialogue:"):
            text = line.split(":")[1].strip()
            scene_image = create_cartoon_scene(character_name, emotion, text)
            scenes.append(scene_image)
    
    return scenes

import cv2

def save_as_video(frames, filename="output.mp4", fps=24):
    """Saves a list of frames as a video file."""
    h, w, _ = frames[0].shape
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    for frame in frames:
        out.write(frame)

    out.release()

final_video = save_as_video(final_frames, "political_satire.mp4")

