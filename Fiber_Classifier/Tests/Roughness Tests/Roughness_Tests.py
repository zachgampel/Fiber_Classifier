import cv2

from Data_Manipulation.Image_File_Manipulator import getNamesImagesMasksBackgrounds
from Extractors.Roughness_Extractor import getMasks, getRoughnessImage
from Utils import getFileName, getFileExtension


# create a mask, then save it next to the original image
def maskingDemo(directory):
    names, images, masks, backgrounds = getNamesImagesMasksBackgrounds(directory)

    # remove 'Mask' images so there's no repeats
    names2, images2 = [], []
    for name, image in zip(names, images):
        if 'Mask' not in name[-1]:
            names2.append(name)
            images2.append(image)
    names = names2
    images = images2

    for name, image in zip(names, images):
        extension = getFileExtension(name[-1])
        last_name = name.pop(-1)
        last_name = getFileName(last_name)
        name.append(last_name)
        name = '\\'.join(name) + ' Mask' + extension
        print(name)

        image = cv2.resize(image, dsize=(90, 67), interpolation=cv2.INTER_CUBIC)
        roughness_image = getRoughnessImage(image=image, mode='squaring')
        _, thresh = cv2.threshold(roughness_image, 20, 255, cv2.THRESH_BINARY)
        thresh_blurred = cv2.medianBlur(thresh, 9)
        _, final_mask = cv2.threshold(thresh_blurred, 100, 255, cv2.THRESH_BINARY)
        final_mask = cv2.cvtColor(final_mask, cv2.COLOR_BGR2GRAY)
        final_mask = cv2.resize(final_mask, dsize=(450, 338), interpolation=cv2.INTER_CUBIC)
        _, final_mask = cv2.threshold(final_mask, 200, 255, cv2.THRESH_BINARY)
        cv2.imwrite(name, final_mask)


if __name__ == '__main__':
    image = cv2.imread('1031191137 i=3, j= 3.jpg')
    contours, mask = getMasks(image)
    cv2.imshow('Image', mask)
    cv2.waitKey(0)
