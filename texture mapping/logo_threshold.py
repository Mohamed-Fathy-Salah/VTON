from colorthief import ColorThief
import cv2 as cv

def show(img):
    cv.imshow("image", img)
    cv.waitKey(0)


img_path = "images/shirt.jpg"
color_thief = ColorThief(img_path)
dominant_color = color_thief.get_color(quality=1)
print(dominant_color)

in_img = cv.imread(img_path)
in_img[0:40,0:40] = dominant_color
show(in_img)
