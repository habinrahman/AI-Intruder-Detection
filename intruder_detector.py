import smtplib
import os
import time
import face_recognition
import pickle
from email.message import EmailMessage

# SMTP2GO Configuration
SMTP_SERVER = "mail.smtp2go.com"
SMTP_PORT = 587
SMTP_USERNAME = "habin"
SMTP_PASSWORD = "nu24mca50"

# Email Details
SENDER_EMAIL = "nnm24mc050@nmamit.in"
RECEIVER_EMAIL = "nnm24mc050@nmamit.in"

# Paths
IMAGE_FOLDER = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\Intruder_Logs"
DB_FILE = "face_db.pkl"
LOG_FILE = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\intruder_log.txt"

def load_authorized_faces():
    """Loads registered faces from the database."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def get_latest_image(folder):
    """Finds the latest image file in the folder."""
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
    """Checks if the captured face matches any authorized faces."""
    authorized_faces = load_authorized_faces()

    intruder_image = face_recognition.load_image_file(image_path)
    intruder_encoding = face_recognition.face_encodings(intruder_image)

    if not intruder_encoding:
        print("⚠️ No face detected in the captured image.")
        return True  # If no face is detected, assume it's an intruder

    intruder_encoding = intruder_encoding[0]

    # Compare with stored faces
    for name, known_encoding in authorized_faces.items():
        results = face_recognition.compare_faces([known_encoding], intruder_encoding, tolerance=0.6)
        if results[0]:
            print(f"✅ Face Matched! Person: {name}")
            return False  # Not an intruder

    print("🚨 Intruder detected! No match found.")
    return True  # Intruder detected

def send_intruder_alert(image_path):
    """Sends an email alert if an intruder is detected."""
    if not is_intruder(image_path):
        print("✅ No alert needed. Authorized person detected.")
        return

    try:
        print("🔹 Connecting to SMTP2GO...")
        msg = EmailMessage()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "🚨 Intruder Alert!"
        msg.set_content(f"An intruder has been detected. See the attached image: {os.path.basename(image_path)}")

        with open(image_path, "rb") as img_file:
            msg.add_attachment(img_file.read(), maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"📧 Email Sent Successfully! Attached: {image_path}")

        # Log the intrusion
        log_intrusion(image_path)

        # Cleanup old images
        cleanup_old_images(IMAGE_FOLDER)

    except Exception as e:
        print(f"❌ Error sending email: {e}")

def log_intrusion(image_path):
    """Logs intrusions with timestamps and image path."""
    try:
        with open(LOG_FILE, "a") as log:
            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Intruder detected: {image_path}\n")
        print("📝 Intrusion logged successfully!")
    except Exception as e:
        print(f"❌ Error logging intrusion: {e}")

def cleanup_old_images(folder, keep_last=5):
    """Keeps only the latest 'keep_last' images and deletes older ones."""
    try:
        image_files = sorted(
            [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
            key=os.path.getmtime
        )
        
        if len(image_files) > keep_last:
            for old_image in image_files[:-keep_last]:  # Keep only the last 'keep_last' images
                os.remove(old_image)
                print(f"🗑️ Deleted old image: {old_image}")

    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

if __name__ == "__main__":
    image_path = get_latest_image(IMAGE_FOLDER)
    if image_path:
        send_intruder_alert(image_path)
