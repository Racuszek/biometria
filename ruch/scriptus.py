import cv2 as cv
import numpy as np

im1=cv.imread('background.jpg')
im1=cv.cvtColor(im1, cv.COLOR_BGR2GRAY)
im1=cv.GaussianBlur(im1,(11,11),0)
im2=cv.imread('hand.jpg')
im2=cv.cvtColor(im2, cv.COLOR_BGR2GRAY)
im2=cv.GaussianBlur(im2,(11,11),0)
height, width = im1.shape[:2]
im3=im2-im1

for i in range(height):
	for j in range(width):
		value=im2[i][j]-im1[i][j]
		if value>255:
			im3[i][j]=255
		if value<0:
			im3[i][j]=0
		else:
			im3[i][j]=value
retval, img_fin = cv.threshold(im3, 230, 255, cv.THRESH_BINARY)
element = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))

img_fin=cv.dilate(img_fin, element, iterations=3)
img_fin=cv.erode(img_fin, element, iterations=5)
img_fin=cv.dilate(img_fin, element, iterations=5)
im_flood = ~img_fin.copy()
mask = np.zeros((height+2, width+2), np.uint8)
cv.floodFill(im_flood, mask, (0,0), 255)
hand_stencil = im_flood & img_fin

stencil = np.ones(img_fin.shape).astype(img_fin.dtype)
color=[255, 255, 255]

contours, hier = cv.findContours(hand_stencil,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
im2=backtorgb = cv.cvtColor(im2,cv.COLOR_GRAY2RGB)
for i in range(len(contours)):
	if cv.contourArea(contours[i])>1000:
		im2=cv.drawContours(im2, contours, i, (0,0,255),2)

cv.imwrite('result.jpg', im2)