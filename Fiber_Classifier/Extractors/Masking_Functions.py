import cv2
import numpy as np

from Utils import imshow


def createMaskFromGreenImage(img):
    mask = np.zeros(img.shape, np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            a, b, c = img[i][j]
            if 50 < a < 90 and 150 < b < 190 and 15 < c < 55:
                mask[i][j] = 255

    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    return mask


# Paint a green mask on top of the image
def greenifyImage(image, mask):
    green_image = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mask[i, j] == 255:
                green_image[i, j] = (70, 170, 35)
    return green_image


# creates the mask based on the roughness_image. Called from getMask in Roughness_Extractor
def createMasks(roughness_image):
    _, thresh = cv2.threshold(roughness_image, 20, 255, cv2.THRESH_BINARY)

    thresh_blurred = cv2.medianBlur(thresh, 9)
    _, final_mask_colored = cv2.threshold(thresh_blurred, 100, 255, cv2.THRESH_BINARY)
    final_mask = cv2.cvtColor(final_mask_colored, cv2.COLOR_BGR2GRAY)
    final_mask = cv2.resize(final_mask, dsize=(450, 338), interpolation=cv2.INTER_CUBIC)
    _, final_mask = cv2.threshold(final_mask, 200, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(final_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return final_mask, contours


if __name__ == '__main__':
    img = cv2.imread('Tests\\Test Folder\\Animal Fibers\\Rabbit\Rabbit_05\\mask.jpg')
    img2 = cv2.imread('Tests\\Test Folder\\Animal Fibers\\Rabbit\Rabbit_05\\Rabbit_05.jpg')
    mask = createMaskFromGreenImage(img)
    # imshow(image)
    # imshow(mask)
    img = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img2 = cv2.bitwise_and(img, img, mask=mask)
    imshow(img2)
    cv2.imwrite('Images//User Mask.jpg', mask)
