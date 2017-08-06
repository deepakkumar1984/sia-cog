"""
Routes and views for the flask application.
"""

import jsonpickle
import simplejson as json
from flask import jsonify
from flask import request

from Interface import app
from langintent import intentanalyzer

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
        else:
            raise Exception("Invalid api call")

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/int/<type>/<name>', methods=['GET'])
def getintobjects(type, name):
    message = "Success"
    code = 200
    result = []
    try:
        if type.lower() == "entity":
            result = intentanalyzer.getEntityRecords(name)
        elif type.lower() == "intent":
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
        data = request.args.get('data')
        print(data)
        result = intentanalyzer.predict(data)
        result = json.loads(jsonpickle.encode(result, unpicklable=False))
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})