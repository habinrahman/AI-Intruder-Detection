import cv2
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# === CONFIGURATION ===
SMTP_SERVER = "mail.smtp2go.com"
SMTP_PORT = 587
SENDER_EMAIL = "nnm24mco050@nmamit.in"
SENDER_PASSWORD = "nu24mca50"
RECIPIENT_EMAIL = "nnm24mco050@nmamit.in"

# === Step 1: Capture Image ===
def capture_intruder_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Cannot access webcam.")
        return None
    
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Error: Failed to capture image.")
        return None

    os.makedirs("Intruder_Logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    img_path = f"Intruder_Logs/intruder_{timestamp}.jpg"
    cv2.imwrite(img_path, frame)
    print(f"📸 Intruder image saved: {img_path}")
    return img_path, timestamp

# === Step 2: Send Email Alert ===
def send_email_with_attachment(image_path, timestamp):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "🚨 Intruder Alert Detected!"

        body = f"An intruder was detected at {timestamp}. Please find the attached image."
        msg.attach(MIMEText(body, 'plain'))

        with open(image_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(image_path)}"')
            msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("📩 Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# === Step 3: Log Intrusion ===
def log_intrusion(image_path, timestamp):
    log_file = "Intruder_Logs/intruder_log.txt"
    with open(log_file, "a") as log:
        log.write(f"[{timestamp}] Intruder captured: {image_path}\n")
    print("📝 Intrusion logged.")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    result = capture_intruder_image()
    if result:
        image_path, timestamp = result
        send_email_with_attachment(image_path, timestamp)
        log_intrusion(image_path, timestamp)
