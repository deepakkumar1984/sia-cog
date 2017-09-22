"""
Routes and views for the flask application.
"""

from flask import jsonify
from flask import request
from datetime import datetime
from Interface import app, projectmgr, constants, logmgr
from bot import chatbot
import os
import shutil
import simplejson as json
import jsonpickle

@app.route('/api/bot/create', methods=['POST'])
def botcreate():
    message = "Success"
    code = 200
    try:
        rjson = request.json
        name = rjson["servicename"]
        projectmgr.UpsertService(name, constants.ServiceTypes.ChatBot, rjson)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/bot/update/<name>', methods=['POST'])
def botupdate(name):
    message = "Success"
    code = 200
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.ChatBot)
        projectmgr.UpsertService(name, constants.ServiceTypes.ChatBot, request.json)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/bot/delete/<name>', methods=['POST'])
def botdelete(name):
    message = "Success"
    code = 200
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.ChatBot)
        botfolder = "./data/__chatbot/" + name
        if os.path.exists(botfolder):
            shutil.rmtree(botfolder)

        projectmgr.DeleteService(name, constants.ServiceTypes.ChatBot)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/bot/train/<name>', methods=['POST'])
def bottrain(name):
    message = "Success"
    code = 200
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.ChatBot)
        id = projectmgr.StartJob(name, constants.ServiceTypes.ChatBot, 0)
        rjson = request.json
        data = rjson["data"]
        corpus = []
        if "corpus" in rjson:
            corpus = rjson["corpus"]
            if not corpus is None:
                chatbot.corpustrain(name, corpus)

        chatbot.train(name, data)
        projectmgr.EndJob(id, "Completed", "Completed", json.dumps({"corpus": corpus, "data": data}))
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/bot/history/<name>', methods=['GET'])
def gettrainhistory(name):
    message = "Success"
    code = 200
    result = []
    try:
        jobs = projectmgr.GetJobs(name, constants.ServiceTypes.ChatBot)
        result = jsonpickle.encode(jobs, unpicklable=False)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/bot/predict/<name>', methods=['POST'])
def botpredict(name):
    message = "Success"
    code = 200
    start = datetime.now()
    result = []
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.ChatBot)
        rjson = request.json
        data = rjson["data"]
        result = chatbot.predict(name, data)
        logmgr.LogPredSuccess(name, constants.ServiceTypes.ChatBot, start)
    except Exception as e:
        code = 500
        message = str(e)
        logmgr.LogPredError(name, constants.ServiceTypes.ChatBot, start, message)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/bot/reset/<name>', methods=['POST'])
def botreset(name):
    message = "Success"
    code = 200
    try:
        chatbot.resetBot(name)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})