import face_recognition
import os
import pickle

AUTHORIZED_DIR = "authorized_faces"
DB_FILE = "face_db.pkl"

def register_faces():
    """Encodes and saves authorized faces."""
    face_encodings = {}

    for filename in os.listdir(AUTHORIZED_DIR):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(AUTHORIZED_DIR, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)

            if encoding:
                face_encodings[filename] = encoding[0]
                print(f"✅ {filename} registered successfully!")

    # Save encodings to a file
    with open(DB_FILE, "wb") as f:
        pickle.dump(face_encodings, f)
    
    print("🗂️ All faces registered successfully!")

if __name__ == "__main__":
    register_faces()
