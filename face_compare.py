# face_compare.py
import face_recognition

def is_authorized_person(captured_path, known_path):
    known_img = face_recognition.load_image_file(known_path)
    captured_img = face_recognition.load_image_file(captured_path)

    try:
        known_encoding = face_recognition.face_encodings(known_img)[0]
        captured_encoding = face_recognition.face_encodings(captured_img)[0]
    except IndexError:
        print("[❌] Face not detected in one of the images")
        return False

    result = face_recognition.compare_faces([known_encoding], captured_encoding)
    return result[0]
