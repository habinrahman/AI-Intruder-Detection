import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="intruder"
)

cursor = conn.cursor()

# Fetch all intrusion records
cursor.execute("SELECT * FROM intrusions")
records = cursor.fetchall()

print("\n📌 Intrusions Detected:")
print("-" * 50)
for record in records:
    print(f"ID: {record[0]}, Image: {record[1]}, Detected At: {record[2]}, Status: {record[3]}")

# Close connection
cursor.close()
conn.close()
