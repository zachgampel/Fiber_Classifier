import cv2
import numpy as np


def getNumberOfCorners(img, mask):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    dst = cv2.dilate(dst, None)
    ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    
    number_of_corners = 0
    for centroid in centroids:
        centroid = np.uint8(centroid)
        if mask[round(centroid[0]), round(centroid[1])] != 0:
            number_of_corners += 1
    
    nonzero_pixels = np.count_nonzero(mask)
    
    proportion_of_corners = number_of_corners/(1+nonzero_pixels)
    return number_of_corners, proportion_of_corners
