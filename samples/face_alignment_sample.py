
import sys, os
import argparse 
import numpy as np
import cv2 as cv
sys.path.append("../src/modules")
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

args = dict(name = 'DNNLandmarks', model = "landmarks-regression-retail-0009.bin",
            config = "landmarks-regression-retail-0009.xml", width = 48, height = 48)
fl = face_recognizer.FaceLandmarks.create(args)
args = dict(name = 'DNNfd', model = "face-detection-retail-0004.bin",
            config = "face-detection-retail-0004.xml", 
            width = 672, height = 384, threshold = 0.9)
det = face_recognizer.FaceDetector.create(args)

cap = cv.VideoCapture(0)
landmarks = []
while(True): 
    _, img = cap.read()
    faces = det.detect(img)
    alignFaces = [None]*len(faces)
    for i, face in enumerate(faces):
        roi = img[face[0][1]:face[1][1], face[0][0]:face[1][0]]
        landmarks = fl.findLandmarks(roi)
        alignFaces[i] = fl.align(roi, landmarks, face_recognizer.refLandmarks)

    for i, alignFace in enumerate(alignFaces):
        cv.imshow("Align Face"+ str(i), alignFace)
    cv.imshow("Sample", img)
    ch = cv.waitKey(5)
    if ch & 0xFF == ord('q'):
        break
cap.release()