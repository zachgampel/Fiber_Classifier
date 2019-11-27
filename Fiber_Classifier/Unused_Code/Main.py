# from Classifier.Classifier import makePrediction
from Data_Manipulation.Image_Splitter.Image_Splitter import imageSplitter
from Data_Manipulation.Write_To_Excel.Write_To_Excel import toggleFeaturesAndParameters


def main():
    folder = 'Test Classification Image\\'
    # imageSplitter(source, mask_minimum_percent=0.05, mask_maximum_percent=0.35)
    toggleFeaturesAndParameters([folder], ['Sheet 1'], excel_name='Test New Normalized.xls', toggle_roughness=True, toggle_roughness2=True,
                                toggle_roughness_scaled=False, toggled_roughness2_scaled=False, toggle_opacity_and_colors=True,
                                toggle_corners=True, toggle_thickness=True, mode='Classification')
    # makePrediction('Classifiers\\model50.h5', 'Test.xls')


if __name__ == '__main__':
    main()
