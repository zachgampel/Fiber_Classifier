import os
import shutil
import time
import cv2
import numpy as np

from Data_Manipulation.Image_File_Manipulator import renameFiles, getImagesAndNames, removeMasklessDirectories, updateImageSize, makeSubfolders, \
    getMaskSizes, removeSmallAndLargeMasks, getImageDirectories
from Data_Manipulation.Write_To_Excel.Write_To_Excel import toggleFeaturesAndParameters
from Extractors.Masking_Functions import greenifyImage, createMaskFromGreenImage
from Extractors.Roughness_Extractor import getMasks
from Utils import getFileName, getFileExtension, resizeImages, printMessage


# Split each image into manageable chunks and save the results
def splitImages(directories, delete_originals=True):
    printMessage('Splitting images...')
    width = 450
    height = 338

    for directory in directories:
        image = cv2.imread(directory)
        for i in range(10):
            for j in range(10):
                if (height * (i + 1)) <= image.shape[0] and (width * (j + 1)) <= image.shape[1]:
                    cv2.imwrite(
                        getFileName(directory) + ' i=' + str(i) + ', j= ' + str(j) + getFileExtension(directory),
                        image[height * i:height * (i + 1), width * j:width * (j + 1)])
                    print(getFileName(directory) + ' i=' + str(i) + ', j= ' + str(j) + getFileExtension(directory))
        if delete_originals:
            os.remove(directory)
    return


# Delete black images
def removeBlackImages(directories, percent):
    printMessage('Removing all-black images...')
    for directory in directories:
        print(directory)
        image = cv2.resize(cv2.imread(directory), (50, 50))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, th1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        th1 = list(th1.flatten())

        # remove if over x% is black
        if th1.count(0) > percent * len(th1):
            os.remove(directory)
    return


def removeBadMasks(directories, lower_percent, upper_percent):
    printMessage('Removing all badly-masked images...')
    for directory in directories:
        image = cv2.imread(directory)
        if 'Background' in directory:
            image = createMaskFromGreenImage(cv2.resize(image, (100, 100)))
            flat = list(image.flatten())
            if flat.count(0) < lower_percent * len(flat) or flat.count(0) > upper_percent * len(flat):
                print(directory)
                parent_folder = directory.split('\\')
                parent_folder.pop(-1)
                parent_folder = '\\'.join(parent_folder)
                shutil.rmtree(parent_folder)
    return


# create a mask if the potential mask is larger than mask_percent
def makeMasksAndBackgrounds(directories, mask_minimum_percent):
    printMessage('Creating masks and backgrounds...')
    counter = 0
    count = len(directories)
    for directory in directories:
        image = cv2.imread(directory)
        counter += 1
        print(directory + ' (' + str(counter) + '/' + str(count) + ')')
        backup_image = image.copy()

        directory = directory.split('\\')
        extension = getFileExtension(directory[-1])
        last_name = directory.pop(-1)
        last_name = getFileName(last_name)
        directory.append(last_name)
        directory = '\\'.join(directory)

        final_mask, contours = getMasks(image)

        for i in range(len(contours)):
            contour = contours[i]
            if cv2.contourArea(contour) / (backup_image.shape[0] * backup_image.shape[1]) > mask_minimum_percent:
                mask = np.zeros(image.shape, np.uint8)
                mask = cv2.fillPoly(mask, pts=[contour], color=(255, 255, 255))

                green_image = image.copy()
                for a in range(image.shape[0]):
                    for j in range(image.shape[1]):
                        if mask[a, j][0] == 255 and mask[a, j][1] == 255 and mask[a, j][2] == 255:
                            green_image[a, j] = (70, 170, 35)

                cv2.imwrite(directory + ' Mask ' + str(i) + extension, green_image)

        green_background = greenifyImage(backup_image, cv2.bitwise_not(final_mask))
        cv2.imwrite(directory + ' Background' + extension, green_background)
    return

"""
    splitImages is the central function for splitting images. Steps are:
        1) Rename files based on their parent source
        2) Rescale images to ultra-hd resolution
        3) Split the images into smaller pieces
        4) Remove images that are mostly black
        5) Move all images into their own subdirectories
        6) Create masks and backgrounds for each image according to the parameter mask_percent
        7) Remove directories without masks
        8) (Optional) Remove small masks
"""


def imageSplitter(folder, mask_minimum_percent, mask_maximum_percent):
    t_start = time.time()

    renameFiles(folder)

    directories = getImageDirectories(folder)
    updateImageSize(directories)

    directories = getImageDirectories(folder)
    splitImages(directories)

    directories = getImageDirectories(folder)
    removeBlackImages(directories, 0.025)

    directories = getImageDirectories(folder)
    makeSubfolders(directories)

    directories = getImageDirectories(folder)
    makeMasksAndBackgrounds(directories, mask_minimum_percent)

    directories = getImageDirectories(folder)
    removeBadMasks(directories, mask_minimum_percent, mask_maximum_percent)

    removeMasklessDirectories(folder)

    # images, names = getImagesAndNames(source)
    # removeSmallAndLargeMasks(images, names, 0.10, 0.45)
    # removeMasklessDirectories(source)

    print(str(time.time() - t_start))


if __name__ == '__main__':
    folder = 'Test\\'
    imageSplitter(folder, mask_minimum_percent=0.05, mask_maximum_percent=0.35)

    image_directories = ['Test\\']
    sheet_names = ['Sheet 1']
    toggleFeaturesAndParameters(image_directories, sheet_names, excel_name='Updated Roughness.xls', toggle_roughness=True, toggle_roughness2=True,
                                toggle_roughness_scaled=False, toggled_roughness2_scaled=False, toggle_opacity_and_colors=True,
                                toggle_corners=True, toggle_thickness=True, mode='Not Classification')
