import cv2
import numpy as np

from Extractors.Masking_Functions import createMaskFromGreenImage
from Utils import imshow


def run():
    image = cv2.imread('Test Image.jpg')
    image = createMaskFromGreenImage(image)
    # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    bordersize = 1
    row, col = image.shape[:2]
    image = cv2.copyMakeBorder(image, top=bordersize, bottom=bordersize, left=bordersize,
                               right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])

    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    for contour in contours:
        print(contour)
    cv2.drawContours(image, contours[0], -1, (0, 255, 0), 3)
    cv2.imshow('Contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # params = cv2.SimpleBlobDetector_Params()
    # params.minThreshold = 2
    # params.maxThreshold = 255
    # params.filterByArea = False
    # params.filterByCircularity = False
    #
    # detector = cv2.SimpleBlobDetector_create()
    # keypoints = detector.detect(image)
    #
    # print(len(keypoints))
    #
    # im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #
    # # Show blobs
    # cv2.imshow("Keypoints", im_with_keypoints)
    # cv2.waitKey(0)

if __name__ == '__main__':
    run()
