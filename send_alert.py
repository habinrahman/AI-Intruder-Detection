import smtplib
import os
import time
import face_recognition
import pickle
from email.message import EmailMessage
import cv2

# 🔹 Import Secure Credentials
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, RECEIVER_EMAIL

# 🔹 Paths
IMAGE_FOLDER = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\Intruder_Logs"
DB_FILE = "face_db.pkl"
LOG_FILE = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\intruder_log.txt"

def load_authorized_faces():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def get_latest_image(folder):
    try:
        image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            print("❌ No intruder images found!")
            return None
        
        latest_image = max(image_files, key=lambda f: os.path.getmtime(os.path.join(folder, f)))
        latest_image_path = os.path.join(folder, latest_image)
        
        print(f"✅ Latest Image Selected: {latest_image_path}")
        return latest_image_path

    except Exception as e:
        print(f"❌ Error finding latest image: {e}")
        return None

def is_intruder(image_path):
    authorized_faces = load_authorized_faces()

    intruder_image = face_recognition.load_image_file(image_path)
    intruder_encoding = face_recognition.face_encodings(intruder_image)

    if not intruder_encoding:
        print("⚠️ No face detected in the captured image.")
        return True  # Assume intruder

    intruder_encoding = intruder_encoding[0]

    for name, known_encoding in authorized_faces.items():
        results = face_recognition.compare_faces([known_encoding], intruder_encoding, tolerance=0.6)
        if results[0]:
            print(f"✅ Face Matched! Person: {name}")
            return False

    print("🚨 Intruder detected! No match found.")
    return True

def send_intruder_alert(image_path, subject="🚨 Intruder Alert!", body=None):
    if not is_intruder(image_path):
        print("✅ No alert needed. Authorized person detected.")
        return

    try:
        print("🔹 Connecting to SMTP2GO...")
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.set_content(body or f"An intruder has been detected. See the attached image: {os.path.basename(image_path)}")

        with open(image_path, "rb") as img_file:
            msg.add_attachment(img_file.read(), maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"📧 Email Sent Successfully! Attached: {image_path}")

        log_intrusion(image_path)

    except Exception as e:
        print(f"❌ Error sending email: {e}")

def log_intrusion(image_path):
    try:
        with open(LOG_FILE, "a") as log:
            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Intruder detected: {image_path}\n")
        print("📝 Intrusion logged successfully!")
    except Exception as e:
        print(f"❌ Error logging intrusion: {e}")

if __name__ == "__main__":
    image_path = get_latest_image(IMAGE_FOLDER)
    if image_path:
        send_intruder_alert(image_path)
