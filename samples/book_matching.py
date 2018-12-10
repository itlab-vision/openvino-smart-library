import sys, os
import cv2
sys.path.append("..\src\modules")
import matching_demo

#Список имен файлов с обложками
templ = [ os.path.join("covers/", b) for b in os.listdir("covers/")
          if os.path.isfile(os.path.join("covers/", b)) ]

capture = cv2.VideoCapture("video.mp4")
ret, frame = capture.read()
while ret:     
    [image_res, tpl_name] = matching_demo.Nice(frame, templ, 0.87, 70, "ORB")
    cv2.imshow("", image_res)
    cv2.waitKey(100)
    if tpl_name == '':
        ret, frame = capture.read()
    else:
        cv2.imshow("", image_res)
        cv2.waitKey(100)
        ret, frame = capture.read()

cv2.destroyAllWindows()
