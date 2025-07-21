import mysql.connector

def store_intrusion(image_path, status="unknown"):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",  # Use your actual password
            database="intruder"
        )
        cursor = conn.cursor()

        query = "INSERT INTO intrusions (image_path, status) VALUES (%s, %s)"
        values = (image_path, status)
        cursor.execute(query, values)
        conn.commit()

        print(f"✅ Intrusion record inserted: {image_path}, Status: {status}")
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

# Example Usage
store_intrusion("intruder_001.jpg", "unknown")
