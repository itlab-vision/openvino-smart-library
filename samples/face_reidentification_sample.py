import sys, os
import argparse
import numpy as np
import cv2 as cv
sys.path.append("../src/modules")
import face_recognizer

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
    parser.add_argument('-i', type = str, default='web',
                        dest = 'image', help = 'Source of images. Specify path to video, or pass <web> to open web-camera')
    args = parser.parse_args()
    return args

args = build_argparse()
rdArgs = dict(name = '', rdXML = '', rdWidth= 0, rdHeight= 0, rdThreshold= 0,
fdName = '', fdXML = '', fdWidth = 0, fdThreshold= 0,
lmName = '', lmXML= 0, lmWidth= 0, lmHeight= 0)

if (args.rdDet != None and args.fdDet != None and args.lmDet != None):
    
    rdArgs ['name'] = args.rdDet
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
    if (args.image != None): 
        src = args.image
        fileName, fileExtension = os.path.splitext(src)

    rec = face_recognizer.FaceRecognizer.create(rdArgs)
   
    if src == 'web' or fileExtension in ('.mkv', '.mp4'):
        src = 0 if src == 'web' else src
        cap = cv.VideoCapture(src)
        identified = False
        while(True):
            _, img = cap.read()
            ch = cv.waitKey(5)
            faces, out = rec.recognize(img)
            if ch & 0xFF == ord('r') and not identified:
                n = rec.register(img)
                cv.putText(img, "You are user #" +  str(n),
                        (0,50), cv.FONT_HERSHEY_SIMPLEX, 2, color=(0, 255, 0))
                cv.imshow("window",  img)
                cv.waitKey(1000)
                
            for face in faces:
                if len(faces) > 1:
                    cv.putText(img, "No more than one person at a time",
                        (0,50), cv.FONT_HERSHEY_SIMPLEX, 1, color=(0, 255, 0))

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
