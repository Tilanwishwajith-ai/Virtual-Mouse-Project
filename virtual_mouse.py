import cv2
import mediapipe as mp
import pyautogui
import math

# 1. කැමරාව සහ Hand Detector සකසා ගැනීම
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1) # එක අතක් පමණක් ගන්න
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

print("Virtual Mouse Started... Check the console for distance numbers!")

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            
            # --- 1. ඇඟිලි හඳුනාගැනීම (Index & Thumb) ---
            # Index Finger (Id 8)
            index_finger = landmarks[8]
            index_x = int(index_finger.x * frame_width)
            index_y = int(index_finger.y * frame_height)
            
            # Thumb (Id 4)
            thumb = landmarks[4]
            thumb_x = int(thumb.x * frame_width)
            thumb_y = int(thumb.y * frame_height)
            
            # රවුම් ඇඳීම (Visuals)
            cv2.circle(frame, (index_x, index_y), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 255), cv2.FILLED)
            
            # --- 2. Mouse එක ගෙනියන කොටස ---
            # Mouse එක ගැස්සෙන්නේ නැති වෙන්න පොඩි ප්‍රදේශයක් (Rectangle) ඇතුළේ වැඩ කරන්න හදමු
            # මේකෙන් Mouse එක Screen එකේ අයිනටම යවන්න ලේසි වෙනවා
            mouse_x = screen_width / frame_width * index_x
            mouse_y = screen_height / frame_height * index_y
            pyautogui.moveTo(mouse_x, mouse_y)
            
            # --- 3. Click කරන කොටස (The Fix) ---
            # ඇඟිලි දෙක අතර දුර මැනීම
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
            
            # CMD එකේ දුර Print කරන්න (මේක බලලා අගය වෙනස් කරගන්න පුළුවන්)
            print(f"Distance: {int(distance)}")
            
            # දුර 40 ට වඩා අඩු නම් Click කරන්න (කලින් තිබ්බේ 30)
            if distance < 40:
                cv2.circle(frame, (index_x, index_y), 15, (0, 255, 0), cv2.FILLED) # Click වෙනකොට කොළ පාට
                pyautogui.click()
                pyautogui.sleep(0.2) # එකපාරට ගොඩක් Click නොවෙන්න පොඩි විරාමයක්

    cv2.imshow('Virtual Mouse - Adjusted', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()