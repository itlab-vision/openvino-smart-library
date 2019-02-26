import sys, os
import cv2
sys.path.append("..\src\modules")
import book_recognizer

#Список имен файлов с обложками
templ = [ os.path.join("covers/", b) for b in os.listdir("covers/")
          if os.path.isfile(os.path.join("covers/", b)) ]
capture = cv2.VideoCapture('video.mp4')
rec = book_recognizer.Recognizer()
rec.Create("SIFT")
ret, frame = capture.read()
while ret:     
    [book_id, tpl, res] = rec.Recognize(frame, templ, 0.87, 70)
    if book_id == -1:
        cv2.imshow("", frame)
        cv2.waitKey(100)
        ret, frame = capture.read()
        continue
    else:
        frame_draw = rec.Draw(frame, tpl, res)
        cv2.imshow("", frame)
        cv2.waitKey(100)
        ret, frame = capture.read()
        continue
  
cv2.destroyAllWindows()
