from utils import *
import time
import cv2
from draw import *
import keyboard




class Gestures:
    def __init__(self):
        self.can_gesture = False
        self.first_cord_captured = False
        self.initial_cord = ()
        self.hand_closed_start_time = None
        self.play_pause_start_time = None
        self.volume_up_start_time = None
        self.volume_mode_start_time = None
        self.volume_mode = False


    def volume_handler(self,thumb_index_dist):
        switch_audio_mode = 35
        min_volume = 30
        max_volume = 300

        if self.volume_mode_start_time is None:
            if thumb_index_dist < switch_audio_mode:
                self.volume_mode = not self.volume_mode 
                self.volume_mode_start_time = time.time()
        elif time.time() - self.volume_mode_start_time > 2:
            if thumb_index_dist < switch_audio_mode:
                    self.volume_mode_start_time = None

        if self.volume_mode is True:

            volume_level = np.interp(thumb_index_dist, [min_volume, max_volume], [0, 100])

            if self.volume_up_start_time is None:
                if volume_level > 50:
                    keyboard.send("Volume Up")
                elif volume_level < 50:
                    keyboard.send("Volume Down")
                self.volume_up_start_time = time.time()
            elif (time.time() - self.volume_up_start_time > 0.05):
                self.volume_up_start_time = None 


    def detect_gestures(self, frame, landmarks_list:list, processed):
        max_hand_closed_timer = 1

        if len(landmarks_list) >= 21:
            middle_wrist_dist = get_distance([landmarks_list[12],landmarks_list[0]])
            thumb_index_dist = get_distance([landmarks_list[8],landmarks_list[4]])
            pinky_thum_dist = get_distance([landmarks_list[20],landmarks_list[4]])

            current_cord = ()
            if middle_wrist_dist > 290:
                self.can_gesture = True
                self.hand_closed_start_time = None

                if not self.first_cord_captured:
                    self.initial_cord = find_landmark_cordinates(frame, processed, 8)            
                    self.first_cord_captured = True
                else:
                    current_cord = find_landmark_cordinates(frame, processed, 8)
            else:
                if self.hand_closed_start_time is None:
                    self.hand_closed_start_time = time.time()
                elif (time.time() - self.hand_closed_start_time) > max_hand_closed_timer: 
                    self.can_gesture = False
                    self.first_cord_captured = False

            #Draw number of distances
            frame_h, frame_w, _ = frame.shape
            cv2.putText(frame, "Can Gesture: {0}".format(str(self.can_gesture)), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
            cv2.putText(frame, "Audio Mode: {0}".format(str(self.volume_mode)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)

            #Draw ready trinagle on initial cordinate 
            if self.first_cord_captured:
                draw_triangle(frame, self.initial_cord)
            
            if self.can_gesture:
                if self.first_cord_captured and current_cord:
                    if self.initial_cord[0] > frame_w / 2 and current_cord[0] < frame_w / 2:
                        keyboard.send("next track")
                        self.initial_cord = ()
                        self.first_cord_captured = False
                    elif self.initial_cord[0] < frame_w / 2 and current_cord[0] > frame_w / 2:
                        keyboard.send("previous track")
                        self.initial_cord = ()
                        self.first_cord_captured = False

                self.volume_handler(thumb_index_dist)

                if pinky_thum_dist < 45:
                    if self.play_pause_start_time is None:
                        keyboard.send("play/pause media")
                        self.play_pause_start_time = time.time()
                    elif (time.time() - self.play_pause_start_time) > 1:
                        self.play_pause_start_time = None
