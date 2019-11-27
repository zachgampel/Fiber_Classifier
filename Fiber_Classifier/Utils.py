import cv2
import os


# quick way to show an image in another window
def imshow(image, title='Image'):
    cv2.imshow(title, image)
    cv2.waitKey()


# This decomposes the file's directory into its subcomponents
# Ex:
#    file_name='Fiber Images\Plant Fibers\Rattlesnake Master\RattlesnakeMaster_01.jpg'
#    breakDown(file_name) --> ['Plant Fibers', 'Rattlesnake Master', 'RattlesnakeMaster_01.jpg']
def combineData(*argv):
    combined_data = []

    for i in range(0, len(argv[0])):
        row = []
        for arg in argv:
            if type(arg[i]) is list:
                for element in arg[i]:
                    row.append(element)
            else:
                row.append(arg[i])
        combined_data.append(row)

    return combined_data


# This converts a list of colored images to grayscale images
def imageListToGray(images):
    images_gray = []
    for img in images:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        images_gray.append(img_gray)

    return images_gray


# Downscale the images in the list to the size of the pair given
def resizeImages(images, pair=(225, 171)):
    images_downscaled = []
    for image in images:
        images_downscaled.append(cv2.resize(image, pair))

    return images_downscaled


# Return the file name without the file extension
def getFileName(file, index=0):
    if type(file) == list:
        return os.path.splitext(file[-1])[index]
    if type(file) == str:
        return os.path.splitext(file)[index]


def getFileExtension(file):
    return getFileName(file, 1)


def printMessage(message):
    print('=========================================================')
    print(message)
    print('=========================================================')


# makes the array square by filling in the right side of the array with blanks
def straightenArray(name_list):
    length = 0
    for row in name_list:
        if len(row) > length:
            length = len(row)

    straight_array = []
    for row in name_list:
        temp = []
        for i in range(0, length):
            temp.append([])
        straight_array.append(temp)

    i = 0
    for row in name_list:
        j = 0
        for element in row:
            straight_array[i][j] = element
            j += 1
        i += 1

    return straight_array
