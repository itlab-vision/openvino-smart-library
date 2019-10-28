import sys, os
import argparse
import numpy as np
import cv2 as cv

sys.path.insert(0,'src/modules')
import face_recognizer
import book_recognizer

sys.path.insert(0, 'src/infrastructure')
from DynamicDatabase import *
from Entities.User import *
from Entities.Book import *

uknownID = -1

def build_argparse():
    parser = argparse.ArgumentParser(description='Face recognition sample')
    parser.add_argument('-reid', type = str, default = 'DNNfr',
                        dest = 'rdDet', help = 'Type  - DNNfr')
    parser.add_argument('-m_rd', type = str, default = 'face-reidentification-retail-0095.xml',
                        dest = 'rdModel', help = 'Path to .xml file')
    parser.add_argument('-w_rd', type = int, default = '128',
                          dest = 'rdWidth', help = 'Image width to resize')
    parser.add_argument('-h_rd', type = int, default = '128',
                          dest = 'rdHeight', help = 'Image height to resize' ) 
    parser.add_argument('-t_rd', type = float, default = '0.8',
                          dest = 'rdThreshold', help = 'Probability threshold for face detections.' ) 
    parser.add_argument('-fd', type = str, default = 'DNNfd',
                        dest = 'fdDet', help = 'Type of detector. Available DNN face detector - DNNfd')
    parser.add_argument('-m_fd', type = str, default = 'face-detection-retail-0004.xml',
                        dest = 'fdModel', help = 'Path to .xml file')
    parser.add_argument('-w_fd', type = int, default = '300',
                          dest = 'fdWidth', help = 'Image width to resize')
    parser.add_argument('-h_fd', type = int, default = '300',
                          dest = 'fdHeight', help = 'Image height to resize' ) 
    parser.add_argument('-t_fd', type = float, default = '0.9',
                          dest = 'fdThreshold', help = 'Probability threshold for face detections.' ) 
    parser.add_argument('-lm', type = str, default = 'DNNLandmarks',
                        dest = 'lmDet', help = 'Type of detector. Available DNN landmarks regression - DNNLandmarks')
    parser.add_argument('-m_lm', type = str, default = 'landmarks-regression-retail-0009.xml',
                        dest = 'lmModel', help = 'Path to .xml file')
    parser.add_argument('-w_lm', type = int, default = '48',
                          dest = 'lmWidth', help = 'Image width to resize')
    parser.add_argument('-h_lm', type = int, default = '48',
                          dest = 'lmHeight', help = 'Image height to resize' ) 
    parser.add_argument('-w', type = int, default='0',
                        dest = 'web', help = 'Specify number of web to open. Default is 0')
    args = parser.parse_args()
    return args

def recUser(img):
    faces, out = rec.recognize(img)
    userID = uknownID
    for face in faces:
        if len(faces) > 1:
            text = 'No more than one person at a time'
            txtSize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2) 
            cv.rectangle(img, (0,50), (txtSize[0][0], 
                   50-txtSize[0][1]), (255, 255, 255), cv.FILLED)
            cv.putText(img, text,(0,50),
                                cv.FONT_HERSHEY_SIMPLEX, 1, (22, 163, 245), 2)

        if np.amax(out) > rec.threshold:
            userID = str(np.argmax(out)+1)
            text = 'User #' + str(userID)
            txtSize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2) 
            cv.rectangle(img, face[0], (face[0][0]+txtSize[0][0], 
                   face[0][1]-txtSize[0][1]-5), (255, 255, 255), cv.FILLED)
            cv.putText(img, text,
                   (face[0][0],face[0][1]-5), cv.FONT_HERSHEY_SIMPLEX, 1, (22, 163, 245), 2)
        else:
            text = 'Unknown'
            txtSize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2) 
            cv.rectangle(img, face[0], (face[0][0]+txtSize[0][0],
                    face[0][1]-txtSize[0][1]-5), (255, 255, 255), cv.FILLED)
            cv.putText(img, text,
                    (face[0][0],face[0][1]-5), cv.FONT_HERSHEY_SIMPLEX, 1, (22, 163, 245), 2)         
        cv.rectangle(img, face[0], face[1], (22, 163, 245), 2)
    return userID
               

args = build_argparse()
rdArgs = dict(rdXML = '', rdWidth= 0, rdHeight= 0, rdThreshold= 0,
fdName = '', fdXML = '', fdWidth = 0, fdThreshold= 0,
lmName = '', lmXML= 0, lmWidth= 0, lmHeight= 0)
BD = DynamicBD()

if (args.rdDet != None and args.fdDet != None and args.lmDet != None):
    rdArgs ['rdName'] = args.rdDet
    if (args.rdModel != None):
        rdArgs ['rdXML'] = args.rdModel
    if (args.rdWidth != None):
        rdArgs ['rdWidth'] = args.rdWidth
    if (args.rdHeight != None):
        rdArgs ['rdHeight'] = args.rdHeight
    if (args.rdThreshold != None):
        rdArgs ['rdThreshold'] = args.rdThreshold

    rdArgs ['fdName'] = args.fdDet
    if (args.fdModel != None):
        rdArgs ['fdXML'] = args.fdModel
    if (args.fdWidth != None):
        rdArgs ['fdWidth'] = args.fdWidth
    if (args.fdHeight != None):
        rdArgs ['fdHeight'] = args.fdHeight
    if (args.fdThreshold != None):
        rdArgs ['fdThreshold'] = args.fdThreshold

    rdArgs ['lmName'] = args.lmDet
    if (args.lmModel != None):
        rdArgs ['lmXML'] = args.lmModel
    if (args.lmWidth != None):
        rdArgs ['lmWidth'] = args.lmWidth
    if (args.lmWidth != None):
        rdArgs ['lmHeight'] = args.lmHeight
    if (args.web != None): 
        src = args.web

    rec = face_recognizer.FaceRecognizer.create(rdArgs)
   
    cap = cv.VideoCapture(src)
    identified = False
    while(True):
        _, img = cap.read()
        
        ch = cv.waitKey(5) & 0xFF

        userID = recUser(img)   
        if userID != uknownID:
            text = 'Place book in the selected area'
            txtSize = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2) 
            cv.rectangle(img, (5,  img.shape[0]),  (5 + txtSize[0][0],  img.shape[0] - 5 - txtSize[0][1]), (255, 255, 255), cv.FILLED)
            cv.putText(img, 'Place book in the selected area',
                    (5, img.shape[0]-5), cv.FONT_HERSHEY_SIMPLEX, 1, (22, 163, 245), 2)

            if ch == ord('b'):
                print('')
            
        elif ch  == ord('r'):
            n = rec.register(img)
            BD.addUser(n)
            cv.putText(img, 'You are user #' +  str(n),
                    (0,50), cv.FONT_HERSHEY_SIMPLEX, 2, (22, 163, 245), 2)
            BD.printUsers()
            cv.imshow('window',  img)
            cv.waitKey(1000)
        
        cv.imshow('window',  img)
        if ch == ord('q'):
            break
    cap.release()
