import cv2

image_path = "/home/ashwani/Workspace/python/youtube_video/images/background2.jpg"
image = cv2.imread(image_path)

if image is None:
    print("❌ OpenCV could not read the image. It might be corrupt.")
else:
    print("✔ OpenCV successfully loaded the image.")