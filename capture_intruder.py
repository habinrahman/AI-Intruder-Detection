import cv2
import time
import os

def capture_images():
    folder = "Intruder_Logs"
    os.makedirs(folder, exist_ok=True)  # Create folder if not exists

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    for i in range(3):  # Capture 3 images
        ret, frame = camera.read()
        if ret:
            filename = f"{folder}/intruder_{time.strftime('%Y%m%d-%H%M%S')}_{i}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")
            time.sleep(1)

    camera.release()
    cv2.destroyAllWindows()
