import cv2
import mediapipe as mp
from math import hypot
from PIL import Image
import numpy as np



cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

c = 0
no = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

    if lmList != []:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        mx = int((x1 + x2) / 2)
        my = int((y1 + y2) / 2)
        d = int((hypot(x2 - x1, y2 - y1)/30))
        print(d)

        if d != 0:
            no += 1
            ROI = img[int((my - 100)/d):my + int((my - 100)/d), mx: mx + d * (mx + 100)]
            cv2.imwrite('ROZ'  + '.png', ROI)

        filez = 'ROZ' + '.png'
        if d == 0:
            imglist=[]
            imglist.append(ROI)
            

            while c < 1:
                with open("sample.html", "a") as file_object:
                    file_object.write(f'<img src = "{filez}"></img>')
                c += 1
        cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
        cv2.circle(img,(mx, my), 13, (0,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        if d != 0:
            cv2.rectangle(img,(mx,my),(d * (mx + 100),int((my - 100)/d)),(0,255,0),4)
        C = 0


    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()