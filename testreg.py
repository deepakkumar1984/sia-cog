import os
import json
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
        result = DLTask.Train(modeljson, True, trainfile, directory)
    else:
        result = SkLearnTask.CompileAndValidate(modeljson, True, trainfile)
    print(result)

def regtest2(name, trainfile, testfile, savePrediction):
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
        result = DLTask.FitAndPredict(modeljson, True, trainfile, testfile, savePrediction, predictionFile)
    else:
        result = SkLearnTask.FitAndPredict(modeljson, True, trainfile, testfile, savePrediction, predictionFile)
    print(result)

if __name__ == '__main__':
    regtest1('regtask2', 'housing.csv')
    