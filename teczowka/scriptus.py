import cv2 as cv

img=cv.imread('iris.png')
#1 Zamiana obrazu na obraz w skali szarości
gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
#2 Normalizacja histogramu

height, width=gray_img.shape
sum=0
for i in range(height):
    for j in range(width):
        sum=sum+gray_img[i][j]
p=sum/(width*height)
p_iris=p/1.5
p_pupil=p/4.5
retval, iris_bin = cv.threshold(gray_img, p_iris, 255, cv.THRESH_BINARY)
retval, pupil_bin = cv.threshold(gray_img, p_pupil, 255, cv.THRESH_BINARY)
cv.imwrite('iris_bin.png', iris_bin)
cv.imwrite('pupil_bin.png', pupil_bin)

pupil_bin_cleared=cv.imread('pupil_bin_cleared.png')
iris_bin_cleared=cv.imread('iris_bin_cleared.png')

pupil_edges=cv.Canny(pupil_bin_cleared, 100, 200)
iris_edges=cv.Canny(iris_bin_cleared, 100, 200)
cv.imshow('edges', pupil_edges)
cv.imshow('edges_iris', iris_edges)




cv.waitKey()
