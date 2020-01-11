import numpy as np
import cv2 as cv
faces_list=['twarz3.png']
# Metoda RGB
for facename in faces_list:
    input=cv.imread(facename)
    height, width=input.shape[:2]
    r_minus_g = np.zeros((height,width, 3), np.uint8) # Tworzenie nowego obrazu o takich samych wymiarach
    for i in range(height):
        for j in range(width):
            val=int(input[i][j][2])-int(input[i][j][1])
            r_minus_g[i][j]=val if val>0 else 0
    retval, binarised=cv.threshold(r_minus_g, 30, 255, cv.THRESH_BINARY)
    final = np.zeros((height,width, 3), np.uint8)
    binarised = cv.cvtColor(binarised, cv.COLOR_RGB2GRAY)

    kernel=np.ones((5,5), np.uint)
    binarised=cv.dilate(binarised, kernel, iterations=2)
    binarised=cv.erode(binarised, kernel, iterations=2)
    binarised=cv.dilate(binarised, kernel, iterations=2)
    binarised=cv.erode(binarised, kernel, iterations=2)
    cv.imshow('mask', binarised)
    cv.waitKey()

    stencil = np.ones(input.shape).astype(input.dtype)
    color=[255, 255, 255]

    contours, hier = cv.findContours(binarised,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(input, contours, -1, (100,0,0),2)
    for cnt in contours:
        if 600<cv.contourArea(cnt):
            cv.fillPoly(stencil, [cnt], color)
            result=cv.bitwise_and(input, stencil)
            cv.imshow('woo', result)
            cv.waitKey()
            print('saving...')
            cv.imwrite('{}_cont.jpg'.format(facename[:-4]), result)