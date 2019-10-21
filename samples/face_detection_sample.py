import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append('../src/modules')
import face_recognizer


def build_argparse():
    parser = argparse.ArgumentParser(description='Face detection sample')
    parser.add_argument('-d', type = str, default = 'DNNfd',
                        dest = 'detector', help = 'Type of detector. Available DNN face detector - DNNfd')
    parser.add_argument('-mf', type = str, default = 'face-detection-retail-0004.xml',
                        dest = 'model', help = 'Path to .xml file')
    parser.add_argument('-w', type = int, default = '300',
                          dest = 'width', help = 'Image width to resize')
    parser.add_argument('-hh', type = int, default = '300',
                          dest = 'height', help = 'Image height to resize' ) 
    parser.add_argument('-t', type = float, default = '0.9',
                          dest = 'threshold', help = 'Probability threshold for face detections.' ) 
    parser.add_argument('-i', type = str,
                        dest = 'image', help = 'Image source')
    parser.add_argument('-v', type = str,
                        dest = 'video', help = 'Video source')
    parser.add_argument('-ww', type = int, default = 0, 
                        dest = 'webcam', help = 'Webcam source')
    args = parser.parse_args()
    return args

detArgs = dict(name = '', modelXML = '',  
            width = 0, height = 0, threshold = 0)
args = build_argparse()

if (args.detector != None):
    detArgs ['name'] = args.detector
    if (args.model != None):
        detArgs ['modelXML'] = args.model
    if (args.width != None):
        detArgs ['width'] = args.width
    if (args.width != None):
        detArgs ['height'] = args.height
    if (args.threshold != None):
        detArgs ['threshold'] = args.threshold
    det = face_recognizer.FaceDetector.create(detArgs)
    print(detArgs)
    cap = cv.VideoCapture(0)
    while(True): 
        _, f = cap.read()
        faces = det.detect(f)
        for face in faces:
            cv.rectangle(f, face[0], face[1], color=(0, 255, 0))
        cv.imshow('window', f) 
        ch = cv.waitKey(5)
        if ch & 0xFF == ord('q'):
            break
    cap.release()