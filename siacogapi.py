"""
Routes and views for the flask application.
"""

import os
import simplejson as json
import jsonpickle
from flask import jsonify, request
from datetime import datetime
from dateutil import parser
from Interface import utility, app, dataanalyzer, sysinfo, dbutility

@app.route('/api/status', methods=['GET'])
def apistatus():
    message = "All Good!"
    code = 200

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/server/<infotype>', methods=['GET'])
def systeminfo(infotype):
    message = "Success"
    code = 200
    try:
        result = {}
        if infotype == "info":
            result = sysinfo.getSystemInfo()
        elif infotype == "cpu":
            result = sysinfo.getCPUUsage()
        elif infotype == "gpu":
            result = sysinfo.getGPUUsage()
    except Exception as e:
        message = str(e)
        code = 500

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/list/<name>', methods=['GET'])
def apilist(name):
    message = "Success"
    code = 200
    try:
        directory = "./data/"
        result = []
        if name == "ml":
            dirs = os.listdir(directory)
            for d in dirs:
                if d == "__vision" or d == "__chatbot" or d == "__intent" or d == "__speech" or d == "__text":
                    continue

                if os.path.isfile(directory + d):
                    continue

                srvpath = directory + d + "/service.json"
                if os.path.exists(srvpath):
                    result.append(utility.getJsonData(srvpath))
        elif name == "vision":
            directory = directory + "__vision/"
            files = os.listdir(directory)
            for f in files:
                if f.endswith(".json"):
                    result.append(utility.getJsonData(directory + f))
        elif name == "bot":
            directory = directory + "__chatbot/"
            dirs = os.listdir(directory)
            for d in dirs:
                if os.path.isfile(directory + d):
                    continue

                botpath = directory + d + "/bot.json"
                if os.path.exists(botpath):
                    result.append(utility.getJsonData(botpath))

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": json.loads(jsonpickle.encode(result, unpicklable=False))})

@app.route('/api/data/info', methods=['POST'])
def databasicinfo():
    message = "Success"
    code = 200
    try:
        rjson = request.json

        if not "name" in rjson:
            raise Exception("Please provide name of the service")

        if not "filename" in rjson:
            raise Exception("Please provide filename")

        columns = None
        count = 5
        if "columns" in rjson:
            columns = rjson["columns"]

        if "count" in rjson:
            count = rjson["count"]

        result = dataanalyzer.basic_info(rjson["name"], rjson["filename"], columns, count)

    except Exception as e:
        message = str(e)
        code = 500
    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/data/plot', methods=['POST'])
def dataplot():
    message = "Success"
    code = 200
    try:
        rjson = request.json
        result = []
        utility.validateParam(rjson, "name")
        utility.validateParam(rjson, "filename")
        utility.validateParam(rjson, "method")
        options = utility.getVal(rjson, "options")
        result = dataanalyzer.plot(rjson["name"], rjson["filename"], rjson["method"], options)

    except Exception as e:
        message = str(e)
        code = 500
    return jsonify({"statuscode": code, "message": message, "result": result})


@app.route('/api/logs/pred', methods=['POST'])
def predlogs():
    message = "Success"
    code = 200
    try:
        rjson = request.json
        result = []
        utility.validateParam(rjson, "category")
        utility.validateParam(rjson, "servicename")
        utility.validateParam(rjson, "status")
        utility.validateParam(rjson, "start")
        utility.validateParam(rjson, "end")
        start = parser.parse(rjson["start"] + " 00:00")
        end = parser.parse(rjson["end"] + " 23:59");
        success = True
        if rjson["status"] == "Error":
            success = False

        result = dbutility.getPredLogs(rjson["category"], rjson["servicename"], start, end, success)

    except Exception as e:
        message = str(e)
        code = 500
    return jsonify({"statuscode": code, "message": message, "result": result})