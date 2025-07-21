import cv2
import os
import time
import datetime
import threading
from send_alert import send_intruder_alert
from log import log_intrusion
import face_recognition
import numpy as np
import argparse

cv2.ocl.setUseOpenCL(False)  # Disable OpenCL for faster startup

# Folder for storing intruder images
IMAGE_FOLDER = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\Intruder_Logs"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def capture_intruder_image(image_folder, show_preview=False):
    def reinitialize_camera():
        nonlocal cap
        print("[INFO] Reinitializing camera...")
        cap.release()
        time.sleep(1.5)
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("[INFO] Initializing camera...")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(1.5)

    # Warm-up camera
    for _ in range(2):
        cap.read()

    # Try grabbing a valid frame
    for attempt in range(3):
        ret, frame = cap.read()
        if ret and frame is not None and frame.size > 0:
            print(f"[INFO] Successfully read frame on attempt {attempt+1}")
            break
        print(f"[WARNING] Failed to read from camera (Attempt {attempt+1}/3). Retrying...")
        reinitialize_camera()
    else:
        print("❌ Camera could not provide a valid frame after retries.")
        cap.release()
        cv2.destroyAllWindows()
        return None, False

    cap.release()
    cv2.destroyAllWindows()

    # Resize for faster detection
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

    face_locations = face_recognition.face_locations(small_frame)
    face_detected = len(face_locations) > 0

    # Scale face locations back to original size
    scaled_face_locations = []
    if face_detected:
        for top, right, bottom, left in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            scaled_face_locations.append((top, right, bottom, left))

    blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)
    if face_detected:
        for top, right, bottom, left in scaled_face_locations:
            face_region = frame[top:bottom, left:right]
            blurred_frame[top:bottom, left:right] = face_region
            cv2.rectangle(blurred_frame, (left, top), (right, bottom), (0, 255, 0), 2)

    if show_preview:
        cv2.imshow("Intruder Detected", blurred_frame)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(image_folder, f"intruder_{timestamp}_blurred.jpg")
    cv2.imwrite(image_path, blurred_frame)

    print(f"🎯 Saved: {image_path}")
    return image_path, face_detected

def detect_intruder(show_preview=False):
    print("==============================")
    print("🔴 INTRUDER DETECTED - ACTION 🔴")
    print("==============================")

    image_path, face_detected = capture_intruder_image(IMAGE_FOLDER, show_preview=show_preview)

    if image_path:
        subject = "🔴 Intruder Alert: Face Detected" if face_detected else "⚠️ Intruder Alert: No Face Detected"
        body = (
            "A face was detected by the Intruder Detection System. See attached image."
            if face_detected
            else "Motion or suspicious activity detected, but no face was recognized. See attached image."
        )

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body += f"\n\nTimestamp: {timestamp}"

        def send_and_log():
            send_intruder_alert(image_path, subject=subject, body=body)
            log_intrusion(image_path)

        threading.Thread(target=send_and_log).start()

if __name__ == "__main__":
    print(r"""
╔══════════════════════════════════════╗
║ 🛡️ INTRUDER DETECTION SYSTEM ACTIVE  ║ 
╚══════════════════════════════════════╝
""")

    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="Show preview window")
    parser.add_argument("--timer", action="store_true", help="Show execution timing")
    args = parser.parse_args()

    start_time = time.time()
    detect_intruder(show_preview=args.preview)
    if args.timer:
        print(f"\n⏱️ Execution Time: {time.time() - start_time:.2f} seconds")
