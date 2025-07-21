from send_alert import get_latest_image, send_intruder_alert
import time

IMAGE_FOLDER = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\Intruder_Logs"

try:
    image_path = get_latest_image(IMAGE_FOLDER)
    if image_path:
        send_intruder_alert(image_path)
    else:
        print("⚠️ No image to process.")
except Exception as e:
    print("❌ ERROR:", e)

input("\nPress Enter to exit...")
