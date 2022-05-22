from cv2 import cv2
import numpy as np

def show(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)

input_img = cv2.imread("shirt.jpg")
mask_img = cv2.imread("mask.jpg", cv2.IMREAD_GRAYSCALE)
# show("input", input_img)
avg_color = np.zeros(3)
cnt = 0
for i in range(mask_img.shape[0]):
    for j in range(mask_img.shape[1]):
        if mask_img[i][j] != 0:
            avg_color = avg_color + input_img[i][j]
            cnt = cnt + 1

avg_color /= cnt

print("----")
print(avg_color)            
avg_img = input_img.copy()

for i in range(60):
    for j in range(60):
        avg_img[i][j] = avg_color

# show("avg", avg_img)

