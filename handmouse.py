import cv2
import mediapipe as mp
import pyautogui
from draw import *
from gestures import Gestures

screen_w, screen_h = pyautogui.size()
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity = 1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands = 1
)
cap = cv2.VideoCapture(0)
draw = mp.solutions.drawing_utils
gestures = Gestures()

try:
    while cap.isOpened():
        ret, frame = cap.read()
        frame_h, frame_w, _ = frame.shape
        
        if not ret:
            break
        frame = cv2.flip(frame,1)
        # print(type(frame))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed = hands.process(frameRGB)
        
        landmarks_list = []

        if processed.multi_hand_landmarks:
            hand_landkarms = processed.multi_hand_landmarks[0]
            # draw.draw_landmarks(frame, hand_landkarms, mpHands.HAND_CONNECTIONS)

            for lm in hand_landkarms.landmark:
                landmarks_list.append((lm.x,lm.y))
        
        draw_landmarks(frame, processed)
        gestures.detect_gestures(frame,landmarks_list,processed)
        
        cv2.imshow('Frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
finally:
    cap.release()
    cv2.destroyAllWindows()