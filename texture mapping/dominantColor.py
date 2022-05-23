import cv2
import numpy as np

def show(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)

def dominant_color(input_img, mask_img):
    # input_img = cv2.imread(input_img)
    # mask_img = cv2.imread(mask_img, cv2.IMREAD_GRAYSCALE)

    masked = cv2.bitwise_and(input_img, input_img, mask=mask_img)
    # show("input", masked)

    cnt = len(masked[np.max(masked, axis=2) > 0])
    avg_color = np.sum(np.sum(masked, axis=0), axis=0) / cnt

    # print(avg_color)

    # avg_img = input_img.copy()
    # avg_img[0:60,0:60] = avg_color

    # show("avg", avg_img)
    return avg_color
