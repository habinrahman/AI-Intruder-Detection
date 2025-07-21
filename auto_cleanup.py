import os
import time

# Set the folder paths
IMAGE_FOLDER = "Intruder_Logs"
LOG_FILE = "logs/intruder_log.txt"

# Set retention time (in seconds)
RETENTION_DAYS = 7  # Change this to the number of days you want to keep files
RETENTION_TIME = RETENTION_DAYS * 24 * 60 * 60  # Convert days to seconds

def delete_old_images():
    """Deletes intruder images older than the retention period."""
    current_time = time.time()

    if not os.path.exists(IMAGE_FOLDER):
        print("📂 No images found to delete.")
        return

    for filename in os.listdir(IMAGE_FOLDER):
        file_path = os.path.join(IMAGE_FOLDER, filename)

        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)

            if file_age > RETENTION_TIME:
                os.remove(file_path)
                print(f"🗑️ Deleted old image: {filename}")

def clean_old_logs():
    """Deletes log entries older than the retention period."""
    if not os.path.exists(LOG_FILE):
        print("📂 No log file found.")
        return

    new_lines = []
    current_time = time.time()

    with open(LOG_FILE, "r") as file:
        for line in file:
            try:
                log_time_str = line.strip().split("at ")[-1]
                log_time = time.mktime(time.strptime(log_time_str, "%Y-%m-%d %H:%M:%S"))

                if current_time - log_time <= RETENTION_TIME:
                    new_lines.append(line)  # Keep recent logs
            except ValueError:
                new_lines.append(line)  # Keep malformed or recent logs

    # Write back only the recent logs
    with open(LOG_FILE, "w") as file:
        file.writelines(new_lines)

    print("🧹 Log cleanup complete!")

if __name__ == "__main__":
    delete_old_images()
    clean_old_logs()
