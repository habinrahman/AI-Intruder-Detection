import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # Use the new password
    database="intruder"
)

if conn.is_connected():
    print("✅ Successfully connected to the database!")

conn.close()
