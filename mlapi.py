"""
Routes and views for the flask application.
"""

import os
import shutil
from datetime import datetime
import simplejson as json
import werkzeug
from flask import jsonify
from flask import request
from Interface import utility, app, projectmgr, logmgr, constants
from ml import backgroundproc, pipeline, scikitlearn, kerasfactory

@app.route('/api/ml/create', methods=['POST'])
def create():
    message = "Success"
    code = 200
    try:
        servicename = request.json.get('servicename')
        subtype = request.json.get('model_type')
        directory = "./data/" + servicename

        if not os.path.exists(directory):
            os.makedirs(directory)

        projectmgr.UpsertService(servicename, "ml", request.json, subtype)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/update/<name>', methods=['POST'])
def update(name):
    message = "Success"
    code = 200
    try:
        directory = "./data/" + name
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        projectmgr.UpsertService(name, "ml", request.json)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/delete/<name>', methods=['POST'])
def delete(name):
    message = "Success"
    code = 200
    try:
        directory = "./data/" + name
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        if os.path.exists(directory):
            shutil.rmtree(directory)

        projectmgr.DeleteService(name, "ml")
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/upload/<name>', methods=['GET', 'POST'])
def upload(name):
    message = "Success"
    code = 200
    try:
        datasetFolder = "./data/" + name + "/dataset/"
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        if not os.path.exists(datasetFolder):
            os.makedirs(datasetFolder)
        if len(request.files) == 0:
            code = 1002
            message = "No file found"
            return jsonify({"statuscode": code, "message": message})
        
        postedfile = request.files.items(0)[0][1]
        postedfile.save(os.path.join(datasetFolder, werkzeug.secure_filename(postedfile.filename)))
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})


@app.route('/api/ml/files/<name>', methods=['GET'])
def getfiles(name):
    message = "Success"
    code = 200
    result = []
    try:
        dataset_folder = "./data/" + name + "/dataset/"
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        if not os.path.exists(dataset_folder):
            os.makedirs(dataset_folder)

        files = os.listdir(dataset_folder)
        for f in files:
            result.append(f)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/delfile/<name>', methods=['POST'])
def delfile(name):
    message = "Success"
    code = 200
    try:
        dataset_folder = "./data/" + name + "/dataset/"
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        if not os.path.exists(dataset_folder):
            os.makedirs(dataset_folder)
        filename = request.json["filename"]
        os.remove(dataset_folder + filename)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/pipeline/<name>', methods=['POST'])
def savepipelineinfo(name):
    message = "Success"
    code = 200
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        projectmgr.UpsertPipeline(name, "ml", request.json)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/pipelineflow/<name>', methods=['POST'])
def pipelineflow(name):
    message = "Success"
    code = 200
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        projectmgr.UpdatePipelineFlow(name, "ml", request.json)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/pipeline/<name>', methods=['GET'])
def pipelineinfo(name):
    message = "Success"
    code = 200
    result = []
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        pipelineRec = projectmgr.GetPipeline(name, "ml")
        if pipelineRec is None:
            raise Exception("No Pipeline Found!")

        result = json.loads(pipelineRec.pipelinedata)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/pipelineflow/<name>', methods=['GET'])
def pipelineflowinfo(name):
    message = "Success"
    code = 200
    result = None
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        pipelineRec = projectmgr.GetPipeline(name, "ml")
        if pipelineRec is None:
            raise Exception("No Pipeline Found!")

        result = json.loads(pipelineRec.pipelineflow)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/model/<name>/<modelname>', methods=['POST'])
def modeldefine(name, modelname):
    message = "Success"
    code = 200
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        projectmgr.UpsertDeepModels(name, "ml", modelname, request.json)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/modelflow/<name>/<modelname>', methods=['POST'])
def modelflow(name, modelname):
    message = "Success"
    code = 200
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        projectmgr.UpdateModelFlow(name, "ml", modelname, request.json)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/model/<name>/<modelname>', methods=['GET'])
def modelinfo(name, modelname):
    message = "Success"
    code = 200
    result = None
    model_json = None
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        modelRec = projectmgr.GetDeepModel(name, constants.ServiceTypes.MachineLearning, modelname)
        if modelRec is None:
            raise Exception("No Model Found!")

        result = json.loads(modelRec.modeldata)
        model_obj = kerasfactory.createModel(result)
        model_json = json.loads(model_obj.to_json())
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result, "model_json": model_json})

@app.route('/api/ml/modelflow/<name>/<modelname>', methods=['GET'])
def modelflowinfo(name, modelname):
    message = "Success"
    code = 200
    result = None
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        modelRec = projectmgr.GetDeepModel(name, constants.ServiceTypes.MachineLearning, modelname)
        if modelRec is None:
            raise Exception("No Model Found!")

        result = json.loads(modelRec.modelflow)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/models/<name>', methods=['GET'])
def modellist(name):
    message = "Success"
    code = 200
    result = []
    try:
        service = projectmgr.GetService(name, constants.ServiceTypes.MachineLearning)
        servicedata = json.loads(service.servicedata)
        modeltype = servicedata["model_type"]
        if modeltype == "mlp":
            models = projectmgr.GetDeepModels(name, constants.ServiceTypes.MachineLearning)
            for m in models:
                result.append({"name": m.modelname, "modifiedon": m.modifiedon})
        elif modeltype == "general":
            models = scikitlearn.getModels()
            for m in models:
                result.append({"name": m, "modifiedon": datetime.utcnow()})

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/execute/<name>', methods=['POST'])
def execute(name):
    message = "Success"
    code = 200
    taskid = ""

    try:
        service = projectmgr.ValidateServiceExists(name, constants.ServiceTypes.MachineLearning)
        data = json.loads(request.data)
        epoches = 32
        batch_size = 32
        taskid = ""
        servicejson = json.loads(service.servicedata)
        if "epoches" in data:
            epoches = data['epoches']
        if "batch_size" in data:
            batch_size = data['batch_size']
        trainingstatus = app.trainingstatus

        if trainingstatus == 1:
            message = "Training in progress! Please try after the current training is completed."
            code = 500
        else:
            if servicejson["model_type"] == "mlp":
                taskid = backgroundproc.StartTrainThread(name, epoches, batch_size)
            elif servicejson["model_type"] == "general":
                taskid = backgroundproc.StartValidateThread(name)

            message = "Job started! Please check status for id: " + taskid
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "jobid": taskid})

@app.route('/api/ml/jobs/<id>', methods=['GET'])
def jobs(id):
    message = "Started"
    result = []
    code = 200
    try:
        job = projectmgr.GetJob(id)
        if not job.result is None:
            result = json.loads(job.result)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/predict/<name>', methods=['POST'])
def predict(name):
    message = "Success"
    code = 200
    result = []
    try:
        start = datetime.now()
        data = json.loads(request.data)
        service = projectmgr.GetService(name, constants.ServiceTypes.MachineLearning)
        servicejson = json.loads(service.servicedata)

        savePrediction = False
        if "save_prediction" in data:
            savePrediction = data['save_prediction']
        result = {}
        if servicejson["data_format"] == "image":
            testfile = data['imagepath']
        elif servicejson["data_format"] == "csv":
            testfile = data['testfile']

        pipeline.init(pipeline, name, servicejson["model_type"])
        predictions = pipeline.Predict(testfile, savePrediction)
        predictions = json.loads(predictions)
        if servicejson["data_format"] == "csv":
            result = predictions["0"]
        else:
            result = predictions

        logmgr.LogPredSuccess(name, constants.ServiceTypes.MachineLearning, start)
    except Exception as e:
        code = 500
        message = str(e)
        logmgr.LogPredError(name, constants.ServiceTypes.MachineLearning, start, message)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/recentjob/<name>', methods=['GET'])
def recentjob(name):
    message = "Completed"
    result = {}
    code = 200
    try:
        data = projectmgr.GetLastTraining(name)
        result = {"epoches": data[0], "losses": data[1]}
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/prevjob/<name>', methods=['GET'])
def prevjob(name):
    message = "Success"
    result = {}
    code = 200
    try:
        data = projectmgr.GetPrevTraining(name)
        result = {"epoches": data[0], "losses": data[1]}
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/reset/<name>', methods=['POST'])
def resetmlmodel(name):
    message = "Success"
    result = {}
    code = 200
    try:
        wpath = "./data/" + name + "/weights.hdf5"
        if os.path.exists(wpath):
            os.remove(wpath)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})
