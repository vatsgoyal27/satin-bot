import serial
import cv2
import numpy as np
import mediapipe as mp
import hand_utils as hu
import time

#Change 'COM3' to match your Arduino's port
#arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
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

while True:
    success, img = fr.read()
    if not success:
        break

    img = cv2.flip(img,1)
    black_img = np.zeros((frameHeight, frameWidth, 3), dtype=np.uint8)

    landmarks, hand_ids = hu.detect_hands(img, hands, frameWidth, frameHeight)

    black_img, xloc, yloc = hu.loc(black_img, landmarks, hindex, lindex, hand_ids, draw=True)
    if xloc != -1:
        data = str(xloc) + ',' + str(yloc) + '\n'  # Add newline so Arduino knows when to stop reading
        print("hand:", hindex, f" landmark: {lindex}, at: ({xloc}, {yloc})")
        xprev = xloc
        yprev = yloc
    else:
        data = str(xprev) + ',' + str(yprev) + '\n'
        print("hand:", hindex, f" landmark: {lindex}, at: ({xprev}, {yprev})")

    #arduino.write(data.encode())  # Convert string to bytes
    print("Sent")
    time.sleep(0.2)  # Optional: slow down for testing

    black_img = hu.draw_hands(black_img, landmarks, hand_ids)
    img = hu.draw_hands(img, landmarks, hand_ids)

    pTime, fps = hu.fpscalc(pTime)
    black_img = hu.draw_text(black_img, fps)

    imgStack = hu.stackImages(0.8, [img, black_img])
    cv2.imshow("Tracked Hand", imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

