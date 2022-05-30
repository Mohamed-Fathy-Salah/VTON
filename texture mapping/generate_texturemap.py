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

front_shirt_coordinates = 547, 254, 462, 525

# wl / ws * wc, hl / hs * hc
def relative_scale(shirt, logo):
    return int(logo[2] / shirt[2] * front_shirt_coordinates[2]), int(logo[3] / shirt[3] * front_shirt_coordinates[3])

# (xl - xs) / ws * wc + xc
def relative_pos(shirt, logo):
    return int((logo[0] - shirt[0]) / shirt[2] * front_shirt_coordinates[2] + front_shirt_coordinates[0]), int((logo[1] - shirt[1]) / shirt[3] * front_shirt_coordinates[3] + front_shirt_coordinates[1])

def generate_texture(image_path):
    image = cv2.imread(image_path)
    # TODO : use os path
    filename = str(image_path).split("/")[-1].split(".")[0]

    garment_mask = get_garment_mask(image)
    dom_color = dominant_color(image, garment_mask)
    logo_mask = get_logo_mask(image, garment_mask, dom_color).astype('uint8')

    logo = cv2.bitwise_and(image, image, mask=logo_mask)
    # show_image(image, "image")
    # show_image(mask, "mask")
    # show_image(logo, "logo")

    shirt_pos = pos(garment_mask)
    logo_pos = pos(logo_mask)

    # print(shirt_pos)
    # print(logo_pos)

    wm, hm = relative_scale(shirt_pos, logo_pos)
    xm, ym = relative_pos(shirt_pos, logo_pos)

    # crop logo
    logo = logo[logo_pos[1]:logo_pos[1] + logo_pos[3], logo_pos[0]:logo_pos[0] + logo_pos[2]]
    logo_mask = logo_mask[logo_pos[1]:logo_pos[1] + logo_pos[3], logo_pos[0]:logo_pos[0] + logo_pos[2]]

    logo = cv2.resize(logo ,(wm, hm))
    logo_mask = cv2.resize(logo_mask ,(wm, hm))

    texture_map = np.zeros((1024, 1024, 3)) 
    texture_map[:,:] = dom_color

    logo[logo_mask == 0] = dom_color
    texture_map[ym : ym + logo.shape[0], xm : xm + logo.shape[1]] = logo

    cv2.imwrite(f"./results/{filename}.png", texture_map)
    # print(xm, ym, wm, hm)
    # cv2.rectangle(texture_map, (xm, ym), (xm + wm, ym + hm), (0,0,255), 2)
    # cv2.imwrite("./results/hi.png", texture_map)
    # show_image(coord, "coord")

if __name__ == "__main__":
    image_path = "./images/lungs.jpg"
    generate_texture(image_path)

    
