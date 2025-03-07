from pydub import AudioSegment
import cv2
import numpy as np
def add_audio(background, effects, timing):
    audio = AudioSegment.from_file(background)
    
    for effect, time in zip(effects, timing):
        effect_audio = AudioSegment.from_file(effect)
        audio = audio.overlay(effect_audio, position=time * 1000)
    
    audio.export("final_audio.mp3", format="mp3")


def smooth_zoom(image, scale_start, scale_end, steps=30):
    h, w = image.shape[:2]
    zoomed_images = []
    
    for step in range(steps):
        scale = scale_start + (scale_end - scale_start) * (step / steps)
        center = (w // 2, h // 2)
        zoomed = cv2.resize(image, None, fx=scale, fy=scale)
        cropped = zoomed[center[1] - h//2:center[1] + h//2, center[0] - w//2:center[0] + w//2]
        
        zoomed_images.append(cropped)
    
    return zoomed_images

def fade_effect(image1, image2, alpha=0.5):
    return cv2.addWeighted(image1, alpha, image2, 1 - alpha, 0)

def pan_effect(image, direction='horizontal', distance=50, steps=30):
    h, w = image.shape[:2]
    frames = []
    
    for step in range(steps):
        if direction == 'horizontal':
            shift_x = int(distance * (step / steps))
            pan_image = np.roll(image, shift_x, axis=1)
        elif direction == 'vertical':
            shift_y = int(distance * (step / steps))
            pan_image = np.roll(image, shift_y, axis=0)
        
        frames.append(pan_image)
    
    return frames

def parallax_effect(background_layers, speed_factors, steps=30):
    # Assume background_layers is a list of image layers (e.g., foreground, middle ground, background)
    height, width = background_layers[0].shape[:2]
    parallax_frames = []

    for step in range(steps):
        parallax_frame = np.zeros_like(background_layers[0])
        
        for i, layer in enumerate(background_layers):
            speed = speed_factors[i]
            shift = int(speed * step)
            shifted_layer = np.roll(layer, shift, axis=1)  # Horizontal movement
            parallax_frame = cv2.add(parallax_frame, shifted_layer)

        parallax_frames.append(parallax_frame)

    return parallax_frames

