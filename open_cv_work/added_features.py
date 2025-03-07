import cv2
import numpy as np
import time

# Smooth interpolation functions for different movements
def lerp(start, end, alpha):
    return start + alpha * (end - start)

def ease_in_out(start, end, alpha):
    alpha = alpha * alpha * (3 - 2 * alpha)  # Smooth transition
    return start + alpha * (end - start)

# Draw animated speech bubble with tail
def draw_speech_bubble(frame, text, position, character_pos, frame_count, total_frames):
    bubble_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Bubble position
    (x, y) = position
    bubble_w, bubble_h = 250, 100

    # Bubble fade-in effect
    alpha = min(1, frame_count / total_frames)
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + bubble_w, y + bubble_h), bubble_color, -1)

    # Draw tail pointing to character
    cv2.line(overlay, (x + 30, y + bubble_h), (character_pos[0], character_pos[1] - 30), bubble_color, 5)

    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Animated text appearance
    chars_to_show = int(alpha * len(text))
    displayed_text = text[:chars_to_show]
    cv2.putText(frame, displayed_text, (x + 10, y + 50), font, 0.7, text_color, 2)

# Zoom effect (Pulsating zoom-in and zoom-out)
def zoom_effect(frame, scale):
    h, w, _ = frame.shape
    center_x, center_y = w // 2, h // 2

    new_w, new_h = int(w * scale), int(h * scale)
    x1, y1 = max(0, center_x - new_w // 2), max(0, center_y - new_h // 2)
    x2, y2 = min(w, center_x + new_w // 2), min(h, center_y + new_h // 2)

    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h))

# Background transition
def transition_background(frame, start_color, end_color, frame_count, total_frames):
    alpha = frame_count / total_frames
    blended_color = (
        int(lerp(start_color[0], end_color[0], alpha)),
        int(lerp(start_color[1], end_color[1], alpha)),
        int(lerp(start_color[2], end_color[2], alpha)),
    )
    frame[:] = blended_color
    return frame

# Flash effect for dramatic emphasis
def flash_effect(frame, frame_count, flash_duration=10):
    if frame_count % flash_duration == 0:
        overlay = frame.copy()
        overlay[:] = (255, 255, 255)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    return frame

# Main animation function
def animate():
    width, height = 640, 480
    total_frames = 150
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Character movement paths
    start_pos1, end_pos1 = (50, 300), (350, 300)
    start_pos2, end_pos2 = (600, 300), (250, 300)  # Opposite direction

    # Speech texts
    speech1 = "We demand justice!"
    speech2 = "And we want reforms!"

    for frame_count in range(total_frames):
        alpha = frame_count / total_frames
        ease_alpha = ease_in_out(0, 1, alpha)

        # Moving characters
        char1_x = int(lerp(start_pos1[0], end_pos1[0], ease_alpha))
        char2_x = int(lerp(start_pos2[0], end_pos2[0], ease_alpha))

        # Background transition effect
        frame = transition_background(frame, (50, 50, 255), (255, 255, 255), frame_count, total_frames)

        # Zoom-in and out pulsating effect
        zoom_factor = 1 + 0.1 * np.sin(frame_count * 0.1)
        frame = zoom_effect(frame, zoom_factor)

        # Camera panning effect (horizontal shifting)
        pan_offset = int(50 * np.sin(alpha * np.pi))
        M = np.float32([[1, 0, pan_offset], [0, 1, 0]])
        frame = cv2.warpAffine(frame, M, (width, height))

        # Drawing characters (simplified as circles)
        cv2.circle(frame, (char1_x, start_pos1[1]), 50, (0, 0, 0), -1)  # Character 1
        cv2.circle(frame, (char2_x, start_pos2[1]), 50, (0, 0, 255), -1)  # Character 2

        # Dynamic facial expressions
        if frame_count % 20 < 10:
            eye_radius = 5
        else:
            eye_radius = 3

        cv2.circle(frame, (char1_x - 15, start_pos1[1] - 15), eye_radius, (255, 255, 255), -1)  # Left eye
        cv2.circle(frame, (char1_x + 15, start_pos1[1] - 15), eye_radius, (255, 255, 255), -1)  # Right eye

        cv2.circle(frame, (char2_x - 15, start_pos2[1] - 15), eye_radius, (255, 255, 255), -1)  # Left eye
        cv2.circle(frame, (char2_x + 15, start_pos2[1] - 15), eye_radius, (255, 255, 255), -1)  # Right eye

        # Speech bubbles with tails
        draw_speech_bubble(frame, speech1, (char1_x + 60, start_pos1[1] - 80), (char1_x, start_pos1[1]), frame_count, total_frames)
        draw_speech_bubble(frame, speech2, (char2_x - 260, start_pos2[1] - 80), (char2_x, start_pos2[1]), frame_count, total_frames)

        # Flash effect at key moments
        frame = flash_effect(frame, frame_count)

        # Display frame
        cv2.imshow("Enhanced Cartoon Animation", frame)
        if cv2.waitKey(50) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()

# Run the enhanced animation
animate()
