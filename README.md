# (INCOMPLETE) Hand Tracking with Wireless nRF24L01 Communication and Motor Control

This project uses Python and Arduino to track a hand landmark using MediaPipe, send the coordinates via serial to an Arduino transmitter, which then wirelessly transmits the coordinates over nRF24L01 radio modules to a receiver Arduino. The receiver Arduino uses that data to control dc motors and effectively follow the landmark

---

## Project Components

- **Python script** (hand tracking and serial communication)
- **Arduino transmitter** (reads serial data, sends via nRF24L01)
- **Arduino receiver** (receives wireless data, controls the dc motors)
- **Hardware:** Webcam, two Arduino boards, two nRF24L01+ radio modules, *To be updated*

---

## Requirements

### Python

- Python 3.9.13 (mediapipe is not supported by python 3.13 or 3.11)
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- NumPy (`numpy`)
- PySerial (`pyserial`)

### Arduino

- Arduino IDE
- RF24 library for nRF24L01 communication ([GitHub: TMRh20/RF24](https://github.com/nRF24/RF24))

### DroidCam

- DroidCam android app

---

## Setup

### Python

1. Clone this repo or copy the Python script files.
2. Install required libraries and dependencies

### Arduino

1. Copy each .ino file into separate files on the Arduino IDE or equivalent
2. Install required libraries
3. Upload to each arduino and assemble 'satin'

### DroidCam

1. Download the mobile DroidCam app from the play store
2. Start DroidCam and connect both your laptop and phone to the same Wi-Fi
3. Comment line *16*, uncomment *line 17* in *serialCom.py* and replace the url with your DroidCam url