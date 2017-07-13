"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from flask import Flask, jsonify
from Interface import app
from Interface import DataManager
from Interface import DataAnalyzer
from Interface import DLTask
import matplotlib.pyplot as plt
import os
import json
from Interface import SkLearnTask
from Interface import utility

@app.route('/api/srv/create', methods=['POST'])
def create():
    message = ""
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

        message = "Created"
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/srv/define/<name>', methods=['POST'])
def define(name):
    message = ""
    code = 200
    try:
        directory = "./data/" + name
        file = directory + "/define.json"

        json_string = json.dumps(request.json)
        file = open(file, "w")
        file.write(json_string)
        file.close()

        message = "Defined"
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/srv/evalute/<name>', methods=['POST'])
def evalute(name):
    message = ""
    code = 200
    try:
        data = json.loads(request.data)
        directory = "./data/" + name
        modelfile = directory + "/define.json"
        srvfile = directory + "/service.json"
        trainfile = directory + "/dataset/" + data['trainfile']
        srvdata = utility.getFileData(srvfile)
        modeldata = utility.getFileData(modelfile)
        srvjson = json.loads(srvdata)
        modeljson = json.loads(modeldata)
        if modeljson['isneuralnetwork']:
            result = DLTask.Evalute(modeljson, trainfile, directory)
        else:
            result = SkLearnTask.Evalute(modeljson, srvjson['regression'], trainfile)
        print(result)
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/srv/continuetraining/<name>', methods=['POST'])
def continuetraining(name):
    message = ""
    code = 200
    try:
        data = json.loads(request.data)
        directory = "./data/" + name
        modelfile = directory + "/define.json"
        trainfile = directory + "/dataset/" + data['trainfile']
        modeldata = utility.getFileData(modelfile)
        modeljson = json.loads(modeldata)
        epoch = 0
        batch_size = 0
        if data['epoch'] != '':
            epoch = data['epoch']
        if data['batch_size'] != '':
            epoch = data['batch_size']

        if modeljson['isneuralnetwork']:
            result = DLTask.ContinueTraining(modeljson, trainfile, directory, epoch, batch_size)
        else:
            code = 500
            message = "Continue training method is only for deep learning models"
        
        print(result)
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message})
