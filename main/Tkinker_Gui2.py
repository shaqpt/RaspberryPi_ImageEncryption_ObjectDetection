import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import tflite_runtime.interpreter as tflite

# Load TensorFlow Lite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="efficientdet_lite0.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Set up GUI
root = tk.Tk()
root.title("Webcam Object Detection")

# Create a label for the video feed
label = tk.Label(root)
label.pack(padx=10, pady=10)

# Open webcam
cap = cv2.VideoCapture(0)

def detect_objects(frame):
    # Preprocess the frame for object detection
    input_shape = input_details[0]['shape']
    resized_frame = cv2.resize(frame, (input_shape[1], input_shape[2]))
    input_data = np.expand_dims(resized_frame, axis=0)

    # Convert input data to UINT8
    input_data = np.uint8(input_data)

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get output
    boxes = interpreter.get_tensor(output_details[0]['index'])
    classes = interpreter.get_tensor(output_details[1]['index'])
    scores = interpreter.get_tensor(output_details[2]['index'])
    num_detections = int(interpreter.get_tensor(output_details[3]['index']))

    # Draw detected objects on frame
    for i in range(num_detections):
        if scores[0][i] > 0.5:  # Confidence threshold
            ymin, xmin, ymax, xmax = boxes[0][i]
            xmin = int(xmin * frame.shape[1])
            xmax = int(xmax * frame.shape[1])
            ymin = int(ymin * frame.shape[0])
            ymax = int(ymax * frame.shape[0])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    return frame

def update_video():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        frame = detect_objects(frame)  # Detect objects
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        label.configure(image=frame)
        label.image = frame
    label.after(10, update_video)

def capture_image():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        print("Image captured and saved as captured_image.jpg")

def stop_program():
    # Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

# Button to capture image
capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack(side=tk.LEFT, padx=10, pady=10)

# Button to stop the program
stop_button = tk.Button(root, text="Stop Program", command=stop_program)
stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Start video update process
update_video()

root.mainloop()
