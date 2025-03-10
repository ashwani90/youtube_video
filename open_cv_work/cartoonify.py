import cv2

def cartoonify_image(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply median blur
    blurred = cv2.medianBlur(gray, 5)
    
    # Detect edges using adaptive threshold
    edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                  cv2.THRESH_BINARY, 9, 10)
    
    # Apply bilateral filter to reduce noise
    color = cv2.bilateralFilter(img, 9, 300, 300)
    
    # Combine edges and color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    # Save and show the output
    cv2.imwrite(output_path, cartoon)
    # cv2.imshow("Cartoon Image", cartoon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
cartoonify_image("../images/abcd.jpeg", "../output/cartoon_output.jpg")
