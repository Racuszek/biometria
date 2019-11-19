import cv2 as cv
import numpy as np
# All images have been cropped in order to remove discolorations.
fingerprints=['odcisk1.jpg', 'odcisk2.jpg', 'odcisk3.jpg', 'odcisk4.jpg']
testarray=['raise.png']
with open('minutiae.txt', 'w+') as file:
    pass

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

    # cv.thinning(img, img2)
    # cv.imshow(img2)
    img=cv.bitwise_not(img)
    # cv.waitKey()
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
    blank_image = np.zeros((height, width), np.uint8)

    final_image=cv.bitwise_not(blank_image)
    for i in range(border, height-border):
        for j in range(border, width-border):
            final_image[i][j]=imagem[i][j]
    # cv.imshow("skel", final_image)
    # cv.waitKey()

    inner_size=5
    outer_size=9
    minutiae=[]
    inner_border=inner_size/2
    outer_border=outer_size/2

    for i in range(border, height-border):
        for j in range(border, width-border):
            inner_counter=0
            outer_counter=0
            for k in range(-inner_border, inner_border+1):
                for l in range(-inner_border, inner_border+1):
                    if (final_image[i+k][j+l]==0) and (k==-2 or k==2 or l==-2 or l==2):
                        inner_counter=inner_counter+1
            for k in range(-outer_border, outer_border+1):
                for l in range(-outer_border, outer_border+1):
                    if (final_image[i+k][j+l]==0) and (k==-2 or k==2 or l==-2 or l==2):
                        outer_counter=outer_counter+1
            if outer_counter==3 and inner_counter==3:
                minutiae.append((i,j))
                if i<height-border-20:
                    i=i+20
                if j<width-border-20:
                    j=j+20
    with open('minutiae.txt', 'a+') as file:
        file.write(str(minutiae))
        file.write('\n\n')
        print(len(minutiae))




    #outer circle loop
    # for i in range(border, height-border):
    #     for j in range(border, width-border):
    #         outer_counter=0
    #         inner_counter=0
            # for k in range(-2, 3):
            #     for l in range(-2, 3):
            #         if final_image[i+k][j+l]==255 and (k==-2 or k==2 or l==-2 or l==2):
            #             inner_counter=inner_counter+1
            # for k in range(-4, 5):
            #     for l in range(-4, 5):
            #         if final_image[i+k][j+l]==255 and (k==-4 or k==4 or l==-4 or l==4):
            #             outer_counter=outer_counter+1
            # if inner_counter==3 and outer_counter==3:
            #     minutiae.append((i, j))
    # print(minutiae)


# cv.imshow('bin', threshold)
# cv.waitKey()