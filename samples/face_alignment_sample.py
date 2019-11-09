import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append('../src/modules')
import face_recognizer

def build_argparse():
    parser = argparse.ArgumentParser(description='Face alignment sample')
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
    parser.add_argument('-i', type = str, default='web',
                        dest = 'image', help = 'Source of images. Specify path to image or video,  or pass <web> to open web-camera. ')
    args = parser.parse_args()
    return args


fdArgs = dict(name = '', modelXML = '',  
            width = 0, height = 0, threshold = 0)
lmArgs = dict(name = '', modelXML = '',  
            width = 0, height = 0, threshold = 0)
args = build_argparse()

if (args.fdDet != None and args.lmDet != None):

    fdArgs ['name'] = args.fdDet
    if (args.fdModel != None):
        fdArgs ['modelXML'] = args.fdModel
    if (args.fdWidth != None):
        fdArgs ['width'] = args.fdWidth
    if (args.fdHeight != None):
        fdArgs ['height'] = args.fdHeight
    if (args.fdThreshold != None):
        fdArgs ['threshold'] = args.fdThreshold

    lmArgs ['name'] = args.lmDet
    if (args.lmModel != None):
        lmArgs ['modelXML'] = args.lmModel
    if (args.lmWidth != None):
        lmArgs ['width'] = args.lmWidth
    if (args.lmWidth != None):
        lmArgs ['height'] = args.lmHeight

    if (args.image != None): 
        src = args.image
        fileName, fileExtension = os.path.splitext(src)

    det = face_recognizer.FaceDetector.create(fdArgs)
    fl = face_recognizer.FaceLandmarks.create(lmArgs)

    if src == 'web' or fileExtension in ('.mkv', '.mp4'):
        src = 0 if src == 'web' else src
        cap = cv.VideoCapture(src)
        landmarks = []
        while(True): 
            _, img = cap.read()
            faces = det.detect(img)
            if len(faces) > 1:
                cv.putText(img, "No more than one person at a time",
                        (0,50), cv.FONT_HERSHEY_SIMPLEX, 2, color=(0, 255, 0))

            for face in faces:
                roi = img[face[0][1]:face[1][1], face[0][0]:face[1][0]]
                landmarks = fl.findLandmarks(roi)
                for point in landmarks:
                    y = int(point[1]*roi.shape[0])
                    x = int(point[0]*roi.shape[1])
                    cv.circle(roi, (x,y) , 3, (219,184,121), -1)
                alignFace = fl.align(roi, landmarks, face_recognizer.refLandmarks)
            if len(faces) == 1: 
                cv.imshow('Align Face', alignFace)
            cv.imshow('Sample', img)
            ch = cv.waitKey(5)
            if ch & 0xFF == ord('q'):
                break
        cap.release()
    elif fileExtension in ('.png', '.jpg','.jpeg', '.bmp'):
        img = cv.imread(src)
        faces = det.detect(img)
        for face, i in enumerate(faces):
            roi = img[face[0][1]:face[1][1], face[0][0]:face[1][0]]
            landmarks = fl.findLandmarks(roi)
            for point in landmarks:
                y = int(point[1]*roi.shape[0])
                x = int(point[0]*roi.shape[1])
                cv.circle(roi, (x,y) , 3, (219,184,121), -1)
            alignFace = fl.align(roi, landmarks, face_recognizer.refLandmarks)
            cv.imshow('Align Face ' + str(i) , alignFace)
        cv.imshow('Sample', img)
        cv.waitKey(0) 
    else:
        print("Wrong source of image")