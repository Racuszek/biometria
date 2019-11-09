import cv2 as cv

img=cv.imread('iris.png')
# cv.imshow('fuck', img)
gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
cv.imshow('gray fuck', gray_img)
cv.waitKey()