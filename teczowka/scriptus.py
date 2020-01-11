import cv2 as cv
from scipy.interpolate import interp1d
import numpy as np
from PIL import Image

img=cv.imread('iris.png')
gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

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

eye_circles=cv.HoughCircles(pupil_bin_cleared, cv.HOUGH_GRADIENT, 1, 200, param1=30, param2=15)
detected_circles = np.uint16(np.around(eye_circles))

img2=img.copy()
for item in detected_circles[0, :]:
        a, b, r = item[0], item[1], item[2]

        # Draw the circumference of the circle.
        cv.circle(img2, (a, b), r, (0, 255, 0), 1)

        cv.circle(img2, (a, b), r+125, (0, 255, 0), 1)

        # Draw a small circle (of radius 1) to show the center.
        cv.circle(img2, (a, b), 1, (0, 0, 255), 3)
        cv.imshow("Detected Circles", img2)
        cv.imwrite("circles.png", img2)
        cv.waitKey(0)

if eye_circles is not None:
    circle = eye_circles[0][0]
    iris_center = (circle[0], circle[1])

if iris_center is not None:
    x = int(iris_center[0])
    y = int(iris_center[1])

    w = int(round(circle[2]) + 127)
    h = int(round(circle[2]) + 127)

    iris_image = img[y-h:y+h,x-w:x+w]
    final_iris = cv.resize(iris_image, (iris_image.shape[1]*2, iris_image.shape[0]*2))

q = np.arange(0.00, np.pi*2, 0.01) #theta
inn = np.arange(0, int(final_iris.shape[0]/2), 1) #radius

rect_image = np.empty(shape = [inn.size, int(final_iris.shape[1]), 3])
m = interp1d([np.pi*2, 0],[0,final_iris.shape[1]])

for r in inn:
    for t in q:
        dougmanX = int((r * np.cos(t)) + final_iris.shape[1]/2)
        dougmanY = int((r * np.sin(t)) + final_iris.shape[0]/2)
        rect_image[r][int(m(t) - 1)] = final_iris[dougmanY][dougmanX]

im = Image.fromarray(final_iris)
im.save('eye.jpeg')
rect_image = rect_image.astype('uint8')
im = Image.fromarray(rect_image)
im.save('rect_eye.jpeg')