import cv2
import numpy as np
import mediapipe as mp
import HandTracking
import keyboard

vid = cv2.VideoCapture(0)
Detector = HandTracking.HandDetector()

blue = (255, 0, 0)
red = (0, 0, 255)
green = (0, 255, 0)
black = (0,0,0)
white = (255,255,255)
size = 10
current_choice = red
mode = 0 # 0 is for drawing
xp, yp = 0,0
img_canvas = np.zeros((480,640,3), dtype=np.uint8)

while True:
    success, image = vid.read()
    index_finger = Detector.detectHands(vid=vid, required_id=8)
    middle_finger = Detector.detectHands(vid=vid, required_id=12)
    if index_finger:
        x = index_finger[0]
        y = index_finger[1]
        cv2.circle(image, (x, y), size, current_choice, cv2.FILLED)
        if 25<y<75 and mode==1:
            if x>75 and x<125:
                current_choice=blue
            elif x>175 and x<225:
                current_choice=black
            elif x>275 and x<325:
                current_choice=green
            elif x>375 and x<425:
                current_choice=red
            elif x>475 and x<525:
                current_choice=white
                mode=3

    if middle_finger and index_finger:
        x1 = middle_finger[0]
        y1 = middle_finger[1]
        if abs(x-x1)<50 and abs(y-y1)<50:
            mode = 1
        else:
            mode = 0
    else:
        mode = 0

    if xp==0 and index_finger:
        xp=x
    if yp==0 and index_finger:
        yp=y
    if mode==0 and index_finger:
        cv2.line(img_canvas, (xp,yp), (x,y), current_choice, size)
    if index_finger:
        xp=x
        yp=y
    if mode==3:
        img_canvas = np.zeros((480, 640, 3))
        mode=1

    cv2.circle(image, (100,50), 25, blue , cv2.FILLED)
    cv2.circle(image, (200, 50), 25, black, cv2.FILLED)
    cv2.circle(image, (300, 50), 25, green, cv2.FILLED)
    cv2.circle(image, (400, 50), 25, red, cv2.FILLED)
    cv2.circle(image, (500, 50), 25, white, cv2.FILLED)
    Detector.drawHands(image=image, dispfps=False)


    cv2.imshow("Virtual Painter", image)
    cv2.imshow("Canvas", img_canvas)
    cv2.waitKey(1)
    if keyboard.is_pressed("q"):
        break