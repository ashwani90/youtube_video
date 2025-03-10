import cv2
import numpy as np

def draw_speech_bubble(image, text, position, progress=1.0):
    bubble = cv2.imread("speech_bubble.png")  # Load a transparent speech bubble
    x, y = position

    # Scale bubble dynamically
    scale = progress
    bubble = cv2.resize(bubble, (int(bubble.shape[1] * scale), int(bubble.shape[0] * scale)))

    image[y:y+bubble.shape[0], x:x+bubble.shape[1]] = bubble

    # Animate text appearance
    num_chars = int(len(text) * progress)
    cv2.putText(image, text[:num_chars], (x + 20, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    return image


def apply_parallax(layers, speeds):
    final_image = np.zeros_like(layers[0])
    
    for i, layer in enumerate(layers):
        shift_x = int(speeds[i] * 10)  # Different speeds per layer
        final_image[:, shift_x:] = layer[:, :-shift_x]  

    return final_image


def zoom_effect(image, scale):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    zoomed = cv2.resize(image, None, fx=scale, fy=scale)
    cropped = zoomed[center[1] - h//2:center[1] + h//2, center[0] - w//2:center[0] + w//2]
    
    return cropped
