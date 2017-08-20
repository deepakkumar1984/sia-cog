"""
Routes and views for the flask application.
"""

import os
import shutil

import simplejson as json
from flask import jsonify
from flask import request
from datetime import datetime
from Interface import app, utility, dbutility
from bot import chatbot


@app.route('/api/bot/create', methods=['POST'])
def botcreate():
    message = "Success"
    code = 200
    try:
        rjson = json.loads(request.json)
        name = rjson["name"]
        threshold = rjson["threshold"]
        defaultResponse = rjson["default_response"]
        chatbot.create(name, threshold, defaultResponse)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/bot/update/<name>', methods=['POST'])
def botupdate(name):
    message = "Success"
    code = 200
    try:
        rjson = json.loads(request.json)
        name = rjson["name"]
        threshold = rjson["threshold"]
        defaultResponse = rjson["default_response"]
        chatbot.update(name, threshold, defaultResponse)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/bot/delete/<name>', methods=['POST'])
def botdelete(name):
    message = "Success"
    code = 200
    try:
        rjson = json.loads(request.json)
        name = rjson["name"]
        chatbot.delete(name)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/bot/train/<name>', methods=['POST'])
def bottrain(name):
    message = "Success"
    code = 200
    try:
        rjson = json.loads(request.json)
        name = rjson["name"]
        data = rjson["data"]
        corpus = []
        if "corpus" in rjson:
            corpus = rjson["corpus"]
            chatbot.corpustrain(name, corpus)

        chatbot.train(name)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/bot/predict/<name>', methods=['POST'])
def botpredict(name):
    message = "Success"
    code = 200
    try:
        start = datetime.now()
        rjson = json.loads(request.json)
        name = rjson["name"]
        data = rjson["data"]
        result = chatbot.predict(name, data)
        dbutility.logCalls(name, start, datetime.now())
    except Exception as e:
        code = 500
        message = str(e)
        dbutility.logCalls(name, start, datetime.now(), False, message)

    return jsonify({"statuscode": code, "message": message, "result": result})
