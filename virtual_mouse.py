# Step 1: Importing Libraries
import cv2
import mediapipe as mp
import pyautogui
import math


# Step 2: Initialize Camera and Hand Detector
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

print("System Initialized...")

# Step 3: Main Loop to capture frames
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Step 4: Process Hand Landmarks
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark   

# Step 5: Identify Index and Thumb fingers
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8: # Index Finger
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4: # Thumb
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)
                    thumb_x = x
                    thumb_y = y

# Step 6: Move Mouse
                    pyautogui.moveTo(index_x, index_y)


# Step 7: Clicking Logic
            # (Check distance between Index (8) and Thumb (4))
            if 'index_x' in locals() and 'thumb_x' in locals():
                distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
                if distance < 40:
                    pyautogui.click()
                    pyautogui.sleep(0.2)

                    