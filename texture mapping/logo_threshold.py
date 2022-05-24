from black import out
import cv2
import numpy as np
from dominantColor import show, dominant_color

def equal(a, b):
    val = np.sum(np.square(a - b))
    # print(val)
    return val < 20000

img_path = "./images/shirt.jpg"
mask_path = "images/shirt_mask.png"


in_img = cv2.imread(img_path)
mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

out_img = in_img.copy()

dom = dominant_color(in_img, mask_img)

for i in range(in_img.shape[0]):
    for j in range(in_img.shape[1]):
        if mask_img[i][j] > 0 and equal(dom, in_img[i][j]) :
            out_img[i][j] = [0, 0, 0]

out_img = cv2.bitwise_and(out_img, out_img, mask=mask_img)
out_img = cv2.medianBlur(out_img, 3)

show("out", out_img)
cv2.imwrite("./results/shirt_logo.png", out_img)
