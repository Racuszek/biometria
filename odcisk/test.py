import cv2 as cv
import numpy as np

img=cv.imread('raise.png')
retval, img = cv.threshold(img, 100, 255, cv.THRESH_BINARY)
    # img=cv.bitwise_not(img)

size=np.size(img)
element = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))
flag=False
skel = np.zeros(img.shape,np.uint8)

while(not flag):
    eroded = cv.erode(img, element)
    temp = cv.dilate(eroded, element)
    temp = cv.subtract(img, temp)
    skel = cv.bitwise_or(skel, temp)
    img = eroded.copy()
    zeros = size - cv.countNonZero(img)
    if zeros==size:
        flag = True
    # For some reasons the output image is negative, so it needs to be inverted.
    imagem=cv.bitwise_not(skel)

cv.imshow(imagem)