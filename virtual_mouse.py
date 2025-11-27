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