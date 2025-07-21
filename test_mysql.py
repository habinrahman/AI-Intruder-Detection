import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="intruder"
    )
    if conn.is_connected():
        print("✅ Successfully connected to MySQL!")
    
    conn.close()

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
