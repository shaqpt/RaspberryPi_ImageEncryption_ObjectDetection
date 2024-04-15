import tkinter as tk
import cv2
from PIL import Image, ImageTk
import tkinter.messagebox as mbox
import numpy as np
import tflite_runtime.interpreter as tflite
import os
import encrypt_decrypt

# Global variables
captured_image = None
video_stopped = False
output_directory = "captured_images"

# Create directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

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
    global video_stopped, captured_image

    if not video_stopped:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            frame = detect_objects(frame)  # Detect objects
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            label.configure(image=frame)
            label.image = frame
            label.after(10, update_video)
    elif captured_image is not None:
        label.configure(image=captured_image)
        label.image = captured_image

def capture_image():
    global video_stopped, captured_image
    ret, frame = cap.read()
    if ret:
        # Draw detected objects on the frame
        frame_with_boxes = detect_objects(frame)

        # Convert the frame with boxes to RGB and create an Image object
        captured_image = cv2.cvtColor(frame_with_boxes, cv2.COLOR_BGR2RGB)
        captured_image = Image.fromarray(captured_image)

        # Save the image to a file
        captured_image.save(os.path.join(output_directory, "captured_image.png"))

        # Convert the captured image to ImageTk format for display
        captured_image = ImageTk.PhotoImage(captured_image)
        video_stopped = True

def restart_video():
    global video_stopped, captured_image
    video_stopped = False
    captured_image = None
    update_video()

def stop_program():
    # Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

# WORKS -- encrypts the entire image
def encrypt_image():
    global video_stopped, encrypted_image
    # Encrypt the captured image
    encrypt_decrypt.encrypt_image(os.path.join(output_directory, "captured_image.png"))
    
    # Load the encrypted image
    encrypted_image = Image.open(os.path.join(output_directory, "captured_encrypted.png"))
    encrypted_image = ImageTk.PhotoImage(encrypted_image)
    
    # Display the encrypted image on the screen
    label.configure(image=encrypted_image)
    label.image = encrypted_image
    mbox.showinfo("Encryption", "Image encrypted successfully.")

def decrypt_image():
    global captured_image
    encrypt_decrypt.decrypt_image(os.path.join(output_directory, "captured_encrypted.png"))
    
    # Load the decrypted image
    decrypted_image = Image.open(os.path.join(output_directory, "captured_decrypted.png"))
    decrypted_image = ImageTk.PhotoImage(decrypted_image)
    
    # Display the decrypted image on the screen
    label.configure(image=decrypted_image)
    label.image = decrypted_image
    mbox.showinfo("Decryption", "Image decrypted successfully.")

# Button to capture image
capture_button = tk.Button(root, text="Capture Image", command=capture_image, bg="blue", fg="white")
capture_button.pack(side=tk.LEFT, padx=10, pady=10)

# Button to restart video feed
restart_button = tk.Button(root, text="Restart Video", command=restart_video, bg="green", fg="white")
restart_button.pack(side=tk.LEFT, padx=10, pady=10)

# Button to stop the program
stop_button = tk.Button(root, text="Stop Program", command=stop_program, bg="red", fg="white")
stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Button to encrypt image
encrypt_button = tk.Button(root, text="Encrypt Image", command=encrypt_image, bg="orange", fg="white")
encrypt_button.pack(side=tk.TOP, padx=10, pady=10)

# Button to decrypt image
decrypt_button = tk.Button(root, text="Decrypt Image", command=decrypt_image, bg="purple", fg="white")
decrypt_button.pack(side=tk.TOP, padx=10, pady=10)

# Start video update process
update_video()

root.mainloop()
