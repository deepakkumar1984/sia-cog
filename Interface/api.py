"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from flask import Flask, jsonify
from SiaWizard import app
from SiaWizard import DataManager
from SiaWizard import DataAnalyzer
import matplotlib.pyplot as plt
import os
import json
from SiaWizard import RegressionTask

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
        srvdata = getFileData(srvfile)
        modeldata = getFileData(modelfile)
        srvjson = json.loads(srvdata)
        modeljson = json.loads(modeldata)
        
    except Exception as e:
        code = 500
        message = e.message

    return jsonify({"statuscode": code, "message": message})

def getFileData(filePath):
    data = ""
    if os.path.exists(filePath):
        with open(filePath, "r") as text_file:
            data = text_file.read()
    return data

if __name__ == '__main__':
    train('regtask1')
    
