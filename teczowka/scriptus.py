import cv2 as cv
import numpy as np

img=cv.imread('iris.png')
#1 Zamiana obrazu na obraz w skali szarosci
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

pupil_bin_cleared = cv.cvtColor(pupil_bin_cleared, cv.COLOR_RGB2GRAY)
iris_bin_cleared = cv.cvtColor(iris_bin_cleared, cv.COLOR_RGB2GRAY)

# cv.imshow('bin', pupil_bin_cleared)
cv.waitKey()

# pupil_edges=cv.Canny(pupil_bin_cleared, 100, 200)
# iris_edges=cv.Canny(iris_bin_cleared, 100, 200)
# cv.imshow('edges', pupil_edges)
# cv.imshow('edges_iris', iris_edges)

detected_pupil=cv.HoughCircles(pupil_bin_cleared, cv.HOUGH_GRADIENT, 1, 200, param1=30, param2=15)
# detected_iris=cv.HoughCircles(iris_bin_cleared, cv.HOUGH_GRADIENT, 1, 200, param1=30, param2=15)
if detected_pupil is not None:

    # Convert the circle parameters a, b and r to integers.
    detected_pupil = np.uint16(np.around(detected_pupil))
    # detected_iris = np.uint16(np.around(detected_iris))

    for pt in detected_pupil[0, :]:
        a, b, r = pt[0], pt[1], pt[2]

        # Draw the circumference of the pupil.
        cv.circle(img, (a, b), r, (0, 255, 0), 1)
        # Draw a small circle (of radius 1) to show the center.
        cv.circle(img, (a, b), 1, (0, 0, 255), 3)
        # Attempt to draw the circumference of the iris.
        cv.circle(img, (a, b), r+25, (0, 255, 0), 1)
    cv.imshow("Detected Circles", img)
    cv.waitKey(0)


cv.waitKey()
