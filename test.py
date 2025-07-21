import cv2

image_path = r"C:\Users\habin\OneDrive\Desktop\INTRUDER\your_image.png"
image = cv2.imread(image_path)

if image is None:
    print("❌ Error: Could not load image. Check the file path.")
else:
    print("✅ Image loaded successfully!")
