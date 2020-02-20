import os
import eyeD3
import pandas
from keras.layers import Dense
from keras.models import Sequential
from keras.models import load_model
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from Data_Manipulation.Image_File_Manipulator import copyDataOver, backupResults
from Data_Manipulation.Image_Splitter.Image_Splitter import imageSplitter
from Data_Manipulation.Write_To_Excel.Write_To_Excel import toggleFeaturesAndParameters


def buildModel(input_size, output_size):
    model = Sequential()
    model.add(Dense(input_size, input_dim=input_size, activation='relu'))
    model.add(Dense(input_size, activation='relu'))
    model.add(Dense(output_size, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def getTrainingAndTestingData(y_column, input_size, training_file, validation_file):
    training_frame = pandas.read_excel(training_file, header=None)
    training_dataset = training_frame.values
    validation_frame = pandas.read_excel(validation_file, header=None)
    validation_dataset = validation_frame.values

    x_training = training_dataset[:, 5:(5 + input_size)].astype(float)
    x_validation = validation_dataset[:, 5:(5 + input_size)].astype(float)

    sc_x = StandardScaler()
    x_training = sc_x.fit_transform(x_training)

    # for x in x_training:
    #     print(x)

    x_validation = sc_x.fit_transform(x_validation)

    y_training = training_dataset[:, y_column]
    y_validation = validation_dataset[:, y_column]

    encoder = LabelEncoder()
    encoder.fit(y_training)
    encoded_y = encoder.transform(y_training)
    y_training = np_utils.to_categorical(encoded_y)

    encoded_y = encoder.transform(y_validation)
    y_validation = np_utils.to_categorical(encoded_y)

    return x_training, y_training, x_validation, y_validation


def trainModel(batch_size, epochs, y_column, input_size, output_size):
    x_training, y_training, x_validation, y_validation = getTrainingAndTestingData(y_column=y_column, input_size=input_size,
                                                                                   training_file='Classification Data\\Excel Files\\training.xls', validation_file='Classification Data\\Excel Files\\validation.xls')

    model = buildModel(input_size=input_size, output_size=output_size)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_training, y_training, epochs=epochs, batch_size=batch_size, verbose=2, validation_data=(x_validation, y_validation), shuffle=True)

    model_name = 'model' + str(epochs) + '.h5'
    model.save(model_name)


def getModelAccuracy(model_name, y_column, input_size):
    for data in ['Classification Data\\Excel Files\\validation.xls', 'Classification Data\\Excel Files\\training.xls']:
        dataframe = pandas.read_excel(data, header=None)
        dataset = dataframe.values

        sc_x = StandardScaler()
        x = dataset[:, 5:(5 + input_size)].astype(float)
        x = sc_x.fit_transform(x)
        y = dataset[:, y_column]

        encoder = LabelEncoder()
        encoder.fit(y)
        encoded_y = encoder.transform(y)
        dummy_y = np_utils.to_categorical(encoded_y)

        model = load_model(model_name)
        score = model.evaluate(x, dummy_y, verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))

        print(encoder.transform(y))


def mostFrequent(list):
    counter = 0
    num = list[0]

    for i in list:
        curr_frequency = list.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i

    return num


def numberToClassification(num):
    # return ['Alpaca', 'Cotton', 'Flax', 'Nylon', 'Polyster', 'Ramie', 'Rayon', 'Silk', 'Wool'][num]
    return ['Alpaca', 'Cotton', 'Flax', 'Nylon', 'Ramie', 'Rayon', 'Silk', 'Wool'][num]


def makePrediction(model_name, excel_file):
    model = load_model(model_name)

    dataframe = pandas.read_excel(excel_file, header=None)
    num_rows = len(dataframe.index)
    training_data = pandas.read_excel('Classification Data\\Excel Files\\training for making predictions.xls')

    dataframe_list = dataframe.values.tolist()
    training_data_list = training_data.values.tolist()
    for i in range(len(training_data_list)):
        dataframe_list.append(training_data_list[i])
    dataframe = pandas.DataFrame(dataframe_list)

    data = dataframe.values.astype(float)

    scaler = StandardScaler()
    data = scaler.fit_transform(data)

    predictions = model.predict(data)
    final_predictions = []
    for prediction in predictions:
        prediction = list(prediction)
        final_predictions.append(prediction.index(max(prediction)))
    final_predictions = final_predictions[0:num_rows]

    f = open('Results\\Results.txt', 'w+')
    for i in final_predictions:
        f.write(numberToClassification(i))
        f.write('\n')
    f.close()

    return numberToClassification(mostFrequent(final_predictions))


def Main(folder):
    results_directory = '\\'.join(os.getcwd().split('\\') + ['Results'])
    results_directory = copyDataOver(folder)
    imageSplitter(results_directory, mask_minimum_percent=0.05, mask_maximum_percent=0.35)
    toggleFeaturesAndParameters([results_directory], ['Sheet 1'], excel_name=results_directory+'\\Extraction Results.xls', toggle_roughness=True, toggle_roughness2=True,
                                toggle_roughness_scaled=False, toggled_roughness2_scaled=False, toggle_opacity_and_colors=True,
                                toggle_corners=True, toggle_thickness=True, mode='Classification')

    prediction = makePrediction('Classification Data\\model50.h5', results_directory+'\\Extraction Results.xls')
    backupResults(folder)
    return prediction


if __name__ == '__main__':
    folder = 'Rayon.jpg'
    prediction = Main(folder)
    print(prediction)

    # trainModel(batch_size=1, epochs=50, y_column=1, input_size=21 - 2, output_size=8)
    # getModelAccuracy(model_name='model50.h5', y_column=1, input_size=21)
    # makePrediction('Classification Data\\model50.h5', 'Classification Data\\Test Unscaled.xls')
