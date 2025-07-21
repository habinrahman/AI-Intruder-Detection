import face_recognition
import cv2

# Load a sample image
image = cv2.imread("habin.png")  # Replace with an actual image path

# Convert image to RGB (face_recognition expects RGB format)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect face locations
face_locations = face_recognition.face_locations(rgb_image)

print("Detected Faces:", face_locations)
