import os
import json
from Interface import SkLearnTask
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
    result = SkLearnTask.CompileAndValidate(modeljson, trainfile)
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
    result = SkLearnTask.FitAndPredict(modeljson, trainfile, testfile, savePrediction, predictionFile)
    print(result)

if __name__ == '__main__':
    regtest2('regtask1', 'housing.csv', 'housing.csv', True)
    