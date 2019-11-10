import cv2 as cv
import numpy as np
# All images have been cropped in order to remove discolorations.
fingerprints=['odcisk1.jpg', 'odcisk2.jpg', 'odcisk3.jpg', 'odcisk4.jpg']

for item in fingerprints:
    img=cv.imread(item)
    img_gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_norm=cv.equalizeHist(img_gray)
    blurred = cv.GaussianBlur(img_norm,(5,5),0)
    retval, img = cv.threshold(blurred, 100, 255, cv.THRESH_BINARY)
    # img=cv.bitwise_not(img)
    img = cv.GaussianBlur(img,(3,3),0)
    retval, img = cv.threshold(img, 100, 255, cv.THRESH_BINARY)

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
    # For some reasons the output image is negative, so it needs to be inverted.
    imagem=cv.bitwise_not(skel)

    #Cropping the image
    height, width=img.shape
    border=5

    # blank_image = np.zeros((height-2*border,width-2*border,3), np.uint8)
    blank_image = np.zeros((height-2*border, width-2*border), np.uint8)
    for i in range(border, height-border):
        for j in range(border, width-border):
            blank_image[i-5][j-5]=imagem[i][j]
    # for i in range(5, width-5):
        # for j in range(5, height-5):
            # blank_image[i-5][j-5]=img[i][j]
    cv.imshow("skel",blank_image)
    cv.waitKey(0)
    # cv.destroyAllWindows()


# cv.imshow('bin', threshold)
# cv.waitKey()