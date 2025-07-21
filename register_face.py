import cv2
import face_recognition
import numpy as np
import pickle

# Load webcam
cap = cv2.VideoCapture(0)

print("Capturing your face. Look at the camera...")

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    # Detect face
    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        # Save the encoding to a file
        with open("authorized_face.pkl", "wb") as f:
            pickle.dump(face_encodings[0], f)
        
        print("✅ Face captured and saved for authentication!")
        break

cap.release()
cv2.destroyAllWindows()
