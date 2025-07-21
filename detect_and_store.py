import cv2
import face_recognition
import numpy as np
import pickle
import time
import mysql.connector
import smtplib
from email.message import EmailMessage

# Load authorized face
with open("authorized_face.pkl", "rb") as f:
    authorized_face = pickle.load(f)

# Initialize camera
cap = cv2.VideoCapture(0)
time.sleep(2)  # Small delay to allow camera to adjust

ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Error capturing image")
    exit()

# Face detection
face_locations = face_recognition.face_locations(frame)
face_encodings = face_recognition.face_encodings(frame, face_locations)

# Check if face is recognized
intruder_detected = True
for face_encoding in face_encodings:
    match = face_recognition.compare_faces([authorized_face], face_encoding, tolerance=0.5)
    if match[0]:
        intruder_detected = False
        print("✅ Authenticated User - No Intrusion")
        break

# If intruder detected, save image & send alert
if intruder_detected:
    image_path = "intruder_detected.jpg"
    cv2.imwrite(image_path, frame)
    print(f"📸 Intruder image captured: {image_path}")

    # Store in database
    conn = mysql.connector.connect(host="localhost", user="root", password="password", database="intruder")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO intrusions (image_path, detected_at, status) VALUES (%s, NOW(), %s)", (image_path, "unknown"))
    conn.commit()
    conn.close()
    print(f"✅ Intrusion record inserted: {image_path}")

    # Send email alert
    msg = EmailMessage()
    msg['Subject'] = '🚨 Intruder Alert!'
    msg['From'] = 'nnm24mc050@nmamit.in'
    msg['To'] = 'nnm24mc050@nmamit.in'
    msg.set_content(f"An intrusion was detected! See attached image.")

    with open(image_path, 'rb') as img:
        msg.add_attachment(img.read(), maintype='image', subtype='jpeg', filename=image_path)

    with smtplib.SMTP('mail.smtp2go.com', 2525) as smtp:
        smtp.starttls()
        smtp.login("habin", "nu24mca50")
        smtp.send_message(msg)

    print("📩 Email alert sent successfully via SMTP2GO!")
