import face_recognition
import os

# Ensure that the known_faces directory exists
known_faces_folder = "known_faces"
if not os.path.exists(known_faces_folder):
    os.makedirs(known_faces_folder)

# Path to your known face image
image_path = os.path.join(known_faces_folder, "habin.png")

try:
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if encodings:
        print("✅ Face encoding loaded successfully.")
    else:
        print("❌ No face found.")
except FileNotFoundError:
    print(f"❌ The image file {image_path} does not exist. Please add it.")
