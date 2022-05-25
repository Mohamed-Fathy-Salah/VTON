import cv2
import numpy as np
from matplotlib import pyplot as plt

def show_image(image, title=None):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.xticks([]), plt.yticks([])
    plt.title(title)
    plt.show()

def get_mask(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, im_th = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY_INV)

    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    im_floodfill = im_th.copy()
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    return im_th | im_floodfill_inv

def dominant_color(image, mask):
    masked = cv2.bitwise_and(image, image, mask=mask)
    cnt = len(masked[np.max(masked, axis=2) > 0])
    avg_color = np.sum(np.sum(masked, axis=0), axis=0) / cnt
    return avg_color

def equal(a, b):
    val = np.sum(np.square(a - b))
    return val < 20000

def get_logo(image, mask):
    out_img = image.copy()

    dom = dominant_color(image, mask)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mask[i][j] > 0 and equal(dom, image[i][j]) :
                out_img[i][j] = [0, 0, 0]

    out_img = cv2.bitwise_and(out_img, out_img, mask=mask)
    out_img = cv2.medianBlur(out_img, 3)

    return out_img

def pos(mask):
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    xm, ym, wm, hm = cv2.boundingRect(cv2.findNonZero(mask))
    return xm, ym, wm, hm

front_shirt_coordinates = 547, 254, 462, 525

# wl / ws * wc, hl / hs * hc
def relative_scale(shirt, logo):
    return int(logo[2] / shirt[2] * front_shirt_coordinates[2]), int(logo[3] / shirt[3] * front_shirt_coordinates[3])

# (xl - xs) / ws * wc + xc
def relative_pos(shirt, logo):
    return int((logo[0] - shirt[0]) / shirt[2] * front_shirt_coordinates[2] + front_shirt_coordinates[0]), int((logo[1] - shirt[1]) / shirt[3] * front_shirt_coordinates[3] + front_shirt_coordinates[1])
    # return (logo[0] - shirt[0]) / shirt[2] * front_shirt_coordinates[2], (logo[1] - shirt[1]) / shirt[3] *front_shirt_coordinates[3]

if __name__ == "__main__":
    image_path = "./images/shirt.jpg"

    image = cv2.imread(image_path)
    mask = get_mask(image)
    logo = get_logo(image, mask)

    # show_image(image, "image")
    # show_image(mask, "mask")
    # show_image(logo, "logo")

    shirt_pos = pos(mask)
    logo_pos = pos(logo)

    print(shirt_pos)
    print(logo_pos)

    wm, hm = relative_scale(shirt_pos, logo_pos)
    xm, ym = relative_pos(shirt_pos, logo_pos)
    
    coord = cv2.imread("./images/old-t-shirt_female.png")
    
    print(xm, ym, wm, hm)
    cv2.rectangle(coord, (xm, ym), (xm + wm, ym + hm), (0,0,255), 2)
    show_image(coord, "coord")
