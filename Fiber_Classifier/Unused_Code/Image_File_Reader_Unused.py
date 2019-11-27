# This function gets the name, image, and mask for each appropriate image. If
# no user-made mask is available, it makes its own mask using roughness_image
import os

import cv2

from Extractors.Masking_Functions import createMaskFromGreenImage
from Extractors.Roughness_Extractor import getRoughnessValue
from Unused_Code.Focus_Stack import stackHDRs


def runMaskOnAllFiles(root_directory='Images\\Fiber Images\\'):
    masking_directories = []
    image_directories = []
    for root, subdir, files in os.walk(root_directory):
        for file in files:
            directory = root + '\\' + file
            split_directory = directory.split('\\')
            if 'Mask' in directory:
                masking_directories.append(split_directory)
            if 'Input' not in directory and 'Mask' not in directory:
                image_directories.append(split_directory)

    images = []
    masks = []
    for image_directory in image_directories:
        images.append(cv2.imread('\\'.join(image_directory)))
        keyword = image_directory[len(image_directory) - 2]
        mask = []
        roughness_images = []

        for mask_directory in masking_directories:
            if keyword == mask_directory[len(image_directory) - 2]:
                mask.append('\\'.join(mask_directory))

        roughness_image, roughness_value = getRoughnessValue(cv2.imread('\\'.join(image_directory)), 'no mask')
        if len(mask) == 1:
            mask = createMaskFromGreenImage(cv2.imread(mask[0]))

        masks.append(mask)
        roughness_images.append(roughness_image)

    return images, masks, roughness_images


# This function looks through files and combines pictures under the source 'Input'
# into a new image called 'merged.png'.
def focus_stack_all_images(root_directory):
    images = []  # each entry contains an image
    names = []  # each entry contains the file path of the corresponding image
    focus_stacking_images = []

    for root, subdir, files in os.walk(root_directory):
        for file in files:
            directory = root + '\\' + file
            names.append(directory)
            cv2.imread(directory)
            split_name = directory.split('\\')
            if split_name[len(split_name) - 2] == 'Input':
                split_name = split_name[0:len(split_name) - 2]
                focus_stacking_images.append(['\\'.join(split_name), cv2.imread(directory)])

    unique_list = []
    for row in focus_stacking_images:
        if row[0] not in unique_list:
            unique_list.append(row[0])

    for image_location in unique_list:
        focus_images = []

        for row in focus_stacking_images:
            if row[0] == image_location:
                focus_images.append(row[1])
        stackHDRs(focus_images, image_location)

    return images, names