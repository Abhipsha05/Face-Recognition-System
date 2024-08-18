import cv2
import time

# Load the trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trained_model.yml")

# Initialize camera
camera = cv2.VideoCapture(0)

# Set camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Load OpenCV face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Define names associated with each label
names = {
    0: "",
    1: "Abhipsha",
    2: "Swayam",
    # Add more names as needed
}

# Define lock status and time
door_locked = True
last_recognition_time = time.time()
unlock_time = None

# Define recognition delay (in seconds)
recognition_delay = 3

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # If the door is locked or enough time has passed since last recognition
    if door_locked or (time.time() - last_recognition_time) >= recognition_delay:
        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in faces:
            # Recognize faces
            label, confidence = recognizer.predict(gray[y : y + h, x : x + w])

            # If the confidence is less than 100, recognized the face
            if confidence < 100:
                name = names.get(label, "Unknown")
                if name:  # Known user
                    print("Recognizing...")
                    print(f"{name} recognized")
                    last_recognition_time = time.time()
                    unlock_time = time.time()
                    cv2.putText(
                        frame,
                        name,
                        (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2,
                    )
                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2,
                    )
                    if door_locked:
                        print("Door unlocked")
                        door_locked = False
                        time.sleep(5)  # Lock after 10 seconds
                        # elif unlock_time and time.time() >= unlock_time:
                        unlock_time = time.time() + 5
                        print("Door locked")
                        door_locked = True
                    time.sleep(3)  # Wait for 3 seconds after recognition
            else:  # Unknown user
                print("Unknown user detected")
                # print("Recognizing...")
                # time.sleep(3)  # Sleep for 3 seconds
            time.sleep(1)
    # Display the resulting frame
    cv2.imshow("frame", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
