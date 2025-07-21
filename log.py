# log.py
import datetime

def log_intrusion(image_path):
    log_file = "intrusion_log.txt"
    with open(log_file, "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] Intruder detected. Image saved at: {image_path}\n")
    print(f"📝 Intrusion logged in {log_file}")
