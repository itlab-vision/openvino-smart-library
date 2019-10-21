import sys, os
import argparse
import numpy as np
import cv2 as cv
sys.path.append("../src/modules")
import face_recognizer

args = dict(name = 'DNN', model = "face-reidentification-retail-0095.bin",
            config = "face-reidentification-retail-0095.xml",
            width = 128, height = 128, threshold = 0.7)
rec = face_recognizer.FaceRecognizer.create(args)

bd = np.empty((0, 256), dtype=np.float32)

cap = cv.VideoCapture(0)
identified = False
while(True):
    _, img = cap.read()
    ch = cv.waitKey(5)

    if ch & 0xFF == ord('r') and not identified:
        bd = np.append(bd, [rec.register(img)], axis=0)
        cv.putText(img, "You are user #" + str(bd.shape[0]),
                (0,50), cv.FONT_HERSHEY_SIMPLEX, 2, color=(0, 255, 0))
        cv.imshow("window",  img)
        cv.waitKey(1000)
    # print("bd")
    # print(bd)
    faces, out = rec.recognize(img, bd)
    # print(out)
    for face in faces:
        if len(faces) > 1:
             cv.putText(img, "No more than one person at a time",
                (0,50), cv.FONT_HERSHEY_SIMPLEX, 2, color=(0, 255, 0))
        if np.amax(out) > rec.threshold:
            identified = True
            cv.putText(img, "User #" + str(np.argmax(out)+1),
                face[0], cv.FONT_HERSHEY_SIMPLEX, 1, color=(0, 255, 0))
        else:
            identified = False
        cv.rectangle(img, face[0], face[1], color=(0, 255, 0))

    cv.imshow("window",  img)
    if ch & 0xFF == ord('q'):
        break
cap.release()