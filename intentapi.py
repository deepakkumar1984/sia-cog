"""
Routes and views for the flask application.
"""

import jsonpickle
import simplejson as json
from flask import jsonify
from flask import request
from datetime import datetime
from Interface import app, dbutility
from langintent import intentanalyzer
import shutil
import os

@app.route('/api/int/define/<objtype>', methods=['POST'])
def defineintobjects(objtype):
    message = "Success"
    code = 200
    try:
        rjson = request.json
        name = rjson["name"]

        if objtype.lower() == "entity":
            keywords = rjson["keywords"]
            intentanalyzer.saveEntity(name, keywords)
        elif objtype.lower() == "intent":
            rentities = rjson["required_entities"]
            oentities = rjson["optional_entities"]
            intentanalyzer.saveIntent(name, rentities, oentities)
            utter = rjson["utter"]
            if not utter is None:
                intentanalyzer.saveUtter(name, utter)

        else:
            raise Exception("Invalid api call")

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/int/delete/<type>', methods=['POST'])
def deleteintobjects(objtype):
    message = "Success"
    code = 200
    try:
        rjson = request.json
        name = rjson["name"]
        if objtype.lower() == "entity":
            intentanalyzer.deleteEntity(name)
        elif objtype.lower() == "intent":
            intentanalyzer.deleteIntent(name)
            shutil.rmtree("./data/__intent/utter/" + name + ".intent")
        else:
            raise Exception("Invalid api call")

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/int/<otype>/<name>', methods=['GET'])
def getintobjects(otype, name):
    message = "Success"
    code = 200
    result = []
    try:
        if otype == "entity":
            result = intentanalyzer.getEntityRecords(name)
        elif otype == "intent":
            result = intentanalyzer.getIntentRecords(name)
        else:
            raise Exception("Invalid api call")

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/int/train', methods=['GET'])
def trainint():
    message = "Success"
    code = 200
    try:
        intentanalyzer.train()
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/int/predict', methods=['GET'])
def predictint():
    message = "Success"
    code = 200
    result = []
    try:
        start = datetime.now()
        data = request.args.get('data')
        print(data)
        result = intentanalyzer.predict(data)
        result = json.loads(jsonpickle.encode(result, unpicklable=False))
        dbutility.logCalls("intent", )
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})