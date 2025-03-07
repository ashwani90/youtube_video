import cv2
import numpy as np

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

def add_speech_bubble(img, text, position=(50, 50), bubble_size=(200, 100)):
    """Adds a speech bubble with text to the image."""
    x, y = position
    w, h = bubble_size

    # Draw the speech bubble
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)

    # Draw tail
    cv2.line(img, (x + w // 2, y + h), (x + w // 2 + 20, y + h + 30), (0, 0, 0), 2)
    cv2.line(img, (x + w // 2 + 20, y + h + 30), (x + w // 2 + 40, y + h), (0, 0, 0), 2)

    # Add text
    cv2.putText(img, text, (x + 10, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return img

def create_cartoon_with_speech_bubble(image_path, text, style="cartoon"):
    """Converts an image into a cartoon, adds a speech bubble, and saves the result."""
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Unable to load image.")
        return

    cartoon = cartoonize_image(img, style)
    cartoon_with_bubble = add_speech_bubble(cartoon, text)

    # cv2.imshow("Cartoon", cartoon_with_bubble)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("../output/cartoon_output_ai.jpg", cartoon_with_bubble)

# Example usage
create_cartoon_with_speech_bubble("../images/abcd.jpeg", "I promise change!", style="cartoon")
