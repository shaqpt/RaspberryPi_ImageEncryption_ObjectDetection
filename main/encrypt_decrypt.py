from PIL import Image, ImageTk
import os
import numpy as np
import random
import tkinter.messagebox as mbox
import cv2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

output_directory = "captured_images"

# Create directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Encrypt Captured Image
def encrypt_image(image_path):
    global image_encrypted, key, key_rgb
    image_input = cv2.imread(image_path)
    (x1, y, _) = image_input.shape
    image_input = image_input.astype(float) / 255.0

    mu, sigma = 0, 0.1  # mean and standard deviation
    key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
    
    # Replicate key across color channels to match image_input shape
    key_rgb = np.tile(key[:, :, np.newaxis], (1, 1, 3))
    
    image_encrypted = image_input / key_rgb
    cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)
    
    encrypted_image = Image.open('image_encrypted.jpg')
    
    # Save the image to a file
    encrypted_image.save(os.path.join(output_directory, "captured_encrypted.png"))
    encrypted_image = ImageTk.PhotoImage(encrypted_image)
    
# Decrypt Captured Image
def decrypt_image(enc_image_path):
    global image_encrypted, key_rgb
    image_output = image_encrypted * key_rgb
    image_output *= 255.0
    cv2.imwrite('image_decrypted.jpg', image_output)

    decrypted_image = Image.open('image_decrypted.jpg')
    
    # Save the image to a file
    decrypted_image.save(os.path.join(output_directory, "captured_decrypted.png"))
    decrypted_image = ImageTk.PhotoImage(decrypted_image)


