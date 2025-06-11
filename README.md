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

### Notes
1. Do not use nRF with the PA/LNA Antenna connected (if powered by onboard 3.3v)
2. cant open serial port of transmitter as it is being used by pyserial

### 🔌 nRF24L01+ Wiring Guide

Connect the nRF24L01+ module to your Arduino Uno or Nano as follows:

- **VCC** → 3.3 V  
 *Do NOT connect to 5 V — it can permanently damage the module!*
  
- **GND** → GND

- **CE** → Pin 9

- **CSN (CS)** → Pin 10

- **SCK** → Pin 13

- **MOSI** → Pin 11

- **MISO** → Pin 12

- **IRQ** → Not connected (optional)

#### ⚠️ Power Tip

If you're using the nRF24L01+ with a built-in antenna amplifier (PA+LNA module), add a **10 μF capacitor** between **VCC and GND**, placed close to the module. This helps prevent instability due to voltage dips.

Some Arduino boards can't provide enough current on the 3.3 V pin for PA+LNA modules — consider using an external 3.3 V voltage regulator like the **AMS1117** if needed.
