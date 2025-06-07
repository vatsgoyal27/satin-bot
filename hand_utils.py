import cv2
import numpy as np
import time
import math
#end of imports

def stackImages(scale,imgArray):
    # stacks images, automatically resizing to match dimensions and supports grayscale and color

    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y]= cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def detect_hands(imgpar, hands_module, width, height):
    """
    Detects hands and returns:
        - List of landmarks (one list per hand)
        - List of handedness labels ("Left", "Right")
    """
    imgRGB = cv2.cvtColor(imgpar, cv2.COLOR_BGR2RGB)
    results = hands_module.process(imgRGB)
    all_landmark_positions = []
    hand_labels = []

    if results.multi_hand_landmarks:
        for idx, handLms in enumerate(results.multi_hand_landmarks):
            landmark_positions = []
            for lm in handLms.landmark:
                cx = int(lm.x * width)
                cy = int(lm.y * height)
                landmark_positions.append((cx, cy))
            all_landmark_positions.append(landmark_positions)

        if results.multi_handedness:
            for hand in results.multi_handedness:
                hand_labels.append(hand.classification[0].label)  # "Left" or "Right"

    return all_landmark_positions, hand_labels

def between_points(imagep, all_landmarks, hand_labels,
                   landmark1_idx=4, landmark2_idx=4,
                   color=(0, 0, 255), thickness=2, drawit = True):
    """
    Draws a line between two specific landmarks on two different hands.

    Args:
        imagep: Image to draw on.
        all_landmarks: List of hands, each with 21 (x, y) landmark tuples.
        hand_labels: List of hands tagged with Left and Right
            This list matches the order of all_landmarks, so:
                all_landmarks[0] corresponds to hand_labels[0] (left or right)
                all_landmarks[1] corresponds to hand_labels[1] (left or right)
            Hence, we can use this to identify left and right hands.
        landmark1_idx: Landmark index in the first hand.
        landmark2_idx: Landmark index in the second hand.
        color: BGR color of the line.
        thickness: Thickness of the line.

    Returns:
        Modified image with the line drawn (if valid hands and landmarks are found).
        Distance between given points.
    """
    d = None
    left_index = right_index = None

    # Find indices for Left and Right hands
    for idx, label in enumerate(hand_labels):
        if label == "Left":
            left_index = idx
        elif label == "Right":
            right_index = idx

    # Proceed if both hands are found
    if left_index is not None and right_index is not None:
        if left_index < len(all_landmarks) and right_index < len(all_landmarks):
            left_hand = all_landmarks[left_index]
            right_hand = all_landmarks[right_index]
            if landmark1_idx < len(left_hand) and landmark2_idx < len(right_hand):
                pt1 = left_hand[landmark1_idx]
                pt2 = right_hand[landmark2_idx]
                if drawit:
                    cv2.line(imagep, pt1, pt2, color, thickness)
                d = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

    return imagep, d

def fpscalc(prev_time):
    """
    Calculates current frames per second (FPS) based on time difference.
    """
    curr_time = time.time()
    fpspar = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
    return curr_time, fpspar

def draw_text(image, textpar):
    """
    Draws given value on the image.
    """
    if textpar is not None:
        cv2.putText(image, f"{int(textpar)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return image

def draw_hands(image, all_landmarks, hand_labels = None, color=(0, 255, 0), radius=5, thickness=2):
    """
    Draw landmarks and hand connections on the image.

    Args:
        image: Image to draw on (numpy array).
        all_landmarks: List of hands; each hand is a list of (x, y) tuples.
        color: Color of landmarks and connections (BGR tuple).
        radius: Radius of landmark circles.
        thickness: Thickness of connection lines.

    Returns:
        Image with drawn landmarks and connections.
        Labelled Hands
    """
    from mediapipe import solutions
    handConnections = solutions.hands.HAND_CONNECTIONS

    for hand_index, hand_landmarks in enumerate(all_landmarks):
        # Draw connections
        for connection in handConnections:
            start_idx, end_idx = connection
            if start_idx < len(hand_landmarks) and end_idx < len(hand_landmarks):
                pt1 = hand_landmarks[start_idx]
                pt2 = hand_landmarks[end_idx]
                cv2.line(image, pt1, pt2, color, thickness)

        # Draw landmarks (circles)
        for lm in hand_landmarks:
            cv2.circle(image, lm, radius, color, cv2.FILLED)

            # Label the hand using wrist position
            if len(hand_landmarks) > 0:
                x, y = hand_landmarks[0]
                label = f"{hand_labels[hand_index]}" if hand_labels and hand_index < len(
                    hand_labels) else f"Hand {hand_index}"
                cv2.putText(image, label, (x - 30, y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    return image


def loc(img, all_landmarks, hand_side, index, hand_ids, draw = True):
    """
    Returns the (x, y) position of a specific landmark on a specified hand ("Left" or "Right").
    Optionally draws a small circle on the landmark location in the given image.

    Args:
        img: The image on which to draw the landmark (if draw=True).
        all_landmarks: A list of hands, where each hand is a list of (x, y) tuples for 21 landmarks.
        hand_side: A string, either "Left" or "Right", indicating which hand to use.
        index: Integer index of the landmark (0 to 20).
        hand_ids: A list of strings like ["Left", "Right"] indicating hand sides for each detected hand.
        draw: Boolean flag indicating whether to draw a circle on the image at the landmark location.

    Returns:
        img: The possibly modified image with the landmark drawn.
        x: The x-coordinate of the specified landmark (or None if not found).
        y: The y-coordinate of the specified landmark (or None if not found).
    """

    handid = None
    for idx, label in enumerate(hand_ids):
        #print(label)
        if label == hand_side:
            handid = idx
            break  # Stop after finding the first matching hand
    #print(hand_ids)
    if handid is not None and handid < len(all_landmarks) and index < len(all_landmarks[handid]):
        x, y = all_landmarks[handid][index]
        if draw:
            cv2.circle(img, (x, y), 7, (0, 0, 255), 3)
            cv2.putText(img, f"coord: {x}, {y}", (x - 30, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return img, x, y
    return img, -1, -1
