"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from flask import Flask, jsonify
import matplotlib.pyplot as plt
import os
import json
from Interface import app, SkLearnTask, ParallelTask,utility, DLTask, DataAnalyzer, DataManager

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
    id = ""
    try:
        data = json.loads(request.data)
        id = ParallelTask.StartEvaluteThread(name, data)
        message = "Evalute job started! Please check status."
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message, "taskid": id})

@app.route('/api/srv/train/<name>', methods=['POST'])
def train(name):
    message = ""
    code = 200
    try:
        data = json.loads(request.data)
        directory = "./data/" + name
        modelfile = directory + "/define.json"
        trainfile = directory + "/dataset/" + data['trainfile']
        modeldata = utility.getFileData(modelfile)
        modeljson = json.loads(modeldata)
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
        message = e

    return jsonify({"statuscode": code, "message": message})
