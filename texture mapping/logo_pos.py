import cv2 as cv 

def pos(mask, img):
    # cnts = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # mx = 0
    # shirt pos
    # xm, ym, wm, hm = 0,0,0,0
    # for c in cnts:
    #     x,y,w,h = cv.boundingRect(c)
    #     if mx < w * h:
    #         mx = w*h
    #         xm, ym, wm, hm = x,y,w,h 

    xm, ym, wm, hm = cv.boundingRect(cv.findNonZero(mask))
    cv.rectangle(img, (xm, ym), (xm + wm, ym + hm), (0,0,255), 2)

    cv.imshow('image', img)
    cv.waitKey()
    return xm, ym, wm, hm

mask = cv.imread("./images/mask.png", cv.IMREAD_GRAYSCALE)
img = cv.imread("./images/dubai.jpg")
logo = cv.imread("results/light.png", cv.IMREAD_GRAYSCALE)

pos(mask, img)
pos(logo, img)
