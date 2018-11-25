import sys, os
import cv2
sys.path.append("..\src\modules")
import matching_demo


sift = cv2.xfeatures2d.SIFT_create() 
#Список имен файлов с обложками
templ = [ os.path.join("covers/", b) for b in os.listdir("covers/") if os.path.isfile(os.path.join("covers/", b)) ]
kp_tpl = [0] * len(templ)
des_tpl = [0] * len(templ)
i = 0
for t in templ:
    img_tpl = cv2.imread(t)
    kp_tpl[i], des_tpl[i] = sift.detectAndCompute(img_tpl, None) # Массив контрольных точек и дескрипторов для шаблонов
    i= i + 1

capture = cv2.VideoCapture("video.mp4")
ret, frame = capture.read()
while ret:     
    [image_res, tpl_name] = matching_demo.Match(frame, kp_tpl, des_tpl)
    cv2.imshow("", image_res)
    cv2.waitKey(100)
    if tpl_name == '':
        ret, frame = capture.read()
    else:
        cv2.imshow("", image_res)
        cv2.waitKey(100)
        print(tpl_name)
        break

cv2.destroyAllWindows()
