import sys, os
import tempfile
import argparse
import numpy as np
import cv2
sys.path.append("../src/modules")
import book_recognizer as br
import QR_generator as qr


# Main
if __name__ == '__main__':
    file = open('qr-codes/qr.txt')
    # Recognizer by OpenCV
    qrDecoder = br.QRBookRecognizerByOpenCv()
    inputImage = 0
    if len(sys.argv) > 1:
        inputImage = cv2.imread(sys.argv[1])
    else:
        inputImage = cv2.imread("C:\images\qr-generated.png")
    qrDecoder.recognize(inputImage)
    # Read images
    images = []
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

    # Try to generate qr-code and recognize by OpenCV
    gen = qr.QRgenerator()
    image = gen.makeQR("Aleksandr Pushkin : 'Evgeniy Onegin' ")
    image.save("qr.png")
    image = cv2.imread("qr.png")
    cv2.imshow("QR-code", image)
    cv2.waitKey(0)
    qrDecoder.recognize(image)

