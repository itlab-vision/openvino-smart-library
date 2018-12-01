import os
import numpy as np
import cv2

MIN_MATCH_COUNT = 100
DIST_COEFF = 0.65

def Match(image, kp_tpl, des_tpl):
        matcher = cv2.BFMatcher()
        templ = [ os.path.join("covers/", b) for b in os.listdir("covers/") if os.path.isfile(os.path.join("covers/", b)) ]
        max_num = 0
        i = 0
        max_tpl = ''
        sift = cv2.xfeatures2d.SIFT_create() 
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kp_big, des_big = sift.detectAndCompute(frame, None) # Поиск точек на кадре
        for t in templ:
            matches = matcher.knnMatch(des_tpl[i], des_big, k = 2) # Сопоставление точек
            good = []
            for m,n in matches:
                if m.distance < n.distance * DIST_COEFF: 
                    good.append(m)
            if (max_num < len(good)):  # Поиск шаблона с наибольшим количеством совпавших точек
                    max_num = len(good)
                    max_tpl = t
                    max_kp = kp_tpl[i]
                    max_good = good
            i = i + 1        
                    
        if (max_num > MIN_MATCH_COUNT):
            img_tpl = cv2.imread(max_tpl)
            src_pts = np.float32([ max_kp[m.queryIdx].pt for m in max_good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp_big[m.trainIdx].pt for m in max_good ]).reshape(-1,1,2)
            M, _ = cv2.findHomography( src_pts, dst_pts, cv2.RANSAC , 5.0 ) # матрица преобразования координат точек
            h, w, _ = img_tpl.shape # размеры шаблона
            pts = np.asarray( [ [0,0], [0,h-1], [w-1,h-1], [w-1,0] ], dtype=np.float32).reshape(-1,1,2)
            dst = cv2.perspectiveTransform( pts, M )
            dst = [np.int32(np.abs(dst))]
            img_res = cv2.polylines(image, dst, True, (0,255,255), 2, cv2.LINE_AA )
            return [img_res, max_tpl]
        else:
            return [image, '']
            
        