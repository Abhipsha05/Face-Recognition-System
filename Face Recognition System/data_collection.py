import cv2
import os

# Initialize camera
camera = cv2.VideoCapture(0)

# Load OpenCV face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Directory to save collected data
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Take user input for name
name = input("Enter your id: ")

# Start collecting data
count = 0
while True:
    # Capture frame-by-frame
    ret, frame = camera.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for x, y, w, h in faces:
        # Draw rectangle around detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Save the captured face
        cv2.imwrite(
            os.path.join(data_dir, f"{name}_{count}.jpg"), gray[y : y + h, x : x + w]
        )

        count += 1

    # If 500 images taken, exit the loop
    if count == 500:
        break

    # Display the resulting frame
    cv2.imshow("frame", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()

print("Data collection done...........")
