import sys, os
import tempfile
import argparse
import numpy as np
import cv2
sys.path.append("../src/modules")
import QR_generator as qr


def createArgparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', type=str, default=None)
    parser.add_argument('-o', '--out', type=str, default="console")
    return parser.parse_args()


# Main
if __name__ == '__main__':
    args = createArgparse()
    gen = qr.QRgenerator()
    if args.string is not None:
        image = gen.makeQR(args.string)
        if args.out == "console":
            image.save("qr.png")
            image = cv2.imread("qr.png")
            cv2.imshow("QR-code", image)
            cv2.waitKey(0)
        else:
            image.save(args.out)
    else:
        print("To use qr-generator, you have to input string you want to encode")
