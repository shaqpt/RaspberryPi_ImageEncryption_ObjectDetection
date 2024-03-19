# Shaqueir Tardif
# ECE 501 Project
# Master's Computer Engineering
# University of Massachusetts Dartmouth
# Electrical and Computer Engineering Department
# Advisor: Dr. Hong Liu

import cv2
import tkinter as tk
from tkinter import ttk
from cryptography.fernet import Fernet
import numpy as np

# Initialize webcam
def init_webcam():
    cap = cv2.VideoCapture(0)
    
    # Continuously capture images from the camera and run inference
    while cap.isOpened():
	    success, image = cap.read()
	    if not success:
		    sys.exit(
		    'ERROR: Unable to read from webcam. Please verify your webcam settings.'
		    )
		    
		    counter += 1
		    image = cv2.flip(image, 1)
		
		    # Stop the program if the ESC key is pressed.
		    if cv2.waitKey(1) == 27:
		        break
		    cv2.imshow('image_envryption', image)

    cap.release()
    cv2.destroyAllWindows()
    return cap

# Function to capture frame
def capture_frame(cap):
    ret, frame = cap.read()
    return frame

# Function to process image (for demonstration, you can replace with your object detection code)
def process_image(frame):
    # Example: Convert to grayscale
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
	# Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return rgb_image

# Function to encrypt image
def encrypt_image(image, key):
    f = Fernet(key)
    encrypted_image = f.encrypt(image)
    return encrypted_image

# Function to decrypt image
def decrypt_image(encrypted_image, key):
    f = Fernet(key)
    decrypted_image = f.decrypt(encrypted_image)
    return decrypted_image

# GUI
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Stream Webcam")
        self.cap = init_webcam()
        self.frame = tk.Label(root)
        self.frame.pack()

        ttk.Button(root, text="Capture Frame", command=self.capture).pack()
        ttk.Button(root, text="Process Image", command=self.process).pack()
        ttk.Button(root, text="Encrypt Image", command=self.encrypt).pack()
        ttk.Button(root, text="Decrypt Image", command=self.decrypt).pack()

    def capture(self):
        frame = capture_frame(self.cap)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.frame.imgtk = imgtk
        self.frame.config(image=imgtk)

    def process(self):
        frame = capture_frame(self.cap)
        processed_frame = process_image(frame)
        cv2image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.frame.imgtk = imgtk
        self.frame.config(image=imgtk)

    def encrypt(self):
        # Encrypt the processed image (for demonstration purposes)
        frame = capture_frame(self.cap)
        processed_frame = process_image(frame)
        _, encrypted_frame = cv2.imencode('.png', processed_frame)
        key = Fernet.generate_key()
        encrypted_data = encrypt_image(encrypted_frame, key)
        # Save or transmit encrypted_data as needed

    def decrypt(self):
        # Decrypt the encrypted image (for demonstration purposes)
        # Replace with actual decryption code
        key = Fernet.generate_key()
        decrypted_data = decrypt_image(encrypted_data, key)
        decrypted_frame = cv2.imdecode(np.frombuffer(decrypted_data, np.uint8), -1)
        cv2.imshow('Decrypted Image', decrypted_frame)
        cv2.waitKey(0)

root = tk.Tk()
app = GUI(root)
root.mainloop()
