import cv2

# Load image
image = cv2.imread("intruder.jpg")

# Save a copy with a new name
cv2.imwrite("detected_faces.jpg", image)

print("Image saved successfully as detected_faces.jpg")
