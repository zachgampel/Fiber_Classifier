# normalize the excel_file before it's saved to excel
import pandas


def normalizeData(data):
    means, variances = getMeansVariances()
    print(means)
    print(variances)
    for i in range(len(data)):
        for j in range(21):
            data[i][j] = (data[i][j] - means[j]) / variances[j]
    return data


def getMeansVariances():
    training_frame = pandas.read_excel('Classification Data\\Excel Files\\training.xls', header=None)
    training_dataset = training_frame.values
    x_training = training_dataset[:, 5:(5 + 21)].astype(float)

    scaler = StandardScaler()
    fit = scaler.fit(x_training)
    scaler.fit_transform(x_training, )
    return fit.mean_, fit.var_
