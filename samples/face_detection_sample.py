import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append('../src/modules')
import face_recognizer


def build_argparse():
    parser = argparse.ArgumentParser(description='Face detection sample')
    parser.add_argument('-fd', type = str, default = 'DNNfd',
                        dest = 'detector', help = 'Type of detector. Available DNN face detector - DNNfd')
    parser.add_argument('-m_fd', type = str, default = 'face-detection-retail-0004.xml',
                        dest = 'model', help = 'Path to .xml file')
    parser.add_argument('-w_fd', type = int, default = '300',
                          dest = 'width', help = 'Image width to resize')
    parser.add_argument('-h_fd', type = int, default = '300',
                          dest = 'height', help = 'Image height to resize' ) 
    parser.add_argument('-t_fd', type = float, default = '0.9',
                          dest = 'threshold', help = 'Probability threshold for face fdections.' ) 
    parser.add_argument('-i', type = str,
                        dest = 'image', help = 'Image source')
    parser.add_argument('-v', type = str,
                        dest = 'video', help = 'Video source')
    parser.add_argument('-web', type = int, default = 0, 
                        dest = 'webcam', help = 'Webcam source')
    args = parser.parse_args()
    return args

fdArgs = dict(name = '', modelXML = '',  
            width = 0, height = 0, threshold = 0)
args = build_argparse()

if (args.detector != None):
    fdArgs ['name'] = args.detector
    if (args.model != None):
        fdArgs ['modelXML'] = args.model
    if (args.width != None):
        fdArgs ['width'] = args.width
    if (args.height != None):
        fdArgs ['height'] = args.height
    if (args.threshold != None):
        fdArgs ['threshold'] = args.threshold
        
    det = face_recognizer.FaceDetector.create(fdArgs)
    print(fdArgs)
    cap = cv.VideoCapture(0)
    while(True): 
        _, f = cap.read()
        faces = det.detect(f)
        for face in faces:
            cv.rectangle(f, face[0], face[1], color=(0, 255, 0))
        cv.imshow('Sample', f) 
        ch = cv.waitKey(5)
        if ch & 0xFF == ord('q'):
            break
    cap.release()