import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def cartoonify(image_path):
    """ Converts an image into a cartoon-style image. """
    img = cv2.imread(image_path)
    img = cv2.resize(img, (800, 800))  

    # Convert to grayscale and apply median blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    # Edge detection using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter for smooth colors
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # Combine edges with the filtered image
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def generate_ai_overlay(prompt, width=512, height=512):
    """ Uses Stable Diffusion API to generate an AI-based satire element. """
    API_URL = "https://your-stable-diffusion-api.com/generate"  # Replace with actual API
    payload = {"prompt": prompt, "width": width, "height": height}

    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        return Image.open(image_data)
    else:
        print("Failed to generate AI overlay. Using default cartoon image.")
        return None

def overlay_images(background, overlay, position=(50, 50)):
    """ Overlays the AI-generated satire image onto the cartoon image. """
    bg = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
    overlay = overlay.resize((200, 200))  
    bg.paste(overlay, position, overlay if overlay.mode == 'RGBA' else None)
    return np.array(bg)

def add_speech_bubble(image, text, position="top-left"):
    """
    Adds a speech bubble with text to the cartoon image.
    
    Position options:
    - "top-left"
    - "top-right"
    - "bottom-left"
    - "bottom-right"
    """
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)

    # Define bubble position and size
    bubble_width = 300
    bubble_height = 100
    margin = 20

    if position == "top-left":
        bubble_pos = (margin, margin, margin + bubble_width, margin + bubble_height)
        tail_start = (bubble_pos[0] + 50, bubble_pos[3])
        tail_end = (bubble_pos[0] + 30, bubble_pos[3] + 30)
    elif position == "top-right":
        bubble_pos = (img.width - bubble_width - margin, margin, img.width - margin, margin + bubble_height)
        tail_start = (bubble_pos[2] - 50, bubble_pos[3])
        tail_end = (bubble_pos[2] - 30, bubble_pos[3] + 30)
    elif position == "bottom-left":
        bubble_pos = (margin, img.height - bubble_height - margin, margin + bubble_width, img.height - margin)
        tail_start = (bubble_pos[0] + 50, bubble_pos[1])
        tail_end = (bubble_pos[0] + 30, bubble_pos[1] - 30)
    else:  # "bottom-right"
        bubble_pos = (img.width - bubble_width - margin, img.height - bubble_height - margin, img.width - margin, img.height - margin)
        tail_start = (bubble_pos[2] - 50, bubble_pos[1])
        tail_end = (bubble_pos[2] - 30, bubble_pos[1] - 30)

    # Draw speech bubble
    draw.ellipse([bubble_pos[0], bubble_pos[1], bubble_pos[2], bubble_pos[3]], fill="white", outline="black", width=3)
    draw.line([tail_start, tail_end], fill="black", width=3)

    # Add text
    font = ImageFont.load_default()
    text_position = (bubble_pos[0] + 10, bubble_pos[1] + 10)
    draw.text(text_position, text, fill="black", font=font)

    return np.array(img)

# Main execution
image_path = "../images/abcd.jpeg"  
prompt = "A politician with an exaggerated nose giving a speech"  

# Convert image to cartoon
cartoon_image = cartoonify(image_path)

# Generate AI satire overlay
# ai_image = generate_ai_overlay(prompt)

# Overlay AI-generated satire if available
# if ai_image:
#     final_image = overlay_images(cartoon_image, ai_image)
# else:
final_image = cartoon_image

# Add a speech bubble
speech_text = "Trust me, everything is fine!"
final_image_with_bubble = add_speech_bubble(final_image, speech_text, position="top-left")

# Save and display
# cv2.imshow("Cartoon Satire", final_image_with_bubble)
# can adjust the position ot the speech buble
cv2.imwrite("../output/cartoon_output_ai.jpg", final_image_with_bubble)
cv2.waitKey(0)
cv2.destroyAllWindows()
