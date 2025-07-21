import cv2
import os
import datetime

def capture_image(folder="intruder_images"):
    # Create timestamp for unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"intruder_{timestamp}.jpg"
    output_path = os.path.join(folder, filename)

    # Access webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return None

    ret, frame = cap.read()

    if ret:
        os.makedirs(folder, exist_ok=True)
        cv2.imwrite(output_path, frame)
        print(f"📸 Intruder image saved at: {output_path}")
    else:
        print("Error: Could not capture the image.")
        output_path = None

    cap.release()
    return output_path
