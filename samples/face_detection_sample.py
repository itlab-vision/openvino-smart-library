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
    parser.add_argument('-i', type = str, default='web',
                        dest = 'image', help = 'Source of images. Specify path to image or video, or pass <web> to open web-camera')
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
    
    if (args.image != None): 
        src = args.image
        fileName, fileExtension = os.path.splitext(src)

    det = face_recognizer.FaceDetector.create(fdArgs)
    if src == 'web' or fileExtension in ('.mkv', '.mp4'):
        src = 0 if src == 'web' else src
        cap = cv.VideoCapture(src)
        while(True): 
            _, img = cap.read()
            faces = det.detect(img)
            for face in faces:
                cv.rectangle(img, face[0], face[1], color=(0, 255, 0))
            cv.imshow('Sample', img) 
            ch = cv.waitKey(5)
            if ch & 0xFF == ord('q'):
                break
        cap.release()
    elif fileExtension in ('.png', '.jpg','.jpeg', '.bmp'):
        img = cv.imread(src)
        faces = det.detect(img)
        for face in faces:
            cv.rectangle(img, face[0], face[1], color=(0, 255, 0))
        cv.imshow('Sample', img)
        cv.waitKey(0) 
    else:
        print("Wrong source of image")
