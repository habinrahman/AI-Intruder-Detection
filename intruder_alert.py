import cv2
import face_recognition
import os
import pickle
import smtplib
import datetime
from email.message import EmailMessage

# Paths
IMAGE_FOLDER = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\Intruder_Logs"
DB_FILE = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\face_db.pkl"
LOG_FILE = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\intruder_log.txt"

# Email Configuration (Replace with actual credentials)
SMTP_SERVER = "mail.smtp2go.com"
SMTP_PORT = 587
SMTP_USERNAME = "habin"
SMTP_PASSWORD = "nu24mca50"
SENDER_EMAIL = "nnm24mc050@nmamit.in"
RECEIVER_EMAIL = "nnm24mc050@nmamit.in"

# Load authorized faces
def load_authorized_faces():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    return {}

# Capture image from webcam
def capture_intruder_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Failed to capture image!")
        return None

    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    image_path = os.path.join(IMAGE_FOLDER, f"intruder_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    cv2.imwrite(image_path, frame)
    print(f"📸 Intruder Image Captured: {image_path}")
    return image_path

# Check if person is an intruder
def is_intruder(image_path):
    authorized_faces = load_authorized_faces()

    intruder_image = face_recognition.load_image_file(image_path)
    intruder_encoding = face_recognition.face_encodings(intruder_image)

    if not intruder_encoding:
        print("⚠️ No face detected in the image.")
        return True  # Assume intruder if no face is found

    intruder_encoding = intruder_encoding[0]

    for name, known_encoding in authorized_faces.items():
        results = face_recognition.compare_faces([known_encoding], intruder_encoding, tolerance=0.6)
        if results[0]:
            print(f"✅ Authorized person detected: {name}")
            return False

    print("🚨 Intruder detected!")
    return True

# Send email alert
def send_intruder_alert(image_path):
    if not is_intruder(image_path):
        return

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "🚨 Intruder Alert!"
    msg.set_content(f"An intruder has been detected. See the attached image.")

    with open(image_path, "rb") as img_file:
        msg.add_attachment(img_file.read(), maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print("📧 Alert email sent successfully!")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

# Log intrusion
def log_intrusion(image_path):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Intruder detected: {image_path}\n")
    print("📝 Intrusion logged!")

if __name__ == "__main__":
    image_path = capture_intruder_image()
    if image_path:
        send_intruder_alert(image_path)
        log_intrusion(image_path)
