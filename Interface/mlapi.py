"""
Routes and views for the flask application.
"""

import os
import shutil

import simplejson as json
import werkzeug
from flask import jsonify
from flask import request

from Interface import app, ParallelTask, utility, DatasetTask
from libml import pipeline


@app.route('/api/ml/create', methods=['POST'])
def create():
    message = "Success"
    code = 200
    try:
        servicename = request.json.get('servicename')
        directory = "./data/" + servicename
        file = directory + "/service.json"
        if not os.path.exists(directory):
            os.makedirs(directory)
            json_string = json.dumps(request.json)
            file = open(file, "w")
            file.write(json_string)
            file.close()
        else:
            code = 1001
            message = "Service already exists!"

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
        file = directory + "/service.json"
        if not os.path.exists(directory):
            code = 1001
            message = "Service does not exists!"
        else:
            json_string = json.dumps(request.json)
            file = open(file, "w")
            file.write(json_string)
            file.close()

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
        if not os.path.exists(directory):
            code = 1001
            message = "Service does not exists!"
        else:
            shutil.rmtree(directory)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/upload/<name>', methods=['GET','POST'])
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

@app.route('/api/ml/data/<name>', methods=['POST'])
def datamgr(name):
    message = "Success"
    code = 200
    result = []
    try:
        rjson = json.loads(request.data)
        result = DatasetTask.invoke(name, rjson)
    except Exception as e:
        code = 500
        message = str(e)

    return result

@app.route('/api/ml/pipeline/<name>', methods=['POST'])
def pipeline(name):
    message = "Success"
    code = 200
    try:
        directory = "./data/" + name
        file = directory + "/pipeline.json"

        json_string = json.dumps(request.json)
        file = open(file, "w")
        file.write(json_string)
        file.close()
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/ml/evalute/<name>', methods=['POST'])
def evalute(name):
    message = ""
    code = 200
    try:
        taskid = ParallelTask.StartValidateThread(name)
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
        directory = "./data/" + name
        epoches = 32
        batch_size = 32
        if "epoches" in data:
            epoches = data['epoches']
        if "batch_size" in data:
            batch_size = data['batch_size']

        taskid = ParallelTask.StartTrainThread(name, epoches, batch_size)
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
        result = ParallelTask.GetStatus(name, id)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify(result)

@app.route('/api/ml/predict/<name>', methods=['POST'])
def predict(name):
    message = "Success"
    code = 200
    try:
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
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})
