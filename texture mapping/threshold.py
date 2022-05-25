import cv2
import numpy as np
from matplotlib import pyplot as plt

def show_image(image, title=None):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.xticks([]), plt.yticks([])
    plt.title(title)
    plt.show()

# Read image
im_in = cv2.imread("./images/old-t-shirt_female.png", cv2.IMREAD_GRAYSCALE)

# resize image
# scale_percent = 60 # percent of original size
# width = int(im_in.shape[1] * scale_percent / 100)
# height = int(im_in.shape[0] * scale_percent / 100)
# dim = (width, height)
# im_in = cv2.resize(im_in, dim, interpolation = cv2.INTER_AREA)

# Threshold.
# Set values equal to or above 220 to 0.
# Set values below 220 to 255.
_, im_th = cv2.threshold(im_in, 220, 255, cv2.THRESH_BINARY_INV)

# Copy the thresholded image.
im_floodfill = im_th.copy()

# Mask used to flood filling.
# Notice the size needs to be 2 pixels than the image.
h, w = im_th.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

# Floodfill from point (0, 0)
cv2.floodFill(im_floodfill, mask, (0, 0), 255)

# Invert floodfilled image
im_floodfill_inv = cv2.bitwise_not(im_floodfill)

# Combine the two images to get the foreground.
im_out = im_th | im_floodfill_inv

# Display images.
show_image(im_in, "input Image")
# cv2.imshow("Thresholded Image", im_th)
# cv2.imshow("Floodfilled Image", im_floodfill)
# cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
show_image(im_out, "Foreground")
# cv2.imshow("Foreground", im_out)

cv2.imwrite("./images/coordinates.png", im_out)
# cv2.imwrite("mask.jpg", im_th)
cv2.waitKey(0)
