import cv2 as cv
from scipy.interpolate import interp1d
import numpy as np
from PIL import Image

def daugman_normalizaton(image, height, width, r_in, r_out):
    thetas = np.arange(0, 2 * np.pi, 2 * np.pi / width)  # Theta values
    r_out = r_in + r_out
    # Create empty flatten image
    flat = np.zeros((height,width, 3), np.uint8)
    circle_x = int(image.shape[0] / 2)
    circle_y = int(image.shape[1] / 2)

    for i in range(width):
        for j in range(height):
            theta = thetas[i]  # value of theta coordinate
            r_pro = j / height  # value of r coordinate(normalized)

            # get coordinate of boundaries
            Xi = circle_x + r_in * np.cos(theta)
            Yi = circle_y + r_in * np.sin(theta)
            Xo = circle_x + r_out * np.cos(theta)
            Yo = circle_y + r_out * np.sin(theta)

            # the matched cartesian coordinates for the polar coordinates
            Xc = (1 - r_pro) * Xi + r_pro * Xo
            Yc = (1 - r_pro) * Yi + r_pro * Yo

            color = image[int(Xc)][int(Yc)]  # color of the pixel

            flat[j][i] = color
    return flat  # liang

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

eye_circles=cv.HoughCircles(pupil_bin_cleared, cv.HOUGH_GRADIENT, 1, 200, param1=30, param2=15)
if eye_circles is not None:
    circle = eye_circles[0][0]
    iris_coordinates = (circle[0], circle[1])

if iris_coordinates is not None:
    x = int(iris_coordinates[0])
    y = int(iris_coordinates[1])

    w = int(round(circle[2]) + 10)
    h = int(round(circle[2]) + 10)

    #cv2.circle(original_eye, iris_coordinates, int(circle[2]), (255,0,0), thickness=2)
    iris_image = img[y-h:y+h,x-w:x+w]
    iris_image_to_show = cv.resize(iris_image, (iris_image.shape[1]*2, iris_image.shape[0]*2))

q = np.arange(0.00, np.pi*2, 0.01) #theta
inn = np.arange(0, int(iris_image_to_show.shape[0]/2), 1) #radius

cartisian_image = np.empty(shape = [inn.size, int(iris_image_to_show.shape[1]), 3])
m = interp1d([np.pi*2, 0],[0,iris_image_to_show.shape[1]])

for r in inn:
    for t in q:
        polarX = int((r * np.cos(t)) + iris_image_to_show.shape[1]/2)
        polarY = int((r * np.sin(t)) + iris_image_to_show.shape[0]/2)
        cartisian_image[r][int(m(t) - 1)] = iris_image_to_show[polarY][polarX]

im = Image.fromarray(iris_image_to_show)
im.save('eye.jpeg')
cartisian_image = cartisian_image.astype('uint8')
im = Image.fromarray(cartisian_image)
im.save('cartesian_eye.jpeg')
# detected_iris=cv.HoughCircles(iris_bin_cleared, cv.HOUGH_GRADIENT, 1, 200, param1=30, param2=15)
# if detected_pupil is not None:
#
#     # Convert the circle parameters a, b and r to integers.
#     detected_pupil = np.uint16(np.around(detected_pupil))
#     # detected_iris = np.uint16(np.around(detected_iris))
#
#     for pt in detected_pupil[0, :]:
#         a, b, r = pt[0], pt[1], pt[2]
#
#         # Draw the circumference of the pupil.
#         cv.circle(img, (a, b), r, (0, 255, 0), 1)
#         # Draw a small circle (of radius 1) to show the center.
#         cv.circle(img, (a, b), 1, (0, 0, 255), 3)
#         # Attempt to draw the circumference of the iris.
#         cv.circle(img, (a, b), r+25, (0, 255, 0), 1)
#     cv.imshow("Detected Circles", img)
#     cv.waitKey(0)
#
# def daugman_normalizaiton(image, height, width, r_in, r_out):
#     thetas = np.arange(0, 2 * np.pi, 2 * np.pi / width)  # Theta values
#     r_out = r_in + r_out
#     # Create empty flatten image
#     flat = np.zeros((height,width, 3), np.uint8)
#     circle_x = int(image.shape[0] / 2)
#     circle_y = int(image.shape[1] / 2)
#
#     for i in range(width):
#         for j in range(height):
#             theta = thetas[i]  # value of theta coordinate
#             r_pro = j / height  # value of r coordinate(normalized)
#
#             # get coordinate of boundaries
#             Xi = circle_x + r_in * np.cos(theta)
#             Yi = circle_y + r_in * np.sin(theta)
#             Xo = circle_x + r_out * np.cos(theta)
#             Yo = circle_y + r_out * np.sin(theta)
#
#             # the matched cartesian coordinates for the polar coordinates
#             Xc = (1 - r_pro) * Xi + r_pro * Xo
#             Yc = (1 - r_pro) * Yi + r_pro * Yo
#
#             color = image[int(Xc)][int(Yc)]  # color of the pixel
#
#             flat[j][i] = color
#     return flat  # liang

# cv.waitKey()
