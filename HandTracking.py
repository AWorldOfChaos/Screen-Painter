import cv2
import numpy as np
import mediapipe as mp
import time
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-s", "--dim",nargs=2, help="Enter size of image", default=[480, 640], type=int)
# args = parser.parse_args()

class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

        # self.vid = cv2.VideoCapture(0)

        self.ptime = 0
        self.ctime = 0

    def display_fps(self, image, fps):
        cv2.putText(image, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255),3)

    def detectHands(self, vid, required_id):
        while True:
            success, image = vid.read()
            h,w,c = image.shape
            # image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)
            if results.multi_hand_landmarks:
                for handlnds in results.multi_hand_landmarks:
                    for id, ln in enumerate(handlnds.landmark):
                        cx,cy = int(w*ln.x), int(h*ln.y)
                        if id==required_id:
                            return [cx, cy]
                    # self.mpDraw.draw_landmarks(image, handlnds, mpHands.HAND_CONNECTIONS)
            return False
            # self.ctime = time.time()
            # fps = 1/(ctime-ptime)
            # self.ptime=self.ctime
            # if dispfps:
            #     self.display_fps()
            # cv2.imshow("Feed", image)
            # cv2.waitKey(1)
    def drawHands(self, image, dispfps):
        results = self.hands.process(image)
        if results.multi_hand_landmarks:
            for handlnds in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(image, handlnds, self.mpHands.HAND_CONNECTIONS)