import os
from sklearn import preprocessing

def getFileData(filePath):
    data = ""
    if os.path.exists(filePath):
        with open(filePath, "r") as text_file:
            data = text_file.read()
    return data

def scaleData(name, data):
    if name == "StandardScaler":
        scaler = preprocessing.StandardScaler().fit(data)
        data = scaler.transform(data)
    elif name == "Binarizer":
        scaler = preprocessing.Binarizer(threshold=0.0).fit(data)
        data = scaler.transform(data)
    elif name == "MinMaxScaler":
        scaler = preprocessing.MinMaxScaler(feature_range=(0, 1)).fit(data)
        data = scaler.transform(data)
    elif name == "Normalizer":
        scaler = preprocessing.Normalizer().fit(data)
        data = scaler.transform(data)
    return data