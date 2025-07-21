import os

# Folder where intruder images are stored
folder = "C:\\Users\\habin\\OneDrive\\Desktop\\INTRUDER\\Intruder_Logs"

# Ensure the folder exists
if not os.path.exists(folder):
    print(f"❌ Folder Not Found: {folder}")
else:
    print(f"✅ Folder Exists: {folder}")

# Get the list of image files
files = [f for f in os.listdir(folder) if f.endswith(".jpg")]

# Print debugging info
print(f"🔍 Found {len(files)} images.")

if files:
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(folder, f)))
    latest_path = os.path.join(folder, latest_file)
    print(f"✅ Latest Image: {latest_path}")
else:
    print("⚠️ No images found! Capture a new one.")
