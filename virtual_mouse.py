import cv2
import mediapipe as mp
import pyautogui
import math
import time
import numpy as np

# --- Configuration ---
# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Width
cap.set(4, 720)  # Height

# Hand Detector Setup
hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils

# Screen Settings
screen_width, screen_height = pyautogui.size()

# Smoothening (To stop shaking)
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Colors (BGR Format)
COLOR_MOUSE = (255, 0, 255)   # Purple
COLOR_CLICK = (0, 255, 0)     # Green
COLOR_TEXT = (255, 255, 255)  # White
COLOR_BOX = (0, 255, 255)     # Yellow

# FPS Variables
pTime = 0

print("Virtual Mouse with UI Started...")

while True:
    # 1. Capture Frame
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    
    # 2. Draw UI Interface (The Box)
    # We define a smaller box for mouse control to make it easier
    frame_reduction = 100 
    cv2.rectangle(frame, (frame_reduction, frame_reduction), 
                  (frame_width - frame_reduction, frame_height - frame_reduction),
                  COLOR_BOX, 2)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    status_text = "Status: Searching..."
    
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            
            # Get Finger Coordinates
            index_finger = landmarks[8]
            thumb_finger = landmarks[4]
            
            x1 = int(index_finger.x * frame_width)
            y1 = int(index_finger.y * frame_height)
            
            x2 = int(thumb_finger.x * frame_width)
            y2 = int(thumb_finger.y * frame_height)
            
            # Check if hand is in the box
            cv2.circle(frame, (x1, y1), 15, COLOR_MOUSE, cv2.FILLED)
            
            # --- Moving Mode ---
            # Convert Coordinates (Interpolation)
            x3 = np.interp(x1, (frame_reduction, frame_width - frame_reduction), (0, screen_width))
            y3 = np.interp(y1, (frame_reduction, frame_height - frame_reduction), (0, screen_height))
            
            # Smoothening Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY
            
            status_text = "Mode: Moving Cursor"

            # --- Clicking Mode ---
            distance = math.hypot(x1 - x2, y1 - y2)
            
            # Visual Bar for distance
            # cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
            
            if distance < 40:
                cv2.circle(frame, (x1, y1), 15, COLOR_CLICK, cv2.FILLED)
                cv2.putText(frame, "CLICK!", (x1 + 20, y1), cv2.FONT_HERSHEY_PLAIN, 2, COLOR_CLICK, 2)
                pyautogui.click()
                status_text = "Mode: CLICKED!"
                # Add a visual flash effect
                cv2.rectangle(frame, (0,0), (frame_width, frame_height), COLOR_CLICK, 5)

    # 3. Add Dashboard Info (FPS & Status)
    # Background for text
    cv2.rectangle(frame, (0, 0), (350, 80), (0, 0, 0), cv2.FILLED)
    
    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, COLOR_TEXT, 2)
    cv2.putText(frame, status_text, (20, 65), cv2.FONT_HERSHEY_PLAIN, 1.5, COLOR_BOX, 2)

    # Show Final Image
    cv2.imshow('AI Virtual Mouse - Pro UI', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()