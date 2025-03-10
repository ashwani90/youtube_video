import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO

def cartoonify(image_path):
    # Load the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (800, 800))  # Resize for better processing

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply median blur
    gray = cv2.medianBlur(gray, 5)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter for smooth color regions
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # Combine edges with the color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

def generate_ai_overlay(prompt, width=512, height=512):
    """
    Uses Stable Diffusion API to generate an AI-based satire element based on the given prompt.
    Replace the API URL with a real text-to-image model or a local Stable Diffusion instance.
    """
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
    """
    Overlays the AI-generated image onto the cartoonified image.
    """
    bg = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
    overlay = overlay.resize((200, 200))  # Resize overlay for better fit
    bg.paste(overlay, position, overlay if overlay.mode == 'RGBA' else None)
    return np.array(bg)

# Main execution
image_path = "../images/abcd.jpeg"  # Replace with your image file
prompt = "A politician with an exaggerated nose giving a speech"  # Modify for satire

# Convert image to cartoon
cartoon_image = cartoonify(image_path)

# Generate AI satire overlay
# ai_image = generate_ai_overlay(prompt)

# If AI-generated image is available, overlay it
# if ai_image:
#     final_image = overlay_images(cartoon_image, ai_image)
# else:
final_image = cartoon_image

# Save and display
# cv2.ismshow("Cartoon Satire", final_image)
cv2.imwrite("../output/cartoon_output_ai.jpg", final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
