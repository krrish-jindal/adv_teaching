import cv2
from simple_facerec import SimpleFacerec
from line import Line_detection
# import serial
# from serial import Serial
# import time
from time import sleep

from pyfirmata import Arduino ,SERVO ,util

# Encode faces from a folder
sfr = SimpleFacerec()
ld = Line_detection()
sfr.load_encoding_images("training images/")


file_name = input('Please enter the name of the Lecture to be recorded:     ')

# Load Camera
cap = cv2.VideoCapture('http://@192.168.29.184:4747/video')

while (cap.isOpened()):
    sleep(0.1)
    # read from camera
    ret, frame = cap.read()

    if ret==True:
        # frame = cv2.flip(frame,0)

        # write the flipped frame
        # out.write(frame)

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            # board.digital[pin].write(sub)

            sub = -(((int(frame.shape[1]/2)) - int((x1 + x2)/2))/5)
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            cv2.circle(frame, (int((x1 + x2) / 2), int((y1 + y2) / 2)), 5, (255, 255, 255), -1)
            ld.draw_grid(frame,(2,2))
            cv2.line(frame,(int((x1 + x2) / 2), 0),(int((x1 + x2) / 2), 480), color=(0, 255, 0), thickness=3)


        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()
