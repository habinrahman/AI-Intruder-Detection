import smtplib
import os
import time
import shutil  # ✅ NEW: Used to copy files
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# SMTP Configuration
SMTP_SERVER = "mail.smtp2go.com"
SMTP_PORT = 587
SMTP_USERNAME = "habin"
SMTP_PASSWORD = "nu24mca50"

EMAIL_FROM = "nnm24mc050@nmamit.in"
EMAIL_TO = "nnm24mc050@nmamit.in"
SUBJECT = "🚨 Intruder Alert!"

# ✅ **Function to get the latest intruder image without renaming it**
def get_latest_intruder_image():
    folder = "C:\\Users\\habin\\OneDrive\\Desktop\\INTRUDER\\Intruder_Logs"

    # 🔹 Ensure folder exists
    if not os.path.exists(folder):
        print("❌ Error: Intruder_Logs folder does not exist!")
        return None

    # 🔹 Find all .jpg images
    files = [f for f in os.listdir(folder) if f.endswith(".jpg")]
    
    if not files:
        print("⚠️ No intruder images found!")
        return None

    # 🔹 Sort images by modification time (newest first)
    file_paths = [os.path.join(folder, f) for f in files]
    file_paths.sort(key=os.path.getmtime, reverse=True)

    latest_path = file_paths[0]  # Most recent file
    print(f"✅ Latest Image Selected: {latest_path}")

    # ✅ **Instead of renaming, copy the file to avoid cache issues**
    temp_path = os.path.join(folder, f"temp_intruder_{int(time.time())}.jpg")
    shutil.copy2(latest_path, temp_path)  # This preserves original timestamps

    return temp_path  # Return the new copy

# ✅ **Function to send the latest intruder image via email**
def send_intruder_alert():
    latest_image = get_latest_intruder_image()
    if not latest_image:
        print("❌ No image to send!")
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = SUBJECT

    # 🔹 Email body
    body = "An intruder has been detected. See the attached image."
    msg.attach(MIMEText(body, "plain"))

    # 🔹 Attach the latest image
    with open(latest_image, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(latest_image)}")
        msg.attach(part)

    try:
        print("🔹 Connecting to SMTP2GO...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        print("✅ Connected & Authenticated!")
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print(f"📧 Email Sent Successfully! Attached: {latest_image}")
        server.quit()
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    send_intruder_alert()
