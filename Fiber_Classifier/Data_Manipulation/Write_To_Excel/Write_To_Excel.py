import time

import cv2
from xlwt import Workbook

from Data_Manipulation.Image_File_Manipulator import getNamesImagesMasksBackgroundsDirectories
from Extractors.Corner_Extractor import getNumberOfCorners
from Extractors.Masking_Functions import createMaskFromGreenImage
from Extractors.Opacity_Extractor import getOpacityAndColor
from Extractors.Roughness_Extractor import getRoughnessValues, getRoughnessValues2
from Extractors.Thickness_Extractor import getThickness
from Utils import combineData, printMessage


# Run runExtractors for variable parameters, and then save the results in excel using writeResultsToExcel
# Parameters and functions to be called are selected here
def toggleFeaturesAndParameters(image_directories, sheet_names, excel_name, toggle_roughness, toggle_roughness2, toggle_roughness_scaled,
                                toggled_roughness2_scaled,
                                toggle_opacity_and_colors, toggle_corners, toggle_thickness, mode):
    sheets = []
    for directory, sheet_name in zip(image_directories, sheet_names):
        sheet = [runExtractors(directory, toggle_roughness, toggle_roughness2, toggle_roughness_scaled,
                               toggled_roughness2_scaled, toggle_opacity_and_colors, toggle_corners,
                               toggle_thickness, mode), sheet_name]
        sheets.append(sheet)

    title = ['Name'] + [''] * 5 + ['Roughness_Overflow', 'Roughness_Absolute', 'Roughness_Square', 'Roughness_Overflow_Overflow',
                                   'Roughness_Overflow_Absolute',
                                   'Roughness_Overflow_Square', 'Roughness_Absolute_Overflow', 'Roughness_Absolute_Absolute',
                                   'Roughness_Absolute_Square',
                                   'Roughness_Square_Overflow', 'Roughness_Square_Absolute', 'Roughness_Square_Square', 'Scaled_Roughness_Overflow',
                                   'Scaled_Roughness_Absolute', 'Scaled_Roughness_Square', 'Scaled_Roughness_Overflow_Overflow',
                                   'Scaled_Roughness_Overflow_Absolute',
                                   'Scaled_Roughness_Overflow_Square', 'Scaled_Roughness_Absolute_Overflow', 'Scaled_Roughness_Absolute_Absolute',
                                   'Scaled_Roughness_Absolute_Square', 'Scaled_Roughness_Square_Overflow', 'Scaled_Roughness_Square_Absolute',
                                   'Scaled_Roughness_Square_Square', 'Opacity',
                                   'Blue', 'Green', 'Red', 'Corner Count', 'Corner Proportion', 'Horizontal Thickness', 'Vertical Thickness',
                                   'Average Thickness', 'Calculation Time', 'Mask Area']
    writeResultsToExcel(title, sheets, excel_name, mode)


# Extract all desired features from all images with all corresponding masks
def runExtractors(folder_directory, toggle_roughness, toggle_roughness2, toggle_roughness_scaled,
                  toggled_roughness2_scaled, toggle_opacity_and_colors, toggle_corners, toggle_thickness, mode):
    name_directories, image_directories, mask_directories, background_directories = getNamesImagesMasksBackgroundsDirectories(folder_directory)
    t_start = time.time()
    period_time = time.time()

    roughness_overflow_absolute_square_list = [['', '', '']] * len(name_directories)
    roughness2_list = [['', '', '', '', '', '', '', '', '']] * len(name_directories)
    scaled_roughness_overflow_absolute_square_list = [['', '', '']] * len(name_directories)
    scaled_roughness2_list = [['', '', '', '', '', '', '', '', '']] * len(name_directories)

    opacity_blue_green_red_list = [['', '', '', '']] * len(name_directories)
    corner_count_corner_proportion_list = [['', '']] * len(name_directories)
    horizontal_vertical_average_thickness = [['', '', '']] * len(name_directories)

    times = []
    areas = []

    printMessage('Processing excel_file in ' + folder_directory)
    for i in range(len(name_directories)):
        image = cv2.imread(image_directories[i])
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_downscaled_and_gray = cv2.resize(img_gray, (225, 171))
        mask = createMaskFromGreenImage(cv2.imread(mask_directories[i]))
        background = createMaskFromGreenImage(cv2.imread(background_directories[i]))

        # Get the roughness value and image for each setting (overflow, absolute value, squaring)
        if toggle_roughness:
            roughness_values_list, roughness_images_list = getRoughnessValues(img_gray, 1, ['overflow', 'absolute_value', 'squaring'], mask)
            roughness_overflow_absolute_square_list[i] = roughness_values_list

        # Pass the roughness function to the results of the roughness function
        if toggle_roughness and toggle_roughness2:
            roughness2_list[i] = getRoughnessValues2(roughness_images_list, 1, ['overflow', 'absolute_value', 'squaring'], mask)

        # Get the roughness of the downscaled images
        if toggle_roughness_scaled:
            scaled_roughness_values_list, scaled_roughness_images_list = getRoughnessValues(img_downscaled_and_gray, 1,
                                                                                            ['overflow', 'absolute_value', 'squaring'], mask)
            scaled_roughness_overflow_absolute_square_list[i] = scaled_roughness_values_list

        # Pass roughness images from downscaled images through roughness image extractor again
        if toggle_roughness_scaled and toggled_roughness2_scaled:
            scaled_roughness2_list[i] = getRoughnessValues2(scaled_roughness_images_list, 1, ['overflow', 'absolute_value', 'squaring'], mask)

        if toggle_opacity_and_colors:
            opacity_blue_green_red_list[i] = list(getOpacityAndColor(image, mask, background))

        if toggle_corners:
            corner_count_corner_proportion_list[i] = list(getNumberOfCorners(image, mask))

        if toggle_thickness:
            horizontal_vertical_average_thickness[i] = list(getThickness(mask))

        flat = list(mask.flatten())
        areas.append(flat.count(255))

        times.append(time.time() - period_time)
        remaining_time = sum(times) / len(times) * (len(name_directories) - i - 1)
        print('Elapsed Time: ' + str(time.time() - t_start) + '\t(' + str(i + 1) + '/' + str(len(name_directories)) + ')\tRemaining Time:\t' + str(
            remaining_time))

        period_time = time.time()

    # When making a classification, some info should be kept out of the csv file
    if mode == 'Classification':
        return combineData(roughness_overflow_absolute_square_list, roughness2_list, opacity_blue_green_red_list, corner_count_corner_proportion_list,
                           horizontal_vertical_average_thickness)

    return combineData(name_directories, roughness_overflow_absolute_square_list, roughness2_list, scaled_roughness_overflow_absolute_square_list,
                       scaled_roughness2_list, opacity_blue_green_red_list, corner_count_corner_proportion_list,
                       horizontal_vertical_average_thickness, times, areas)


# Write all results to excel
# Results are stored in a list, each element contains the excel_file that will be written to one sheet
def writeResultsToExcel(titles, sheets, file_name, mode):
    # Workbook is created
    wb = Workbook()

    for sheet in sheets:
        excel_sheet = wb.add_sheet(sheet[1])

        if mode != 'Classification':
            for i in range(0, len(titles)):
                excel_sheet.write(0, i, titles[i])
            row = 1
        else:
            row = 0

        for rowEntry in sheet[0]:
            for i in range(0, len(rowEntry)):
                excel_sheet.write(row, i, rowEntry[i])
            row += 1

    wb.save(file_name)


if __name__ == '__main__':
    image_directories = ['Processed Images\\']
    sheet_names = ['Sheet 1']
    toggleFeaturesAndParameters(image_directories, sheet_names, excel_name='Updated Roughness.xls', toggle_roughness=True, toggle_roughness2=True,
                                toggle_roughness_scaled=True, toggled_roughness2_scaled=True, toggle_opacity_and_colors=True,
                                toggle_corners=True, toggle_thickness=True, mode='Not Classification')
