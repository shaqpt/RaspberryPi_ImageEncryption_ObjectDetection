# RaspberryPi_ImageEncryption_ObjectDetection

This project utilizes a Tensorflow deep learning framework for on-device inference. This framework is versatile in the fact that it can be deployed remotely using a variety of different devices with varuous computational abilities such as mobile devices. For this application, the framework is used within a Raspberry Pi application. The TensorFlow Lite framework allows for object detection algorithm to be displayed as a live video feed coninously displays. This oject detection algorithm runs in real-time throughout the live video feed.

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


### Future Expansions
This is a project that will be expanded on later on, but this is the initial starting point of the project. In future expansions, I'd like to trigger the encryption functions autonomously when specific objects are detected. I'd also like to get this program and all of its functionality to run in real-time, keeping in mind the computational limitations of the Raspberry Pi device. In this current version of the project, the encryption and decryption methods do not run while the live video feed is running. The encryption/decryption methods only run on a still image.


