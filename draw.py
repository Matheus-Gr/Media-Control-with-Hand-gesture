from utils import *
import cv2
import numpy as np

def draw_landmarks(frame: np.ndarray, processed) -> None: 
    index_finger_tip = find_landmark_cordinates(frame, processed, 8)
    thumb_finger_tip = find_landmark_cordinates(frame, processed, 4)
    wrist = find_landmark_cordinates(frame, processed, 0)
    middle_figer_tip = find_landmark_cordinates(frame, processed, 12)
    pinky_finger_tip = find_landmark_cordinates(frame, processed, 20)

    if index_finger_tip:
        cv2.circle(frame, (index_finger_tip[0],index_finger_tip[1]), 10, (0,255,0), 2)
    if thumb_finger_tip:
        cv2.circle(frame, (thumb_finger_tip[0],thumb_finger_tip[1]), 10, (255,125,0), 2)
    if wrist:
        cv2.circle(frame, (wrist[0],wrist[1]), 10, (0,255,255), 2)
    if middle_figer_tip:
        cv2.circle(frame, (middle_figer_tip[0],middle_figer_tip[1]), 10, (255,255,86), 2)
    if pinky_finger_tip:
        cv2.circle(frame, (pinky_finger_tip[0],pinky_finger_tip[1]), 10, (20,20,20), 2)



def draw_triangle(frame: np.ndarray, middle_cordinates) -> None:
    cx, cy = middle_cordinates
    size = 30
    half_size = size / 2
    color = (210,0,255)
    thickness = 2
    pt1 = (int(cx), int(cy - half_size))
    pt2 = (int(cx - half_size), int(cy + half_size))
    pt3 = (int(cx + half_size), int(cy + half_size))  
    triangle_cnt = np.array([pt1, pt2, pt3])
    cv2.drawContours(frame, [triangle_cnt], 0, color, thickness)