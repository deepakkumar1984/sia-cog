"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from flask import Flask, jsonify,url_for
import matplotlib.pyplot as plt
import os
import json
from Interface import app, SkLearnTask, ParallelTask,utility, DLTask, DataAnalyzer, DataManager, KApplications, DatasetTask
import shutil
import werkzeug

@app.route('/api/srv/create', methods=['POST'])
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

@app.route('/api/srv/update/<name>', methods=['POST'])
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

@app.route('/api/srv/delete/<name>', methods=['POST'])
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

@app.route('/api/srv/upload/<name>', methods=['GET','POST'])
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

@app.route('/api/srv/data/<name>', methods=['POST'])
def datamgr(name):
    message = "Success"
    code = 200
    result = []
    try:
        datasetFolder = "./data/" + name + "/dataset/"
        rjson = json.loads(request.data)
        action = rjson['action']
        filename = rjson['filename']
        if action == 'peek':
            result = DatasetTask.peekData(datasetFolder, filename, rjson)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/srv/define/<name>', methods=['POST'])
def define(name):
    message = "Success"
    code = 200
    try:
        directory = "./data/" + name
        file = directory + "/define.json"

        json_string = json.dumps(request.json)
        file = open(file, "w")
        file.write(json_string)
        file.close()
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/srv/evalute/<name>', methods=['POST'])
def evalute(name):
    message = "Success"
    code = 200
    id = ""
    try:
        data = json.loads(request.data)
        id = ParallelTask.StartEvaluteThread(name, data)
        message = "Evalute job started! Please check status."
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "taskid": id})

@app.route('/api/srv/train/<name>', methods=['POST'])
def train(name):
    message = "Success"
    code = 200
    try:
        data = json.loads(request.data)
        directory = "./data/" + name
        modelfile = directory + "/define.json"
        trainfile = directory + "/dataset/" + data['trainfile']
        modeldata = utility.getFileData(modelfile)
        modeljson = json.loads(modeldata)
        modeljson['name'] = name
        epoches = 0
        batch_size = 0
        if data['epoches'] != '':
            epoches = data['epoepochesch']
        if data['batch_size'] != '':
            batch_size = data['batch_size']

        if modeljson['isneuralnetwork']:
            result = DLTask.ContinueTraining(modeljson, trainfile, directory, epoches, batch_size)
        else:
            code = 500
            message = "Training method is only for deep learning models"
        
        print(result)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/srv/predict/<name>', methods=['POST'])
def predict(name):
    message = "Success"
    code = 200
    try:
        data = json.loads(request.data)
        directory = "./data/" + name
        modelfile = directory + "/define.json"
        servicefile = directory + "/service.json"
        result = {}
        testfile = data['testfile']
        if testfile.startswith('http://') or testfile.startswith('https://') or testfile.startswith('ftp://'):
            testfile = testfile
        else:
            testfile = directory + "/dataset/" + testfile

        predictionFile = directory + "/dataset/prediction.csv"
        modeldata = utility.getFileData(modelfile)
        modeljson = json.loads(modeldata)
        servicejson = json.loads(utility.getFileData(servicefile))
        modeljson['name'] = name

        if modeljson['isneuralnetwork']:
            if modeljson['modeltype'] == "normal":
                result = DLTask.Predict(modeljson, directory, testfile)
            elif modeljson['modeltype'] == "imagenet":
                result = KApplications.predict(modeljson, testfile)
        else:
            trainfile = directory + "/dataset/" + data['trainfile']
            result = SkLearnTask.Predict(modeljson, servicejson['regression'], trainfile, testfile, predictionFile)
        
        print(result)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})
