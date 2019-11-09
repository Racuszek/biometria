import cv2 as cv

img=cv.imread('iris.png')
#1 Zamiana obrazu na obraz w skali szarości
gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
#2 Normalizacja histogramu


cv.waitKey()