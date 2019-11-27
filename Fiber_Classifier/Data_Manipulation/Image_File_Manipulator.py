import os
import cv2
from shutil import rmtree, copy, copytree
from Extractors.Masking_Functions import createMaskFromGreenImage
from Utils import getFileExtension, straightenArray, printMessage, getFileName
import time


# returns the directory of all image files in the root_directory
def getAllFilePaths(root_directory='Fiber Images\\'):
    file_paths = []  # each entry contains the file path of the corresponding image
    for root, subdir, files in os.walk(root_directory):
        for file in files:
            directory = root + '\\' + file
            file_paths.append(directory)
    return file_paths


# returns a list of paths that lead to main images and a list of paths that lead to masks
def organizePaths(all_file_paths):
    masking_paths, image_paths, background_paths = [], [], []

    for file_path in all_file_paths:
        if 'Mask' in file_path:
            masking_paths.append(file_path)
        if 'Background' in file_path:
            background_paths.append(file_path)
        if 'Input' not in file_path and 'Mask' not in file_path and 'Background' not in file_path:
            image_paths.append(file_path)

    return image_paths, masking_paths, background_paths


# Get the file path, image, its mask (optional), and background (optional)
# Missing masks and backgrounds are represented with a string
def getNamesImagesMasksBackgrounds(root_directory='Fiber Images\\'):
    printMessage('Retrieving files...')

    all_file_paths = getAllFilePaths(root_directory)
    image_paths, masking_paths, background_paths = organizePaths(all_file_paths)
    # split each path into a list, each element is a source/subfolder and the last element is the file

    for i in range(len(image_paths)):
        image_paths[i] = image_paths[i].split('\\')
    for i in range(len(masking_paths)):
        masking_paths[i] = masking_paths[i].split('\\')
    for i in range(len(background_paths)):
        background_paths[i] = background_paths[i].split('\\')

    images, masks, image_names, backgrounds = [], [], [], []
    remaining_images = list.copy(image_paths)

    for image_path in image_paths:
        match_found = False
        for masking_path in masking_paths:
            if masking_path[len(masking_path) - 2] == image_path[len(image_path) - 2]:
                images.append(cv2.imread('\\'.join(image_path)))
                masks.append(createMaskFromGreenImage(cv2.imread('\\'.join(masking_path))))
                image_names.append(masking_path)
                print(masking_path)
                match_found = True
        if match_found:
            remaining_images.remove(image_path)

    for unmasked_image in remaining_images:
        images.append(cv2.imread('\\'.join(unmasked_image)))
        masks.append('no mask')
        image_names.append(unmasked_image)
        print(unmasked_image)

    for image_name in image_names:
        match_found = False
        for background in background_paths:
            if background[len(background) - 2] == image_name[len(image_name) - 2]:
                match_found = True
                backgrounds.append(createMaskFromGreenImage(cv2.imread('\\'.join(background))))
        if not match_found:
            backgrounds.append('no background')

    image_names = straightenArray(image_names)
    return image_names, images, masks, backgrounds


def getNamesImagesMasksBackgroundsDirectories(root_directory):
    printMessage('Retrieving files...')

    all_file_paths = getAllFilePaths(root_directory)
    image_paths, masking_paths, background_paths = organizePaths(all_file_paths)
    # split each path into a list, each element is a source/subfolder and the last element is the file

    for i in range(len(image_paths)):
        image_paths[i] = image_paths[i].split('\\')
    for i in range(len(masking_paths)):
        masking_paths[i] = masking_paths[i].split('\\')
    for i in range(len(background_paths)):
        background_paths[i] = background_paths[i].split('\\')

    name_directories, image_directories, mask_directories, background_directories = [], [], [], []
    remaining_images = list.copy(image_paths)

    for image_path in image_paths:
        match_found = False
        for masking_path in masking_paths:
            if masking_path[len(masking_path) - 2] == image_path[len(image_path) - 2]:
                image_directories.append('\\'.join(image_path))
                mask_directories.append('\\'.join(masking_path))
                name_directories.append(masking_path)
                print(masking_path)
                match_found = True
        if match_found:
            remaining_images.remove(image_path)

    for unmasked_image in remaining_images:
        image_directories.append('\\'.join(unmasked_image))
        mask_directories.append('no mask')
        name_directories.append(unmasked_image)
        print(unmasked_image)

    for image_name in name_directories:
        match_found = False
        for background in background_paths:
            if background[len(background) - 2] == image_name[len(image_name) - 2]:
                match_found = True
                background_directories.append('\\'.join(background))
        if not match_found:
            background_directories.append('no background')

    name_directories = straightenArray(name_directories)
    return name_directories, image_directories, mask_directories, background_directories


# Fetch all images and their corresponding name/file path
def getImagesAndNames(root_directory):
    printMessage('Retrieving images...')
    images = []  # each entry contains an image
    names = []  # each entry contains the file path of the corresponding image
    for root, subdir, files in os.walk(root_directory):
        for file in files:
            directory = root + '\\' + file
            images.append(cv2.imread(directory))
            names.append(directory)
            print(directory)

    return images, names


def getImageDirectories(root_directory):
    printMessage('Retrieving images...')
    directories = []
    for root, subdir, files in os.walk(root_directory):
        for file in files:
            directory = root + '\\' + file
            print(directory)
            directories.append(directory)
    return directories


# rename all files in the directory based on their parent directory
def renameFiles(root_directory):
    printMessage('Renaming files...')
    all_file_paths = getAllFilePaths(root_directory)
    image_paths, masking_paths, background_paths = organizePaths(all_file_paths)

    a = 0
    for i in range(len(image_paths)):
        if i > 0:
            if image_paths[i].split('\\')[-2] != image_paths[i - 1].split('\\')[-2]:
                a = 0
        new_name = image_paths[i].split('\\')
        new_name[-1] = new_name[-2] + ' ' + str(a) + getFileExtension(new_name)
        new_name = '\\'.join(new_name)
        print(new_name)
        a += 1
        os.rename(image_paths[i], new_name)
    return


# remove directories that are missing masks
def removeMasklessDirectories(directory):
    for root, subdir, files in os.walk(directory):
        found_mask = False
        for file in files:
            if 'Mask' in file:
                found_mask = True
        if not found_mask and len(files) > 0:
            print(root)
            rmtree(root)


# overwrite images in ultra-hd resolution
def updateImageSize(directories):
    printMessage('Resizing images...')
    for directory in directories:
        image = cv2.imread(directory)
        print(directory)
        if image.shape[0] * image.shape[1] != 3492 * 4656:
            if image.shape[0] > image.shape[1]:
                pair = (3492, 4656)
            else:
                pair = (4656, 3492)

            image_scaled = cv2.resize(image, pair)
            os.remove(directory)
            cv2.imwrite(directory, image_scaled)


# remove masks that are too small or large
def removeSmallAndLargeMasks(images, names, lower_bound, upper_bound):
    printMessage('Removing small and large masks...')
    for image, name in zip(images, names):
        if 'Mask' in name:
            image = createMaskFromGreenImage(cv2.resize(image, (100, 100)))
            mask_percentage = cv2.countNonZero(image)/(image.shape[0]*image.shape[1])

            if upper_bound < mask_percentage or mask_percentage < lower_bound:
                print('Removing ' + name)
                os.remove(name)


# print the size of the masks
def getMaskSizes(images, names):
    for image, name in zip(images, names):
        percentages = []
        if 'Mask' in name:
            image = createMaskFromGreenImage(cv2.resize(image, (100, 100)))
            percentage = cv2.countNonZero(image) / (image.shape[0] * image.shape[1])
            if percentage < -1 or percentage > 0.35:
                print(str(percentage) + '\t' + name)
            percentages.append(percentage)

    print(len(percentages))


# Move each image into its own subfolder
def makeSubfolders(directories):
    printMessage('Putting images in subfolders...')
    for directory in directories:
        if os.path.exists(getFileName(directory)):
            print('Path exists')
        else:
            os.mkdir(getFileName(directory))
            temp = directory.split('\\')
            temp.append(temp[len(temp) - 1])
            temp[len(temp) - 2] = getFileName(temp)
            temp = '\\'.join(temp)
            print(temp)

            cv2.imwrite(temp, cv2.imread(directory))
            os.remove(directory)


# Copy the input image to the 'Results' directory
def copyDataOver(source):
    # first clear out the source
    destination = '\\'.join(os.getcwd().split('\\') + ['Results'])

    for filename in os.listdir(destination):
        file_path = os.path.join(destination, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # next copy in the contents of the source selected
    if os.path.isfile(source):
        copy(source, destination)
    if os.path.isdir(source):
        rmtree(destination)
        copytree(source, destination)

    return destination


def backupResults(starting_file_name):
    results_location = '\\'.join(os.getcwd().split('\\') + ['Results'])
    destination = '\\'.join(os.getcwd().split('\\') + ['Old Results', str(time.strftime("%Y-%m-%d %H,%M,%S", time.gmtime())) + ' ' + starting_file_name])

    # print(destination)
    # print(results_location)

    copytree(results_location, destination)
    return


if __name__ == '__main__':
    pass
