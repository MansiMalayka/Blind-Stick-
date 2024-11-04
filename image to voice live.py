from ultralytics import YOLO
import cvzone
import cv2
import os
import pyttsx3
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Load the YOLO model (make sure the path to 'yolov10n.pt' is correct)
model = YOLO('yolov10n.pt')

# Path to the image
image_path = 'path/to/your/image.jpg'

if not os.path.exists(image_path):
    print(f"Error: The file {image_path} does not exist.")
else:
    # Detect objects in the image if it exists
    results = model(image_path)
    results[0].show()

# Initialize webcam (try different indices if it doesn't work)
cap = cv2.VideoCapture(0)  # Change index as needed

# Keep track of the last spoken class to avoid repeating
last_spoken_class = None

while True:
    ret, image = cap.read()
    if not ret:
        print("Failed to grab frame from webcam.")
        break  # Exit if the camera feed is not working

    # Run YOLO detection on the captured frame
    results = model(image)

    # Draw bounding boxes and labels on detected objects
    for info in results:
        parameters = info.boxes
        for box in parameters:
            # Extract coordinates, confidence, and class name
            x1, y1, x2, y2 = box.xyxy[0].numpy().astype('int')
            confidence = int(box.conf[0].numpy() * 100)
            class_detected_number = int(box.cls[0].numpy())
            class_detected_name = results[0].names[class_detected_number]

            # Draw rectangle and label
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cvzone.putTextRect(image, f'{class_detected_name} {confidence}%', 
                               [x1 + 8, y1 - 12], thickness=2, scale=1.5, colorR=(0, 255, 0))

            # Check if the current class is different from the last spoken class
            if class_detected_name != last_spoken_class:
                # Speak the detected class
                engine.say(f"Detected {class_detected_name} with confidence {confidence}%")
                engine.runAndWait()
                # Update the last spoken class
                last_spoken_class = class_detected_name
                # Add a short delay to reduce load
                time.sleep(2)  # Delay in seconds

    # Check if the image is valid before displaying
    if image is None or image.size == 0:
        print("Error: Image is empty or not loaded correctly.")
        continue

    # Display the frame with detections
    cv2.imshow('frame', image)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
