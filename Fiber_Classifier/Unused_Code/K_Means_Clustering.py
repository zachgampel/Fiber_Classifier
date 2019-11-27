import numpy as np
import cv2

def getKMeansImage(img, K=4):
    img = cv2.imread('northernLights.png')
    Z = img.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    return res.reshape((img.shape)),center
    

def maskMostCommonColor(img,mask, K=8):
    kMeansImage,center = getKMeansImage(img, K)
    
    pixels = []
    for i in range(kMeansImage.shape[0]):
        for j in range(kMeansImage.shape[1]):
            pixels.append(kMeansImage[i][j])
    
    pixelCount = []
    for color in center:
        counter = 0
        for pixel in pixels:
            if pixel[0]==color[0] and pixel[1]==color[1] and pixel[2]==color[2]:
                counter = counter+1
        colorFrequency = [counter, pixel]
        pixelCount.append(colorFrequency)
    
    #get the most common color
    top = 0
    color = []
    for i in range(len(pixelCount)):
        if pixelCount[i][0] > top:
            top = pixelCount[i][0]
            color = pixelCount[i][1]


    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            pixel = kMeansImage[i][j]
            if pixel[0]==color[0] and pixel[1]==color[1] and pixel[2]==color[2]:
                mask[i][j] = 0
    
    return mask









    



