import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# SMTP2GO Credentials (Replace these only in a safe environment)
SMTP_SERVER = "mail.smtp2go.com"
SMTP_PORT = 587
SENDER_EMAIL = "nnm24mco050@nmamit.in"
SENDER_PASSWORD = "nu24mca50"
RECIPIENT_EMAIL = "nnm24mco050@nmamit.in"  # Or whoever you want to alert

def send_intruder_alert(image_path):
    """
    Sends an email alert with the intruder's captured image using SMTP2GO.
    """
    try:
        # Create email message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "🚨 Intruder Alert - Unauthorized Access Detected!"

        # Email body text
        body = "An intruder has been detected. The captured image is attached below."
        msg.attach(MIMEText(body, "plain"))

        # Attach the image
        with open(image_path, "rb") as attachment:
            mime = MIMEBase("application", "octet-stream")
            mime.set_payload(attachment.read())
            encoders.encode_base64(mime)
            mime.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(image_path)}",
            )
            msg.attach(mime)

        # Send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("📩 Alert email sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
