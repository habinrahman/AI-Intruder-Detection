import cv2
import time

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 for default webcam

# Give the camera time to adjust
time.sleep(2)

# Capture the image
ret, frame = cap.read()

if ret:
    image_path = "intruder_detected.jpg"
    cv2.imwrite(image_path, frame)
    print(f"📸 Intruder image captured: {image_path}")
else:
    print("❌ Failed to capture image")

# Release the camera
cap.release()
cv2.destroyAllWindows()
