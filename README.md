# RaspberryPi_ImageEncryption_ObjectDetection

This project utilizes a Tensorflow deep learning framework for on-device inference. This framework is versatile in the fact that it can be deployed remotely using a variety of different devices with various computational abilities such as mobile devices. For this application, the framework is used within a Raspberry Pi application. The TensorFlow Lite framework allows for an object detection algorithm to run in real-time throughout a live video feed.

## Raspberry Pi model in use:
```
Raspberry Pi 4b (2019 release) (https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
```

The live video feed is obtained through a USB Webcam device connected to the Raspberry Pi.
## USB Webcam in use:
```
Logitech C920s PRO HD WEBCAM (https://www.logitech.com/en-us/products/webcams/c920s-pro-hd-webcam.960-001257.html)
```

## TensorFlow Lite Project
```
https://github.com/tensorflow/examples/tree/fff4bcda7201645a1efaea4534403daf5fc03d42
```

An encryption method, inspired by AES encryption schemes, is utilized to encrypt captured images extracted from the live feed. The encryption method jumbles the pixels within the image to make the image unintelligible.
Similarly, a decryption method is also utilized to revert the encrypted image back into its original format.

The idea behind this project is to be able to hide information from an image that may be classified autonomously. For example, if there is a car in a video, the idea is to be able to hide the license plate from being viewable in an effort to protect the identity and security of the car owner.


## How To Use:

1) Follow the Raspberry Pi setup process explained in this video:
https://www.youtube.com/watch?v=9fEnvDgxwbI

2) Follow the TensorFlow deep learning model framework installation explained in this video:
https://www.youtube.com/watch?v=NPXBRX7N3ec

3) In the previous step, you created a directory containing your python virtual environment. In the same directory that contains both the created env/ and example/ folders, create a project folder to deploy this project into. Run a git clone command on this repository and point the resulting code to your newly created folder.
   ```
   git clone
   ```
4) Ensure all necessary packages are installed:
   ```
   Numpy
   OpenCv
   Pillow
   Tkinker
   Tensorflow runtime
   Cryptography
   Pycryptodome
   ```
5) run main.py (must be ran while running in the python virtual environment)
   ```
   python3 main.py
   ```
6) GUI Window with Live Video Feed will appear. You'll then have the following options:
   ```
    Capture - captures a screenshot of the live video feed and the detected object in the image
    Encrypt - encrypts the entire captured image (saves output to file and displays output to GUI window)
    Decrypt - Decrypts the encrypted image (saves file and shows output in GUI window)
    Restart Video - Restarts the live video feed and object detection
    Stop Program - Exits the application
   ```
### Future Expansions
This is a project that will be expanded on later on, but this is the initial starting point of the project. In future expansions, I'd like to trigger the encryption functions autonomously when specific objects are detected. I'd also like to get this program and all of its functionality to run in real-time, keeping in mind the computational limitations of the Raspberry Pi device. In this current version of the project, the encryption and decryption methods do not run while the live video feed is running. The encryption/decryption methods only run on a still image.


