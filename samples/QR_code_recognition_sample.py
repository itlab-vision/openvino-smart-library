import sys, os
import tempfile
import pyzbar
import argparse
import numpy as np
import cv2 as cv
sys.path.append('../src/modules')
import book_recognizer as br


# Display QR code location
def display(frame, decodedObjects):
    # Loop over all decoded objects
    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0, n):
            cv.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)


def createArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-br', type=str, default='QR', 
                         dest = 'br', help = 'Type - QR' )
    parser.add_argument('-i', type = str, default='web',
                        dest = 'image', help = 'Source of images. Specify path to image or video, or pass <web> to open web-camera')
    return parser.parse_args()


# Main
if __name__ == '__main__':
    args = createArgparse()
    brArgs = dict(name='')
    if (args.br != None and args.image != None):
        brArgs['name'] = args.br
        src = args.image
        fileName, fileExtension = os.path.splitext(src)

    qrDecoder = br.BookRecognizer.create(brArgs)
    if src == 'web' or fileExtension in ('.mkv', '.mp4', 'avi'):
        src = 0 if src == 'web' else src
        cap = cv.VideoCapture(src)
        if not cap.isOpened():
            raise IOError('Cannot open WebCam')

        while True:
            _, img = cap.read()
            data = qrDecoder.recognize(img)
            
            if data == '':
                print('QR-code not detected!')
            else:
                display(img, qrDecoder.objects)
                print('Decoded Data : {}'.format(data))

            cv.imshow('QR codes recognition sample', img)
            key = cv.waitKey(5) & 0xFF
            if key == 27  or key == ord('q') or key == ord('Q'):
                break
        cap.release()
        cv.destroyAllWindows()
    elif fileExtension in ('.png', '.jpg','.jpeg', '.bmp'):
        img = cv.imread(src)
        data = qrDecoder.recognize(img)
        if data == '':
            print('QR-code not detected!')
        else:
            # print(qrDecoder.objects)
            display(img, qrDecoder.objects)
            cv.imshow('QR codes recognition sample', img)
            print('Decoded Data : {}'.format(data))
        cv.waitKey(0) 
    else:
        print('Wrong parameters')

