import cv2
import numpy as np
import time

def cartoonize_image(img, style="cartoon"):
    """Applies different cartoon styles to an image."""
    if style == "pencil_sketch":
        gray, sketch = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        return sketch
    elif style == "oil_painting":
        return cv2.xphoto.oilPainting(img, 7, 1)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon

def add_speech_bubble(img, text, position=(50, 50), bubble_size=(300, 130), fade_in_frames=30):
    """Animates a speech bubble appearing gradually."""
    x, y = position
    w, h = bubble_size
    frame = img.copy()

    for i in range(fade_in_frames + 1):
        alpha = i / fade_in_frames  # Gradual appearance
        overlay = frame.copy()
        
        # Draw the speech bubble
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), -1)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 0, 0), 2)
        
        # Draw tail
        cv2.line(overlay, (x + w // 2, y + h), (x + w // 2 + 20, y + h + 30), (0, 0, 0), 2)
        cv2.line(overlay, (x + w // 2 + 20, y + h + 30), (x + w // 2 + 40, y + h), (0, 0, 0), 2)

        # Merge with transparency
        blended = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        cv2.imshow("Cartoon Transition", blended)
        cv2.waitKey(30)

    return frame

def animate_text(img, text, position=(65, 80), delay=150):
    """Animates text appearing word by word in the speech bubble."""
    words = text.split()
    display_text = ""
    
    for word in words:
        display_text += word + " "
        temp_img = img.copy()
        cv2.putText(temp_img, display_text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        cv2.imshow("Cartoon with Speech", temp_img)
        cv2.waitKey(delay)

    return temp_img

def transition_to_cartoon(image_path, text, style="cartoon", transition_frames=50):
    """Applies a smooth transition from original image to a cartoon effect with animated speech bubble and text."""
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Unable to load image.")
        return

    cartoon = cartoonize_image(img, style)

    for i in range(transition_frames + 1):
        alpha = i / transition_frames
        blended = cv2.addWeighted(cartoon, alpha, img, 1 - alpha, 0)
        cv2.imshow("Cartoon Transition", blended)
        cv2.waitKey(30)

    frame_with_bubble = add_speech_bubble(cartoon, text)
    final_frame = animate_text(frame_with_bubble, text)
    
    cv2.imshow("Final Cartoon", final_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("cartoon_output.jpg", final_frame)

# Example usage
transition_to_cartoon("politician.jpg", "I promise change!", style="cartoon")
