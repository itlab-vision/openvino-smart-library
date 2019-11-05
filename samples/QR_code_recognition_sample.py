import sys, os
import tempfile
import pyzbar
import argparse
import numpy as np
import cv2
sys.path.append("../src/modules")
import book_recognizer as br


# Display QR code location
def display(frame, decodedObjects):
    # Loop over all decoded objects
    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        # If the points do not form a quad, find convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        # Number of points in the convex hull
        n = len(hull)

        # Draw the convext hull
        for j in range(0, n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

    cv2.imshow("Results", frame)
    cv2.waitKey(0)


def createArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recognizer', type=str, default='QR')
    parser.add_argument('-n', '--name', type=str, default=None)
    return parser.parse_args()


# Main
if __name__ == '__main__':
    args = createArgparse()
    qrDecoder = br.BookRecognizer.create(args)
    if args.name is not None:
        if args.name == 'GUI':
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                raise IOError("Cannot open WebCam")
            data = ""
            while True:
                ret, image = cap.read()
                cv2.imshow('WebCam', image)
                key = cv2.waitKey(10) & 0xff
                if key == 27:
                    break
                data = qrDecoder.recognize(image)
                if data != "":
                    break
            print("Decoded Data : {}".format(data))
            cap.release()
            cv2.destroyAllWindows()
        else:
            s = args.name
            image = cv2.imread(s)
            data = qrDecoder.recognize(image)
            if data == "":
                print("QR-code not detected!!!")
            else:
                # print(qrDecoder.objects)
                display(image, qrDecoder.objects)
                cv2.waitKey(0)
                print("Decoded Data : {}".format(data))
    else:
        print("To use recognizer, you have to input type of recognizer and method name('GUI' or name of your image as arguments of program)")
