import mysql.connector
import cv2

# ✅ Replace 'root' and 'your_actual_password' with your correct MySQL username and password
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Change this if your MySQL user is different
    password="your_actual_password",  # Change this to your actual MySQL password
    database="intruder"
)
cursor = conn.cursor()


# Fetch the latest intruder image
cursor.execute("SELECT image_path FROM intruder_logs ORDER BY detected_at DESC LIMIT 1")
result = cursor.fetchone()

if result:
    image_path = result[0]
    print(f"Displaying: {image_path}")
    
    # Show the image
    img = cv2.imread(image_path)
    cv2.imshow("Intruder Detected", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No intruder images found.")

cursor.close()
conn.close()
