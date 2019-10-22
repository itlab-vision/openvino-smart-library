import sys, os
import argparse
import numpy as np
import cv2
sys.path.append("../src/modules")
import book_recognizer as br


# Main
if __name__ == '__main__':
    # Read images
    images = []
    file = open('qr-codes/qr.txt')
    while(True):
        s = file.readline()
        if s == '':
            break
        else:
            images.append(cv2.imread(s[0:len(s)-1]))

    # Get information from QR
    answer = []
    for i in images:
        answer.append(br.QRBookRecognizer.recognize(i))
        cv2.imshow("Results", br.QRBookRecognizer.display(i))
        cv2.waitKey(0)

    # Print our results
    for i in answer:
        print(i)


