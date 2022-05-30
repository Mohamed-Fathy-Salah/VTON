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
back_shirt_coordinates = 10, 258, 491, 505

# wl / ws * wc, hl / hs * hc
def relative_scale(shirt, logo, coords):
    return int(logo[2] / shirt[2] * coords[2]), int(logo[3] / shirt[3] * coords[3])

# (xl - xs) / ws * wc + xc
def relative_pos(shirt, logo, coords):
    return int((logo[0] - shirt[0]) / shirt[2] * coords[2] + coords[0]), int((logo[1] - shirt[1]) / shirt[3] * coords[3] + coords[1])

def generate_texture(front_image_path, back_image_path):
    front_image = cv2.imread(front_image_path)
    back_image = cv2.imread(back_image_path)
    # TODO : use os path
    # filename = str(front_image_path).split("/")[-1].split(".")[0]

    back_garment_mask = get_garment_mask(back_image)
    front_garment_mask = get_garment_mask(front_image)

    dom_color = dominant_color(front_image, back_garment_mask)

    front_logo_mask = get_logo_mask(front_image, front_garment_mask, dom_color).astype('uint8')
    front_logo = cv2.bitwise_and(front_image, front_image, mask=front_logo_mask)
    back_logo_mask = get_logo_mask(back_image, back_garment_mask, dom_color).astype('uint8')
    back_logo = cv2.bitwise_and(back_image, back_image, mask=back_logo_mask)

    front_shirt_pos = pos(front_garment_mask)
    front_logo_pos = pos(front_logo_mask)
    back_shirt_pos = pos(back_garment_mask)
    back_logo_pos = pos(back_logo_mask)

    (wf, hf), (xf, yf) = relative_scale(front_shirt_pos, front_logo_pos, front_shirt_coordinates), relative_pos(front_shirt_pos, front_logo_pos, front_shirt_coordinates)
    (wb, hb), (xb, yb) = relative_scale(back_shirt_pos, back_logo_pos, back_shirt_coordinates), relative_pos(back_shirt_pos, back_logo_pos, back_shirt_coordinates)

    # crop logo
    front_logo = front_logo[front_logo_pos[1]:front_logo_pos[1] + front_logo_pos[3], front_logo_pos[0]:front_logo_pos[0] + front_logo_pos[2]]
    front_logo = cv2.resize(front_logo ,(wf, hf))
    front_logo_mask = front_logo_mask[front_logo_pos[1]:front_logo_pos[1] + front_logo_pos[3], front_logo_pos[0]:front_logo_pos[0] + front_logo_pos[2]]
    front_logo_mask = cv2.resize(front_logo_mask ,(wf, hf))
    back_logo = back_logo[back_logo_pos[1]:back_logo_pos[1] + back_logo_pos[3], back_logo_pos[0]:back_logo_pos[0] + back_logo_pos[2]]
    back_logo = cv2.resize(back_logo ,(wb, hb))
    back_logo_mask = back_logo_mask[back_logo_pos[1]:back_logo_pos[1] + back_logo_pos[3], back_logo_pos[0]:back_logo_pos[0] + back_logo_pos[2]]
    back_logo_mask = cv2.resize(back_logo_mask ,(wb, hb))

    texture_map = np.zeros((1024, 1024, 3)) 
    texture_map[:,:] = dom_color

    front_logo[front_logo_mask == 0] = dom_color
    back_logo[back_logo_mask == 0] = dom_color

    texture_map[yf : yf + front_logo.shape[0], xf : xf + front_logo.shape[1]] = front_logo
    texture_map[yb : yb + back_logo.shape[0], xb : xb + back_logo.shape[1]] = back_logo

    return texture_map
    # cv2.imwrite(f"./results/{filename}.png", texture_map)
    # print(xm, ym, wm, hm)
    # cv2.rectangle(texture_map, (xm, ym), (xm + wm, ym + hm), (0,0,255), 2)
    # cv2.imwrite("./results/hi.png", texture_map)
    # show_image(coord, "coord")

if __name__ == "__main__":
    front_image_path = "./images/lungs.jpg"
    # back_image_path = "./images/blackheart.jpg"
    texture = generate_texture(front_image_path, front_image_path)
    cv2.imwrite("./results/lungs.png", texture)

    
