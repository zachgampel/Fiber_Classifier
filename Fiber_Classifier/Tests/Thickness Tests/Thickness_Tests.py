# This chunk of code adds the parent directory to the system path so we can use those modules
import os, sys, inspect
import cv2
import numpy as np

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Extractors.Masking_Functions import createMaskFromGreenImage
from Extractors.Thickness_Extractor import getThickness, getSides


def showEdges(mask, left_pixels, right_pixels):
    rgb = cv2.cvtColor(np.zeros(mask.shape, np.uint8), cv2.COLOR_GRAY2RGB)

    for l in left_pixels:
        rgb[l[0], l[1]] = (255, 255, 0)  # blue
    for r in right_pixels:
        rgb[r[0], r[1]] = (0, 255, 255)  # yellow

    return rgb


if __name__ == '__main__':
    mask = cv2.imread('mask.jpg')
    mask = createMaskFromGreenImage(mask)
    left_x, left_y, right_x, right_y, top_x, top_y, bottom_x, bottom_y = getSides(mask)

    left_pixels, right_pixels = [], []
    for i in range(len(left_x)):
        temp = [left_y[i], left_x[i]]
        left_pixels.append(temp)
    for i in range(len(right_x)):
        temp = [right_y[i], right_x[i]]
        right_pixels.append(temp)

    cv2.imwrite('Edges.png', showEdges(mask, left_pixels, right_pixels))
    left_right_distance, top_bottom_distance, thickness = getThickness(mask)
    print(getThickness(mask))
