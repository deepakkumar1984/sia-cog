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

@app.route('/api/srv/train/<name>', methods=['POST'])
def train(name):
    message = ""
    code = 200
    try:
        trainfile = request.json.get('file')
        directory = "./data/" + name
        modelfile = directory + "/define.json"
        srvfile = directory + "/service.json"
        trainfile = directory + "/dataset/" + trainfile
        srvdata = utility.getFileData(srvfile)
        modeldata = utility.getFileData(modelfile)
        srvjson = json.loads(srvdata)
        modeljson = json.loads(modeldata)
        SkLearnTask.Run(modeljson, trainfile)
    except Exception as e:
        code = 500
        message = e

    return jsonify({"statuscode": code, "message": message})
