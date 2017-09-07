import pickle

import jsonpickle
import numpy
import pandas
import simplejson as json

from Interface import utility, projectmgr
from ml import pipelinecomponents

srvname = ""
model_type = ""
jobid = ""

class NumpyFloatHandler(jsonpickle.handlers.BaseHandler):
    """
    Automatic conversion of numpy float  to python floats
    Required for jsonpickle to work correctly
    """
    def flatten(self, obj, data):
        """
        Converts and rounds a Numpy.float* to Python float
        """
        return round(obj,6)

def init(self, srvname, model_type, jobid):
    self.srvname = srvname
    self.model_type = model_type
    self.jobid = jobid

    pipelinecomponents.init(pipelinecomponents, srvname, model_type, jobid)

def getPipelineData():
    pipelinejson = json.loads(projectmgr.GetPipeline(srvname, "ml").pipelinedata)
    return pipelinejson

def Run():
    pickleFile = pipelinecomponents.projectfolder + '/pipeline.out'
    pipelinejson = getPipelineData()
    resultset = {}

    for p in pipelinejson:
        name = p['name']
        module = p['module']
        options = {}
        if "options" in p:
            options = p["options"]
            pipelinecomponents.addOption(options)

        if module == "return_result":
            continue

        input = {}
        if "input" in p:
            input = p['input']
        func = getattr(pipelinecomponents, module)
        args = {}
        for i in input:
            inputValue = input[i]
            if "output->" in inputValue:
                args[i] = resultset[inputValue]
                continue

            args[i] = inputValue

        args['pipeline'] = p
        output = func(**args)

        if type(output) is tuple:
            count = 0
            for t in output:
                resultset["output->" + name + "->" + str(count)] = t
                count = count + 1
        else:
            resultset["output->" + name] = output

    savePipeline = True

    if savePipeline is True:
        with open(pickleFile, "wb") as f:
            pickle.dump(resultset, f)

def Predict(filename, savePrediction = False):
    pipelinecomponents.init(pipelinecomponents, srvname, model_type, jobid)
    pipelinefile = pipelinecomponents.projectfolder + '/pipeline.json'
    pipelinejson = utility.getJsonData(pipelinefile)
    resultset = {}
    initialX = []
    predType = "csv"
    for p in pipelinejson:
        name = p['name']
        module = p['module']
        input = {}

        options = {}
        if "options" in p:
            options = p["options"]
            pipelinecomponents.addOption(options)

        if module == "return_result":
            continue

        if module == "data_loadcsv":
            p["input"]["filename"] = filename

        if module == "data_loadimg":
            p["input"]["imagepath"] = filename
            predType = "img"

        if module == "data_handlemissing" or module == "data_filtercolumns":
            continue

        if "input" in p:
            input = p['input']

        if module == "data_getxy":
            module = "data_getx"

        if "model_" in module:
            if module != "model_evalute" and module != "model_train":
                continue
            else:
                module = "model_predict"
                name = "model_predict"
                del input["model"]
                del input["Y"]

        args = {}
        if module == "data_featureselection" or module == "data_featureselection_withestimator":
            module = "data_getfeatures"
            args['result'] = Output(name, 2)

        func = getattr(pipelinecomponents, module)

        for i in input:
            inputValue = input[i]
            if "output->" in inputValue:
                args[i] = resultset[inputValue]
                continue

            args[i] = inputValue

        args['pipeline'] = p
        output = func(**args)
        if type(output) is tuple:
            count = 0
            for t in output:
                resultset["output->" + name + "->" + str(count)] = t
                count = count + 1
        else:
            resultset["output->" + name] = output

        if module == "data_loadcsv":
            initialX = output

    predictions = resultset["output->model_predict"]
    if predType == "csv":
        predictions = pandas.DataFrame(predictions).to_json()
    if savePrediction is True:
        if predType == "csv":
            initialX['pred_result'] = predictions
            initialX.to_csv(pipelinecomponents.projectfolder + "/dataset/predictions.csv")
        elif predType == "img":
            with open(pipelinecomponents.projectfolder + "/dataset/predictions.json", "wb") as f:
                json.dump(predictions, f)

    return predictions

def ContinueTraining(epoches=32, batch_size=32):
    pipelinecomponents.init(pipelinecomponents, srvname, model_type, jobid)
    pipelineFile = pipelinecomponents.projectfolder + '/pipeline.json'
    pickleFile = pipelinecomponents.projectfolder + '/pipeline.out'
    pipelinejson = utility.getJsonData(pipelineFile)

    resultset = {}
    for p in pipelinejson:
        name = p['name']
        module = p['module']
        input = {}
        options = {}
        if "options" in p:
            options = p["options"]
            pipelinecomponents.addOption(options)

        if module == "return_result":
            continue

        if "input" in p:
            input = p['input']

        if module == "model_train":
            options['epoches'] = epoches
            options['batch_size'] = batch_size
            input['more'] = "true"
        func = getattr(pipelinecomponents, module)
        args = {}
        for i in input:
            inputValue = input[i]
            if "output->" in inputValue:
                args[i] = resultset[inputValue]
                continue

            args[i] = inputValue

        args['pipeline'] = p
        output = func(**args)

        if type(output) is tuple:
            count = 0
            for t in output:
                resultset["output->" + name + "->" + str(count)] = t
                count = count + 1
        else:
            resultset["output->" + name] = output

    savePipeline = True
    if savePipeline is True:
        with open(pickleFile, "wb") as f:
            pickle.dump(resultset, f)

def Output(name, num = None, to_json=False):
    pipelinecomponents.init(pipelinecomponents, srvname, model_type, jobid)
    result = pipelinecomponents.return_result(name, num)
    jsonpickle.handlers.registry.register(numpy.int, NumpyFloatHandler)
    jsonpickle.handlers.registry.register(numpy.int32, NumpyFloatHandler)
    jsonpickle.handlers.registry.register(numpy.int64, NumpyFloatHandler)
    jsonpickle.handlers.registry.register(numpy.float, NumpyFloatHandler)
    jsonpickle.handlers.registry.register(numpy.float32, NumpyFloatHandler)
    jsonpickle.handlers.registry.register(numpy.float64, NumpyFloatHandler)

    return jsonpickle.encode(result, unpicklable=False)