"""
Routes and views for the flask application.
"""

from flask import request
from flask import jsonify
import simplejson as json
from Interface import app, LangIntentApplications
import jsonpickle

@app.route('/api/int/define/<type>', methods=['POST'])
def defineintobjects(type):
    message = "Success"
    code = 200
    try:
        rjson = request.json
        name = rjson["name"]

        if type.lower() == "entity":
            keywords = rjson["keywords"]
            LangIntentApplications.saveEntity(name, keywords)
        elif type.lower() == "intent":
            rentities = rjson["required_entities"]
            oentities = rjson["optional_entities"]
            LangIntentApplications.saveIntent(name, rentities, oentities)
        else:
            raise Exception("Invalid api call")

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/int/delete/<type>', methods=['POST'])
def deleteintobjects(type):
    message = "Success"
    code = 200
    try:
        rjson = request.json
        name = rjson["name"]
        if type.lower() == "entity":
            LangIntentApplications.deleteEntity(name)
        elif type.lower() == "intent":
            LangIntentApplications.deleteIntent(name)
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
            result = LangIntentApplications.getEntityRecords(name)
        elif type.lower() == "intent":
            result = LangIntentApplications.getIntentRecords(name)
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
        LangIntentApplications.train()
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
        result = LangIntentApplications.predict(data)
        result = jsonpickle.encode(result, unpicklable=False)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})