import os, sys, inspect
import cv2
import math

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from Utils import imshow


# get the average width of the fiber
def getThickness(mask):
    left_x, left_y, right_x, right_y, top_x, top_y, bottom_x, bottom_y = getSides(mask)

    avg_left_x = sum(left_x) / len(left_x)
    avg_left_y = sum(left_y) / len(left_y)
    avg_right_x = sum(right_x) / len(right_x)
    avg_right_y = sum(right_y) / len(right_y)

    avg_top_x = sum(top_x) / len(top_x)
    avg_top_y = sum(top_y) / len(top_y)
    avg_bottom_x = sum(bottom_x) / len(bottom_x)
    avg_bottom_y = sum(bottom_y) / len(bottom_y)

    left_right_distance = math.sqrt((avg_right_x - avg_left_x) ** 2 + (avg_right_y - avg_left_y) ** 2)
    top_bottom_distance = math.sqrt((avg_bottom_x - avg_top_x) ** 2 + (avg_bottom_y - avg_top_y) ** 2)

    return left_right_distance, top_bottom_distance, (left_right_distance + top_bottom_distance) / 2


def getSides(mask):
    left_x, left_y, right_x, right_y, top_x, top_y, bottom_x, bottom_y = [225], [225], [225], [225], [169], [169], [
        169], [169]
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1] - 1):
            if mask[i, j] == 0 and mask[i, j + 1] == 255:
                left_x.append(j)
                left_y.append(i)
            if mask[i, j] == 255 and mask[i, j + 1] == 0:
                right_x.append(j)
                right_y.append(i)

    for i in range(mask.shape[0] - 1):
        for j in range(mask.shape[1]):
            if mask[i, j] == 0 and mask[i + 1, j] == 255:
                top_x.append(j)
                top_y.append(i)
            if mask[i, j] == 255 and mask[i + 1, j] == 0:
                bottom_x.append(j)
                bottom_y.append(i)

    return left_x, left_y, right_x, right_y, top_x, top_y, bottom_x, bottom_y


if __name__ == '__main__':
    mask = cv2.imread('mask_01.jpg')
    imshow(mask)
    left_right_distance, top_bottom_distance, thickness = getThickness(mask)
    print(thickness)
