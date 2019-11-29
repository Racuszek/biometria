import numpy as np
import cv2 as cv
faces_list=['twarz_ideal.png', 'twarz1.png', 'twarz2.png', 'twarz3.png', 'twarz4.png', 'twarz5.png', 'twarz6.png', 'twarz8.jpg', 'twarz9.jpeg']

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

    for i in range(height):
        for j in range(width):
            final[i][j]=input[i][j] if binarised[i][j]==255 else [0, 0, 0]
    cv.imshow('woo', final)
    cv.waitKey()
