import cv2

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

ret, frame = cap.read()
if ret:
    cv2.imshow("Captured Image", frame)
    cv2.imwrite("intruder.jpg", frame)  # Save image
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
