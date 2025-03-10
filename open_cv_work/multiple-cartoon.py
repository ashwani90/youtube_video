import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def cartoonify(image_path, style="classic"):
    """ Converts an image into a cartoon-style image based on the selected style. """
    img = cv2.imread(image_path)
    img = cv2.resize(img, (800, 800))  

    if style == "classic":
        # Grayscale + Edge Detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    elif style == "watercolor":
        # Apply watercolor effect
        cartoon = cv2.stylization(img, sigma_s=60, sigma_r=0.6)

    elif style == "comic":
        # Strong edges + color quantization
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        quantized = cv2.pyrMeanShiftFiltering(img, 20, 40)
        cartoon = cv2.bitwise_and(quantized, quantized, mask=edges)
    
    elif style == "cel_shading":
        # Reduce color depth + strong outlines
        blurred = cv2.medianBlur(img, 5)
        edges = cv2.Canny(blurred, 100, 200)
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    
    else:
        raise ValueError("Invalid style. Choose 'classic', 'watercolor', 'comic', or 'cel_shading'.")

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

def add_speech_bubbles(image, texts, positions):
    """
    Adds multiple speech bubbles with text to the cartoon image.

    - `texts`: List of text strings.
    - `positions`: List of positions, one for each text. Options: "top-left", "top-right", "bottom-left", "bottom-right".
    """
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)

    bubble_width = 300
    bubble_height = 100
    margin = 20

    for i, text in enumerate(texts):
        position = positions[i]
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
selected_style = "comic"  # Change to 'classic', 'watercolor', 'comic', or 'cel_shading'

# Convert image to cartoon with the selected style
cartoon_image = cartoonify(image_path, style=selected_style)

# Generate AI satire overlay
# ai_image = generate_ai_overlay(prompt)

# Overlay AI-generated satire if available
# if ai_image:
#     final_image = overlay_images(cartoon_image, ai_image)
# else:
final_image = cartoon_image

# Add multiple speech bubbles
speech_texts = [
    "We promise transparency!",
    "Meanwhile, behind closed doors..."
]
bubble_positions = ["top-left", "bottom-right"]

final_image_with_bubbles = add_speech_bubbles(final_image, speech_texts, bubble_positions)

# Save and display
# cv2.imshow("Cartoon Satire", final_image_with_bubbles)
cv2.imwrite("../output/cartoon_output_ai.jpg", final_image_with_bubbles)
cv2.waitKey(0)
cv2.destroyAllWindows()
