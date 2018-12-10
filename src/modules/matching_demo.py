import numpy as np
import cv2


def Nice(frame, tpls, coeff, min_count, det_name):
    max_num_kp = 0
    for t in tpls:
        tpl = cv2.imread(t)
        res = Matcher(frame, tpl, coeff, det_name)
        print(len(res[0]),"совпадения",t)
        if len(res[0]) > max_num_kp:
            max_num_kp = len(res[0])
            good_res = res
            good_name = t
            good_tpl = tpl
            
    if max_num_kp > min_count:
        img = Draw(frame, good_tpl, good_res[1], good_res[2], good_res[0])
        return [img, good_name]
   
    else:
        return [frame,'']
        
#Сопоставление двух изображений
def Matcher(image_big, tpl, coeff, det_name):
    matcher = cv2.BFMatcher()
    if (det_name == "ORB"):
        det = cv2.ORB_create() 
    elif (det_name == "SIFT"):
        det = cv2.xfeatures2d.SIFT_create()
    elif (det_name == "SURF"):
        det = cv2.xfeatures2d.SURF_create()
    else:
        print("Wrong detector name")
    image_gray = cv2.cvtColor(image_big, cv2.COLOR_BGR2GRAY)
    tpl_gray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
    kp_big, des_big = det.detectAndCompute(image_gray, None)
    kp_tpl, des_tpl = det.detectAndCompute(tpl_gray, None)
    matches = matcher.knnMatch(des_tpl, des_big, k = 2)
    good = []
    for m,n in matches:
        if m.distance < n.distance * coeff: 
            good.append(m)
    result = [good, kp_big, kp_tpl]        
    return result             
        
#Отрисовка рамки
def Draw(frame, tpl, kp_frame, kp_tpl, good):
    src_pts = np.float32([ kp_tpl[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp_frame[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    M, _ = cv2.findHomography( src_pts, dst_pts, cv2.RANSAC , 5.0 ) # матрица преобразования координат точек
    h, w, _ = tpl.shape # размеры шаблона
    pts = np.asarray( [ [0,0], [0,h - 1], [w - 1,h - 1], [w - 1,0] ],
                      dtype=np.float32).reshape(-1,1,2)
    dst = cv2.perspectiveTransform( pts, M )
    dst = [np.int32(np.abs(dst))]
    img_res = cv2.polylines(frame, dst, True, (0,255,255), 2, cv2.LINE_AA )
    return img_res
