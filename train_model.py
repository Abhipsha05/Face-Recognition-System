import cv2
import numpy as np
import os

# Directory containing training data
data_dir = "data"

# Initialize LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()


# Load training data
def get_images_and_labels(data_dir):
    image_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    images = []
    labels = []
    for image_path in image_paths:
        # Read image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        images.append(image)
        # Extract label from file name
        label = os.path.basename(image_path).split("_")[0]
        labels.append(int(label))
        cv2.imshow("Training", image)
        cv2.waitKey(1)
    return images, np.array(labels)


images, labels = get_images_and_labels(data_dir)

# Convert labels to the correct data type
labels = labels.astype(np.int32)

# Train the recognizer
recognizer.train(images, labels)

# Save the trained model
recognizer.save("trained_model.yml")

print("Training complete. Model saved as 'trained_model.yml'.")
