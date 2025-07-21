import time
import os

# Global variable to store the last logged time
last_logged_time = 0  # Stores the last time an intrusion was logged
cooldown_time = 10  # Minimum seconds between logs

def log_intrusion():
    global last_logged_time
    folder = "logs"
    os.makedirs(folder, exist_ok=True)  # Ensure logs folder exists

    log_file = f"{folder}/intruder_log.txt"
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Prevent logging too frequently (cooldown)
    current_time = time.time()
    if current_time - last_logged_time < cooldown_time:
        print("⏳ Skipping duplicate intrusion log (too soon)")
        return  # Skip logging if cooldown period hasn't passed

    last_logged_time = current_time  # Update last logged time

    # Append log entry
    with open(log_file, "a") as file:
        file.write(f"Intruder detected at {timestamp}\n")

    print(f"✅ Intrusion logged: {timestamp}")  # Print log confirmation
