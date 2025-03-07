import cv2
import numpy as np
import time

# Smooth transition function using linear interpolation
def lerp(start, end, alpha):
    return start + alpha * (end - start)

# Function to add animated text in a speech bubble
def draw_speech_bubble(frame, text, position, frame_count, total_frames):
    bubble_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Bubble size
    (x, y) = position
    bubble_w, bubble_h = 250, 100

    # Draw bubble with fade-in effect
    alpha = min(1, frame_count / total_frames)
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + bubble_w, y + bubble_h), bubble_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Animated text appearing gradually
    chars_to_show = int(alpha * len(text))
    displayed_text = text[:chars_to_show]
    cv2.putText(frame, displayed_text, (x + 10, y + 50), font, 0.7, text_color, 2)

# Function to apply a zoom effect
def zoom_effect(frame, scale):
    h, w, _ = frame.shape
    center_x, center_y = w // 2, h // 2

    # Compute cropping bounds
    new_w, new_h = int(w * scale), int(h * scale)
    x1, y1 = max(0, center_x - new_w // 2), max(0, center_y - new_h // 2)
    x2, y2 = min(w, center_x + new_w // 2), min(h, center_y + new_h // 2)

    # Crop and resize
    cropped = frame[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h))

# Function to transition background color smoothly
def transition_background(frame, start_color, end_color, frame_count, total_frames):
    alpha = frame_count / total_frames
    blended_color = (
        int(lerp(start_color[0], end_color[0], alpha)),
        int(lerp(start_color[1], end_color[1], alpha)),
        int(lerp(start_color[2], end_color[2], alpha)),
    )
    frame[:] = blended_color
    return frame

# Main animation function
def animate():
    width, height = 640, 480
    total_frames = 100

    # Create a blank frame
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Character start and end positions for smooth movement
    start_pos = (50, 300)
    end_pos = (400, 300)

    # Speech text
    speech_text = "We demand justice!"

    for frame_count in range(total_frames):
        current_pos_x = int(lerp(start_pos[0], end_pos[0], frame_count / total_frames))
        current_pos_y = start_pos[1]

        # Smooth background transition from blue to white
        frame = transition_background(frame, (50, 50, 255), (255, 255, 255), frame_count, total_frames)

        # Draw moving character (using a simple circle as a placeholder)
        cv2.circle(frame, (current_pos_x, current_pos_y), 50, (0, 0, 0), -1)

        # Draw animated speech bubble
        draw_speech_bubble(frame, speech_text, (current_pos_x + 60, current_pos_y - 80), frame_count, total_frames)

        # Apply zoom effect
        zoom_factor = 1 + 0.1 * (frame_count / total_frames)  # Zoom-in gradually
        frame = zoom_effect(frame, zoom_factor)

        # Show frame
        cv2.imshow("Cartoon Animation", frame)
        if cv2.waitKey(50) & 0xFF == ord("q"):  # Press 'q' to exit
            break

    cv2.destroyAllWindows()

# Run the animation
animate()
