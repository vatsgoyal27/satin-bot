import serial
import cv2
import numpy as np
import mediapipe as mp
import hand_utils as hu
import time

#Change 'COM3' to match your Arduino's port
arduino = serial.Serial(port='COM13', baudrate=9600, timeout=1)
time.sleep(2)  # Let Arduino reset

pTime = 0

frameHeight = 480
frameWidth = 640
fr = cv2.VideoCapture(0)
#fr = cv2.VideoCapture("http://192.168.1.100:4747/video")
fr.set(3, frameWidth)
fr.set(4, frameHeight)
fr.set(10, 150)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1)
mpDraw = mp.solutions.drawing_utils
handConnections = mpHands.HAND_CONNECTIONS

hindex = ("Right")
lindex = 8
xprev = 0
yprev = 0

x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C
A, B, C = coff

while True:
    success, img = fr.read()
    if not success:
        break

    img = cv2.flip(img,1)
    black_img = np.zeros((frameHeight, frameWidth, 3), dtype=np.uint8)

    landmarks, hand_ids = hu.detect_hands(img, hands, frameWidth, frameHeight)

    black_img, xloc, yloc = hu.loc(black_img, landmarks, hindex, lindex, hand_ids, draw=True)

    lnval = -1  # default value if ln is not calculated yet
    if len(landmarks) != 0:
        img, ln = hu.between_points(img, landmarks, 5, 17, color=(0, 255, 255), thickness=3, drawit=True)
        if ln:
            ln = float(ln)
            distanceCM = A * ln ** 2 + B * ln + C
            lnval =  distanceCM
            hu.draw_text(img, f"Dist: {round(distanceCM, 2)}", 440, 30)

    if xloc != -1:
        data = f"{xloc},{int(lnval)}\n"  # format: x,ln
        print(f"Sent to Arduino: {data.strip()} (xloc={xloc}, ln={int(lnval)})")
        xprev = xloc
        yprev = yloc
    else:
        data = f"{xprev},{int(lnval)}\n"
        print(f"Sent to Arduino: {data.strip()} (xprev={xprev}, ln={int(lnval)})")

    arduino.write(data.encode())  # Convert string to bytes
    print("Sent")
    time.sleep(0.2)  # Optional: slow down for testing

    black_img = hu.draw_hands(black_img, landmarks, hand_ids)
    img = hu.draw_hands(img, landmarks, hand_ids)

    pTime, fps = hu.fpscalc(pTime)
    black_img = hu.draw_text(black_img, f"fps: {round(fps, 2)}", 10, 30)

    imgStack = hu.stackImages(0.8, [img, black_img])
    cv2.imshow("Tracked Hand", imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

