import os
import json
from Interface import RegressionTask
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
    RegressionTask.Run(modeljson, trainfile)

if __name__ == '__main__':
    regtest1('regtask1', 'housing.csv')
    