import threading
import json
from Interface import utility, DLTask, SkLearnTask
import uuid
import os

def saveResult(directory, result):
    resultFile = directory + "/results.json"
    resultData = utility.getFileData(resultFile)
    if resultData == "":
        resultjson = []
    else:
        resultjson = json.load(resultData)
        
    resultjson.append(result)
    with open(resultFile, 'w') as outfile:
        outfile.write(resultjson)

def Evalute(id, name, data):
    directory = "./data/" + name
    resultList = []
    taskFolder = directory + "/task"
    if not os.path.exists(taskFolder):
        os.makedirs(taskFolder)
    
    modelfile = directory + "/define.json"
    srvfile = directory + "/service.json"
    trainfile = directory + "/dataset/" + data['trainfile']
    srvdata = utility.getFileData(srvfile)
    modeldata = utility.getFileData(modelfile)
    srvjson = json.loads(srvdata)
    modeljson = json.loads(modeldata)
    if modeljson['isneuralnetwork']:
        result = DLTask.Evalute(id, modeljson, trainfile, directory)
    else:
        result = SkLearnTask.Evalute(modeljson, srvjson['regression'], trainfile)
    
    saveResult(directory, result)

def StartEvaluteThread(name, data):
    id = uuid.uuid4()
    t = threading.Thread(Evalute, args=(id, name, data))
    t.start()
    return id