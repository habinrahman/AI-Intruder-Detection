import sqlite3
import time
import os

def store_in_database(image_path):
    folder = "database"
    os.makedirs(folder, exist_ok=True)  # Ensure database folder exists

    conn = sqlite3.connect(f"{folder}/intruder_records.db")
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intruders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            image_path TEXT
        )
    """)

    # Insert record
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO intruders (timestamp, image_path) VALUES (?, ?)", (timestamp, image_path))

    conn.commit()
    conn.close()
    print("✅ Intruder data stored in database!")

# Example Usage
image_path = "Intruder_Logs/intruder_2025-03-25_20-18-51.jpg"  # Update with correct path
store_in_database(image_path)
