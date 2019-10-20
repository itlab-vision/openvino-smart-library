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
        answer.append(br.Recognizer2.recognize(i))
        br.Recognizer2.display(i)

    # Print our results
    for i in answer:
        print(i)


