import os
import json
from sklearn import preprocessing

def getFileData(filePath):
    data = ""
    if os.path.exists(filePath):
        with open(filePath, "r") as text_file:
            data = text_file.read()
    return data

def saveFileData(filePath, content):
    with open(filePath, "w") as text_file:
        text_file.write(content)

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

def updateModelResetCache(name, flag):
    directory = "./data/" + name
    modelfile = directory + "/define.json"
    print(modelfile)

    jsondata = getFileData(modelfile)
    if jsondata == "":
        return
    
    modeljson = json.loads(jsondata)
    modeljson['reset_cache'] = flag
    json_string = json.dumps(modeljson)
    saveFileData(modelfile, json_string)
    
