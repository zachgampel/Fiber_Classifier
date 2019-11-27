import numpy as np
import cv2


def getOpacityAndColor(img, mask, background):
    if type(background) == str:
        background = cv2.bitwise_not(mask)

    row, col = img.shape[0], img.shape[1]

    blue_background = [0]
    green_background = [0]
    red_background = [0]

    blue_fiber = [0]
    second_color_fiber = [0]
    third_color_fiber = [0]

    # a value of 255 signifies the part of the picture being shown
    # a value of 0 signifies a pixel that is not shown
    for i in range(row):
        for j in range(col):
            if background[i][j] != 0:  # background
                blue_background.append(img[i][j][0])
                green_background.append(img[i][j][1])
                red_background.append(img[i][j][2])
            if mask[i][j] != 0:
                blue_fiber.append(img[i][j][0])
                second_color_fiber.append(img[i][j][1])
                third_color_fiber.append(img[i][j][2])

    average_blue_background = sum(blue_background) / len(blue_background)
    average_green_background = sum(green_background) / len(green_background)
    average_red_background = sum(red_background) / len(red_background)

    average_blue_fiber = sum(blue_fiber) / len(blue_fiber)
    average_green_fiber = sum(second_color_fiber) / len(second_color_fiber)
    average_red_fiber = sum(third_color_fiber) / len(third_color_fiber)

    opacity = np.abs(average_blue_background - average_blue_fiber) + np.abs(
        average_green_background - average_green_fiber) + np.abs(average_red_background - average_red_fiber)
    return opacity, average_blue_fiber, average_green_fiber, average_red_fiber
