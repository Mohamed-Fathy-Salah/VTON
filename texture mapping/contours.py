from sys import stdin
import cv2
import numpy as np

def show(image):
    cv2.imshow("hi", cv2.resize(image, (500, 500)))
    cv2.waitKey(0)

paths = stdin.readlines()
# paths = ['./img/A.jpg\n']
for path in paths:
    image = cv2.imread(path[:-1])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.blur(gray, (3, 3))
    # blur = gray
    blur = cv2.normalize(blur, None, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # edge = cv2.Laplacian(blur, ddepth=cv2.CAP_V4L)
    edge = cv2.Laplacian(blur, ddepth=cv2.CV_8U)
    # show(edge)
    
    # edge = cv2.medianBlur(edge, 5)
    ret2, edge = cv2.threshold(edge, 0, 255, cv2.THRESH_OTSU)

    kernel = np.ones((5, 5), np.uint8)
    # edge = cv2.dilate(edge, kernel, iterations=1)
    # kernel = np.ones((3, 3), np.uint8)
    # edge = cv2.erode(edge, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    # cv2.drawContours(image, contours, -1, (255,0,0), cv2.FILLED)
    mask = np.zeros(gray.shape, np.uint8)
    for h, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 20:
            cv2.drawContours(mask, [cnt], 0, 255, -1)
    # image = cv2.floodFill(image, None, (0, 0), 255)

    show(mask)
    show(image)
