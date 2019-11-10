import cv2 as cv
import numpy as np
# All images have been cropped in order to remove discolorations.
fingerprints=['odcisk1.jpg', 'odcisk2.jpg', 'odcisk3.jpg', 'odcisk4.jpg']

img=cv.imread('odcisk1.jpg')
img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img_norm=cv.equalizeHist(img_gray)
blurred = cv.GaussianBlur(img_norm,(3,3),0)
retval, img = cv.threshold(blurred, 100, 255, cv.THRESH_BINARY)

size = np.size(img)
skel = np.zeros(img.shape,np.uint8)

element = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))
flag=False

while(not flag):
    eroded = cv.erode(img, element)
    temp = cv.dilate(eroded, element)
    temp = cv.subtract(img, temp)
    skel = cv.bitwise_or(skel, temp)
    img = eroded.copy()
    zeros = size - cv.countNonZero(img)
    if zeros==size:
        flag = True

imagem=cv.bitwise_not(skel)
cv.imshow("skel",imagem)
cv.waitKey(0)
cv.destroyAllWindows()


# cv.imshow('bin', threshold)
# cv.waitKey()