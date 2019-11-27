# This chunk of code adds the parent directory to the system path so we can use those modules
import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import cv2
from Utils import imshow
from Extractors.Masking_Functions import createMaskFromGreenImage

if __name__ == '__main__':
    img = cv2.imread('Test Folder\\Animal Fibers\\Rabbit\Rabbit_05\\mask.jpg')
    img2 = cv2.imread('Test Folder\\Animal Fibers\\Rabbit\Rabbit_05\\Rabbit_05.jpg')
    # imshow(image)
    print(img)
    mask = createMaskFromGreenImage(img)
    # imshow(image)
    # imshow(mask)
    img = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.bitwise_and(img, img, mask=mask)
    imshow(img2)
    cv2.imwrite('User Mask.jpg', mask)
