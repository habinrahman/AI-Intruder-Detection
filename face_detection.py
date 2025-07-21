import cv2
import face_recognition

# Load the image
image_path = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\your_image.png"  # Update if necessary
image = cv2.imread(image_path)

# Convert the image from BGR (OpenCV) to RGB (face_recognition)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect face locations
face_locations = face_recognition.face_locations(rgb_image)

# Print the detected face coordinates
print(f"✅ Detected {len(face_locations)} face(s):", face_locations)

# Draw rectangles around detected faces
for (top, right, bottom, left) in face_locations:
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

# Display the image with detected faces
cv2.imshow("Detected Faces", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
