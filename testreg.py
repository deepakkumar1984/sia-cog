import os
import json
import uuid
import keras
import tensorflow
from Interface import SkLearnTask, DLTask
from Interface import utility
def regtest1(name, trainfile):
    directory = "./data/" + name
    modelfile = directory + "/define.json"
    srvfile = directory + "/service.json"
    trainfile = directory + "/dataset/" + trainfile
    srvdata = utility.getFileData(srvfile)
    modeldata = utility.getFileData(modelfile)
    srvjson = json.loads(srvdata)
    modeljson = json.loads(modeldata)
    if modeljson['isneuralnetwork'] == True:
        result = DLTask.Evalute(str(uuid.uuid1()), modeljson, trainfile, directory)
    else:
        result = SkLearnTask.Evalute(modeljson, True, trainfile)
    
    
    print(result)

def regtest2(name, trainfile, testfile):
    directory = "./data/" + name
    modelfile = directory + "/define.json"
    srvfile = directory + "/service.json"
    trainfile = directory + "/dataset/" + trainfile
    testfile = directory + "/dataset/" + testfile
    predictionFile = directory + "/dataset/prediction.csv"
    srvdata = utility.getFileData(srvfile)
    modeldata = utility.getFileData(modelfile)
    srvjson = json.loads(srvdata)
    modeljson = json.loads(modeldata)
    if modeljson['isneuralnetwork'] == True:
        result = DLTask.Predict(modeljson, directory, testfile)
    else:
        result = SkLearnTask.Predict(modeljson, True, trainfile, testfile, predictionFile)
    print(result)

if __name__ == '__main__':
    regtest1('regtask2', 'housing.csv')
    