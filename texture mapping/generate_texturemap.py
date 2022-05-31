import cv2
import numpy as np
from matplotlib import pyplot as plt

def show_image(image, title=None):
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.imshow(image)
    # plt.xticks([]), plt.yticks([])
    # plt.title(title)
    # plt.show()
    cv2.imshow(image, title)
    cv2.waitKey(0)

def get_garment_mask(image):
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

def get_logo_mask(image, mask, dom):

    image = (np.sum(np.square(np.subtract(image, dom)), axis= 2) > 20000) * 255
    image = cv2.bitwise_and(image, image, mask=mask).astype('float32')
    image = cv2.medianBlur(image, 3)
    # kernel = np.array([[1, 0, 1],[0, 1, 0],[1, 0, 1]], np.uint8)
    # image = cv2.erode(image, kernel)
    # image = cv2.dilate(image, kernel)
    return image

def pos(mask):
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    xm, ym, wm, hm = cv2.boundingRect(cv2.findNonZero(mask))
    return xm, ym, wm, hm

# front_shirt_coordinates = 547, 254, 462, 525
# back_shirt_coordinates = 10, 258, 491, 505
# [0]= back, [1]= front
shirt_coordinates = [(20, 258, 471, 505), (557, 254, 442, 525)]

# wl / ws * wc, hl / hs * hc
def relative_scale(shirt, logo, coords):
    return int(logo[2] / shirt[2] * coords[2]), int(logo[3] / shirt[3] * coords[3])

# (xl - xs) / ws * wc + xc
def relative_pos(shirt, logo, coords):
    return int((logo[0] - shirt[0]) / shirt[2] * coords[2] + coords[0]), int((logo[1] - shirt[1]) / shirt[3] * coords[3] + coords[1])

def generate_texture(front_image_path, back_image_path):
    texture_map = np.zeros((1024, 1024, 3)) 
    for idx, image_path in enumerate([back_image_path, front_image_path]):
        image = cv2.imread(image_path)
        garment_mask = get_garment_mask(image)

        dom_color = dominant_color(image, garment_mask)

        logo_mask = get_logo_mask(image, garment_mask, dom_color).astype('uint8')
        logo = cv2.bitwise_and(image, image, mask=logo_mask)

        shirt_pos = pos(garment_mask)
        logo_pos = pos(logo_mask)

        (w, h), (x, y) = relative_scale(shirt_pos, logo_pos, shirt_coordinates[idx]), relative_pos(shirt_pos, logo_pos, shirt_coordinates[idx])

        logo = logo[logo_pos[1]:logo_pos[1] + logo_pos[3], logo_pos[0]:logo_pos[0] + logo_pos[2]]
        logo = cv2.resize(logo ,(w, h))
        logo_mask = logo_mask[logo_pos[1]:logo_pos[1] + logo_pos[3], logo_pos[0]:logo_pos[0] + logo_pos[2]]
        logo_mask = cv2.resize(logo_mask ,(w, h))

        texture_map[:,idx*512:idx*512+512] = dom_color

        logo[logo_mask == 0] = dom_color
        texture_map[y : y + logo.shape[0], x : x + logo.shape[1]] = logo

    return texture_map

if __name__ == "__main__":
    front_image_path = "./images/dubai.jpg"
    back_image_path = "./images/blackheart.jpg"
    texture = generate_texture(front_image_path, back_image_path)
    cv2.imwrite("./results/l.png", texture)

    
