import cv2
from simple_facerec import SimpleFacerec
from line import Line_detection
# import serial
# from serial import Serial
import time
import mediapipe as mp
from math import hypot  
from time import sleep

#from pyfirmata import Arduino ,SERVO ,util

# Encode faces from a folder
sfr = SimpleFacerec()
ld = Line_detection()
sfr.load_encoding_images("training images/")

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
c = 0
no = 1
b=0
i = 101
r = 100


file_name = input('Please enter the name of the Lecture to be recorded:     ')

# Load Camera
# cap = cv2.VideoCapture('rtsp://192.168.29.184:4747/video')

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS, 60)

if (cap.isOpened() == False): 
    print("Error reading from camera source")

out = cv2.VideoWriter('RecordedVideo' + file_name + '.avi', -1, 20.0, (640,480))

# start a serial port from arduino
# arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

# port ="/dev/ttyUSB0"
# pin=9
# board =Arduino(port)
# board.digital[pin].mode=SERVO
# board.digital[pin].write(90)

angle=90
while (cap.isOpened()):
    sleep(0.1)
    # read from camera
    ret, img = cap.read()

    if ret==True:

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
            if d != 0:
                ROI = img[int((my - 100)/d):my + int((my - 100)/d), mx: mx + d * (mx + 100)]
            #print(i)

            if d == 0:
                i = 1
                #print("*********** Screenshot Detected **************")

            if i == 40:
                print("Screenshot:" +  str(no) + "taken")
                cv2.imshow('screenshot: '+  str(no), ROI)
                cv2.imwrite('ROZ' +str(no) + '.png', ROI)
                filez = 'ROZ' +str(no) + '.png'
                with open("sample.html", "a") as file_object:
                    file_object.write(f'<img src = "{filez}"></img>')
                no = no + 1


            if i < 40 and i%8 == 0:
                string = "Taking Screenshot in: " + str(int(i/4))
                print(string)
                cv2.putText(img, string, (0,0), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)


            cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)
            cv2.circle(img,(mx, my), 13, (0,0,255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
            if d != 0:
                cv2.rectangle(img,(mx,my),(d * (mx + 100),int((my - 100)/d)),(0,255,0),4)

            if i != 0:
                i = i+1
        # img = cv2.flip(img,0)

        # write the flipped img
        out.write(img)

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(img)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            # board.digital[pin].write(sub)

            sub = -(((int(img.shape[1]/2)) - int((x1 + x2)/2))/5)
            #angle=int(90-sub)
            if sub > 7:
                if angle > 5:
                    angle = angle - 3
            if sub < -7:
                if angle < 175:
                    angle = angle + 3
            # board.digital[pin].write(160)
            print(angle)
            #board.digital[pin].write(angle)
            # arduino.write(bytes(sub, 'utf-8'))
            time.sleep(0.05)

            # cv2.putText(img, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 200), 4)
            # cv2.circle(img, (int((x1 + x2) / 2), int((y1 + y2) / 2)), 5, (255, 255, 255), -1)
            # ld.draw_grid(img,(2,2))
            # cv2.line(img,(int((x1 + x2) / 2), 0),(int((x1 + x2) / 2), 480), color=(0, 255, 0), thickness=3)

            

        cv2.imshow("image", img)

        key = cv2.waitKey(1)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()