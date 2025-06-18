# Hand Tracking with Wireless nRF24L01 Communication and Motor Control

This project uses Python and Arduino to track a hand landmark using MediaPipe, send the coordinates via serial to an Arduino transmitter, which then wirelessly transmits the coordinates over nRF24L01 radio modules to a receiver Arduino. The receiver Arduino uses that data to control DC motors and effectively follow the landmark.

---

##  Project Components

- **Python script** – Hand tracking and serial communication
- **Arduino transmitter** – Reads serial data, sends via nRF24L01
- **Arduino receiver** – Receives wireless data, controls DC motors
- **Hardware:** Webcam, 2× Arduino boards, 2× nRF24L01+ modules, L298N motor driver, 2× DC motors, Battery

---

##  Requirements

### Python

- Python 3.9.13 (MediaPipe is not supported on 3.11 or 3.13)
- `opencv-python`
- `mediapipe`
- `numpy`
- `pyserial`

```bash
pip install opencv-python mediapipe numpy pyserial
```

### Arduino

- Arduino IDE
- RF24 library by TMRh20  
  → [GitHub: nRF24/RF24](https://github.com/nRF24/RF24)

---

## Setup Instructions

### Python Script

1. Clone or copy the Python files.
2. Install required libraries using `pip install` above.
3. Update the serial port in the Python script to match your Arduino (e.g. `'COM11'` or `'/dev/ttyUSB0'`).

### Arduino

1. Open and upload the transmitter and receiver `.ino` files to their respective boards.
2. Ensure the `RF24` library is installed.
3. Power the receiver Arduino from the 5 V output of the L298N motor driver (see wiring below).

### DroidCam (Optional)

1. Install DroidCam on your phone.
2. Connect phone and laptop to the same Wi-Fi network.
3. In the Python script:
   - Comment out the webcam line.
   - Uncomment the DroidCam line.
   - Replace the IP with your DroidCam address.

---

## Notes

- **Do NOT use the nRF24L01+ PA/LNA version directly on Arduino 3.3 V.** It may cause instability or permanent damage. Use an external 3.3 V regulator like **AMS1117** with capacitors.
- PySerial will lock the serial port — the Arduino IDE cannot access it at the same time.
- If you're powering the Arduino using the 5 V output of the L298N, do not connect the USB cable at the same time.

---

## Wiring Guide

###  Transmitter Arduino (with nRF24L01+)

| nRF24L01+ Pin | Arduino Pin         |
|---------------|---------------------|
| VCC           | 3.3 V (NOT 5 V)      |
| GND           | GND                 |
| CE            | D9                  |
| CSN (CS)      | D10                 |
| SCK           | D13 (SPI)           |
| MOSI          | D11 (SPI)           |
| MISO          | D12 (SPI)           |
| IRQ           | Not connected       |

> For PA/LNA versions, use a 10 μF capacitor across VCC and GND near the module.

---

### Receiver Arduino with Motor Control

#### nRF24L01+ Module

| nRF24L01+ Pin | Arduino Pin         |
|---------------|---------------------|
| VCC           | 3.3 V (regulated)   |
| GND           | GND                 |
| CE            | D9                  |
| CSN (CS)      | D10                 |
| SCK           | D13                 |
| MOSI          | D11                 |
| MISO          | D12                 |

#### L298N Motor Driver to Arduino

| L298N Pin | Arduino Pin | Description         |
|----------|-------------|---------------------|
| IN1      | D2          | Motor A direction   |
| IN2      | D3          | Motor A direction   |
| ENA      | D6 (PWM)    | Motor A speed (PWM) |
| IN3      | D4          | Motor B direction   |
| IN4      | D7          | Motor B direction   |
| ENB      | D5 (PWM)    | Motor B speed (PWM) |

> Remove the jumpers on ENA and ENB to allow PWM control from the Arduino.

---

### Power Setup

| Source               | Destination         | Notes                                |
|----------------------|---------------------|--------------------------------------|
| Battery + (7–12 V)    | L298N `12V`         | Main motor power                     |
| Battery –            | L298N `GND`         | Shared ground                        |
| L298N `5V`           | Arduino `5V`        | Powers Arduino (leave 5V enable jumper ON) |
| L298N `GND`          | Arduino `GND`       | Required for common ground           |

> Do **not** connect USB + 5 V from L298N to Arduino at the same time.

---

### DC Motor Wiring

| L298N Pin | Connect To     |
|-----------|----------------|
| OUT1      | Left Motor +   |
| OUT2      | Left Motor –   |
| OUT3      | Right Motor +  |
| OUT4      | Right Motor –  |

> Reverse wires if motors spin in the wrong direction.

---

### L298N Jumper Configuration

| Jumper     | State     | Purpose                              |
|------------|-----------|--------------------------------------|
| 5V Enable  | ✅ ON      | Activates 5 V regulator              |
| ENA        | ❌ REMOVED | Allows PWM from Arduino D6           |
| ENB        | ❌ REMOVED | Allows PWM from Arduino D5           |

---

## Summary

- MediaPipe tracks hand → sends landmark coordinates over Serial
- Arduino transmitter reads serial → sends data via nRF24L01+
- Arduino receiver gets data → controls motor direction + speed with PWM

---