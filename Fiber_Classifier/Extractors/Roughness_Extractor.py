import numpy as np
import cv2

from Extractors.Masking_Functions import createMasks


# if a mask is specified, then only analyze over that area
def getRoughnessImage(image, mode, mask='no mask', kernel_distance=1):
    roughness_image = np.zeros(image.shape, np.uint8)

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    row, col = image.shape

    for i in range(row):
        for j in range(col):
            if (type(mask) != str and mask[i, j] != 0) or type(mask) == str:
                roughness_list = []
                for a in range(i - kernel_distance, i + kernel_distance + 1):
                    for b in range(j - kernel_distance, j + kernel_distance + 1):
                        if 0 <= a < row and 0 <= b < col:
                            if mode == 'overflow':
                                roughness_list.append(image[i, j] - image[a, b])
                            else:
                                if image[i, j] > image[a, b]:
                                    roughness_list.append(image[i, j] - image[a, b])
                                else:
                                    roughness_list.append(image[a, b] - image[i, j])

                if mode == 'squaring':
                    roughness_list = [i ** 2 for i in roughness_list]

                roughness_image[i][j] = sum(roughness_list) / (len(roughness_list) - 1)

    return roughness_image


# Input must be a grayscale image
# A lower roughness value means a smoother image
def getRoughnessValue(image, mask, mode, kernel_distance=1):
    roughness_image = getRoughnessImage(image, mode, mask=mask, kernel_distance=kernel_distance)
    if type(mask) == str:
        print('Mask is missing!')

    rough_values = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mask[i][j] != 0:
                rough_values.append(roughness_image[i, j])

    if len(rough_values) == 0:
        roughness = 0
    else:
        roughness = sum(rough_values) / len(rough_values)
    return roughness, roughness_image


def getRoughnessValues(image, kernel_distance, modes, mask):
    roughness_values, roughness_images = [], []
    for mode in modes:
        roughness_value, roughness_image = getRoughnessValue(image, mask, mode, kernel_distance)
        roughness_values.append(roughness_value)
        roughness_images.append(roughness_image)
    return roughness_values, roughness_images


def getRoughnessValues2(images, kernel_distance, modes, mask):
    roughness2_values = []
    for image in images:
        for mode in modes:
            roughness_value, _ = getRoughnessValue(image, mask, mode, kernel_distance)
            roughness2_values.append(roughness_value)

    return roughness2_values


# Get the downscaled roughness image, then send it to createMask to get the mask
def getMasks(image):
    image = cv2.resize(image, dsize=(90, 67), interpolation=cv2.INTER_CUBIC)
    roughness_image = getRoughnessImage(image=image, mode='squaring')

    return createMasks(roughness_image)


if __name__ == '__main__':
    image = cv2.imread('0 i=4, j= 6.jpg')
    final_mask, contours = getMasks(image)
    for i in range(len(contours)):
        contour = contours[i]
        if cv2.contourArea(contour) > 10000:
            print(str(cv2.contourArea(contour)))
            mask = np.zeros(image.shape)
            mask = cv2.fillPoly(mask, pts=[contour], color=(255, 255, 255))
            cv2.imwrite('mask' + str(i) + '.png', mask)
