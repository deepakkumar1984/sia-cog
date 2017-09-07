"""
Routes and views for the flask application.
"""

import os
import shutil
from datetime import datetime
import simplejson as json
import werkzeug
from flask import jsonify, sessions
from flask import request

from Interface import utility, app, dbutility, projectmgr
from ml import backgroundproc, pipeline


@app.route('/api/ml/create', methods=['POST'])
def create():
    message = "Success"
    code = 200
    try:
        servicename = request.json.get('servicename')
        directory = "./data/" + servicename

        if not os.path.exists(directory):
            os.makedirs(directory)

        projectmgr.UpsertService(servicename, "ml", request.json)

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
        if not os.path.exists(directory):
            code = 1001
            message = "Service does not exists!"
        else:
            if request.json["servicename"] != name:
                code = 1001
                message = "Service name is not matching with the api calls"
            else:
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
        if not os.path.exists(dataset_folder):
            os.makedirs(dataset_folder)
        filename = request.json["filename"]
        os.remove(dataset_folder + filename)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/pipeline/<name>', methods=['POST'])
def pipeline(name):
    message = "Success"
    code = 200
    try:
        projectmgr.UpsertPipeline(name, "ml", request.json)
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/pipeline/<name>', methods=['GET'])
def pipelineinfo(name):
    message = "Success"
    code = 200
    result = []
    try:
        pipelineRec = projectmgr.GetPipeline(name, "ml")
        if pipelineRec is None:
            raise Exception("No Pipeline Found!")

        result = json.loads(pipelineRec.pipelinedata)
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/ml/evaluate/<name>', methods=['POST'])
def evaluate(name):
    message = ""
    code = 200
    try:
        taskid = ""
        trainingstatus = app.trainingstatus

        if trainingstatus == 1:
            message = "Training in progress! Please try after the current training is completed."
            code = 500
        else:
            taskid = backgroundproc.StartValidateThread(name)
            message = "Job started! Please check status for id: " + taskid
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "jobid": taskid})

@app.route('/api/ml/train/<name>', methods=['POST'])
def train(name):
    message = "Success"
    code = 200
    try:
        data = json.loads(request.data)
        epoches = 32
        batch_size = 32
        taskid = ""
        if "epoches" in data:
            epoches = data['epoches']
        if "batch_size" in data:
            batch_size = data['batch_size']
        trainingstatus = app.trainingstatus

        if trainingstatus == 1:
            message = "Training in progress! Please try after the current training is completed."
            code = 500
        else:
            taskid = backgroundproc.StartTrainThread(name, epoches, batch_size)
            message = "Job started! Please check status for id: " + taskid
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "jobid": taskid})

@app.route('/api/ml/jobs/<name>', methods=['GET'])
def jobs(name):
    message = "Started!"
    code = 200
    try:
        id = request.args.get("id")
        result = backgroundproc.GetStatus(name, id)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify(result)

@app.route('/api/ml/predict/<name>', methods=['POST'])
def predict(name):
    message = "Success"
    code = 200
    try:
        start = datetime.now()
        data = json.loads(request.data)
        servicedata = utility.getFileData("./data/" + name + "/service.json")
        servicejson = json.loads(servicedata)

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

        end = datetime.now()
        dbutility.logCalls("ml", name, start, end)
    except Exception as e:
        code = 500
        message = str(e)
        dbutility.logCalls("ml", name, start, end, False, message)

    return jsonify({"statuscode": code, "message": message, "result": result})
